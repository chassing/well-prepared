import json
import random
from pathlib import Path

EMOJI_DB = json.loads((Path(__file__).resolve().parent / "emoji.json").read_text())


def matching_emojis(keyword: str) -> list[str]:
    return list({
        emoji["emoji"] for emoji in EMOJI_DB if keyword.lower() in emoji["keywords"]
    })


def random_emoji(keyword: str) -> str:
    try:
        return random.choice(matching_emojis(keyword))  # noqa: S311
    except IndexError:
        return ""
