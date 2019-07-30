# Generated by Django 2.2.3 on 2019-07-25 03:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Circulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('CO', 'Check out'), ('OH', 'On hold'), ('R', 'Return'), ('L', 'Lost')], max_length=3)),
                ('expiry_days', models.PositiveSmallIntegerField()),
                ('memo', models.TextField()),
                ('is_completed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='location',
            name='is_deleted',
        ),
        migrations.DeleteModel(
            name='Action',
        ),
        migrations.AddField(
            model_name='circulation',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Inventory'),
        ),
        migrations.AddField(
            model_name='circulation',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]