# Generated by Django 3.0 on 2022-04-17 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0033_auto_20220417_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='article_images/', verbose_name='Image'),
        ),
    ]
