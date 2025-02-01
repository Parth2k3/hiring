from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import FAQ
from django.db import models
from django.urls import path
from django.shortcuts import render


from django import forms

class FAQAdminForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        question = cleaned_data.get('question')
        answer = cleaned_data.get('answer')

        if question and len(question.split()) > 50:
            raise forms.ValidationError(
                _("Question should not exceed 50 words.")
            )

        return cleaned_data


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):

    form = FAQAdminForm
    list_display = ('question','answer')
    search_fields = ('question', 'answer')
    readonly_fields = ('created_at', 'updated_at')
    
    # Add these fields to your FAQ model if not already present
    

    readonly_fields = ('translation_preview', 'created_at', 'updated_at')

    def translation_preview(self, obj):
        if not obj.pk:
            return _("Save the FAQ first to see translations")

        preview_html = []
        for lang_code, content in obj.translations.items():
            print(obj.translations.items(), content.get('question'))
            translated_question = content.get('question')
            preview_html.append(
                f'<div style="margin-bottom: 10px;">'
                f'<strong>{lang_code}:</strong><br>'
                f'{translated_question or "<em>No translation available</em>"}'
                f'</div>'
            )

        return format_html(''.join(preview_html))

    translation_preview.short_description = _("Translation Preview")

    def get_list_display(self, request):
        """
        Dynamically generate list_display based on user permissions
        """
        list_display = ['question']
        if request.user.has_perm('faq.can_see_metadata'):
            list_display.extend(['created_at', 'updated_at'])
        return list_display

    def get_queryset(self, request):
        """
        Optimize queryset for list view
        """
        qs = super().get_queryset(request)
        return qs.select_related().prefetch_related()


  
    actions = ['translate_selected_faqs', 'clear_translations']

    def translate_selected_faqs(self, request, queryset):
        """Translate selected FAQs"""
        for faq in queryset:
            faq.save()  # This will trigger the translation in the save method
        
        self.message_user(
            request,
            f"Successfully initiated translation for {queryset.count()} FAQs."
        )
    
    translate_selected_faqs.short_description = _("Translate selected FAQs")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:faq_id>/preview/',
                self.admin_site.admin_view(self.preview_view),
                name='faq-preview',
            ),
        ]
        return custom_urls + urls

    def preview_view(self, request, faq_id):
        """Preview FAQ in different languages"""
        faq = self.get_object(request, faq_id)
        context = {
            'faq': faq,
            'languages': [
                ('en', 'English'),
                ('hi', 'Hindi'),
                ('bn', 'Bengali'),
            ],
            'title': f'Preview FAQ: {faq.question[:50]}...',
            **self.admin_site.each_context(request),
        }
        return render(request, 'admin/faq/preview.html', context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_preview'] = True
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )