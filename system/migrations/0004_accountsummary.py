# Generated by Django 3.0 on 2022-04-02 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_fieldreservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountSummary',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('transaction_name', models.TextField(default='')),
                ('transaction_amount', models.IntegerField(default=0)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='system.User')),
            ],
        ),
    ]