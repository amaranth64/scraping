import jsonfield
from django.db import models
from django.db.models import ForeignKey

from scraping.utils import from_cyrillic_to_eng


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название", unique=True)
    slug = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = "Города"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(self.name)
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название", unique=True)
    slug = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = "Языки программирования"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(self.name)
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name="Название")
    company = models.CharField(max_length=250, verbose_name="Компания")
    description = models.TextField(verbose_name="Описание")
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name="Город")
    language = models.ForeignKey("Language", on_delete=models.CASCADE, verbose_name="Язык программирования")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = "Вакансии"
        ordering = ['-timestamp']


    def __str__(self):
        return self.title


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()


def default_url():
    return {'work': '', 'rabota': '', 'dou': '', 'djinni': ''}


class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name="Город")
    language = models.ForeignKey("Language", on_delete=models.CASCADE, verbose_name="Язык программирования")
    url_data = jsonfield.JSONField(default=default_url)

    class Meta:
        unique_together = ('city', 'language')

    def __str__(self):
        return self.city.name + ' - ' + self.language.name
