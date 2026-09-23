from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import obradi_tekst

class VektorskiModel:

    def __init__(self,oglasi):
        self.oglasi = oglasi
        naslovi = [o.get("naslov","") for o in self.oglasi]
        opisi = [o.get("opis","")for o in self.oglasi]
        self.vectorizer_naslov = TfidfVectorizer(tokenizer=obradi_tekst,token_pattern=None)
        self.vectorizer_opis = TfidfVectorizer(tokenizer=obradi_tekst,token_pattern=None)
        self.matrica_naslov = self.vectorizer_naslov.fit_transform(naslovi)
        self.matrica_opis = self.vectorizer_opis.fit_transform(opisi)

    def pretrazi(self,upit,top_k = 10, polje="sve"):
        if not upit or not isinstance(upit, str) or not upit.strip():
            return []

        if polje == "naslov":
            upit_vec = self.vectorizer_naslov.transform([upit])
            ukupni_skorovi = cosine_similarity(upit_vec, self.matrica_naslov)[0]

        elif polje == "opis":
            upit_vec = self.vectorizer_opis.transform([upit])
            ukupni_skorovi = cosine_similarity(upit_vec, self.matrica_opis)[0]

        else:
            upit_naslov_vec = self.vectorizer_naslov.transform([upit])
            upit_opis_vec = self.vectorizer_opis.transform([upit])
            skorovi_naslov = cosine_similarity(upit_naslov_vec, self.matrica_naslov)[0]
            skorovi_opis = cosine_similarity(upit_opis_vec,self.matrica_opis)[0]
            ukupni_skorovi = (0.6*skorovi_naslov) + (0.4*skorovi_opis)

        rezultati = []
        for i, skor in enumerate(ukupni_skorovi):
            if skor > 0:
                rezultati.append({
                    "oglas": self.oglasi[i],
                    "skor" : round(float(skor),3)
                })

        rezultati.sort(key = lambda x: x["skor"], reverse=True)
        return rezultati[:top_k]