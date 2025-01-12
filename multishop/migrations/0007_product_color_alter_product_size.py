# Generated by Django 5.1.2 on 2024-10-18 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multishop', '0006_color_size_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.ManyToManyField(blank=True, to='multishop.color'),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(blank=True, to='multishop.size'),
        ),
    ]
