from preprocessing import obradi_tekst

def kreiraj_indeks(oglasi):
    indeks = {
        "naslov":{},
        "opis":{},
    }
    for o in oglasi:
        doc_id = o.get("id")
        polja = {
            "naslov": obradi_tekst(o.get("naslov","")),
            "opis":  obradi_tekst(o.get("opis",""))
        }
        for nazivPolja, listaReci in polja.items():
            for rec in listaReci:
                if rec not in indeks[nazivPolja]:
                    indeks[nazivPolja][rec] = set()
                indeks[nazivPolja][rec].add(doc_id)
    return indeks


def bulova_pretraga(upit, indeks, svi_id, polje="sve"):
    if not upit or not isinstance(upit, str):
        return set()

    delovi = upit.strip().split()

    grupe = [[]]

    for deo in delovi:
        if deo.upper() == "OR":
            grupe.append([])
        else:
            grupe[-1].append(deo)

    konacan_rezultat = set()

    for grupa in grupe:
        rezultat = None
        negacija = False

        for deo in grupa:
            deo_upper = deo.upper()

            if deo_upper == "AND":
                continue

            if deo_upper == "NOT":
                negacija = True
                continue

            obradjene_reci = obradi_tekst(deo)

            if not obradjene_reci:
                continue

            koren = obradjene_reci[0]
            skup_za_rec = nadji_oglase_za_rec(koren, indeks, polje)

            if rezultat is None:
                if negacija:
                    rezultat = svi_id - skup_za_rec
                else:
                    rezultat = set(skup_za_rec)
            else:
                if negacija:
                    rezultat = rezultat - skup_za_rec
                else:
                    rezultat = rezultat & skup_za_rec

            negacija = False

        if rezultat is not None:
            konacan_rezultat = konacan_rezultat | rezultat

    return konacan_rezultat


def nadji_oglase_za_rec(rec, indeks, polje):

    if polje != "sve" and polje in indeks:
        return indeks[polje].get(rec, set())
    else:
        rezultat = set()
        for p in indeks:
            rezultat = rezultat | indeks[p].get(rec, set())
        return rezultat
