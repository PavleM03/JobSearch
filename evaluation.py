import json

from inverted_index import kreiraj_indeks, bulova_pretraga
from vector_model import VektorskiModel

K = 10


def izracunaj_precision(pronadjeni, relevantni):
    pronadjeni_set = set(pronadjeni)
    relevantni_set = set(relevantni)

    if len(pronadjeni_set) == 0:
        return 0.0

    tacno_pronadjeni = len(pronadjeni_set & relevantni_set)
    return tacno_pronadjeni / len(pronadjeni_set)


def izracunaj_recall(pronadjeni, relevantni):
    pronadjeni_set = set(pronadjeni)
    relevantni_set = set(relevantni)

    if len(relevantni_set) == 0:
        return 0.0

    tacno_pronadjeni = len(pronadjeni_set & relevantni_set)
    return tacno_pronadjeni / len(relevantni_set)


def izracunaj_f1(precision, recall):
    if precision + recall == 0:
        return 0.0

    return 2 * (precision * recall) / (precision + recall)


def pokreni_evaluaciju(putanja_jobs="data/jobs.json", putanja_gt="data/ground_truth.json"):
    with open(putanja_jobs, "r", encoding="utf-8") as f:
        svi_oglasi = json.load(f)

    test_oglasi = svi_oglasi[:100]
    svi_test_id = {o["id"] for o in test_oglasi}

    with open(putanja_gt, "r", encoding="utf-8") as f:
        ground_truth = json.load(f)

    indeks = kreiraj_indeks(test_oglasi)
    vektorski_model = VektorskiModel(test_oglasi)

    rezultati_evaluacije = []

    for stavka in ground_truth:
        upit = stavka["upit"]
        relevantni = set(stavka["relevantni_id"])

        bool_pronadjeni = bulova_pretraga(upit, indeks, svi_test_id)
        p_bool = izracunaj_precision(bool_pronadjeni, relevantni)
        r_bool = izracunaj_recall(bool_pronadjeni, relevantni)
        f1_bool = izracunaj_f1(p_bool, r_bool)

        vec_rezultati = vektorski_model.pretrazi(upit, top_k=K)
        vec_pronadjeni = {r["oglas"]["id"] for r in vec_rezultati}
        p_vec = izracunaj_precision(vec_pronadjeni, relevantni)
        r_vec = izracunaj_recall(vec_pronadjeni, relevantni)
        f1_vec = izracunaj_f1(p_vec, r_vec)

        rezultati_evaluacije.append({
            "upit": upit,
            "bool_p": round(p_bool, 3), "bool_r": round(r_bool, 3), "bool_f1": round(f1_bool, 3),
            "vec_p": round(p_vec, 3), "vec_r": round(r_vec, 3), "vec_f1": round(f1_vec, 3)
        })

    return rezultati_evaluacije
