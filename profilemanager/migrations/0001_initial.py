# Generated by Django 5.0 on 2023-12-14 09:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VendorProfile',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('contact_details', models.TextField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('vendor_code', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('on_time_delivery_rate', models.FloatField(max_length=32, null=True)),
                ('quality_rating_avg', models.FloatField(max_length=32, null=True)),
                ('average_response_time', models.FloatField(max_length=32, null=True)),
                ('fulfillment_rate', models.FloatField(max_length=16, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalPerformanceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('on_time_delivery_rate', models.FloatField(max_length=32, null=True)),
                ('quality_rating_avg', models.FloatField(max_length=32, null=True)),
                ('average_response_time', models.FloatField(max_length=32, null=True)),
                ('fulfillment_rate', models.FloatField(max_length=16, null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profilemanager.vendorprofile')),
            ],
        ),
    ]
