from django.db import models

# Create your models here.
class Listing(models.Model):
    class Category(models.TextChoices):
        TRADING_CARDS = "trading_cards", "Trading Cards"
        MANGA = "manga", "Manga"
        COMICS = "comics", "Comics"
        FIGURES = "figures", "Figures & Statues"
        GAMING = "gaming", "Video Games & Consoles"
        LEGO = "lego", "LEGO"
        OTHER = "other", "Other"
        
    class Condition(models.TextChoices):
        NEW = "new", "New"
        LIKE_NEW = "like_new", "Like New"
        GOOD = "good", "Good"
        FAIR = "fair", "Fair"
        POOR = "poor", "Poor"
        
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    category = models.CharField(max_length=20, choices=Category.choices)
    condition = models.CharField(max_length=20, choices=Condition.choices)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

