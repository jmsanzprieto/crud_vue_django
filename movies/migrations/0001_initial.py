# Generated by Django 3.2.12 on 2023-10-25 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_movie', models.CharField(max_length=50)),
                ('gender_movie', models.CharField(max_length=50)),
                ('year_movie', models.CharField(max_length=50)),
                ('director_movie', models.CharField(max_length=50)),
            ],
        ),
    ]
