from django.db import models

from apps.security.models import User


class ImageUploadManager(models.Manager):
    def get_all_by_user_ImageUpload(self, username):
        try:
            user = User.objects.get(username=username)
            if user.is_authenticated:
                return self.filter(user=user)
        except User.DoesNotExist:
            return None
        
    def get_image_and_description_by_user(self, username):
        try:
            user = User.objects.get(username=username);
            print(user)
            if user.is_authenticated:
                values = self.filter(user=user).order_by('-created_at').values('image', 'description', 'id')
                print(values)
                return values
        except User.DoesNotExist:
            return None

class ImageUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    
    objects = ImageUploadManager()
    
    class Meta:
        verbose_name = 'Image Upload'
        verbose_name_plural = 'Image Uploads'
        ordering = ['-created_at']
        
    def __str__(self, *args, **kwargs):
        return f'Image uploaded by {self.user.username} - {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'
    
