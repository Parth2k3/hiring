# faqs/tests/test_translations.py

import pytest
from unittest.mock import patch, Mock
from faqs.models import FAQ
from django.core.cache import cache

@pytest.mark.django_db
class TestTranslations:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Clear cache before each test
        cache.clear()

    @pytest.fixture
    def sample_faq(self):
        return FAQ.objects.create(
            question="Test question?",
            answer="Test answer."
        )

    @patch('faqs.models.Translator')
    def test_translation_service(self, MockTranslator, sample_faq):
        # Configure mock
        mock_translator = Mock()
        MockTranslator.return_value = mock_translator

        # Create different mock responses for question and answer
        mock_question_translation = Mock()
        mock_question_translation.text = "¿Pregunta de prueba?"
        
        mock_answer_translation = Mock()
        mock_answer_translation.text = "Respuesta de prueba."

        # Configure mock to return different responses for question and answer
        mock_translator.translate.side_effect = [
            mock_question_translation,  # First call (question)
            mock_answer_translation,    # Second call (answer)
        ]

        # Test translation
        translation = sample_faq.translate_to('es')
        assert translation['question'] == "¿Pregunta de prueba?"
        assert translation['answer'] == "Respuesta de prueba."

        # Verify both calls were made correctly
        assert mock_translator.translate.call_count == 2
        
       

    @patch('faqs.models.Translator')
    def test_translation_error_handling(self, MockTranslator, sample_faq):
        # Configure mock to raise exception
        mock_translator = Mock()
        MockTranslator.return_value = mock_translator
        mock_translator.translate.side_effect = Exception("Translation service error")

        # Test translation with error
        translation = sample_faq.translate_to('fr')
        assert translation['question'] == sample_faq.question
        assert translation['answer'] == sample_faq.answer

    @patch('faqs.models.Translator')
    def test_cached_translation(self, MockTranslator, sample_faq):
        # Configure mock
        mock_translator = Mock()
        MockTranslator.return_value = mock_translator
        
        mock_translation = Mock()
        mock_translation.text = "Cached translation"
        mock_translator.translate.return_value = mock_translation

        # First call
        first_translation = sample_faq.translate_to('es')
        assert first_translation['question'] == "Cached translation"
        
        # Reset mock and verify cache is used
        mock_translator.translate.reset_mock()
        second_translation = sample_faq.translate_to('es')
        assert second_translation['question'] == "Cached translation"
        mock_translator.translate.assert_not_called()

    @patch('faqs.models.Translator')
    def test_multiple_languages(self, MockTranslator, sample_faq):
        # Configure mock
        mock_translator = Mock()
        MockTranslator.return_value = mock_translator

        translations = {
            'es': "¿Pregunta de prueba?",
            'fr': "Question de test?",
            'de': "Testfrage?"
        }

        def mock_translate(text, dest, **kwargs):
            mock_result = Mock()
            mock_result.text = translations[dest]
            return mock_result

        mock_translator.translate.side_effect = mock_translate

        # Test translations for each language
        for lang, expected in translations.items():
            translation = sample_faq.translate_to(lang)
            assert translation['question'] == expected

    def test_english_translation(self, sample_faq):
        # Test that requesting English returns original text
        translation = sample_faq.translate_to('en')
        assert translation['question'] == sample_faq.question
        assert translation['answer'] == sample_faq.answer