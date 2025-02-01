# faqs/tests/test_views.py

import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from faqs.models import FAQ

@pytest.mark.django_db
class TestFAQViews:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def sample_faq(self):
        return FAQ.objects.create(
            question="Test question?",
            answer="Test answer."
        )

    def test_list_faqs(self, api_client, sample_faq):
        url = reverse('faq-list')
        response = api_client.get(url)

        assert response.status_code == 200
        # Check if response.data is paginated
        if isinstance(response.data, dict) and 'results' in response.data:
            # Paginated response
            assert len(response.data['results']) == 1
            assert response.data['results'][0]['question'] == sample_faq.question
        else:
            # Non-paginated response
            assert len(response.data) == 1
            assert response.data[0]['question'] == sample_faq.question

    def test_get_faq_with_language(self, api_client, sample_faq):
        url = reverse('faq-detail', kwargs={'pk': sample_faq.pk})
        response = api_client.get(f'{url}?lang=es')
        
        assert response.status_code == 200
        assert 'question' in response.data
        assert 'answer' in response.data


    def test_delete_faq(self, api_client, sample_faq):
        url = reverse('faq-detail', kwargs={'pk': sample_faq.pk})
        response = api_client.delete(url)
        
        assert response.status_code == 204
        assert FAQ.objects.count() == 0

    def test_list_faqs_with_language(self, api_client, sample_faq):
        url = reverse('faq-list')
        response = api_client.get(f'{url}?lang=es')
        
        assert response.status_code == 200
        if isinstance(response.data, dict) and 'results' in response.data:
            # Paginated response
            assert len(response.data['results']) == 1
        else:
            # Non-paginated response
            assert len(response.data) == 1

    @pytest.mark.parametrize('lang', ['es', 'fr', 'de'])
    def test_faq_translation_languages(self, api_client, sample_faq, lang):
        url = reverse('faq-list')
        response = api_client.get(f'{url}?lang={lang}')
        
        assert response.status_code == 200