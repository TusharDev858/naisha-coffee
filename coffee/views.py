from decimal import Decimal

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    Branch, ContactMessage, GalleryImage, MenuCategory,
    MenuItem, Order, OrderItem, SiteSettings, TeamMember, Testimonial,
)


def site_context():
    return {"site": SiteSettings.load()}


# ---------- Cart helpers (session based) ----------
def _get_cart(request):
    """Cart is a dict: { "item_id": quantity }"""
    return request.session.get("cart", {})


def _save_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True


def _cart_count(request):
    return sum(_get_cart(request).values())


def _cart_detail(request):
    """Return list of line dicts + subtotal."""
    cart = _get_cart(request)
    items, subtotal = [], Decimal("0")
    for item_id, qty in cart.items():
        try:
            mi = MenuItem.objects.get(pk=int(item_id))
        except (MenuItem.DoesNotExist, ValueError):
            continue
        line_total = mi.price * qty
        subtotal += line_total
        items.append({"item": mi, "qty": qty, "line_total": line_total})
    return items, subtotal


# ---------- Pages ----------
def home(request):
    context = site_context()
    context["categories"] = MenuCategory.objects.prefetch_related("items").all()
    context["featured_items"] = MenuItem.objects.filter(is_featured=True, is_available=True)[:6]
    context["ticker_items"] = list(
        MenuItem.objects.filter(is_available=True)
        .exclude(image="").exclude(image__isnull=True)
        .select_related("category")
    )
    context["testimonials"] = Testimonial.objects.filter(is_active=True)[:6]
    context["gallery_images"] = GalleryImage.objects.all()[:8]
    context["branches"] = Branch.objects.all()
    context["cart_count"] = _cart_count(request)
    return render(request, "home.html", context)


def about(request):
    context = site_context()
    context["team"] = TeamMember.objects.all()
    context["branches"] = Branch.objects.all()
    context["cart_count"] = _cart_count(request)
    return render(request, "about.html", context)


def menu(request):
    context = site_context()
    context["categories"] = MenuCategory.objects.prefetch_related("items").all()
    context["cart_count"] = _cart_count(request)
    return render(request, "menu.html", context)


def testimonials(request):
    context = site_context()
    context["testimonials"] = Testimonial.objects.filter(is_active=True)
    context["cart_count"] = _cart_count(request)
    return render(request, "testimonials.html", context)


def gallery(request):
    context = site_context()
    context["gallery_images"] = GalleryImage.objects.all()
    context["cart_count"] = _cart_count(request)
    return render(request, "gallery.html", context)


def branches(request):
    context = site_context()
    context["branches"] = Branch.objects.all()
    context["cart_count"] = _cart_count(request)
    return render(request, "branches.html", context)


def contact(request):
    context = site_context()
    context["cart_count"] = _cart_count(request)
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message_text = request.POST.get("message", "").strip()
        if name and email and message_text:
            ContactMessage.objects.create(
                name=name, email=email, subject=subject, message=message_text
            )
            messages.success(request, "Thanks for reaching out! We'll get back to you soon.")
            return redirect("contact")
        messages.error(request, "Please fill in your name, email and message.")
    return render(request, "contact.html", context)


# ---------- Cart actions ----------
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id, is_available=True)
    cart = _get_cart(request)
    key = str(item_id)
    qty = 1
    if request.method == "POST":
        try:
            qty = max(1, int(request.POST.get("quantity", 1)))
        except ValueError:
            qty = 1
    cart[key] = cart.get(key, 0) + qty
    _save_cart(request, cart)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"ok": True, "cart_count": _cart_count(request), "item": item.name})

    messages.success(request, f"Added {item.name} to your cart.")
    return redirect(request.META.get("HTTP_REFERER", "menu"))


def update_cart(request, item_id):
    cart = _get_cart(request)
    key = str(item_id)
    action = request.POST.get("action")
    if key in cart:
        if action == "increase":
            cart[key] += 1
        elif action == "decrease":
            cart[key] -= 1
            if cart[key] <= 0:
                del cart[key]
        elif action == "remove":
            del cart[key]
    _save_cart(request, cart)
    return redirect("cart")


def cart(request):
    context = site_context()
    items, subtotal = _cart_detail(request)
    delivery_fee = context["site"].delivery_fee if items else Decimal("0")
    context.update({
        "cart_items": items,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": subtotal + delivery_fee,
        "cart_count": _cart_count(request),
    })
    return render(request, "cart.html", context)


def checkout(request):
    context = site_context()
    items, subtotal = _cart_detail(request)

    if not items:
        messages.error(request, "Your cart is empty. Add something delicious first!")
        return redirect("menu")

    delivery_fee = context["site"].delivery_fee
    total = subtotal + delivery_fee

    if request.method == "POST":
        name = request.POST.get("customer_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        address = request.POST.get("address", "").strip()
        branch_id = request.POST.get("branch") or None
        notes = request.POST.get("notes", "").strip()
        payment_method = request.POST.get("payment_method", "cod")

        if name and phone and address:
            order = Order.objects.create(
                customer_name=name, phone=phone, email=email, address=address,
                branch_id=branch_id if branch_id else None,
                notes=notes, payment_method=payment_method,
                subtotal=subtotal, delivery_fee=delivery_fee, total=total,
            )
            for line in items:
                OrderItem.objects.create(
                    order=order, menu_item=line["item"], item_name=line["item"].name,
                    price=line["item"].price, quantity=line["qty"],
                )
            # Clear cart
            _save_cart(request, {})
            return redirect("order_success", order_id=order.pk)
        messages.error(request, "Please fill in your name, phone and delivery address.")

    context.update({
        "cart_items": items,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
        "branches": Branch.objects.all(),
        "cart_count": _cart_count(request),
    })
    return render(request, "checkout.html", context)


def order_success(request, order_id):
    context = site_context()
    order = get_object_or_404(Order, pk=order_id)
    context["order"] = order
    context["cart_count"] = _cart_count(request)
    return render(request, "order_success.html", context)
