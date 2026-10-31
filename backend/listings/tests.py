from decimal import Decimal

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Listing

# Create your tests here.

class ListingAPITests(APITestCase):
    
    def setUp(self):
        self.listing = Listing.objects.create(
            title = "Pokemon Charizard Card",
            description = "First edition collectible card",
            price = Decimal("1499.99"),
            category = Listing.Category.TRADING_CARDS,
            condition = Listing.Condition.LIKE_NEW
        )
        
        self.list_url = reverse("listing-list")
        self.detail_url = reverse("listing-detail", kwargs={"pk" : self.listing.pk})
        
    def valid_listing_data(self):
        return {
            "title" : "Naruto Manga Volume 1",
            "description" : "First volume of Naruto Manga",
            "price": "299.99",
            "category": Listing.Category.MANGA,
            "condition": Listing.Condition.GOOD
        }
        

    #GET TESTS
    
    def test_get_all_listings(self):
        
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_get_single_listing(self):
        
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.listing.title)
        
    def test_non_existing_listing(self):
        
        url = reverse("listing-detail", kwargs = {"pk" : self.listing.pk + 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
        
    
        
        