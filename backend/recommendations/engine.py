"""Rule-based AI Gift Recommendation Engine.

Scores every product against the recipient profile (age, gender,
relationship, occasion, budget) the user submits on the AI Gift Finder
page, and returns the best matches together with a human-readable
explanation of why each one was picked.

This stands in for a call to the OpenAI API: it is deterministic, free,
and works offline, while still feeling personalized because the score
and "reason" are computed per-product instead of being a static list.
"""

from products.models import Product

# Relationship → categories that are traditionally well-received for that bond.
RELATIONSHIP_CATEGORY_HINTS = {
    'partner': ['jewelry', 'flowers', 'perfume', 'personalized'],
    'spouse': ['jewelry', 'flowers', 'perfume', 'personalized'],
    'parent': ['home-decor', 'personalized', 'electronics', 'wellness'],
    'sibling': ['electronics', 'fashion', 'books', 'games'],
    'friend': ['personalized', 'books', 'games', 'fashion'],
    'colleague': ['stationery', 'gourmet', 'home-decor'],
    'child': ['toys', 'games', 'books'],
}

# Occasion → categories that are conventionally associated with that event.
OCCASION_CATEGORY_HINTS = {
    'birthday': ['jewelry', 'flowers', 'personalized', 'gift-box'],
    'anniversary': ['jewelry', 'flowers', 'perfume', 'personalized'],
    'wedding': ['home-decor', 'personalized', 'gift-box'],
    'graduation': ['electronics', 'stationery', 'personalized'],
    'valentine': ['flowers', 'jewelry', 'perfume', 'gift-box'],
    'christmas': ['gift-box', 'personalized', 'home-decor'],
    'mothers_day': ['flowers', 'jewelry', 'personalized', 'wellness'],
    'fathers_day': ['electronics', 'gourmet', 'personalized'],
    'baby_shower': ['toys', 'home-decor'],
    'general': ['gift-box', 'personalized'],
}


def recommend_gifts(age, gender, relationship, occasion, min_budget, max_budget, limit=8):
    """Return a ranked list of (product, score, reasons) tuples.

    The score is a simple weighted sum across five signals: budget fit,
    age range fit, gender fit, occasion fit and relationship fit. Each
    matching signal also contributes a plain-English reason so the
    frontend can explain *why* a gift was suggested.
    """
    candidates = Product.objects.filter(stock__gt=0, price__gte=min_budget, price__lte=max_budget)

    relationship_categories = RELATIONSHIP_CATEGORY_HINTS.get(relationship, [])
    occasion_categories = OCCASION_CATEGORY_HINTS.get(occasion, [])

    results = []
    for product in candidates.select_related('category'):
        score = 0
        reasons = []

        # Budget fit (already filtered, but reward gifts comfortably inside the range)
        score += 2
        reasons.append(f'Fits your budget of KSh {min_budget:,.0f} - {max_budget:,.0f}')

        # Age fit
        if product.min_age <= age <= product.max_age:
            score += 3
            reasons.append(f'Suitable for age {age}')

        # Gender fit
        if product.gender == gender or product.gender == 'unisex':
            score += 2
            reasons.append(f'Matches recipient gender ({product.get_gender_display()})')

        # Occasion fit
        if product.occasion == occasion:
            score += 3
            reasons.append(f'Perfect for {product.get_occasion_display()}')
        elif product.category.slug in occasion_categories:
            score += 1
            reasons.append(f'Commonly chosen for {dict(Product.OCCASION_CHOICES).get(occasion, occasion)}')

        # Relationship fit
        if product.category.slug in relationship_categories:
            score += 2
            reasons.append(f'A thoughtful pick for a {relationship}')

        # Slight boost for trending/highly rated items, used as a tie-breaker
        if product.is_trending:
            score += 1
            reasons.append('Trending right now')
        if product.rating and product.rating >= 4:
            score += 1
            reasons.append(f'Highly rated ({product.rating}/5)')

        if score > 0:
            results.append({'product': product, 'score': score, 'reasons': reasons})

    results.sort(key=lambda r: r['score'], reverse=True)
    return results[:limit]
