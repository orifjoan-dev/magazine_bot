from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name='Telegram username',max_length=100,null=True)
    telegram_id = models.BigIntegerField(verbose_name='Telegram ID',unique=True,default=1)

    def __str__(self):
        return f"{self.id} - {self.telegram_id} - {self.username}"

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(verbose_name='Mahsulot nomi',max_length=50)
    photo = models.URLField(verbose_name='Rasm',max_length=100)
    price = models.CharField(verbose_name='Narx',max_length=30)
    description = models.TextField(verbose_name='Mahsulot haqida',max_length=3000,null=True)

    category_code = models.CharField(verbose_name='Kategoriya kodi',max_length=30)
    category_name = models.CharField(verbose_name='Kategoriya nomi',max_length=30)
    subcategory_code = models.CharField(verbose_name='Subkategoriya kodi',max_length=30)
    subcategory_name = models.CharField(verbose_name='Subkategoriya nomi',max_length=30)

    def __str__(self):
        return f"{self.category_name} -{self.subcategory_name} - {self.product_name}"
