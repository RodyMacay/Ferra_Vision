from django.contrib import admin
from ..core.models import UserMood,Emotion
# Register your models here.
@admin.register(Emotion)
class EmotionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(UserMood)
class UserMoodAdmin(admin.ModelAdmin):
    list_display = ['user', 'emotion']
    search_fields = ['user__username', 'emotion__name']