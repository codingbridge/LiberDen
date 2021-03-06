# Generated by Django 2.2.4 on 2019-08-21 02:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('slug_hash', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('mailing_address', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('slug_hash', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('isbn', models.CharField(max_length=30)),
                ('sub_title', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('memo', models.CharField(blank=True, max_length=500, null=True)),
                ('word_count', models.PositiveIntegerField(blank=True, null=True)),
                ('page_count', models.PositiveIntegerField(blank=True, null=True)),
                ('ranking', models.PositiveSmallIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(9)])),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('slug_hash', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('type', models.CharField(choices=[('AR', 'ArPoints'), ('AT', 'ATOS book level'), ('C', 'Cover type'), ('G', 'Genres'), ('IL', 'Interest level'), ('L', 'Language'), ('LL', 'Lexile level'), ('RL', 'Reading level'), ('QN', 'Quiz number'), ('S', 'Subject'), ('SE', 'Series')], max_length=3)),
                ('value', models.CharField(blank=True, max_length=10, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('slug_hash', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('code', models.CharField(max_length=5)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='documents/%Y/%m/%d/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
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
        migrations.CreateModel(
            name='TestData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('slug_hash', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('content', models.CharField(max_length=10)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Author')),
                ('categories', models.ManyToManyField(to='inventory.Category')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('slug_hash', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('mailing_address', models.CharField(blank=True, max_length=200, null=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Country')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
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
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('modified_datetime', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('slug_hash', models.CharField(blank=True, max_length=32, null=True, unique=True)),
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
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('price_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('price_currency', models.CharField(choices=[('RMB', 'RMB'), ('USD', 'US Dollar')], default='USD', max_length=3)),
                ('acquired_date', models.DateField(blank=True, null=True)),
                ('retired_date', models.DateField(blank=True, null=True)),
                ('condition', models.CharField(choices=[('G', 'Good'), ('P', 'Poor')], default='G', max_length=1)),
                ('status', models.CharField(choices=[('m', 'Maintenance'), ('o', 'On loan'), ('a', 'Available'), ('r', 'Reserved')], default='A', max_length=1)),
                ('memo', models.CharField(blank=True, max_length=500, null=True)),
                ('call_number', models.CharField(max_length=20, unique=True)),
                ('is_retired', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Book')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Location')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
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
                ('handled_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Operator', to=settings.AUTH_USER_MODEL)),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Inventory')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(to='inventory.Category'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Publisher'),
        ),
        migrations.AddField(
            model_name='book',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='author',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Country'),
        ),
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
