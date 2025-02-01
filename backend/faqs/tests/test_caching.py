# faqs/tests/test_caching.py

import pytest
from django.core.cache import cache
from faqs.models import FAQ
from django.urls import reverse
from rest_framework.test import APIClient
import time

@pytest.mark.django_db
class TestCaching:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Clear cache before each test
        cache.clear()
        
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def sample_faq(self):
        return FAQ.objects.create(
            question="Test question?",
            answer="Test answer."
        )

    def test_cache_expiration(self, sample_faq):
        """Test if cache expires correctly"""
        # Set a very short timeout for this test
        SHORT_TIMEOUT = 2  # 2 seconds

        # First request with short timeout
        translation1 = sample_faq.translate_to('es', cache_timeout=SHORT_TIMEOUT)
        cache_key = sample_faq._get_cache_key('es')

        # Verify it's in cache
        assert cache.get(cache_key) is not None

        # Wait for cache to expire
        time.sleep(SHORT_TIMEOUT + 1)

        # Clear Django's internal cache
        cache.clear()

        # Verify cache has expired
        assert cache.get(cache_key) is None

    def test_api_cache(self, api_client, sample_faq):
        """Test if API responses are being cached"""
        url = reverse('faq-list')

        # First request
        response1 = api_client.get(f'{url}?lang=es')
        initial_data = response1.data

        # Modify the FAQ in database and clear cache
        sample_faq.question = "Modified question"
        sample_faq.save()
        cache.clear()  # Ensure cache is cleared

        # Second request - should get new data
        response2 = api_client.get(f'{url}?lang=es')

        # Responses should be different after cache clear
        assert response1.data != response2.data

    def test_cache_invalidation(self, sample_faq):
        """Test if cache is invalidated when FAQ is updated"""
        # First request - cache the translation
        translation1 = sample_faq.translate_to('es')
        cache_key = sample_faq._get_cache_key('es')

        # Verify initial cache
        assert cache.get(cache_key) is not None

        # Update the FAQ
        sample_faq.question = "Updated question"
        sample_faq.save()

        # Cache should be invalidated
        assert cache.get(cache_key) is None

    def test_cache_performance(self, sample_faq):
        """Test performance improvement with caching"""
        # First request - should be slower (no cache)
        start_time = time.time()
        translation1 = sample_faq.translate_to('es')
        first_request_time = time.time() - start_time

        # Second request - should be faster (cached)
        start_time = time.time()
        translation2 = sample_faq.translate_to('es')
        second_request_time = time.time() - start_time

        # Second request should be faster
        assert second_request_time < first_request_time