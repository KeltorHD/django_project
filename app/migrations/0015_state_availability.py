# Generated by Django 2.0.5 on 2018-06-30 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20180625_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='availability',
            field=models.CharField(default='+', max_length=2),
            preserve_default=False,
        ),
    ]
