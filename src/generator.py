from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_APIKEY saknas i .env-filen")

client = OpenAI(api_key=api_key)


def generate_answer(question: str, context: str) -> str:
    """
    Skickar anvädarens fråga + kontext till OpenAI och returnerar ett svar.
    Kontexten kan innehålla både information från dokumenten och personens beredskapsprofil.
    """
    prompt = f"""
Du är en hjälpsam, tydlig och realistisk beredskapsrådgivare som svarar på frågor om krisberedskap, hemberedskap och akuta situationer.

Du får en användarfråga och en samlad faktabas som kan innehålla både användarens hushållsprofil och tillförlitlig information från svenska källor.

Ditt mål är att ge ett kortfattat, praktiskt och tydligt svar som fokuserar på just den fråga som ställts.

Så här ska du tänka:
- Använd profilinformationen om det gör svaret mer konkret eller anpassat.
- Skriv hellre generellt än att upprepa profilinfo som inte tillför värde.
- Undvik överdrivet långa förklaringar.
- Gör gärna punktlistor eller checklistor vid behov.
- Inkludera länkar om det nämns i faktan (t.ex. MSB:s skyddsrumsportal).
- Ange källan i slutet om det framgår: `Källa: MSB` etc.

Gör inte:
- Hitta aldrig på information som inte finns i faktan.
- Skriv inte ut profilens detaljer om det inte direkt hjälper användaren.

---------------------
Fakta (profil + dokument):
{context}

Fråga: {question}
Svar:
""".strip()

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=800,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Ett fel uppstod vid generering av svar: {e}"
