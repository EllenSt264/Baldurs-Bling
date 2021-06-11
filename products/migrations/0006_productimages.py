# Generated by Django 3.2.4 on 2021-06-11 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20210611_2010'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('more_images_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('more_images', models.ImageField(upload_to='')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='products.product')),
            ],
        ),
    ]