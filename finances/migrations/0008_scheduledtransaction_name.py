# Generated by Django 5.0.3 on 2024-07-14 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0007_alter_scheduledtransaction_weekday'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledtransaction',
            name='name',
            field=models.CharField(default='scheduled transaction', help_text='Give a short name for this transaction', max_length=100),
            preserve_default=False,
        ),
    ]
