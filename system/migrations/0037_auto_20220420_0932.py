# Generated by Django 3.0 on 2022-04-20 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0036_ticketuser_account_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountsummary',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]