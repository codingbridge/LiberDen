# Generated by Django 2.2.3 on 2019-07-25 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0002_auto_20190724_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='circulation',
            name='handled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Operator', to=settings.AUTH_USER_MODEL),
        ),
    ]
