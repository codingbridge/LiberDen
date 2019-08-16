# Generated by Django 2.2.4 on 2019-08-14 19:35

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
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('slug_hash', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('valid_in_days', models.PositiveIntegerField()),
                ('max_book_count', models.PositiveIntegerField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='inventory',
            name='is_retired',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='status',
            field=models.CharField(choices=[('m', 'Maintenance'), ('o', 'On loan'), ('a', 'Available'), ('r', 'Reserved')], default='A', max_length=1),
        ),
        migrations.CreateModel(
            name='MembershipCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(auto_now=True)),
                ('is_valid_membership', models.BooleanField(default=True)),
                ('membership_activated_date', models.DateTimeField()),
                ('membership_expiry_date', models.DateTimeField()),
                ('membership', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Membership')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]