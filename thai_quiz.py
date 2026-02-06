import random

# Basic Thai consonant list (you can expand later)
THAI_CONSONANTS = [
    ("ก", "ko kai"),
    ("ข", "kho khai"),
    ("ค", "kho khwai"),
    ("ง", "ngo ngu"),
    ("จ", "cho chan"),
    ("ฉ", "cho ching"),
    ("ช", "cho chang"),
    ("ซ", "so so"),
    ("ญ", "yo ying"),
]

def render_quiz():
    """Return a simple flashcard-style quiz as HTML"""

    letter, name = random.choice(THAI_CONSONANTS)

    html = f"""
    <h2>Thai Consonant Flashcard</h2>
    <p style="font-size: 80px;">{letter}</p>
    <details>
        <summary>Show pronunciation</summary>
        <p>{name}</p>
    </details>
    <br>
    <a href="/">Next card</a>
    """

    return html
