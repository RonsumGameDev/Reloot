from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .models import Listing
from .serializers import ListingSerializer

# Create your views here.
@api_view(["GET", "POST"])
def listing_list(request):
    
    if request.method == "GET":
        listings = Listing.objects.all()
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = ListingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    
    if request.method == "GET":
        serializer = ListingSerializer(listing)
        return Response(serializer.data)
    
    elif request.method in ["PUT", "PATCH"]:
        serializer = ListingSerializer(listing, data=request.data, partial=(request.method == "PATCH"))
        
        if(serializer.is_valid()):
            serializer.save()
            
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        listing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
        
    