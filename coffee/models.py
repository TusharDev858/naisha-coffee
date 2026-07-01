from django.core.exceptions import ValidationError
from django.db import models


class SiteSettings(models.Model):
    # Branding
    site_name = models.CharField(max_length=60, default="Naisha Coffee")
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    favicon = models.ImageField(upload_to="branding/", blank=True, null=True)

    # Hero section
    hero_badge = models.CharField(max_length=60, default="Best Coffee In Town", blank=True)
    hero_title = models.CharField(max_length=120, default="Best Coffee")
    hero_subtitle = models.CharField(max_length=200, default="Make your day great with our special coffee!")
    hero_description = models.TextField(default="Welcome to our coffee paradise, where every bean tells a story and every cup sparks joy.")
    hero_image = models.ImageField(upload_to="branding/", blank=True, null=True)
    hero_button_text = models.CharField(max_length=40, default="Order Now")
    hero_button_link = models.CharField(max_length=200, default="#menu")
    hero_secondary_button_text = models.CharField(max_length=40, default="Contact Us", blank=True)
    hero_secondary_button_link = models.CharField(max_length=200, default="#contact", blank=True)

    # About section
    about_title = models.CharField(max_length=120, default="Our Story")
    about_text = models.TextField(default="Founded with a love for great coffee, Naisha Coffee brings you freshly roasted beans, a cozy atmosphere and baristas who treat every cup like a craft.")
    about_image = models.ImageField(upload_to="branding/", blank=True, null=True)
    years_experience = models.PositiveIntegerField(default=5)
    cups_served = models.PositiveIntegerField(default=50000)
    happy_customers = models.PositiveIntegerField(default=12000)

    # Contact / footer info
    address = models.CharField(max_length=200, default="House 12, Road 5, Gulshan, Dhaka, Bangladesh")
    phone = models.CharField(max_length=40, default="+880 1234 567890")
    email = models.EmailField(default="hello@naishacoffee.com")
    opening_hours = models.CharField(max_length=200, default="Mon - Sun: 8:00 AM - 10:00 PM", blank=True)
    map_embed_url = models.URLField(blank=True, help_text="Google Maps embed URL (optional)")
    delivery_fee = models.DecimalField(
        max_digits=8, decimal_places=2, default=60,
        help_text="Flat delivery fee (৳) added to every order",
    )

    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    whatsapp_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    footer_text = models.CharField(max_length=250, default="Brewed with love, served with a smile.", blank=True)
    copyright_text = models.CharField(max_length=150, default="© Naisha Coffee. All rights reserved.", blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Branch(models.Model):
    name = models.CharField(max_length=80, help_text="e.g. Naisha Coffee Gulshan")
    area = models.CharField(max_length=80, help_text="e.g. Gulshan, Dhaka")
    address = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="branches/", blank=True, null=True)
    phone = models.CharField(max_length=40, blank=True)
    opening_hours = models.CharField(max_length=120, blank=True, default="8:00 AM - 10:00 PM")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name


class MenuCategory(models.Model):
    name = models.CharField(max_length=60)
    icon = models.CharField(max_length=10, blank=True, help_text="Optional emoji icon, e.g. ☕")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Menu Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="menu/", blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text="Show in 'Popular Picks'")
    is_available = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} ({self.category})"


class Testimonial(models.Model):
    name = models.CharField(max_length=80)
    role = models.CharField(max_length=80, blank=True, help_text="e.g. Regular Customer")
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]

    def clean(self):
        if not (1 <= self.rating <= 5):
            raise ValidationError({"rating": "Rating must be between 1 and 5."})

    def stars_range(self):
        return range(self.rating)

    def empty_stars_range(self):
        return range(5 - self.rating)

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=120, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return self.caption or f"Gallery image #{self.pk}"


class TeamMember(models.Model):
    name = models.CharField(max_length=80)
    role = models.CharField(max_length=80, default="Barista")
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    bio = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    subject = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject or 'No subject'}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("preparing", "Preparing"),
        ("out_for_delivery", "Out for Delivery"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    PAYMENT_CHOICES = [
        ("cod", "Cash on Delivery"),
        ("bkash", "bKash"),
        ("nagad", "Nagad"),
        ("card", "Card on Delivery"),
    ]

    # Customer details
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    address = models.TextField(help_text="Full delivery address")
    branch = models.ForeignKey(
        "Branch", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="orders",
        help_text="Preferred / nearest branch",
    )
    notes = models.TextField(blank=True, help_text="Any special instructions")

    # Order details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="cod")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, default=60)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} — {self.customer_name} (৳{self.total})"

    @property
    def order_number(self):
        return f"NC{self.pk:05d}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.SET_NULL, null=True, blank=True
    )
    item_name = models.CharField(max_length=80)  # snapshot in case item is deleted
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} × {self.item_name}"

    @property
    def line_total(self):
        return self.price * self.quantity
