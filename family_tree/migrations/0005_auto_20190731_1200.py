# Generated by Django 2.2.3 on 2019-07-31 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0004_person_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(blank=True, choices=[('m', 'male'), ('f', 'female'), ('d', 'diverse')], max_length=1, null=True),
        ),
    ]
