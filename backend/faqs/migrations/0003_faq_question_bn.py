# Generated by Django 5.1.5 on 2025-01-31 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faqs', '0002_remove_faq_question_bn_faq_answer_bn_faq_answer_hi'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='question_bn',
            field=models.TextField(blank=True, null=True),
        ),
    ]
