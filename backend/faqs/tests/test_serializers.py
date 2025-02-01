import pytest
from faqs.serializers import FAQSerializer
from faqs.models import FAQ

@pytest.mark.django_db
class TestFAQSerializer:
    @pytest.fixture
    def sample_faq(self):
        return FAQ.objects.create(
            question="Test question?",
            answer="Test answer."
        )

    def test_serializer_contains_expected_fields(self, sample_faq):
        serializer = FAQSerializer(instance=sample_faq)
        data = serializer.data
        
        assert set(data.keys()) == {'id', 'question', 'answer', 'available_languages'}

    def test_serializer_with_language_context(self, sample_faq):
        context = {'language': 'es'}
        serializer = FAQSerializer(instance=sample_faq, context=context)
        data = serializer.data
        
        assert 'question' in data
        assert 'answer' in data