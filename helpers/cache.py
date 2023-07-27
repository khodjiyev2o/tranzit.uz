import random
import string


class CacheTypes:  # noqa
    registration_sms_verification = "registration_sms_verification"
    forget_pass_verification = "forget_pass_verification"
    change_phone_verification = "change_phone_verification"


def generate_cache_key(type_, *args):
    return f"{type_}{''.join(args)}"


def generate_code():
    return "".join(random.choice(string.digits) for _ in range(6))
