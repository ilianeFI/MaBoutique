from django.utils import timezone
from datetime import timedelta
from .models import Product
from orders.models import Order
from cart.models import Cart


def dashboard_callback(request, context):

    now   = timezone.now()
    today = now.date()

    # ── Stat cards ──────────────────────────────────────
    context["total_products"] = Product.objects.count()
    context["total_orders"]   = Order.objects.count()
    context["total_carts"]    = Cart.objects.count()
    context["low_stock"]      = Product.objects.filter(quantity__lte=5).count()

    # ── Low stock product list (for bottom panel) ────────
    context["low_stock_products"] = (
        Product.objects.filter(quantity__lte=5).order_by("quantity")[:6]
    )

    # ── Revenue ──────────────────────────────────────────
    orders_this_month = Order.objects.filter(
        date__year=now.year,
        date__month=now.month,
    )
    all_orders = Order.objects.all()

    context["revenue_month"] = sum(o.prix for o in orders_this_month) or 0
    context["revenue_total"] = sum(o.prix for o in all_orders) or 0
    context["avg_order"]     = (
        round(context["revenue_total"] / context["total_orders"], 2)
        if context["total_orders"] > 0 else 0
    )

    # ── Recent orders (table) ────────────────────────────
    context["recent_orders"] = (
        Order.objects.select_related("user")
        .order_by("-date")[:8]
    )

    # ── Chart — orders per day last 7 days ───────────────
    labels     = []
    chart_data = []
    day_names  = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = Order.objects.filter(date__date=day).count()
        labels.append(day_names[day.weekday()])
        chart_data.append(count)

    context["chart_labels"] = labels
    context["chart_data"]   = chart_data

    return context