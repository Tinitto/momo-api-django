# Generated by Django 2.2.6 on 2019-10-14 23:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('momo_requests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='momorequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='momorequest',
            name='last_modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='momorequest',
            name='financial_transaction_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='momorequest',
            name='payee_note',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='momorequest',
            name='payer_message',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='momorequest',
            name='payer_party_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='momorequest',
            name='payer_party_id_type',
            field=models.CharField(default='MSISDN', max_length=100),
        ),
        migrations.AlterField(
            model_name='momorequest',
            name='reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
