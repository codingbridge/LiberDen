# Generated by Django 2.2.4 on 2019-08-28 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(to='inventory.Author'),
        ),
        migrations.DeleteModel(
            name='TestData',
        ),
    ]
