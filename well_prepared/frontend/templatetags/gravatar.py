import hashlib
from urllib.parse import urlencode

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def gravatar_url(email: str, size: int) -> str:
    email_encoded = email.lower().encode("utf-8")
    email_hash = hashlib.sha256(email_encoded).hexdigest()
    params = urlencode({"s": str(size)})
    return f"https://www.gravatar.com/avatar/{email_hash}?{params}"


@register.filter
def gravatar(email: str, size: int = 30) -> str:
    return mark_safe(gravatar_url(email, size))  # noqa: S308
