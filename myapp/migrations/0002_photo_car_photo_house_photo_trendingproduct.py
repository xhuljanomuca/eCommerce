# Generated by Django 5.1.6 on 2025-02-18 23:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photos/')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='photo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='car_photos', to='myapp.photo'),
        ),
        migrations.AddField(
            model_name='house',
            name='photo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='house_photos', to='myapp.photo'),
        ),
        migrations.CreateModel(
            name='TrendingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.category')),
                ('photo', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='trending_product_photos', to='myapp.photo')),
            ],
        ),
    ]
