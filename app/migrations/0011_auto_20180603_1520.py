# Generated by Django 2.0.5 on 2018-06-03 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20180603_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='school_class',
            field=models.CharField(max_length=10),
        ),
    ]
