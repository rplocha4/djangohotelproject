# Generated by Django 4.0.4 on 2022-06-04 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('method', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Room_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('beds', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupancy', models.BooleanField()),
                ('name', models.CharField(max_length=20)),
                ('img', models.ImageField(upload_to='media/')),
                ('size', models.CharField(max_length=20)),
                ('accesories', models.CharField(max_length=200)),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.room_type')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.method')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.room')),
            ],
        ),
    ]