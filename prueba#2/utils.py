import re

def extract_emails(text):
    # Coincide con correos normales
    return ", ".join(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text))

def extract_phones(text):
    # Mejora: permite +57, espacios, guiones y paréntesis, pero evita capturar secuencias tipo "2023-05-20"
    raw_numbers = re.findall(r"\+?\(?\d{1,4}\)?[\s\-]?\d{2,4}[\s\-]?\d{2,4}[\s\-]?\d{2,4}", text)
    
    # Limpieza opcional: quitar espacios redundantes
    cleaned = [re.sub(r"\s+", " ", num.strip()) for num in raw_numbers]
    return ", ".join(cleaned)
