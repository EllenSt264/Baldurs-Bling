# Generated by Django 3.2.4 on 2021-06-11 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_product_has_sizes'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(related_name='_products_product_size_+', to='products.Product'),
        ),
    ]
