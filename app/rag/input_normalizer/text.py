from unicodedata import normalize
from app.rag.core.string_guard import require_str

# Normalization rules (v1): Do NOT change meaning, Do NOT expand abbreviations, Do NOT infer semantics, Only perform mechanical cleanup
# Not handling - > No digit normalization, No newline semantics, No paragraph inference, No heading detection, No abbreviation expansion, No language logic

def normalize_data(text:str) -> str:
    text = require_str(text,name="input_normalizer,text.py") #string check
    unicode_normalized_text = normalize("NFKC",text) #normalization
    normalized_text = " ".join(unicode_normalized_text.split()) #handling whitespaces (space,new line,leading and ending white spaces)
    return normalized_text