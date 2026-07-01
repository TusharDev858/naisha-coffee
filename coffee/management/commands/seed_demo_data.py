import os
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from coffee.models import (
    Branch, GalleryImage, MenuCategory, MenuItem,
    SiteSettings, TeamMember, Testimonial,
)


def seed_file(static_rel, media_rel):
    """Copy a file from static/ to media/ and return the relative media path."""
    src = Path(settings.BASE_DIR) / "static" / static_rel
    dst = Path(settings.MEDIA_ROOT) / media_rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists():
        shutil.copy2(src, dst)
        return media_rel
    return None


class Command(BaseCommand):
    help = "Populate the site with demo Naisha Coffee content."

    def handle(self, *args, **options):
        # ---------- Site Settings ----------
        s = SiteSettings.load()
        s.site_name = "Naisha Coffee"
        s.hero_badge = "Best Coffee In Town"
        s.hero_title = "Best Coffee"
        s.hero_subtitle = "Make your day great with our special coffee!"
        s.hero_description = (
            "Welcome to our coffee paradise, where every bean tells a story "
            "and every cup sparks joy."
        )
        s.about_title = "Our Story"
        s.about_text = (
            "Naisha Coffee started as a small neighbourhood roastery with one "
            "promise: every cup should feel like a warm hug. Today we source "
            "ethically grown beans, roast them in small batches, and serve "
            "them with care in a cozy, modern space designed for slow "
            "mornings and good conversations."
        )
        s.years_experience = 6
        s.cups_served = 85000
        s.happy_customers = 15000
        s.address = "House 12, Road 5, Gulshan, Dhaka, Bangladesh"
        s.phone = "+880 1711 000000"
        s.email = "hello@naishacoffee.com"
        s.opening_hours = "Mon – Sun: 8:00 AM – 10:00 PM"
        s.instagram_url = "https://www.instagram.com/_chaosoracle_?igsh=MTdma2twZXMybWN5bA=="
        s.facebook_url = "https://www.facebook.com/"
        s.whatsapp_url = "https://wa.me/8801711000000"
        s.youtube_url = "https://www.youtube.com/"
        s.footer_text = "Brewed with love, served with a smile."
        s.copyright_text = "© Naisha Coffee. All rights reserved."

        owner_path = seed_file("img/owner.png", "branding/owner.png")
        if owner_path:
            s.about_image = owner_path
        s.save()

        # ---------- Menu ----------
        categories_data = [
            ("Hot Coffee", "☕"),
            ("Cold & Iced", "🧊"),
            ("Pastries", "🥐"),
            ("Specials", "✨"),
        ]
        cats = {}
        for i, (name, icon) in enumerate(categories_data):
            c, _ = MenuCategory.objects.get_or_create(name=name, defaults={"icon": icon, "order": i})
            cats[name] = c

        items_data = [
            # (category, name, desc, price, featured, static_img, media_img)
            ("Hot Coffee", "Espresso", "Rich, bold single shot of pure espresso.", 120, True, "img/menu/cupping.png", "menu/cupping.png"),
            ("Hot Coffee", "Cappuccino", "Espresso topped with perfectly steamed milk foam.", 180, True, "img/menu/latte-art.png", "menu/latte-art.png"),
            ("Hot Coffee", "Caffe Latte", "Smooth espresso blended with silky steamed milk.", 190, False, "img/menu/barista.jpg", "menu/barista.jpg"),
            ("Hot Coffee", "Mocha", "Espresso, rich chocolate and steamed milk.", 210, False, None, None),
            ("Cold & Iced", "Iced Latte", "Chilled espresso poured over ice and cold milk.", 200, True, "img/menu/kettle.jpg", "menu/kettle.jpg"),
            ("Cold & Iced", "Cold Brew", "Slow-steeped for 18 hours — smooth and naturally sweet.", 220, True, None, None),
            ("Cold & Iced", "Frappe", "Blended iced coffee topped with whipped cream.", 240, False, None, None),
            ("Cold & Iced", "Raspberry Mocha Freddo", "Chilled mocha blended with raspberry — a house special.", 260, True, "img/menu/raspberry-mocha.png", "menu/raspberry-mocha.png"),
            ("Pastries", "Butter Croissant", "Flaky, buttery croissant baked fresh every morning.", 150, True, None, None),
            ("Pastries", "Granola Parfait", "Layered yogurt, honey granola and a golden croissant.", 180, False, "img/menu/granola.png", "menu/granola.png"),
            ("Pastries", "Cinnamon Roll", "Soft roll swirled with cinnamon sugar glaze.", 160, False, None, None),
            ("Specials", "Caramel Macchiato", "Vanilla, espresso, steamed milk and caramel drizzle.", 230, True, "img/menu/mug.png", "menu/mug.png"),
            ("Specials", "Hazelnut Delight", "Espresso with hazelnut syrup and fresh cream.", 220, False, None, None),
        ]
        for order, (cat_name, name, desc, price, featured, src, dst) in enumerate(items_data):
            item, _ = MenuItem.objects.get_or_create(
                category=cats[cat_name], name=name,
                defaults={"description": desc, "price": price, "is_featured": featured, "order": order},
            )
            if src and dst and not item.image:
                path = seed_file(src, dst)
                if path:
                    item.image = path
                    item.save(update_fields=["image"])

        # ---------- Branches ----------
        branches_data = [
            ("Naisha Coffee Gulshan", "Gulshan, Dhaka", "House 12, Road 5, Gulshan-1, Dhaka 1212", "+880 1711 001100", "img/branches/gulshan.jpg", "branches/gulshan.jpg"),
            ("Naisha Coffee Banani", "Banani, Dhaka", "Road 11, Block C, Banani, Dhaka 1213", "+880 1711 002200", "img/branches/banani.jpg", "branches/banani.jpg"),
            ("Naisha Coffee Mirpur", "Mirpur, Dhaka", "Section 10, Main Road, Mirpur, Dhaka 1216", "+880 1711 003300", "img/branches/mirpur.jpeg", "branches/mirpur.jpeg"),
            ("Naisha Coffee Mohammadpur", "Mohammadpur, Dhaka", "Nabodoy Housing, Road 3, Mohammadpur, Dhaka 1207", "+880 1711 004400", "img/branches/mohammadpur.jpg", "branches/mohammadpur.jpg"),
        ]
        for order, (name, area, address, phone, src, dst) in enumerate(branches_data):
            branch, _ = Branch.objects.get_or_create(
                name=name,
                defaults={"area": area, "address": address, "phone": phone, "opening_hours": "Mon – Sun: 8:00 AM – 10:00 PM", "order": order},
            )
            if src and not branch.photo:
                path = seed_file(src, dst)
                if path:
                    branch.photo = path
                    branch.save(update_fields=["photo"])

        # ---------- Testimonials ----------
        tests = [
            ("Anika Rahman", "Regular Customer", "The cold brew here is unmatched. It's become part of my morning routine!", 5),
            ("Tahsin Ahmed", "Coffee Enthusiast", "Cozy vibe, friendly staff, and the cappuccino foam art is always perfect.", 5),
            ("Farzana Islam", "Food Blogger", "Their granola parfait pairs beautifully with the house blend. Highly recommend!", 4),
            ("Imran Hossain", "Office Worker", "I visit the Banani branch daily. Fast service, great ambiance.", 5),
            ("Sadia Akter", "Student", "The Raspberry Mocha Freddo is simply divine. Nothing compares!", 5),
            ("Rafiq Uddin", "Freelancer", "Perfect place to work. Strong WiFi, great coffee, zero distractions.", 4),
        ]
        for order, (name, role, msg, rating) in enumerate(tests):
            Testimonial.objects.get_or_create(name=name, defaults={"role": role, "message": msg, "rating": rating, "order": order})

        # ---------- Gallery ----------
        gallery_data = [
            ("img/menu/latte-art.png", "gallery/latte-art.png", "Latte art by our baristas"),
            ("img/menu/barista.jpg", "gallery/barista.jpg", "Crafting your perfect cup"),
            ("img/menu/cupping.png", "gallery/cupping.png", "Coffee cupping session"),
            ("img/menu/kettle.jpg", "gallery/kettle.jpg", "The art of the pour"),
            ("img/menu/raspberry-mocha.png", "gallery/raspberry-mocha.png", "Raspberry Mocha Freddo"),
            ("img/menu/mug.png", "gallery/mug.png", "Craft Great Coffee"),
            ("img/menu/granola.png", "gallery/granola.png", "Morning granola parfait"),
        ]
        for i, (src, dst, caption) in enumerate(gallery_data):
            if not GalleryImage.objects.filter(caption=caption).exists():
                path = seed_file(src, dst)
                if path:
                    GalleryImage.objects.create(image=path, caption=caption, order=i)

        # ---------- Team ----------
        team_data = [
            ("Naisha", "Founder & Creative Director", "Started Naisha Coffee with a vision for exceptional, ethically sourced coffee and a welcoming community space.", "img/owner.png", "team/owner.png"),
            ("Sabbir Hossain", "Web Developer & Partner", "Co-founder who built the Naisha Coffee digital experience from the ground up. Passionate about beautiful design and seamless performance.", "img/sabbir.jpg", "team/sabbir.jpg"),
            ("Sumaiya Akter", "Pastry Chef", "Bakes fresh croissants and pastries every single morning before sunrise.", None, None),
        ]
        for order, (name, role, bio, src, dst) in enumerate(team_data):
            member, _ = TeamMember.objects.get_or_create(name=name, defaults={"role": role, "bio": bio, "order": order})
            if src and not member.photo:
                path = seed_file(src, dst)
                if path:
                    member.photo = path
                    member.save(update_fields=["photo"])

        self.stdout.write(self.style.SUCCESS("Naisha Coffee demo content created successfully."))
