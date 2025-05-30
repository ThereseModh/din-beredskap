# Din Beredskap – AI assistent för hemberedskap och krishantering

Ett AI-projekt som hjälper människor att få svar på frågor kring samhällskriser, personlig beredskap och akuta situationer. Svaren baseras på officiella informationskällor som MSB, Röda Korset, Civilförsvarsförbundet och Livsmedelsverket.

---

## Funktioner

- Läser in källmaterial från `.txt`-filer
- Delar upp materialet i mindre textavsnitt (chunks)
- Skapar semantiska embeddings med `sentence-transformers`
- Söker fram relevanta textstycken baserat på användarens fråga
- Skickar fråga + relevant information till OpenAI\:s API
- Visar AI-genererat svar i terminalen med källhänvisning

---

## Installation

1. Klona projektet:

```bash
git clone https://github.com/ditt-anvandarnamn/din-beredskap.git
cd din-beredskap
```

2. Skapa och aktivera en virtuell miljö (valfritt):

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

3. Installera beroenden:

```bash
pip install -r requirements_clean.txt
```

---

## Mappstruktur

```
data/
├── MSB/
├── Livsmedelsverket/
├── chunks.json                 ← genereras från .txt-filer
└── chunk_embeddings.pkl        ← genereras från chunks.json

src/
├── app.py                      ← frågegränssnitt (terminal)
├── retriever.py                ← hämtar relevant information
├── generator.py                ← skickar fråga till OpenAI
└── chunker.py                  ← delar upp textfiler

scripts/
├── create_chunks_json.py       ← bygger chunks.json
└── precompute_embeddings.py    ← bygger chunk_embeddings.pkl
```

---

## Så här använder du projektet

```bash
python src/app.py
```

Exempel:

```
Ställ en beredskapsfråga: Hur mycket vatten behöver jag spara vid kris?

AI:s svar:
Vid en kris behöver en vuxen person vanligtvis tre till fem liter vatten per dag...
Källa: MSB, Civilförsvarsförbundet
```

---

## Kommande utveckling

- Webbaserat gränssnitt med Streamlit
- Stöd för PDF-tolkning av broschyrer
- Scenario-simulator och personlig beredskapsprofil
- Offline/PWA-version

---

## Använd teknik

- Python 3.10+
- sentence-transformers (all-MiniLM-L6-v2)
- OpenAI GPT-3.5 Turbo
- Embedding-baserad informationssökning
