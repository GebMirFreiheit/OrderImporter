# Generated by Django 3.2.6 on 2022-07-30 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.IntegerField(unique=True)),
                ('dollar_price', models.IntegerField()),
                ('ruble_price', models.FloatField()),
                ('delivery_time', models.DateField()),
            ],
        ),
    ]