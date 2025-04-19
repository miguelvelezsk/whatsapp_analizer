import re
from collections import Counter
from utils.helpers import stopwords
import random

def analize_chat(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        chat = f.read().lower()

    chat_clean = re.sub(r"^\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}(?:\s?[ap]\.\s?m\.)? - .*?: ", "", chat, flags=re.MULTILINE)

    total = len(chat_clean.splitlines())
    te_amo = chat_clean.count("te amo")
    te_quiero = chat_clean.count("te quiero")

    def get_random_line(range_iterator):
        lines = chat_clean.splitlines()

        new_stopwords = ['null', 'multimedia', 'omitted', '<multimedia omitido>']

        filtered_lines = [line for line in lines if not any(word in new_stopwords for word in line.split())]

        range_iterator = min(len(filtered_lines), range_iterator)

        random_lines = random.sample(filtered_lines, range_iterator)

        return random_lines

    emoji_pattern = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE
    )

    skin_tone_modifiers = {
    "\U0001F3FB",
    "\U0001F3FC",
    "\U0001F3FD", 
    "\U0001F3FE", 
    "\U0001F3FF", 
    }

    emojis_raw = emoji_pattern.findall(chat_clean)
    emojis = []
    previous = ""

    for e in emojis_raw:
        if e != previous:
            if e not in skin_tone_modifiers:
                emojis.append(e)
        previous = e

    emoji_freq = Counter(emojis)

    def emoji_to_filename(e):
        return '-'.join(f"{ord(c):x}" for c in e) + ".png"
    
    for e, count in Counter(emojis).most_common(10):
        print(f"{e}: {count} veces → nombre: {emoji_to_filename(e)}")

    words = re.findall(r'\b\w+\b', chat_clean)
    filtered_words = [p for p in words if p not in stopwords and len(p) > 3]
    freq_words = Counter(filtered_words)

    return te_amo, te_quiero, emoji_freq, freq_words, total, get_random_line(100)

