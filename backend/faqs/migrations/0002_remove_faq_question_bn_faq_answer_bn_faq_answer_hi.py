# Generated by Django 5.1.5 on 2025-01-31 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faqs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faq',
            name='question_bn',
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_bn',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_hi',
            field=models.TextField(blank=True, null=True),
        ),
    ]
