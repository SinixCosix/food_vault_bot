def format_product(product):
    variant = f"{product['variant']}" if product.get('variant') else ""

    text = (
        f"Category: {product['category']}\n"
        f"Brand: {product['product']}\n"
        f"Variant: {variant}\n"
        f"Flavor: {product['flavor']}\n"
        "\n"
        f"🦖 Arina: {product['rating_arina']}/10\n"
        f"💬 {product.get('comment_arina') or '—'}\n\n"
        f"🌵 Andrew: {product['rating_andrew']}/10\n"
        f"💬 {product.get('comment_andrew') or '—'}"
    )

    return text
