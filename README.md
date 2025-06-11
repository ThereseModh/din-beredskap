# Din Beredskap – AI-baserad rådgivare för hemberedskap och krishantering

**Din Beredskap** är en AI-assistent som hjälper användare att få konkreta råd vid samhällskriser, personligt beredskap och akuta situationer. Svaren anpassas efter användarens hushållsprofil och baseras på tillförlitlig information från svenska myndigheter och organisationer.

Projektet använder RAG (Retrieval-Augmented Generation), där relevanta textavsnitt hämtas från dokument och används som kontext för att generera AI-svar via OpenAI:s API.

---

## Funktioner

- Kontextuell retrieval med TF-IDF
- Svar baserade på svenska krisinformationskällor
- Anpassade svar utifrån hushållets storlek, boendeform, barn etc.
- Användaren kan se och redigera sin beredskapsprofil
- Scenariobaserade frågor (t.ex. elavbrott, matbrist, brand)
- Enkelt och tydligt gränssnitt med Streamlit

---

## ⚙️ Så här kör du projektet

1. **Installera beroenden**

   ```bash
   pip install -r requirements.txt
   ```

2. **Lägg till din OpenAI-nyckel**

   Skapa en `.env`-fil i projektroten med innehållet:

   ```env
   OPENAI_API_KEY=din-nyckel-här
   ```

3. **Starta appen**

   ```bash
   streamlit run src/app.py
   ```

---

## 📁 Projektstruktur

```
data/
├── chunks.json
├── chunk_embeddings.pkl
├── profile.json
├── MSB/, Röda korset/, ...

scripts/
├── create_chunks_json.py
└── precompute_embeddings.py

src/
├── app.py
├── chunker.py
├── generator.py
├── profile_handler.py
├── retriever.py
├── streamlit_new.py
└── style_new.css

README.md
requirements.txt
.env
```

---

## 📚 Informationskällor

- MSB – Myndigheten för samhällsskydd och beredskap
- Krisinformation.se
- Röda Korset
- Livsmedelsverket
- Civilförsvarsförbundet

---

## 🔍 Förslag på vidareutveckling

- Bättre retrieval (FAISS, Chroma)
- DSPy för utvärdering och prompt-tuning
- Fler krisscenarier
- Export av profil och frågor/svar
- UI med betygssättning av svar
- Offline-läge med lokal profil och cache av scenariodata för mobilanvändning (PWA eller native wrapper)

---

## 🧾 Om projektet

Detta projekt är en MVP skapad inom kursen "Applicerad AI", för att visa hur LLM-teknik kan användas praktiskt inom krisberedskap.
