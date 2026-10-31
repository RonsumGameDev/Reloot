from django.urls import path
from .views import listing_list, listing_detail
urlpatterns = [
    path("", listing_list, name="listing-list"),
    path("<int:pk>/", listing_detail, name="listing-detail"),
]