# Generated by Django 2.0.5 on 2018-06-02 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20180531_2123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='state',
            options={'ordering': ['date']},
        ),
        migrations.RemoveField(
            model_name='state',
            name='people',
        ),
        migrations.AddField(
            model_name='state',
            name='people',
            field=models.ManyToManyField(help_text='Фамилия и имя учащегося', related_name='peoples', to='app.People'),
        ),
    ]
