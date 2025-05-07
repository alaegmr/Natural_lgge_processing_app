import re
from farasa.stemmer import FarasaStemmer


class TextCleaner:
    def __init__(self, interactive_mode=False):
        """Initialise le stemmer Farasa"""
        self.stemmer = FarasaStemmer(interactive=interactive_mode)

    @staticmethod
    def clean_arabic_text(text):
        """Nettoie le texte arabe (sans racinisation)"""
        # Supprime tous les diacritiques (tashkeel)
        text = re.sub(r'[\u064B-\u065F\u0670]', '', text)

        # Normalisation des caractères arabes
        text = re.sub(r'[أإآ]', 'ا', text)  # Normalise les différentes formes de alif
        text = re.sub(r'ة', 'ه', text)  # Convertit le ta marbuta en ha
        text = re.sub(r'ى', 'ي', text)  # Convertit l'alif maqsura en ya

        # Supprime les caractères non-arabes
        text = re.sub(r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\s،؛؟]', '', text)

        # Normalise les espaces
        return re.sub(r'\s+', ' ', text).strip()

    def clean_and_stem(self, text):
        """Combine nettoyage ET racinisation"""
        cleaned_text = self.clean_arabic_text(text)
        return self.stemmer.stem(cleaned_text)

    def process_batch(self, texts):
        """Traite une liste de textes (optimisé pour les performances)"""
        return [self.clean_and_stem(text) for text in texts]