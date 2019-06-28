from difflib import SequenceMatcher

def match_percentage(str1: str, str2: str):
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio() * 100
