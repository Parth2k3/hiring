from rest_framework import serializers
from .models import FAQ
from googletrans import LANGUAGES

class FAQSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()
    available_languages = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'available_languages']

    def get_question(self, obj):
        lang = self.context.get('language', 'en')
        translation = obj.get_translation(lang)
        return translation['question']

    def get_answer(self, obj):
        lang = self.context.get('language', 'en')
        translation = obj.get_translation(lang)
        return translation['answer']

    def get_available_languages(self, obj):
        # Return list of languages that have translations
        available = ['en'] + list(obj.translations.keys())
        return {code: LANGUAGES.get(code, code) for code in available}