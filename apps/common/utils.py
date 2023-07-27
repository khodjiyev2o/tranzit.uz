import environ
from django.conf import settings
from django.core.cache import cache
from eskiz_sms import EskizSMS

from helpers.cache import generate_cache_key, generate_code


env = environ.Env()


def send_activation_code_via_sms(phone: str, cache_type: str, session: str):
    if settings.TEST is True:
        code = generate_code()
        cache.set(generate_cache_key(cache_type, phone, session), code, timeout=5)
    else:
        code = generate_code()
        cache.set(generate_cache_key(cache_type, phone, session), code, timeout=120)

        # message_data = f"Tranzit.uz uchun <#> Tasdiqlash kodi: {code}"
        # email = env.str("ESKIZ_USER_EMAIL")
        # password = env.str("ESKIZ_USER_PASSWORD")
        # eskiz = EskizSMS(email=email, password=password)
        # eskiz.send_sms(mobile_phone=phone[1:], message=message_data, from_whom="4546", callback_url=None)
