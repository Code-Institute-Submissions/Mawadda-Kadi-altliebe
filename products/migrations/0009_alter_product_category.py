# Generated by Django 4.2.10 on 2024-03-09 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.IntegerField(choices=[(0, 'Electronics'), (1, 'Fashion and Apparel'), (2, 'Home and Garden'), (3, 'Sports and Outdoors'), (4, 'Toys and Games'), (5, 'Books and Media'), (6, 'Pet Supplies'), (7, 'Others')], default=0),
        ),
    ]
