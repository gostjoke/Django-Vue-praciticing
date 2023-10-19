from django.db import models
from django.utils import timezone

from article.models import Article
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete = models.CASCADE,  
        related_name = 'comments')
    
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE,
        related_name = 'comments')
    
    content = models.TextField()

    created = models.DateTimeField(
        default = timezone.now
    )
    # one comment only can have a parent but parent can have many children
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete = models.CASCADE,
        related_name = 'children'

    )

    class Meta:
        ordering = ['-created',]

    def __str__(self):
        return self.content[:20]