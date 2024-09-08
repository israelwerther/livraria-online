# books/models.py

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    first_publish_year = models.IntegerField(null=True, blank=True)
    cover_id = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Preço do livro
    
    def __str__(self):
        return self.title

    @property
    def cover_url(self):
        # Gera a URL da capa dinamicamente com base no cover_id
        if self.cover_id:
            return f'https://covers.openlibrary.org/b/id/{self.cover_id}-L.jpg'
        return None

