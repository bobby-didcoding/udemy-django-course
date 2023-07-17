# Generated by Django 4.2 on 2023-07-17 18:46

from django.db import migrations, models
import ecommerce.models.product


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_cart_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='amount',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='default_image.jpg', upload_to=ecommerce.models.product.product_directory_path, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='cart_products', to='ecommerce.product', verbose_name='products'),
        ),
    ]
