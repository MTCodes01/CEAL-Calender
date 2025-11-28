from django.db import models


class Club(models.Model):
    """
    Represents a college club/organization
    """
    slug = models.SlugField(unique=True, max_length=100)
    name = models.CharField(max_length=120)
    color = models.CharField(max_length=7, default="#3B82F6", help_text="Hex color code for calendar display")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
