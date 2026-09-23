import json
import random

gradovi = [
    "Beograd", "Novi Sad", "Nis", "Kragujevac", 
    "Subotica", "Cacak", "Zrenjanin", "Remote"
]

senioriteti = ["Junior", "Medior", "Senior"]

kompanije = [
    "Tech Solutions d.o.o.", "CodeCraft Studio", "Nova Informatika", 
    "Digital Systems Beograd", "Cloud Peak Technologies", "Smart Software Group", 
    "Balkan Tech Hub", "Apex Digital", "DataWave Solutions", "SyncIT Labs",
    "Levi9 Services", "Endava Development", "Vega IT Sourcing", "HTEC Group",
    "Comtrade System", "Asseco Solutions", "Saga d.o.o.", "Quantox Technology",
    "Clarivate Analytics", "NetSet Global"
]

benefiti = [
    " Nudimo rad u hibridnom modelu i fleksibilno radno vreme.",
    " Obezbedjeno privatno zdravstveno osiguranje i budzet za strucno usavrsavanje.",
    " Mogucnost rada u potpunosti od kuce (remote) uz obezbedjenu najnoviju opremu.",
    " Rad na velikim enterprise projektima uz mentorsku podrsku i godisnje bonuse.",
    " Odlicna radna atmosfera, fleksibilni uslovi i placeni kursevi i sertifikacije.",
    " Rad u modernom timu uz koriscenje najnovijih cloud tehnologija i alata."
]

uloge_konfiguracija = [
    {
        "naslov": "Python Backend Inzenjer",
        "sabloni": [
            "Trazimo {senioritet} backend inzenjera za rad na razvoju web servisa. Neophodno je poznavanje {framework} framework-a i rad sa bazom {baza}. Pozeljno iskustvo sa alatom {alat}.",
            "Kompanija prosiruje tim i trazi {senioritet} inzenjera sa odlicnim znanjem Python-a. Fokus je na {framework} arhitekturi, optimizaciji baze {baza} i koriscenju {alat} alata.",
            "Potreban {senioritet} inzenjer za rad na skalabilnim API resenjima. Obavezno poznavanje {framework} tehnologije, dok je rad sa {baza} bazom i {alat} sistemom velika prednost."
        ],
        "parametri": {
            "framework": ["Django", "FastAPI", "Flask"],
            "baza": ["PostgreSQL", "MySQL", "MongoDB"],
            "alat": ["Docker", "Redis", "Celery", "Kafka"]
        }
    },
    {
        "naslov": "Frontend Inzenjer",
        "sabloni": [
            "Potreban {senioritet} frontend inzenjer sa odlicnim poznavanjem jezika {jezik} i radom u {framework}. Glavni zadaci su izrada interfejsa i upravljanje stanjem aplikacije kroz {stanje}.",
            "Trazimo kreativnog {senioritet} inzenjera za moderan UI/UX. Neophodno je vladanje {jezik} standardima i {framework} bibliotekom. Pozeljno poznavanje {stanje} biblioteke.",
            "Otvorena pozicija za {senioritet} frontend developera. Rad na razvoju web aplikacija u {framework} okruzenju uz koriscenje {jezik} jezika i {stanje} za state management."
        ],
        "parametri": {
            "jezik": ["JavaScript", "TypeScript"],
            "framework": ["React", "Vue.js", "Angular"],
            "stanje": ["Redux", "Zustand", "Pinia", "Context API"]
        }
    },
    {
        "naslov": "Java Backend Inzenjer",
        "sabloni": [
            "Otvorena pozicija za {senioritet} Java inzenjera. Zaduzenja obuhvataju razvoj mikroservisa koriscenjem {framework} framework-a. Obavezno iskustvo u radu sa bazom {baza} i ORM alatom {orm}.",
            "Trazimo odgovornog {senioritet} inzenjera za rad na robustnim backend servisima. Glavni stack cine {framework}, relacione baze poput {baza} i perzistencija podataka uz {orm}.",
            "Potreban {senioritet} Java programer za rad na finansijskim platformama. Razvoj u {framework} okruzenju, dizajn baza podataka u {baza} i mapiranje uz pomoc {orm} alata."
        ],
        "parametri": {
            "framework": ["Spring Boot", "Quarkus", "Micronaut"],
            "baza": ["PostgreSQL", "MySQL", "Oracle"],
            "orm": ["Hibernate", "MyBatis"]
        }
    },
    {
        "naslov": "Full Stack Inzenjer",
        "sabloni": [
            "Trazi se {senioritet} Full Stack inzenjer za razvoj web platformi. Potrebno je iskustvo na backendu sa {backend}, kao i na frontendu uz {frontend}. Za skladistenje podataka koristi se baza {baza}.",
            "Pozicija za {senioritet} inzenjera koji vlada i serverskom i klijentskom stranom. Razvoj API servisa u {backend}, moderan interfejs uz {frontend} i perzistencija podataka u {baza}."
        ],
        "parametri": {
            "backend": ["Node.js (Express)", "Python (FastAPI)", "Java (Spring Boot)", "C# (.NET)"],
            "frontend": ["React", "Vue.js", "Angular"],
            "baza": ["MongoDB", "PostgreSQL", "MySQL"]
        }
    },
    {
        "naslov": "DevOps Inzenjer",
        "sabloni": [
            "Sirimo tim i trazimo {senioritet} DevOps inzenjera. Glavni fokus je automatizacija infrastrukture, rad sa kontejnerima uz {kontejner} i odrzavanje servisa na {cloud} platformi. Neophodno poznavanje {cicd} alata.",
            "Potreban {senioritet} Cloud/DevOps inzenjer za upravljanje produkcionim okruzenjima. Klucne tehnologije su {cloud}, orkestracija preko {kontejner} i implementacija {cicd} procesa."
        ],
        "parametri": {
            "kontejner": ["Docker", "Kubernetes"],
            "cloud": ["AWS", "Azure", "Google Cloud"],
            "cicd": ["GitLab CI", "GitHub Actions", "Jenkins", "Terraform"]
        }
    },
    {
        "naslov": "QA Inzenjer",
        "sabloni": [
            "Raspisujemo konkurs za radno mesto: {senioritet} QA inzenjer. Posao obuhvata automatsko testiranje aplikacija koriscenjem alata {alat}, testiranje API servisa kroz {api} i prijavu gresaka preko alata {sistem}.",
            "Trazimo posvecenog {senioritet} inzenjera za kontrolu kvaliteta softvera. Fokus je na automatizaciji testova uz {alat}, validaciji integracija preko {api} i pracenju taskova u {sistem} alatu."
        ],
        "parametri": {
            "alat": ["Selenium", "Cypress", "Playwright"],
            "api": ["Postman", "RestAssured"],
            "sistem": ["Jira", "TestRail"]
        }
    },
    {
        "naslov": "Inzenjer za podatke",
        "sabloni": [
            "Trazimo {senioritet} inzenjera za podatke. Zadaci ukljucuju obradu velikih skupova podataka pomocu tehnologije {obrada} i rad sa skladistem podataka {baza}. Neophodno je poznavanje {vestina}.",
            "Otvaramo poziciju za {senioritet} Data Engineer-a. Fokus je na izgradnji pouzdanih data pipeline-ova kroz {obrada}, upravljanju modernim skladistima {baza} i optimizaciji {vestina}."
        ],
        "parametri": {
            "obrada": ["Apache Spark", "Apache Airflow", "Python Pandas"],
            "baza": ["Snowflake", "BigQuery", "PostgreSQL"],
            "vestina": ["SQL upita", "ETL procesa", "data warehouse arhitekture"]
        }
    },
    {
        "naslov": "C# .NET Inzenjer",
        "sabloni": [
            "Pozicija za {senioritet} .NET inzenjera na razvoju enterprise servisa. Neophodno poznavanje {framework} framework-a, rad sa bazom {baza} i ORM alatom {orm}.",
            "Trazimo {senioritet} programera sa iskustvom u Microsoft ekosistemu. Glavna zaduzenja ukljucuju {framework} web servise, relacione baze {baza} i rad uz {orm} biblioteku."
        ],
        "parametri": {
            "framework": [".NET Core", "ASP.NET Core", ".NET 8"],
            "baza": ["SQL Server", "PostgreSQL"],
            "orm": ["Entity Framework", "Dapper"]
        }
    },
    {
        "naslov": "Inzenjer za masinsko ucenje",
        "sabloni": [
            "Trazimo {senioritet} Machine Learning inzenjera za rad na prediktivnim modelima. Obavezno poznavanje biblioteka {biblioteka} i rada sa {alati}. Iskustvo u obradi podataka uz {baza} je prednost.",
            "Potreban {senioritet} AI inzenjer za razvoj algoritama vestacke inteligencije. Koriste se {biblioteka} okruzenja, deployment modela preko {alati} i integracija sa bazom {baza}."
        ],
        "parametri": {
            "biblioteka": ["PyTorch", "TensorFlow", "Scikit-Learn"],
            "alati": ["MLflow", "Docker", "FastAPI"],
            "baza": ["PostgreSQL", "MongoDB"]
        }
    },
    {
        "naslov": "Mobilni Inzenjer",
        "sabloni": [
            "Potreban {senioritet} mobilni inzenjer za razvoj cross-platform aplikacija. Neophodno odlicno poznavanje tehnologije {tehnologija} i rada sa {api} servisima. Pozeljno poznavanje {stanje} biblioteke.",
            "Otvorena pozicija za {senioritet} inzenjera za mobilne platforme. Rad na razvoju aplikacija uz {tehnologija}, integracija sa eksternim {api} sistemima i upravljanje stanjem preko {stanje}."
        ],
        "parametri": {
            "tehnologija": ["Flutter", "React Native"],
            "api": ["REST API", "GraphQL"],
            "stanje": ["Bloc", "Redux", "Provider"]
        }
    },
    {
        "naslov": "Sistem Administrator",
        "sabloni": [
            "Trazimo {senioritet} sistem administratora za odrzavanje IT infrastrukture. Obavezno poznavanje {os} operativnih sistema, mrezne konfiguracije i alata za automatizaciju {alat}. Rad sa servisom {servis}.",
            "Potreban pouzdan {senioritet} administrator sistema. Zaduzenja obuhvataju nadzor servera pod {os} okruzenjem, administraciju alata {alat} i konfiguraciju servisa {servis}."
        ],
        "parametri": {
            "os": ["Linux (Ubuntu/CentOS)", "Windows Server"],
            "alat": ["Ansible", "Bash skripti", "PowerShell skripti"],
            "servis": ["Active Directory", "Nginx", "Apache"]
        }
    },
    {
        "naslov": "Inzenjer za bezbednost",
        "sabloni": [
            "Potreban {senioritet} Cybersecurity inzenjer za analizu bezbednosnih rizika. Obavezno poznavanje {analiza} metoda i alata kao sto je {alat}. Iskustvo sa protokolima {protokol} je neophodno.",
            "Otvaramo poziciju za {senioritet} inzenjera informacione bezbednosti. Zaduzenja ukljucuju penetraciono testiranje preko {alat}, implementaciju {analiza} strategija i monitoring {protokol} saobracaja."
        ],
        "parametri": {
            "analiza": ["penetration testing", "vulnerability assessment"],
            "alat": ["Wireshark", "Burp Suite", "Metasploit", "Nessus"],
            "protokol": ["mreznog", "aplikativnog", "VPN i SSL"]
        }
    },
    {
        "naslov": "Inzenjer za ugradjene sisteme",
        "sabloni": [
            "Trazimo {senioritet} Embedded inzenjera za razvoj firmware-a. Neophodno poznavanje jezika {jezik} i rad sa mikrokontrolerima {hardver}. Iskustvo sa protokolom {protokol} je obavezno.",
            "Otvorena pozicija za {senioritet} inzenjera u oblasti ugradjenog softvera. Razvoj koda u {jezik}, testiranje na platformi {hardver} i komunikacija preko {protokol} interfejsa."
        ],
        "parametri": {
            "jezik": ["C", "C++", "Rust"],
            "hardver": ["ARM Cortex", "STM32", "ESP32"],
            "protokol": ["CAN", "SPI i I2C", "UART"]
        }
    },
    {
        "naslov": "Scrum Master",
        "sabloni": [
            "Trazimo posvecenog {senioritet} Scrum Master-a za vodenje razvojnih timova. Obavezno poznavanje {metodologija} praksi i pracenje procesa kroz alat {alat}. Rad na unapredjenju timske efikasnosti.",
            "Potreban {senioritet} Agile / Scrum Master. Zaduzenja ukljucuju fasilitaciju sastanaka, primenu {metodologija} okvira i upravljanje taskovima u sistemu {alat}."
        ],
        "parametri": {
            "metodologija": ["Agile i Scrum", "Kanban", "Agile metodologije"],
            "alat": ["Jira", "Confluence", "Azure DevOps"]
        }
    }
]

def formatiraj_opis(uloga, senioritet):
    izabrani_sablon = random.choice(uloga["sabloni"])
    izabrane_tehnologije = {k: random.choice(v) for k, v in uloga["parametri"].items()}
    izabrane_tehnologije["senioritet"] = senioritet
    
    opis = izabrani_sablon.format(**izabrane_tehnologije)
    opis += random.choice(benefiti)
    return opis

def generisi_podatke(broj_oglasa):
    oglasi = []
    for i in range(broj_oglasa):
        uloga = random.choice(uloge_konfiguracija)
        senioritet = random.choice(senioriteti)
        
        oglas = {
            "id": i + 1,
            "naslov": f"{senioritet} {uloga['naslov']}",
            "kompanija": random.choice(kompanije),
            "lokacija": random.choice(gradovi),
            "opis": formatiraj_opis(uloga, senioritet)
        }
        oglasi.append(oglas)
    return oglasi

if __name__ == "__main__":
    oglasi = generisi_podatke(1000)
    with open("data/jobs.json", "w", encoding="utf-8") as f:
        json.dump(oglasi, f, indent=2)
    print(f"Izgenerisano je {len(oglasi)} oglasa u fajlu jobs.json!")
