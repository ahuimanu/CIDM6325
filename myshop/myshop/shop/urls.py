from django.urls import path
from . import views

app_name = "shop"  # namespace for the URL patterns of the shop application
urlpatterns = [
    # all names are used for reverse lookup
    path("", views.product_list, name="product_list"),
    path("<slug:category_slug>/", views.product_list, name="product_list_by_category"),
    path("<int:id>/<slug:slug>/", views.product_detail, name="product_detail"),
]
