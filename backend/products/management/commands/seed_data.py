"""Seeds the database with demo categories, products, users and orders.

Run with: python manage.py seed_data
Safe to re-run - it clears existing demo data first.
"""
import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from cart.models import CartItem
from orders.models import Order, OrderItem
from products.models import Category, Product
from reminders.models import Reminder
from wishlist.models import WishlistItem

User = get_user_model()

CATEGORIES = [
    ('Jewelry', 'jewelry', 'FaGem'),
    ('Flowers', 'flowers', 'FaSeedling'),
    ('Personalized Gifts', 'personalized', 'FaPenFancy'),
    ('Electronics', 'electronics', 'FaLaptop'),
    ('Books', 'books', 'FaBook'),
    ('Toys & Games', 'toys', 'FaPuzzlePiece'),
    ('Games', 'games', 'FaGamepad'),
    ('Home Decor', 'home-decor', 'FaHome'),
    ('Fashion', 'fashion', 'FaTshirt'),
    ('Gourmet & Treats', 'gourmet', 'FaCookieBite'),
    ('Wellness', 'wellness', 'FaSpa'),
    ('Stationery', 'stationery', 'FaPencilAlt'),
    ('Gift Boxes', 'gift-box', 'FaGifts'),
    ('Perfume & Beauty', 'perfume', 'FaSprayCan'),
]

# (name, category_slug, price, occasion, gender, min_age, max_age, rating, trending, featured)
PRODUCTS = [
    ("Rose Gold Pendant Necklace", 'jewelry', 4500, 'birthday', 'female', 16, 45, 4.7, True, True),
    ("Diamond Stud Earrings", 'jewelry', 8500, 'anniversary', 'female', 18, 60, 4.8, False, True),
    ("Men's Leather Wrap Bracelet", 'jewelry', 2200, 'birthday', 'male', 16, 50, 4.3, False, False),
    ("Birthstone Ring", 'jewelry', 3800, 'birthday', 'female', 16, 40, 4.6, True, False),
    ("Fresh Red Roses Bouquet (12 Stems)", 'flowers', 3200, 'valentine', 'female', 16, 70, 4.9, True, True),
    ("Mixed Tulips Bouquet", 'flowers', 2500, 'birthday', 'female', 16, 70, 4.5, False, False),
    ("Sunflower Bunch", 'flowers', 1800, 'general', 'unisex', 10, 80, 4.4, False, False),
    ("Orchid Plant in Ceramic Pot", 'flowers', 4200, 'anniversary', 'unisex', 18, 80, 4.6, False, False),
    ("Personalized Photo Mug", 'personalized', 1500, 'birthday', 'unisex', 10, 80, 4.5, True, True),
    ("Engraved Wooden Photo Frame", 'personalized', 2800, 'anniversary', 'unisex', 16, 80, 4.6, False, False),
    ("Custom Name Necklace", 'personalized', 3500, 'birthday', 'female', 14, 45, 4.7, True, False),
    ("Personalized Leather Wallet", 'personalized', 3200, 'fathers_day', 'male', 18, 70, 4.5, False, True),
    ("Custom Star Map Print", 'personalized', 2600, 'anniversary', 'unisex', 16, 70, 4.4, False, False),
    ("Wireless Bluetooth Earbuds", 'electronics', 4800, 'birthday', 'unisex', 14, 45, 4.4, True, True),
    ("Smart Fitness Watch", 'electronics', 7500, 'graduation', 'unisex', 16, 50, 4.6, True, True),
    ("Portable Bluetooth Speaker", 'electronics', 3900, 'birthday', 'unisex', 12, 50, 4.3, False, False),
    ("Instant Mini Photo Printer", 'electronics', 5200, 'birthday', 'female', 14, 35, 4.2, False, False),
    ("Best-Selling Novel Collection (Set of 3)", 'books', 2400, 'graduation', 'unisex', 14, 60, 4.5, False, False),
    ("Motivational Journal & Pen Set", 'books', 1700, 'graduation', 'unisex', 14, 60, 4.3, False, False),
    ("Kids' Illustrated Storybook Set", 'books', 1900, 'baby_shower', 'kids', 1, 10, 4.6, False, False),
    ("Building Blocks Mega Set", 'toys', 2900, 'baby_shower', 'kids', 2, 10, 4.7, False, True),
    ("Plush Teddy Bear (Large)", 'toys', 2100, 'birthday', 'kids', 1, 12, 4.8, True, False),
    ("Remote Control Race Car", 'toys', 3400, 'birthday', 'kids', 5, 14, 4.4, False, False),
    ("Family Board Game Bundle", 'games', 3100, 'christmas', 'unisex', 8, 70, 4.5, False, False),
    ("Wireless Gaming Controller", 'games', 5600, 'birthday', 'male', 12, 35, 4.3, True, False),
    ("Puzzle Cube Set", 'games', 1200, 'birthday', 'kids', 6, 18, 4.1, False, False),
    ("Scented Candle Gift Set", 'home-decor', 2300, 'general', 'unisex', 16, 80, 4.5, False, True),
    ("Decorative Wall Clock", 'home-decor', 3600, 'wedding', 'unisex', 18, 80, 4.2, False, False),
    ("Cozy Throw Blanket", 'home-decor', 2700, 'christmas', 'unisex', 14, 80, 4.6, False, False),
    ("Ceramic Vase Set", 'home-decor', 3300, 'wedding', 'unisex', 18, 80, 4.3, False, False),
    ("Silk Scarf", 'fashion', 2200, 'birthday', 'female', 18, 65, 4.4, False, False),
    ("Designer Sunglasses", 'fashion', 4100, 'birthday', 'unisex', 16, 50, 4.5, True, False),
    ("Classic Leather Belt", 'fashion', 2600, 'fathers_day', 'male', 18, 65, 4.2, False, False),
    ("Premium Tote Bag", 'fashion', 3700, 'birthday', 'female', 16, 50, 4.3, False, False),
    ("Gourmet Chocolate Hamper", 'gourmet', 3000, 'valentine', 'unisex', 12, 80, 4.8, True, True),
    ("Artisan Coffee & Mug Gift Set", 'gourmet', 2800, 'fathers_day', 'unisex', 18, 80, 4.5, False, False),
    ("Wine & Cheese Gift Basket", 'gourmet', 5400, 'anniversary', 'unisex', 21, 80, 4.6, False, False),
    ("Spa Relaxation Gift Set", 'wellness', 3500, 'mothers_day', 'female', 18, 70, 4.7, True, True),
    ("Aromatherapy Diffuser Set", 'wellness', 2900, 'general', 'unisex', 16, 70, 4.4, False, False),
    ("Yoga Mat & Accessories Kit", 'wellness', 3300, 'birthday', 'female', 14, 55, 4.3, False, False),
    ("Premium Notebook & Pen Set", 'stationery', 1600, 'graduation', 'unisex', 12, 60, 4.2, False, False),
    ("Desk Organizer Set", 'stationery', 1900, 'graduation', 'unisex', 14, 60, 4.1, False, False),
    ("Luxury Gift Hamper Box", 'gift-box', 4700, 'christmas', 'unisex', 16, 80, 4.7, True, True),
    ("Birthday Surprise Gift Box", 'gift-box', 3900, 'birthday', 'unisex', 10, 80, 4.6, True, False),
    ("New Baby Gift Box", 'gift-box', 4100, 'baby_shower', 'kids', 0, 2, 4.5, False, False),
    ("Floral Eau de Parfum", 'perfume', 4600, 'birthday', 'female', 16, 60, 4.6, False, True),
    ("Men's Signature Cologne", 'perfume', 4400, 'fathers_day', 'male', 16, 60, 4.5, False, False),
    ("Luxury Skincare Gift Set", 'perfume', 3800, 'mothers_day', 'female', 18, 70, 4.7, True, False),
]


class Command(BaseCommand):
    help = 'Seed the database with demo categories, products, users, orders and reminders.'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing demo data...')
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        CartItem.objects.all().delete()
        WishlistItem.objects.all().delete()
        Reminder.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('Creating categories...')
        category_map = {}
        for name, slug, icon in CATEGORIES:
            category_map[slug] = Category.objects.create(name=name, slug=slug, icon=icon)

        self.stdout.write('Creating products...')
        for name, cat_slug, price, occasion, gender, min_age, max_age, rating, trending, featured in PRODUCTS:
            Product.objects.create(
                name=name,
                slug=slugify(name),
                description=(
                    f'{name} - a thoughtfully chosen gift, perfect for '
                    f'{dict(Product.OCCASION_CHOICES).get(occasion, occasion)} celebrations.'
                ),
                price=price,
                category=category_map[cat_slug],
                occasion=occasion,
                gender=gender,
                stock=random.randint(5, 60),
                image_url=f'https://picsum.photos/seed/{slugify(name)}/500/500',
                rating=rating,
                rating_count=random.randint(8, 320),
                is_trending=trending,
                is_featured=featured,
                min_age=min_age,
                max_age=max_age,
            )

        self.stdout.write('Creating users...')
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(username='admin', email='admin@giftgenius.ai', password='Admin@123')
        demo_user, created = User.objects.get_or_create(
            username='demo', defaults={'email': 'demo@giftgenius.ai', 'first_name': 'Demo', 'last_name': 'User'}
        )
        if created:
            demo_user.set_password('Demo@123')
            demo_user.save()

        self.stdout.write('Creating sample reminders...')
        today = date.today()
        Reminder.objects.create(
            user=demo_user, person_name='Mum', occasion='birthday',
            date=today + timedelta(days=5), notes='She loves flowers and jewelry.'
        )
        Reminder.objects.create(
            user=demo_user, person_name='Alex & Jamie', occasion='anniversary',
            date=today + timedelta(days=20), notes='Their 3rd wedding anniversary.'
        )

        self.stdout.write('Creating a sample order...')
        sample_products = list(Product.objects.all()[:2])
        if sample_products:
            order = Order.objects.create(
                user=demo_user,
                total_amount=sum(p.price for p in sample_products),
                status='completed',
                payment_method='mpesa',
                full_name='Demo User',
                phone_number='0712345678',
                address='123 Kimathi Street',
                city='Nairobi',
            )
            for product in sample_products:
                OrderItem.objects.create(order=order, product=product, quantity=1, price=product.price)

        self.stdout.write(self.style.SUCCESS(
            f'Seed complete: {Category.objects.count()} categories, {Product.objects.count()} products. '
            f'Admin login -> admin / Admin@123. Demo login -> demo / Demo@123.'
        ))
