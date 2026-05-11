import re

import config


PLAY_INTENTS = (
    "baja do",
    "play",
    "song",
    "gana",
    "music",
    "baja",
    "chalao",
    "chala",
    "lagao",
)

MOOD_SEARCHES = {
    "sad": "best hindi sad songs",
    "romantic": "best hindi romantic songs",
    "lovely": "best hindi romantic songs",
    "love": "best hindi romantic songs",
    "gym": "best workout songs",
    "study": "lofi study music",
    "coding": "lofi coding music",
    "party": "best hindi party songs",
    "night": "late night hindi songs",
    "alone": "late night hindi songs",
}

FILLER_WORDS = (
    "ek",
    "acha",
    "accha",
    "sa",
    "koi",
    "please",
    "pls",
    "kar",
    "karo",
)


class PlayMessageProxy:
    def __init__(self, message, query):
        self._message = message
        self.text = f"/play {query}"
        self.command = ["play", query]

    def __getattr__(self, name):
        return getattr(self._message, name)


def _has_word(text, word):
    return re.search(rf"(?<!\w){re.escape(word)}(?!\w)", text) is not None


def parse_music_request(text):
    if not text:
        return None

    lowered = text.lower().strip()
    if lowered.startswith(("/", "!", "%", ",", ".", "@", "#")):
        return None

    has_wake = any(_has_word(lowered, word) for word in config.WAKE_WORDS)
    has_intent = any(intent in lowered for intent in PLAY_INTENTS)
    if not has_wake or not has_intent:
        return None

    for mood, search in MOOD_SEARCHES.items():
        if _has_word(lowered, mood):
            return search

    query = lowered
    for word in config.WAKE_WORDS:
        query = re.sub(rf"(?<!\w){re.escape(word)}(?!\w)", " ", query)
    for intent in sorted(PLAY_INTENTS, key=len, reverse=True):
        query = query.replace(intent, " ")
    for word in FILLER_WORDS:
        query = re.sub(rf"(?<!\w){re.escape(word)}(?!\w)", " ", query)

    query = re.sub(r"\s+", " ", query).strip()
    return query or None
