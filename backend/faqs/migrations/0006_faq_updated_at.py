# Generated by Django 5.1.5 on 2025-01-31 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faqs', '0005_faq_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
