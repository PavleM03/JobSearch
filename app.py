import streamlit as st
import json
import pandas as pd

from inverted_index import kreiraj_indeks, bulova_pretraga
from vector_model import VektorskiModel
from evaluation import pokreni_evaluaciju

st.set_page_config(page_title="Pretraživač IT Poslova", page_icon="💼", layout="wide")

@st.cache_resource
def ucitaj_sistem():
    with open("data/jobs.json", "r", encoding="utf-8") as f:
        oglasi = json.load(f)
    
    svi_id = {o["id"] for o in oglasi}
    indeks = kreiraj_indeks(oglasi)
    vektorski_model = VektorskiModel(oglasi)
    mapa_oglasa = {o["id"]: o for o in oglasi}
    
    return oglasi, indeks, vektorski_model, svi_id, mapa_oglasa

oglasi, indeks, vektorski_model, svi_id, mapa_oglasa = ucitaj_sistem()

st.title("💼 Sistem za pretraživanje poslova")
st.caption("Projekat iz predmeta Pretraživanje informacija | IR Engine")

tab_pretraga, tab_evaluacija = st.tabs(["🔍 Pretraga Poslova", "📊 Evaluacija Sistema"])

with tab_pretraga:
    col_unos, col_opcije = st.columns([2, 1])

    with col_unos:
        upit = st.text_input("Unesite upit za pretragu:", placeholder="npr. Python Backend, React OR Angular, DevOps NOT Junior")

    with col_opcije:
        model_izbor = st.radio(
            "Izaberite model pretrage:",
            ["Vektorski model (TF-IDF)", "Bulov model (AND, OR, NOT)"]
        )

    col_polje, col_limit = st.columns(2)
    with col_polje:
        polje = st.selectbox("Pretraži po polju:", ["sve", "naslov", "opis"])
    with col_limit:
        top_k = st.slider("Maksimalan broj rezultata:", min_value=5, max_value=30, value=10)

    lokacije = ["sve"] + sorted(set(o["lokacija"] for o in oglasi))
    kompanije = ["sve"] + sorted(set(o["kompanija"] for o in oglasi))

    col_lokacija, col_kompanija = st.columns(2)
    with col_lokacija:
        lokacija_filter = st.selectbox("Lokacija:", lokacije)
    with col_kompanija:
        kompanija_filter = st.selectbox("Kompanija:", kompanije)

    dugme_pretrazi = st.button("🔎 Pretraži poslove", use_container_width=True)

    if dugme_pretrazi:
        if not upit.strip():
            st.warning("Molimo unesite tekst upita pre pretrage.")
        else:
            if model_izbor == "Vektorski model (TF-IDF)":
                rezultati = vektorski_model.pretrazi(upit, top_k=len(oglasi), polje=polje)
            else:
                pronadjeni_id = bulova_pretraga(upit, indeks, svi_id, polje=polje)
                rezultati = [{"oglas": mapa_oglasa[doc_id], "skor": None} for doc_id in pronadjeni_id]

            if lokacija_filter != "sve":
                rezultati = [r for r in rezultati if r["oglas"]["lokacija"] == lokacija_filter]

            if kompanija_filter != "sve":
                rezultati = [r for r in rezultati if r["oglas"]["kompanija"] == kompanija_filter]

            ukupno = len(rezultati)
            prikazani = rezultati[:top_k]

            st.subheader(f"Pronađeno rezultata: {ukupno} (Prikazano prvih {len(prikazani)})")

            if not prikazani:
                st.info("Nijedan oglas ne zadovoljava unete kriterijume.")
            else:
                for r in prikazani:
                    o = r["oglas"]
                    skor = r["skor"]
                    with st.container(border=True):
                        c1, c2 = st.columns([4, 1])
                        with c1:
                            st.markdown(f"### {o['naslov']}")
                            st.markdown(f"🏢 **Kompanija:** {o['kompanija']} | 📍 **Lokacija:** {o['lokacija']}")
                            st.write(o["opis"])
                        with c2:
                            if skor is not None:
                                st.metric("Sličnost", f"{skor * 100:.1f}%")
                            else:
                                st.caption(f"ID oglasa: {o['id']}")

with tab_evaluacija:
    st.header("📊 Evaluacija pretraživača (Ground Truth)")
    st.write(
        "Evaluacija se vrši nad kontrolisanim skupom od **prvih 100 oglasa** "
        "korišćenjem unapred definisanih 5 test upita i ručno označenih relevantnih dokumenata."
    )

    if st.button("🚀 Pokreni evaluaciju modela", use_container_width=True):
        with st.spinner("Računanje metrika u toku..."):
            podaci_evaluacije = pokreni_evaluaciju()

            df = pd.DataFrame(podaci_evaluacije)
            
            df_prikaz = df.rename(columns={
                "upit": "Test Upit",
                "bool_p": "Bulov Precision",
                "bool_r": "Bulov Recall",
                "bool_f1": "Bulov F1",
                "vec_p": "Vektorski Precision",
                "vec_r": "Vektorski Recall",
                "vec_f1": "Vektorski F1"
            })

            st.dataframe(df_prikaz, use_container_width=True)

            c1, c2 = st.columns(2)
            with c1:
                st.info("📌 **Bulov model (Prosek):**")
                st.write(f"- **Precision:** {df['bool_p'].mean():.3f}")
                st.write(f"- **Recall:** {df['bool_r'].mean():.3f}")
                st.write(f"- **F1 Score:** {df['bool_f1'].mean():.3f}")

            with c2:
                st.success("📌 **Vektorski model (Prosek):**")
                st.write(f"- **Precision:** {df['vec_p'].mean():.3f}")
                st.write(f"- **Recall:** {df['vec_r'].mean():.3f}")
                st.write(f"- **F1 Score:** {df['vec_f1'].mean():.3f}")