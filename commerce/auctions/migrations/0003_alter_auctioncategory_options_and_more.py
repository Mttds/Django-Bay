# Generated by Django 4.0.5 on 2022-07-11 10:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctioncategory_auctionlisting_auctioncomment_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auctioncategory',
            options={'verbose_name_plural': 'Auction categories'},
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='current_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12),
        ),
    ]