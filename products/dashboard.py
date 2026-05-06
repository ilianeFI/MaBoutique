from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from .models import Product
from orders.models import Order

# ─────────────────────────────────────────────────────────────
#  Badges sidebar (appelés dynamiquement par Unfold)
# ─────────────────────────────────────────────────────────────

def badge_produits(request):
    """Affiche le total produits dans la sidebar."""
    count = Product.objects.count()
    return str(count) if count else None


def badge_commandes(request):
    """Commandes des 24 dernières heures."""
    depuis = timezone.now() - timedelta(hours=24)
    count = Order.objects.filter(date__gte=depuis).count()
    return str(count) if count else None


def badge_alertes(request):
    """Produits en stock critique — badge rouge dans la sidebar."""
    count = Product.objects.filter(quantity__lte=5).count()
    return str(count) if count else None


# ─────────────────────────────────────────────────────────────
#  Callback principal du dashboard
# ─────────────────────────────────────────────────────────────

def dashboard_callback(request, context):
    """
    Injecte les données dans le contexte du template dashboard.html.
    Appelé automatiquement par Unfold via DASHBOARD_CALLBACK.
    """
    aujourd_hui = timezone.now()
    debut_mois  = aujourd_hui.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    hier        = aujourd_hui - timedelta(days=1)

    # ── Produits ──────────────────────────────────────────────
    total_products  = Product.objects.count()
    low_stock       = Product.objects.filter(quantity__lte=5).count()
    out_of_stock    = Product.objects.filter(quantity=0).count()

    # ── Commandes ─────────────────────────────────────────────
    total_orders        = Order.objects.count()
    orders_ce_mois      = Order.objects.filter(date__gte=debut_mois).count()
    orders_hier         = Order.objects.filter(
                            date__date=hier.date()
                          ).count()

    # ── Chiffre d'affaires ────────────────────────────────────
    # Adapte "total_price" au nom de ton champ réel
    ca_total  = Order.objects.aggregate(total=Sum("prix"))["total"] or 0
    ca_mois   = Order.objects.filter(
                    date__gte=debut_mois
                ).aggregate(total=Sum("prix"))["total"] or 0

    # ── Clients ───────────────────────────────────────────────
    try:
        from users.models import CustomUser
        total_clients = CustomUser.objects.filter(is_staff=False).count()
        nouveaux_clients = CustomUser.objects.filter(
            date_joined__gte=debut_mois, is_staff=False
        ).count()
    except Exception:
        total_clients    = 0
        nouveaux_clients = 0

    # ── Paniers ───────────────────────────────────────────────
    try:
        from cart.models import Cart
        paniers_actifs = Cart.objects.count()
    except Exception:
        paniers_actifs = 0

    # ── Commandes récentes (5 dernières) ──────────────────────
    recent_orders = (
        Order.objects
        .select_related("user")          # adapte si ton champ FK s'appelle autrement
        .order_by("-date")[:5]
    )

    # ── Produits à réapprovisionner ───────────────────────────
    critical_products = (
        Product.objects
        .filter(quantity__lte=5)
        .order_by("quantity")[:6]
    )

    # ── Graphique : commandes 7 derniers jours ────────────────
    chart_labels = []
    chart_data   = []
    for i in range(6, -1, -1):
        jour = (aujourd_hui - timedelta(days=i)).date()
        nb   = Order.objects.filter(date__date=jour).count()
        chart_labels.append(jour.strftime("%d/%m"))
        chart_data.append(nb)

    context.update({
        # Totaux globaux
        "total_products"  : total_products,
        "total_orders"    : total_orders,
        "low_stock"       : low_stock,
        "out_of_stock"    : out_of_stock,
        "total_clients"   : total_clients,
        "paniers_actifs"  : paniers_actifs,

        # Ce mois
        "orders_ce_mois"  : orders_ce_mois,
        "nouveaux_clients": nouveaux_clients,
        "ca_mois"         : ca_mois,
        "ca_total"        : ca_total,

        # Listes
        "recent_orders"   : recent_orders,
        "critical_products": critical_products,

        # Graphique
        "chart_labels"    : chart_labels,   # liste Python → json_script dans le template
        "chart_data"      : chart_data,
    })

    return context