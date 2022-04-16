# Generated by Django 4.0.3 on 2022-04-16 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_date', models.DateTimeField()),
                ('reservation_cost', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('init_meter_reading', models.IntegerField()),
                ('end_meter_reading', models.IntegerField()),
                ('meter_rate', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('utility_cost', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('paid_amount', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('unpaid_amount', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('misc_charges', models.DecimalField(decimal_places=2, max_digits=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], default='unpaid', max_length=20)),
                ('method', models.CharField(choices=[('cash', 'Cash Payment'), ('card', 'Card Payment'), ('online', 'Online Payment')], default='cash', max_length=20)),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('state', models.CharField(choices=[('new', 'New Booking'), ('pending', 'Pending Approval')], default='new', max_length=20)),
                ('lease_doc_url', models.CharField(max_length=100)),
                ('lease_is_signed_by_user', models.BooleanField()),
                ('admin_comments', models.CharField(max_length=20)),
                ('bill_detail_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='booking', to='adminhome.billdetail')),
                ('parking_spot_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='booking', to='adminhome.parkingspot')),
                ('vehicle_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='booking', to='adminhome.vehicle')),
            ],
        ),
        migrations.AddField(
            model_name='billdetail',
            name='payment_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='booking', to='adminhome.payment'),
        ),
    ]
