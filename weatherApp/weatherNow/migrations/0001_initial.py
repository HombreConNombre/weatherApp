# Generated by Django 4.2.3 on 2023-07-28 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prov_code', models.CharField(max_length=100)),
                ('prov_name', models.CharField(max_length=100)),
                ('autono_code', models.CharField(max_length=100)),
                ('com_auton', models.CharField(max_length=100)),
                ('capital_city', models.CharField(max_length=100)),
            ],
        ),
    ]
