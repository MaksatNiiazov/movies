# Generated by Django 4.0.3 on 2022-05-15 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviesapp', '0002_alter_position_options_alter_reviews_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='date_of_death',
            field=models.DateField(blank=True, null=True, verbose_name='Дата смерти'),
        ),
    ]
