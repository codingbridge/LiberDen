# Generated by Django 2.2.3 on 2019-07-20 01:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('price_amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('price_currency', models.CharField(choices=[('RMB', 'RMB'), ('USD', 'US Dollar')], default='USD', max_length=3)),
                ('acquired_date', models.DateField()),
                ('retired_date', models.DateField()),
                ('condition', models.CharField(choices=[('G', 'Good'), ('P', 'Poor')], default='G', max_length=1)),
                ('status', models.CharField(choices=[('A', 'Available'), ('N', 'Not available'), ('R', 'Retired')], default='A', max_length=1)),
                ('memo', models.CharField(max_length=500)),
                ('call_number', models.CharField(max_length=20)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Book')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Location')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('action', models.CharField(choices=[('CO', 'Check out'), ('OH', 'On hold'), ('R', 'Return')], max_length=3)),
                ('expiry_days', models.PositiveSmallIntegerField()),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Inventory')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]