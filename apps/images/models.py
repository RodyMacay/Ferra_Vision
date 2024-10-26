from django.db import models

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/')
    description = models.TextField(blank=True, null=True)
    materials = models.TextField(blank=True, null=True)
    construction_steps = models.TextField(blank=True, null=True)
    estimated_time = models.CharField(max_length=100, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    difficulty = models.CharField(max_length=50, blank=True, null=True)
    prices_materials = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)