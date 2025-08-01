import pytest

from utils.format import format_product


def test_format_product_full_data():
    product = {
        'category': 'Coffee',
        'variant': 'Espresso',
        'flavor': 'Caramel',
        'rating_arina': 8,
        'comment_arina': 'Smooth taste',
        'rating_andrew': 7,
        'comment_andrew': 'Too sweet'
    }
    expected = (
        "Coffee\n"
        "Espresso\n"
        "Caramel\n"
        "\n"
        "🦖 Arina: 8/10\n"
        "💬 Smooth taste\n"
        "\n"
        "🌵 Andrew: 7/10\n"
        "💬 Too sweet"
    )
    assert format_product(product) == expected


def test_format_product_no_variant():
    product = {
        'category': 'Tea',
        'flavor': 'Green',
        'rating_arina': 6,
        'comment_arina': None,
        'rating_andrew': 5,
        'comment_andrew': 'Bitter'
    }
    expected = (
        "Tea\n"
        "Green\n"
        "\n"
        "🦖 Arina: 6/10\n"
        "💬 —\n"
        "\n"
        "🌵 Andrew: 5/10\n"
        "💬 Bitter"
    )
    assert format_product(product) == expected


def test_format_product_no_comments():
    product = {
        'category': 'Juice',
        'variant': 'Fresh',
        'flavor': 'Orange',
        'rating_arina': 9,
        'rating_andrew': 8
    }
    expected = (
        "Juice\n"
        "Fresh\n"
        "Orange\n"
        "\n"
        "🦖 Arina: 9/10\n"
        "💬 —\n"
        "\n"
        "🌵 Andrew: 8/10\n"
        "💬 —"
    )
    assert format_product(product) == expected


def test_format_product_missing_category():
    product = {
        'variant': 'Espresso',
        'flavor': 'Caramel',
        'rating_arina': 8,
        'comment_arina': 'Smooth taste',
        'rating_andrew': 7,
        'comment_andrew': 'Too sweet'
    }
    with pytest.raises(KeyError, match="'category'"):
        format_product(product)


def test_format_product_missing_flavor():
    product = {
        'category': 'Coffee',
        'variant': 'Espresso',
        'rating_arina': 8,
        'comment_arina': 'Smooth taste',
        'rating_andrew': 7,
        'comment_andrew': 'Too sweet'
    }
    with pytest.raises(KeyError, match="'flavor'"):
        format_product(product)


def test_format_product_missing_ratings():
    product = {
        'category': 'Coffee',
        'variant': 'Espresso',
        'flavor': 'Caramel',
        'comment_arina': 'Smooth taste',
        'comment_andrew': 'Too sweet'
    }
    with pytest.raises(KeyError, match="'rating_arina'"):
        format_product(product)
