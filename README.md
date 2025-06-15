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

### Terminalversion:

```bash
python src/app.py
```

### Streamlit-version (webbgränssnitt):

```bash
streamlit run src/streamlit_main.py
```

---

## 📁 Projektstruktur

```
data/
├── chunks.json # Textbitar från dokumenten
├── chunk_embeddings.pkl # Embeddings för retrieval (pickle-format)
├── profile.json # Användarens hushållsprofil (JSON format)
├── MSB/, Röda korset/, ... # Råmaterial från olika svenska kriskällor

scripts/
├── create_chunks_json.py # Delar upp texter i mindre chunkar
└── precompute_embeddings.py # Skapar embeddings för chunks och sparar dom

src/
├── app.py # Terminalversionens startfil
├── chunker.py # Funktion för att dela upp texter
├── generator.py # Skickar prompt + kontext till OpenAI
├── profile_handler.py # Läser, sparar och visar hushållsprofil
├── retriever.py # Hämtar relevanta chunks mha embeddings
├── streamlit_main.py # Webappens startfil (STreamlit-gränssnitt)
└── style.css # CSS för Streamlit-utseende

README.md # Projektbeskrivning och instruktioner
requirements.txt # Lista över beroenden
.env # Dold, innehåller API-nyckel
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

- Byt ut TF-IDF eller likhetsmått mot FAISS/Chroma för snabbare och smartare retrieval
- DSPy för utvärdering och prompt-tuning
- Fler krisscenarier och mer variation i svaren
- Export av profil och frågor/svar
- UI med betygssättning av svar
- Offline-läge med lokal profil och cache av scenariodata för mobilanvändning (PWA eller native wrapper)

---

## 🧾 Om projektet

Detta projekt är en MVP skapad inom kursen "Applicerad AI", för att visa hur LLM-teknik kan användas praktiskt inom krisberedskap.
