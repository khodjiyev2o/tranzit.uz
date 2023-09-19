from django.conf import settings
from modeltranslation.translator import TranslationOptions, register

from apps.common.models import FrontTranslation


@register(FrontTranslation)
class FrontTranslationTranslationOptions(TranslationOptions):
    fields = ("text",)
    required_languages = settings.MODELTRANSLATION_LANGUAGES
