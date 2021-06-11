# Generated by Django 3.2.4 on 2021-06-11 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_product_has_sizes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='size',
            new_name='sizes',
        ),
        migrations.AlterField(
            model_name='product',
            name='has_sizes',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
