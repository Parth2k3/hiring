from django.db import models
from ckeditor.fields import RichTextField
import hashlib
from django.core.cache import cache
from googletrans import Translator, LANGUAGES
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    translations = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return self.question

    def _get_cache_key(self, lang_code):
        """Get cache key for a specific language"""
        return f'faq_{self.id}_translation_{lang_code}'

    def _clear_cache(self):
        """Clear all cached translations for this FAQ"""
        # Clear cache for known languages
        for lang in ['es', 'fr', 'de', 'hi', 'bn']:  # Add more languages as needed
            cache.delete(self._get_cache_key(lang))

    def save(self, *args, **kwargs):
        """Override save to clear cache when FAQ is updated"""
        # Clear cache before saving
        self._clear_cache()
        super().save(*args, **kwargs)

    def translate_to(self, target_lang, cache_timeout=3600):  # 1 hour default timeout
        """
        Translate FAQ to specified language
        """
        # If target language is English, return original
        self.updated_at = datetime.now()
        self.save()
        if target_lang == 'en':
            return {
                'question': self.question,
                'answer': self.answer
            }

        cache_key = self._get_cache_key(target_lang)
        cached_translation = cache.get(cache_key)

        if cached_translation:
            logger.info(f"Cache hit for FAQ {self.id} in {target_lang}")
            return cached_translation

        logger.info(f"Cache miss for FAQ {self.id} in {target_lang}")

        try:
            translator = Translator()
            
            # Translate question
            translated_question = translator.translate(
                self.question, 
                dest=target_lang
            ).text

            # Translate answer
            translated_answer = translator.translate(
                self.answer, 
                dest=target_lang
            ).text

            translation = {
                'question': translated_question,
                'answer': translated_answer
            }

            # Store in cache with timeout
            cache.set(cache_key, translation, timeout=cache_timeout)
            
            # Store in database
            self.translations[target_lang] = translation
            super().save(update_fields=['translations'])

            return translation

        except Exception as e:
            logger.error(f"Translation error for FAQ {self.id} to {target_lang}: {str(e)}")
            return {
                'question': self.question,
                'answer': self.answer
            }

    
    def get_translation(self, lang_code):
        """
        Get translation for specified language
        """
        # If requested language is English, return original content
        if lang_code == 'en':
            return {
                'question': self.question,
                'answer': self.answer
            }

        # Check if translation exists in database
        if lang_code in self.translations:
            return self.translations[lang_code]

        # If not, generate translation
        return self.translate_to(lang_code)

    


    