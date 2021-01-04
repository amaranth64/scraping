from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    slug = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Города'
        verbose_name_plural = "Города"
        
    def __str__(self):
        return self.name
