from openai import OpenAI
import os
from dotenv import load_dotenv

# Läser in miljövariabler från en .env-fil
load_dotenv()

# Hämtar API-nyckeln från miljövariabler
api_key = os.getenv("OPENAI_API_KEY")

# Om API-nyckeln saknas, stoppa programmet med ett tydligt felmeddelande
if not api_key:
    raise ValueError("OPENAI_APIKEY saknas i .env-filen")

# Initierar OpenAI-klienten med API-nyckeln
client = OpenAI(api_key=api_key)


def generate_answer(question: str, context: str) -> str:
    """
    Skickar användarens fråga + kontext till OpenAI och returnerar ett svar.
    Kontexten kan innehålla både information från dokumenten och personens beredskapsprofil.
    """
    # Bygger upp prompten som AI:n ska svara på – innehåller både instruktioner och innehåll
    prompt = f"""
Du är en tydlig, realistisk och hjälpsam beredskapsrådgivare som svarar på frågor om hemberedskap, samhällskriser, nödsituationer och specifika krisscenarier.

Du får en användarfråga och tillhörande faktabas som kan innehålla både personens beredskapsprofil och relevant information från tillförlitliga svenska källor (exempelvis MSB, Röda Korset, Civilförsvarsförbundet, Livsmedelsverket).

Ditt mål är att ge ett praktiskt, konkret och tydligt svar som hjälper användaren att fatta rätt beslut i en krissituation.

---

Så här ska du tänka:
- Anpassa svaret utifrån profilinfo om det gör rådet mer relevant.
- Om frågan gäller ett specifikt scenario (t.ex. strömavbrott eller översvämning), fokusera på just det.
- Använd punktlistor, checklistor eller underrubriker där det passar.
- Om det nämns i faktan, inkludera ev. länkar eller källor i slutet.
- Håll språket konkret och lättförståeligt.

Undvik:
- Att gissa eller hitta på information som inte finns i faktan.
- Att repetera profiluppgifter om de inte tillför något till svaret.

---------------------
Fakta (profil + dokument):
{context}

Fråga: {question}
Svar:
""".strip()

    try:
        # Skickar prompten till OpenAI:s API och hämtar svaret från första förslaget
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=800,
        )
        return response.choices[0].message.content.strip()

    # Returnerar ett felmeddelande om något går fel vid anropet
    except Exception as e:
        return f"Ett fel uppstod vid generering av svar: {e}"
