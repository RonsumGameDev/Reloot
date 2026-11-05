from decimal import Decimal

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Listing

# SETUP

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
    
    #POST TESTS
    
    def test_create_listing(self):
        
        data = self.valid_listing_data()
        
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Listing.objects.count(), 2)
        
        self.assertEqual(response.data["title"], data["title"])
        
    def test_create_listing_with_invalid_categories(self):
        data = self.valid_listing_data()
        data["category"] = "food"
        
        response = self.client.post(self.list_url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.assertIn("category", response.data)
        
    #PUT TESTS
    
    def test_update_listing(self):
        
        data = {
            "title": "Updated Charizard Card",
            "description": "Updated Collectable description",
            "price": "1999.99",
            "category": Listing.Category.TRADING_CARDS,
            "condition": Listing.Condition.GOOD
        }
        
        response = self.client.put(self.detail_url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.listing.refresh_from_db()
        
        self.assertEqual(self.listing.price, Decimal("1999.99"))
        
    def test_put_with_missing_fields(self):
        data = {
            "title" : "Incomplete Update"
        }
        
        response = self.client.put(self.detail_url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    #PATCH TESTS
    
    def test_partial_update_listing(self):
        data = {
            "price": "1299.99"
        }
        
        response = self.client.patch(self.detail_url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.listing.refresh_from_db()
        
        self.assertEqual(self.listing.price, Decimal("1299.99"))

        self.assertEqual(self.listing.title, "Pokemon Charizard Card")
        
        
    #DELETE TESTS
    
    def test_delete_listing(self):
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertFalse(Listing.objects.filter(pk=self.listing.pk).exists())
        
    def test_get_deleted_listing(self):
        
        self.client.delete(self.detail_url)
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    #HTTP METHODS
    
    def test_unsupported_method(self):
            
        response = self.client.post(self.detail_url, self.valid_listing_data(), format = "json")
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)