# Generated by Django 2.2.3 on 2019-07-30 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_auto_20190729_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='book.Country'),
        ),
        migrations.AlterField(
            model_name='author',
            name='mailing_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]