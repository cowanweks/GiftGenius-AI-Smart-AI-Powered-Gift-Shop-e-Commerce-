from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text='React-icon name, e.g. FaGift')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    OCCASION_CHOICES = [
        ('birthday', 'Birthday'),
        ('anniversary', 'Anniversary'),
        ('wedding', 'Wedding'),
        ('graduation', 'Graduation'),
        ('valentine', "Valentine's Day"),
        ('christmas', 'Christmas'),
        ('mothers_day', "Mother's Day"),
        ('fathers_day', "Father's Day"),
        ('baby_shower', 'Baby Shower'),
        ('general', 'General / Just Because'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unisex', 'Unisex'),
        ('kids', 'Kids'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES, default='general')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex')
    stock = models.PositiveIntegerField(default=0)
    company = models.ForeignKey(
        'vendors.Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='products',
        help_text='Supplying company, if this product was listed by a vendor rather than the store admin.',
    )
    is_approved = models.BooleanField(
        default=True, help_text='Vendor-submitted products start unapproved until admin reviews them.',
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text='Fallback external image URL')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.PositiveIntegerField(default=0)
    is_trending = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    min_age = models.PositiveIntegerField(default=0)
    max_age = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url
