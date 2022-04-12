# Generated by Django 3.0 on 2022-04-12 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0023_merge_20220410_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.ForeignKey(default=None, limit_choices_to=models.Q(role__in=['player']), null=True, on_delete=django.db.models.deletion.CASCADE, to='system.User'),
        ),
    ]
