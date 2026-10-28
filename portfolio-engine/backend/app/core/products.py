"""Curated Product Showcase Data.

This module serves as the maintainable content source for curated products
and projects displayed across the portfolio.

Each product entry supports:
- name: The product's name (str, required)
- description: A concise explanation of the product, its purpose, the problem
               it addresses, and the value it offers (str, required)
- product_url: Optional URL directing visitors to the live product, demo,
               landing page, or public destination (str | None, optional)
- visual_url: Optional product screenshot or preview image URL (str | None, optional)

Proprietary implementation details (languages, frameworks, databases, source code)
are intentionally omitted in favor of product-level value propositions.
"""

from typing import TypedDict


class ProductEntry(TypedDict):
    name: str
    description: str
    product_url: str | None
    visual_url: str | None


PRODUCTS: list[ProductEntry] = [
    {
        "name": "Portfolio Engine",
        "description": (
            "A content-driven portfolio management system and API designed to present "
            "professional engineering work, manage evolving showcase content, and decouple "
            "domain data from frontend presentation. Built to accommodate career growth "
            "without requiring periodic redesigns."
        ),
        "product_url": "/docs",
        "visual_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1000&auto=format&fit=crop&q=80",
    },
    {
        "name": "Distributed Event Pipeline",
        "description": (
            "An asynchronous message distribution and task coordination service engineered "
            "to reliably buffer, process, and deliver high-volume background workloads "
            "while maintaining operational isolation and fault tolerance."
        ),
        "product_url": "https://pipeline.example.com",
        "visual_url": None,
    },
    {
        "name": "AuthGuard Zero-Trust Gateway",
        "description": (
            "A centralized identity and session boundary service providing cryptographic "
            "verification, scoped authorization tokens, and perimeter access policies "
            "for multi-service environments."
        ),
        "product_url": None,
        "visual_url": None,
    },
]


def get_showcase_products() -> list[ProductEntry]:
    """Retrieve all curated products for showcase display."""
    return PRODUCTS
