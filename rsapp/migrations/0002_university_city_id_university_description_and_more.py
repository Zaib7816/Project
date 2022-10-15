# Generated by Django 4.0.1 on 2022-06-27 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='city_id',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='university',
            name='description',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='university',
            name='address',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='university',
            name='city',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='university',
            name='name',
            field=models.CharField(default='', max_length=300),
        ),
    ]