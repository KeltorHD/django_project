# Generated by Django 2.1.1 on 2018-09-15 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_schoolclass_stats'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolclass',
            name='number',
            field=models.IntegerField(default=0, max_length=2),
            preserve_default=False,
        ),
    ]
