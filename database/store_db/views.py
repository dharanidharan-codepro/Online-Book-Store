
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import (
    Book, Category, FeaturedBook, CartItem, Order, OrderItem
)


def home(request):
    books = Book.objects.select_related("category").all()
    categories = Category.objects.all()
    featured_books = FeaturedBook.objects.filter(
        is_active=True
    ).select_related("book").order_by("display_order")

    cart_items = []
    cart_total = Decimal("0.00")

    if request.user.is_authenticated:
        cart_items = list(
            CartItem.objects.filter(user=request.user).select_related("book")
        )
        cart_total = sum(
            (item.book.price * item.quantity for item in cart_items),
            Decimal("0.00")
        )

    return render(request, "home.html", {
        "books": books,
        "categories": categories,
        "featured_books": featured_books,
        "cart_items": cart_items,
        "cart_total": cart_total,
    })


@login_required
@require_POST
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if book.stock_quantity < 1:
        messages.error(request, "This book is out of stock.")
        return redirect("home")

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={"quantity": 1},
    )

    if not created:
        if item.quantity < book.stock_quantity:
            item.quantity += 1
            item.save(update_fields=["quantity"])
        else:
            messages.warning(request, "Maximum available stock reached.")

    return redirect("home")


@login_required
@require_POST
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, user=request.user)

    try:
        quantity = int(request.POST.get("quantity", "1"))
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        item.delete()
    elif quantity <= item.book.stock_quantity:
        item.quantity = quantity
        item.save(update_fields=["quantity"])
    else:
        messages.error(request, "Requested quantity exceeds available stock.")

    return redirect("home")


@login_required
@require_POST
def remove_from_cart(request, item_id):
    CartItem.objects.filter(pk=item_id, user=request.user).delete()
    return redirect("home")


@login_required
def checkout(request):
    cart_items = list(
        CartItem.objects.filter(user=request.user).select_related("book")
    )

    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect("home")

    total = sum(
        (item.book.price * item.quantity for item in cart_items),
        Decimal("0.00")
    )

    if request.method == "POST":
        name = request.POST.get("customer_name", "").strip()
        email = request.POST.get("email", "").strip()
        address = request.POST.get("address", "").strip()

        if not name or not email or not address:
            messages.error(request, "Please fill in all checkout fields.")
            return render(request, "home.html", {
                "books": Book.objects.select_related("category").all(),
                "categories": Category.objects.all(),
                "featured_books": FeaturedBook.objects.filter(
                    is_active=True
                ).select_related("book").order_by("display_order"),
                "cart_items": cart_items,
                "cart_total": total,
                "checkout_open": True,
            })

        try:
            with transaction.atomic():
                # Lock books and verify stock before saving the order.
                for item in cart_items:
                    book = Book.objects.select_for_update().get(pk=item.book_id)
                    if item.quantity > book.stock_quantity:
                        raise ValueError(
                            f"Not enough stock for {book.title}."
                        )

                order = Order.objects.create(
                    user=request.user,
                    customer_name=name,
                    email=email,
                    address=address,
                    total_amount=total,
                )

                for item in cart_items:
                    book = Book.objects.select_for_update().get(pk=item.book_id)
                    OrderItem.objects.create(
                        order=order,
                        book=book,
                        quantity=item.quantity,
                        price_at_purchase=book.price,
                    )
                    book.stock_quantity -= item.quantity
                    book.save(update_fields=["stock_quantity"])

                CartItem.objects.filter(user=request.user).delete()

            messages.success(request, f"Order #{order.pk} placed successfully!")
            return redirect("order_history")

        except ValueError as error:
            messages.error(request, str(error))
            return redirect("home")

    return render(request, "home.html", {
        "books": Book.objects.select_related("category").all(),
        "categories": Category.objects.all(),
        "featured_books": FeaturedBook.objects.filter(
            is_active=True
        ).select_related("book").order_by("display_order"),
        "cart_items": cart_items,
        "cart_total": total,
        "checkout_open": True,
    })


@login_required
def order_history(request):
    if request.user.is_staff:
        orders = Order.objects.select_related("user").prefetch_related(
            "items__book"
        ).all()
    else:
        orders = Order.objects.filter(user=request.user).prefetch_related(
            "items__book"
        )

    return render(request, "home.html", {
        "books": Book.objects.select_related("category").all(),
        "categories": Category.objects.all(),
        "featured_books": FeaturedBook.objects.filter(
            is_active=True
        ).select_related("book").order_by("display_order"),
        "orders": orders,
        "show_orders": True,
    })


def staff_check(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(staff_check)
def add_book(request):
    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        author = request.POST.get("author", "").strip()
        description = request.POST.get("description", "").strip()
        category_id = request.POST.get("category")
        price_text = request.POST.get("price", "").strip()
        stock_text = request.POST.get("stock_quantity", "0").strip()

        try:
            price = Decimal(price_text)
            stock = int(stock_text)
            category = Category.objects.get(pk=category_id)

            if not title or not author or price < 0 or stock < 0:
                raise ValueError

            Book.objects.create(
                title=title,
                author=author,
                description=description,
                category=category,
                price=price,
                stock_quantity=stock,
            )
            messages.success(request, "Book added successfully.")
            return redirect("home")

        except (ValueError, TypeError, Category.DoesNotExist):
            messages.error(request, "Please enter valid book details.")

    return render(request, "home.html", {
        "books": Book.objects.select_related("category").all(),
        "categories": categories,
        "featured_books": FeaturedBook.objects.filter(
            is_active=True
        ).select_related("book").order_by("display_order"),
        "show_add_book": True,
    })
