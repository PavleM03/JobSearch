import re
from stemmer import stem_arr

# Potrebno je pokrenuti(zbog stemera): 
# python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"

TEHNOLOGIJE = {
    "c++", "c#", ".net", "asp.net",
    "node.js", "vue.js"
}

def obradi_tekst(tekst):
    if not tekst or not isinstance(tekst, str):
        return []

    tekst = tekst.lower()
    pattern = r'\.?[a-z0-9]+(?:[.+#][a-z0-9+#]*)*'
    reci = re.findall(pattern, tekst)
    stopReci = ["i","u","na","za","sa","je","su","se","od","da","ali","ili","kao","pa","te","ni","niti","a","nego","vec","jer","ako","ukoliko","kad","li","dok","kada","posto","zato","sto","uz","kroz","iz","do","o","po","koji","koja","koje","ce","bi"]

    reci = [rec for rec in reci if rec not in stopReci and not rec.isdigit()]
    rezultat = []
    for rec in reci:
        if rec in TEHNOLOGIJE:
            rezultat.append(rec)
        else:
            rezultat.extend(stem_arr(rec))

    return rezultat