from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import FAQ
@receiver([post_save, post_delete], sender=FAQ)
def invalidate_faq_cache(sender, instance, **kwargs):
    # Invalidate all language caches for this FAQ
    languages = ['en', 'hi', 'bn']  # Add all supported languages here
    for lang_code in languages:
        cache_key = f'faq_translation_{instance.pk}_{lang_code}'
        cache.delete(cache_key)

# In models.py or a separate signals.py file
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import FAQ
from googletrans import Translator
from django.conf import settings

translator = Translator()

@receiver(pre_save, sender=FAQ)
def translate_faq(sender, instance, **kwargs):
    target_languages = ['hi', 'bn'] 
    if instance.pk:
        old_instance = FAQ.objects.get(pk=instance.pk)
        if old_instance.question == instance.question:
            return

    for lang in target_languages:
        try:
            translated = translator.translate(instance.question, dest=lang)
            setattr(instance, f'question_{lang}', translated.text)

            translated_answer = translator.translate(instance.answer, dest=lang)
            setattr(instance, f'answer_{lang}', translated_answer.text)
        except Exception as e:
            print(f"Error translating to {lang}: {e}")
            setattr(instance, f'question_{lang}', None)
            setattr(instance, f'answer_{lang}', None)