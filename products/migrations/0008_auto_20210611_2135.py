# Generated by Django 3.2.4 on 2021-06-11 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_productimages_more_images_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='more_images',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='more_images_url',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.DeleteModel(
            name='ProductImages',
        ),
    ]
