# Generated by Django 3.0 on 2022-04-23 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0038_alter_post_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldreservation',
            name='account_summary',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.AccountSummary'),
        ),
    ]
