# Generated by Django 4.2.7 on 2024-06-14 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_product_model_year_product_model_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelyear',
            name='year',
            field=models.IntegerField(),
        ),
    ]