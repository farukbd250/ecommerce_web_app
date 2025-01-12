# Generated by Django 5.1.2 on 2024-10-18 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multishop', '0003_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
            ],
        ),
    ]
