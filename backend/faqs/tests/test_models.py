import pytest
from django.core.cache import cache
from faqs.models import FAQ

@pytest.mark.django_db
class TestFAQModel:
    @pytest.fixture
    def sample_faq(self):
        return FAQ.objects.create(
            question="What is this?",
            answer="This is a test answer."
        )

    def test_faq_creation(self, sample_faq):
        assert FAQ.objects.count() == 1
        assert sample_faq.question == "What is this?"

    def test_translation_method(self, sample_faq):
        # Test translation to Hindi
        translation = sample_faq.get_translation('hi')
        assert translation is not None
        assert 'question' in translation
        assert 'answer' in translation

    def test_translation_caching(self, sample_faq):
        cache_key = f'faq_{sample_faq.id}_translation_fr'
        
        # First call should cache the translation
        translation1 = sample_faq.get_translation('fr')
        cached_translation = cache.get(cache_key)
        
        assert cached_translation is not None
        assert translation1 == cached_translation

    def test_fallback_to_english(self, sample_faq):
        # Test with invalid language code
        translation = sample_faq.get_translation('invalid_code')
        assert translation['question'] == sample_faq.question
        assert translation['answer'] == sample_faq.answer