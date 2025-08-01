def format_product(product):
    variant = f"{product['variant']}\n" if product.get('variant') else ""

    text = (
        f"{product['category']}\n"
        f"{variant}"
        f"{product['flavor']}\n"
        "\n"
        f"🦖 Arina: {product['rating_arina']}/10\n"
        f"💬 {product.get('comment_arina') or '—'}\n\n"
        f"🌵 Andrew: {product['rating_andrew']}/10\n"
        f"💬 {product.get('comment_andrew') or '—'}"
    )

    return text
