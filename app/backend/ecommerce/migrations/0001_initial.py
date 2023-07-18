# Generated by Django 4.2 on 2023-07-18 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields
import django_extensions.db.fields
import ecommerce.models.product
import utils.fields.enums
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('external_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='external id')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1, verbose_name='status')),
                ('activate_date', models.DateTimeField(blank=True, help_text='keep empty for an immediate activation', null=True)),
                ('deactivate_date', models.DateTimeField(blank=True, help_text='keep empty for indefinite activation', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='id')),
                ('default_source', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_user', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('external_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='external id')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1, verbose_name='status')),
                ('activate_date', models.DateTimeField(blank=True, help_text='keep empty for an immediate activation', null=True)),
                ('deactivate_date', models.DateTimeField(blank=True, help_text='keep empty for indefinite activation', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='id')),
                ('interval_count', models.IntegerField(blank=True, default=1, null=True)),
                ('amount', models.FloatField(default=1.0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('external_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='external id')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title', verbose_name='slug')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1, verbose_name='status')),
                ('activate_date', models.DateTimeField(blank=True, help_text='keep empty for an immediate activation', null=True)),
                ('deactivate_date', models.DateTimeField(blank=True, help_text='keep empty for indefinite activation', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='id')),
                ('image', models.ImageField(default='default_image.jpg', upload_to=ecommerce.models.product.product_directory_path, verbose_name='image')),
                ('price', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_price', to='ecommerce.price')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SessionItem',
            fields=[
                ('external_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='external id')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1, verbose_name='status')),
                ('activate_date', models.DateTimeField(blank=True, help_text='keep empty for an immediate activation', null=True)),
                ('deactivate_date', models.DateTimeField(blank=True, help_text='keep empty for indefinite activation', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='id')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sessionitem_customer', to='ecommerce.customer', verbose_name='session item customer')),
                ('price', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='session_price', to='ecommerce.price', verbose_name='price')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='session_product', to='ecommerce.product', verbose_name='product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('external_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='external id')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1, verbose_name='status')),
                ('activate_date', models.DateTimeField(blank=True, help_text='keep empty for an immediate activation', null=True)),
                ('deactivate_date', models.DateTimeField(blank=True, help_text='keep empty for indefinite activation', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='id')),
                ('session_mode', django_enumfield.db.fields.EnumField(blank=True, default=0, enum=utils.fields.enums.SessionMode, null=True)),
                ('session_status', django_enumfield.db.fields.EnumField(blank=True, default=1, enum=utils.fields.enums.SessionStatus, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='session_customer', to='ecommerce.customer', verbose_name='session customer')),
                ('session_items', models.ManyToManyField(blank=True, related_name='session_session_items', to='ecommerce.sessionitem', verbose_name='session items')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('external_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='external id')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1, verbose_name='status')),
                ('activate_date', models.DateTimeField(blank=True, help_text='keep empty for an immediate activation', null=True)),
                ('deactivate_date', models.DateTimeField(blank=True, help_text='keep empty for indefinite activation', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='id')),
                ('quantity', models.IntegerField(blank=True, default=1, null=True, verbose_name='quantity')),
                ('amount', models.IntegerField(blank=True, default=0, null=True)),
                ('amount_excluding_tax', models.IntegerField(blank=True, default=0, null=True)),
                ('currency', models.CharField(blank=True, max_length=3, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('period_end', models.DateTimeField(blank=True, null=True)),
                ('period_start', models.DateTimeField(blank=True, null=True)),
                ('unit_amount_excluding_tax', models.IntegerField(blank=True, default=0, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoiceitem_customer', to='ecommerce.customer', verbose_name='customer')),
                ('price', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.price', verbose_name='price')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('external_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='external id')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1, verbose_name='status')),
                ('activate_date', models.DateTimeField(blank=True, help_text='keep empty for an immediate activation', null=True)),
                ('deactivate_date', models.DateTimeField(blank=True, help_text='keep empty for indefinite activation', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='id')),
                ('charge', models.CharField(blank=True, max_length=150, null=True)),
                ('amount_due', models.IntegerField(blank=True, default=0, null=True)),
                ('amount_paid', models.IntegerField(blank=True, default=0, null=True)),
                ('amount_remaining', models.IntegerField(blank=True, default=0, null=True)),
                ('amount_shipping', models.IntegerField(blank=True, default=0, null=True)),
                ('application_fee_amount', models.IntegerField(blank=True, default=0, null=True)),
                ('attempt_count', models.IntegerField(blank=True, default=0, null=True)),
                ('attempted', models.BooleanField(default=False)),
                ('currency', models.CharField(blank=True, max_length=3, null=True)),
                ('invoice_status', django_enumfield.db.fields.EnumField(blank=True, enum=utils.fields.enums.InvoiceStatus, null=True)),
                ('subtotal', models.IntegerField(blank=True, default=0, null=True)),
                ('subtotal_excluding_tax', models.IntegerField(blank=True, default=0, null=True)),
                ('tax', models.IntegerField(blank=True, default=0, null=True)),
                ('total', models.IntegerField(blank=True, default=0, null=True)),
                ('total_excluding_tax', models.IntegerField(blank=True, default=0, null=True)),
                ('period_end', models.DateTimeField(blank=True, null=True)),
                ('period_start', models.DateTimeField(blank=True, null=True)),
                ('schedule_created', models.BooleanField(default=False)),
                ('hosted_invoice_url', models.URLField(blank=True, null=True)),
                ('invoice_pdf', models.URLField(blank=True, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_customer', to='ecommerce.customer', verbose_name='customer')),
                ('invoice_items', models.ManyToManyField(blank=True, to='ecommerce.invoiceitem', verbose_name='invoice items')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1, verbose_name='status')),
                ('activate_date', models.DateTimeField(blank=True, help_text='keep empty for an immediate activation', null=True)),
                ('deactivate_date', models.DateTimeField(blank=True, help_text='keep empty for indefinite activation', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='id')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart_customer', to='ecommerce.customer', verbose_name='user')),
                ('products', models.ManyToManyField(blank=True, related_name='cart_products', to='ecommerce.product', verbose_name='products')),
            ],
            options={
                'ordering': ['created'],
                'abstract': False,
            },
        ),
    ]
