from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Opcional
    def __str__(self):
        return self.user.username

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_recipes', blank=True)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)  # Opcional

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title
    


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower} follows {self.followed}"