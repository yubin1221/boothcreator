# Generated by Django 4.1.6 on 2023-02-17 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=50)),
                ('super_permission', models.IntegerField()),
                ('user_permission', models.IntegerField()),
                ('is_object', models.BooleanField()),
                ('is_array', models.BooleanField()),
                ('is_object_array', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Attribute_Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]