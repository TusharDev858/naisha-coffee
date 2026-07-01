from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Branch, ContactMessage, GalleryImage,
    MenuCategory, MenuItem, Order, OrderItem, SiteSettings, TeamMember, Testimonial,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Branding", {"fields": ("site_name", "logo", "favicon")}),
        ("Hero Section", {"fields": ("hero_badge", "hero_title", "hero_subtitle", "hero_description", "hero_image", "hero_button_text", "hero_button_link", "hero_secondary_button_text", "hero_secondary_button_link")}),
        ("About Section", {"fields": ("about_title", "about_text", "about_image", "years_experience", "cups_served", "happy_customers")}),
        ("Contact & Footer", {"fields": ("address", "phone", "email", "opening_hours", "delivery_fee", "map_embed_url", "facebook_url", "instagram_url", "whatsapp_url", "youtube_url", "twitter_url", "footer_text", "copyright_text")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.load()
        from django.shortcuts import redirect
        return redirect("admin:coffee_sitesettings_change", obj.pk)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "area", "phone", "order")
    list_editable = ("order",)
    search_fields = ("name", "area", "address")

    def thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:40px;width:60px;object-fit:cover;border-radius:6px;" />', obj.photo.url)
        return "—"
    thumb.short_description = ""


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ("name", "price", "image", "is_featured", "is_available", "order")


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "order", "item_count")
    list_editable = ("order",)
    inlines = [MenuItemInline]

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Items"


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "category", "price", "is_featured", "is_available", "order")
    list_editable = ("price", "is_featured", "is_available", "order")
    list_filter = ("category", "is_featured", "is_available")
    search_fields = ("name", "description")

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        return "—"
    thumb.short_description = ""


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "rating", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("is_active", "rating")
    search_fields = ("name", "message")


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("thumb", "caption", "order")
    list_editable = ("order",)

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;width:70px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        return "—"
    thumb.short_description = ""


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order")
    list_editable = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")




class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("item_name", "price", "quantity", "line_total")
    fields = ("item_name", "price", "quantity", "line_total")

    def line_total(self, obj):
        return f"৳{obj.line_total}"
    line_total.short_description = "Line Total"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "customer_name", "phone", "total", "payment_method", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "payment_method", "created_at", "branch")
    search_fields = ("customer_name", "phone", "email", "address")
    readonly_fields = ("customer_name", "phone", "email", "address", "branch", "notes",
                       "payment_method", "subtotal", "delivery_fee", "total", "created_at", "order_number")
    inlines = [OrderItemInline]
    fieldsets = (
        ("Order Info", {"fields": ("order_number", "status", "created_at")}),
        ("Customer", {"fields": ("customer_name", "phone", "email", "address", "branch", "notes")}),
        ("Payment", {"fields": ("payment_method", "subtotal", "delivery_fee", "total")}),
    )

    def has_add_permission(self, request):
        return False


admin.site.site_header = "Naisha Coffee Admin"
admin.site.site_title = "Naisha Coffee Admin"
admin.site.index_title = "Manage your coffee shop website"
