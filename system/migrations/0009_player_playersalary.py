# Generated by Django 3.0 on 2022-04-02 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_match_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerSalary',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('fan_tier', models.TextField()),
                ('salary', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('salary', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.PlayerSalary')),
            ],
        ),
    ]
