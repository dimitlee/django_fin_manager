# Generated by Django 5.0.3 on 2024-03-31 17:24

import django.db.models.deletion
import django.utils.timezone
import finances.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0002_alter_category_user_alter_transaction_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='description',
            field=models.CharField(blank=True, default='', help_text='Describe this transaction', max_length=200),
        ),
        migrations.AddField(
            model_name='transaction',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ScheduledTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', help_text='Enter name for this transaction', max_length=200)),
                ('frequency', models.CharField(choices=[('w', 'Weekly'), ('m', 'Monthly'), ('y', 'Yearly')], default='m', help_text='How often is the transaction occuring?', max_length=1)),
                ('weekday', models.IntegerField(null=True, validators=[finances.models.weekday_validator])),
                ('monthday', models.IntegerField(null=True, validators=[finances.models.monthday_validator])),
                ('year_date', models.DateField(null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='finances.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
