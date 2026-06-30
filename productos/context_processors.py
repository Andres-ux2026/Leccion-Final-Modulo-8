def carrito_count(request):
    if request.user.is_authenticated:
        carrito = request.session.get("carrito", {})
        count = sum(item["cantidad"] for item in carrito.values())
        return {"carrito_count": count}
    return {"carrito_count": 0}
