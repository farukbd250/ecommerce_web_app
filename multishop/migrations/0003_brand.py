# Generated by Django 5.1.2 on 2024-10-18 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multishop', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='brands/')),
            ],
        ),
    ]
