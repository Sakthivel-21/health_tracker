from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=200)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foods')
    calories = models.FloatField()
    protein = models.FloatField(null=True, blank=True)
    carbs = models.FloatField(null=True, blank=True)
    fats = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class FoodLog(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Snacks'),
        ('dinner', 'Dinner'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='food_logs')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    date = models.DateField(auto_now_add=True)
    quantity = models.FloatField(default=1)  # multiplier for nutrition

    def __str__(self):
        return f"{self.user.username} - {self.meal_type} - {self.food.name}"

class Routine(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='routines')
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username}'s routine: {self.title}"
