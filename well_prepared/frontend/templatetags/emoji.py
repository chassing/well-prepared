import re

from django import template


def first_is_emoji(value: str) -> bool:
    emoji_pattern = re.compile(
        r"^[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002600-\U000026FF\U00002700-\U000027BF]"
    )
    return bool(emoji_pattern.match(value))


register = template.Library()
register.filter("first_is_emoji", first_is_emoji)
