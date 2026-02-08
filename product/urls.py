from django.urls import path
from .views import (
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    CategoryCreateListView,
    CategoryRetrieveUpdateDestroyView,
    ProductCommentListCreateView,
    ProductCommentRetrieveUpdateDestroyView,
)

urlpatterns = [

    path("products/", ProductListCreateView.as_view(), name="product-list-create"),
    path("products/<int:pk>/", ProductRetrieveUpdateDestroyView.as_view(), name="product-detail"),

    path("categories/", CategoryCreateListView.as_view(), name="category-list-create"),
    path("categories/<int:pk>/", CategoryRetrieveUpdateDestroyView.as_view(), name="category-detail"),

    path("products/<int:product_id>/comments/", ProductCommentListCreateView.as_view(), name="product-comments"),
    path("comments/<int:pk>/", ProductCommentRetrieveUpdateDestroyView.as_view(), name="comment-detail"),
]
