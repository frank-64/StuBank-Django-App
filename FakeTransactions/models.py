from django.db import models
from django.http import request
from django.urls.base import reverse

from FakeTransactions import costs


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='FakeProducts', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    price = models.FloatField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, db_index=True)

    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])