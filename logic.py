import random

DRILLS = [
    {"prompt": "Hello", "answer": "สวัสดี"},
    {"prompt": "Thank you", "answer": "ขอบคุณ"},
    {"prompt": "Yes", "answer": "ใช่"},
]

def get_random_drill():
    return random.choice(DRILLS)
