# Generated by Django 3.0 on 2022-04-03 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0016_auto_20220403_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='location',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(limit_choices_to=models.Q(role__in=['admin', 'journalist']), on_delete=django.db.models.deletion.CASCADE, to='system.User'),
        ),
    ]
