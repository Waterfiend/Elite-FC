# Generated by Django 3.0 on 2022-04-02 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_auto_20220402_1412'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.TextField(default='XX/XX/XX')),
                ('time', models.TextField(default='XX:XX')),
                ('team1', models.TextField(default='')),
                ('team2', models.TextField(default='')),
                ('score1', models.IntegerField(default=0)),
                ('score2', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('ticket_type', models.TextField(default='General Admission')),
                ('price', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('match', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.Match')),
            ],
        ),
    ]