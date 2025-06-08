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
Du är en hjälpsam, tydlig och realistisk beredskapsrådgivare som hjälper människor att förbereda sig för samhällskriser och akuta situationer.

Du får nu en fråga från en användare samt fakta om deras personliga förutsättningar och hushållsprofil. 
Svara på frågan baserat på både användarens profil och de bifogade informationskällorna. Anpassa dina råd till följande faktorer om de finns tillgängliga:

- Hushållets storlek och antal barn
- Boendeform (hus/lägenhet)
- Plats: tätort eller landsbygd
- Tillgång till bil, husdjur, egen brunn eller vedeldning
- Elberoende (t.ex. medicinsk utrustning)
- Ort (försök anpassa till platsen om relevant – t.ex. landsbygd i Dalsland)

Viktigt:
- Om någon information saknas (t.ex. om profilen inte är angiven), ge istället generella men praktiska råd.
- Hitta aldrig på fakta. Om något inte finns i källorna, säg det ärligt.
- Använd punktlistor, rubriker eller checklistor där det passar.
- Svara med ett varmt, tydligt och tillförlitligt språk.
- Om det framgår vilken källa något kommer från (t.ex. MSB, Röda Korset), ange det i slutet med: "Källa: ___".

---------------------
Fakta att använda (användarprofil + relevant information från källor):
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
