# Generated by Django 3.0 on 2022-04-20 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0035_auto_20220419_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketuser',
            name='account_summary',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accountsummary', to='system.AccountSummary'),
        ),
    ]