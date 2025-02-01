from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from googletrans import LANGUAGES
from .models import FAQ
from .serializers import FAQSerializer
from django.core.cache import cache

class FAQViewSet(ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Get language from query params, default to English
        context['language'] = self.request.query_params.get('lang', 'en')
        return context

    @action(detail=True, methods=['post'])
    def translate(self, request, pk=None):
        """
        Endpoint to request translation to a specific language
        """
        faq = self.get_object()
        target_lang = request.data.get('language')

        if not target_lang:
            return Response(
                {'error': 'Language code is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if language code is valid
        if target_lang not in LANGUAGES:
            return Response(
                {'error': 'Invalid language code'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        translation = faq.translate_to(target_lang)
        return Response({
            'language': target_lang,
            'translation': translation
        })

    @action(detail=False, methods=['get'])
    def available_languages(self, request):
        """
        Return list of all supported languages
        """
        return Response(LANGUAGES)
    
    def list(self, request, *args, **kwargs):
        # Clear cache when listing to ensure fresh data
        cache.clear()
        return super().list(request, *args, **kwargs)