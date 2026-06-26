"""Copies business data from the legacy SQLite database into Postgres.

Reads every row through the Django ORM against the 'sqlite' alias (defined
in settings.py only while db.sqlite3 exists) so dates/decimals/booleans are
parsed correctly, then re-inserts each row into the 'default' (Postgres)
connection preserving primary keys. Image/file fields only carry their
stored relative path string across - no files in MEDIA_ROOT are touched.

Run with: python manage.py migrate_sqlite_to_postgres
Add --flush to wipe target tables first (for re-runs).
Add --skip-users 1,5 to exclude specific source user PKs (e.g. a seed
account that collides with a real account already created in Postgres).
"""
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connections, transaction

from cart.models import CartItem
from orders.models import Order, OrderItem
from products.models import Category, Product
from reminders.models import Reminder
from users.models import User
from wishlist.models import WishlistItem

# Dependency order matters: a model must come after every model it has a
# ForeignKey to, so FK targets already exist in Postgres when it's copied.
MODELS_IN_ORDER = [User, Category, Product, CartItem, WishlistItem, Order, OrderItem, Reminder]


class Command(BaseCommand):
    help = 'Copy Users/Products/Categories/Cart/Wishlist/Orders/Reminders from the sqlite alias into Postgres.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', action='store_true',
            help='Delete existing rows in each target table before copying (for re-runs).',
        )
        parser.add_argument(
            '--skip-users', default='',
            help='Comma-separated SQLite user PKs to exclude (e.g. a seed admin that collides with a real account).',
        )

    def handle(self, *args, **options):
        if 'sqlite' not in connections.databases:
            self.stderr.write(self.style.ERROR(
                "No 'sqlite' database alias configured. db.sqlite3 may already have been removed."
            ))
            return

        skip_user_ids = {int(pk) for pk in options['skip_users'].split(',') if pk.strip()}
        report = []

        for model in MODELS_IN_ORDER:
            report.append(self._copy_model(model, flush=options['flush'], skip_user_ids=skip_user_ids))

        self._copy_user_m2m(skip_user_ids)
        self._print_report(report)

    def _copy_model(self, model, flush, skip_user_ids):
        label = model._meta.label
        source_qs = model.objects.using('sqlite').all().order_by('pk')

        if model is User and skip_user_ids:
            source_qs = source_qs.exclude(pk__in=skip_user_ids)

        source_count = source_qs.count()

        if flush:
            model.objects.using('default').all().delete()

        copied, skipped = 0, []
        for obj in source_qs.iterator():
            try:
                with transaction.atomic(using='default'):
                    obj.save(using='default', force_insert=True)
                copied += 1
            except Exception as exc:  # noqa: BLE001 - report every failure, don't abort the run
                skipped.append((obj.pk, str(exc)))

        self._reset_sequence(model)
        target_count = model.objects.using('default').count()

        return {
            'model': label,
            'source_count': source_count,
            'copied': copied,
            'target_count': target_count,
            'skipped': skipped,
        }

    def _reset_sequence(self, model):
        with connections['default'].cursor() as cursor:
            for sql in connections['default'].ops.sequence_reset_sql(no_style(), [model]):
                cursor.execute(sql)

    def _copy_user_m2m(self, skip_user_ids):
        """Map groups/permissions across by natural key, since their PKs are
        regenerated fresh by `migrate` and won't match the SQLite side."""
        for source_user in User.objects.using('sqlite').exclude(pk__in=skip_user_ids):
            try:
                target_user = User.objects.using('default').get(pk=source_user.pk)
            except User.DoesNotExist:
                continue

            group_names = list(source_user.groups.using('sqlite').values_list('name', flat=True))
            if group_names:
                target_user.groups.set(Group.objects.using('default').filter(name__in=group_names))

            perm_keys = list(
                source_user.user_permissions.using('sqlite')
                .values_list('content_type__app_label', 'content_type__model', 'codename')
            )
            if perm_keys:
                perms = Permission.objects.using('default').filter(
                    content_type__app_label__in={k[0] for k in perm_keys},
                    codename__in={k[2] for k in perm_keys},
                )
                target_user.user_permissions.set(perms)

    def _print_report(self, report):
        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('Migration report'))
        all_ok = True
        for r in report:
            status = self.style.SUCCESS('OK') if r['source_count'] == r['copied'] and not r['skipped'] else self.style.WARNING('CHECK')
            if r['skipped']:
                all_ok = False
            self.stdout.write(
                f"{status}  {r['model']:<25} source={r['source_count']:<4} copied={r['copied']:<4} "
                f"target_total={r['target_count']:<4} skipped={len(r['skipped'])}"
            )
            for pk, err in r['skipped']:
                self.stdout.write(self.style.WARNING(f"        - skipped pk={pk}: {err}"))
        self.stdout.write('')
        if all_ok:
            self.stdout.write(self.style.SUCCESS('All rows copied successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Some rows were skipped - see above.'))
