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
Du är en hjälpsam och tydlig beredskapsrådgivare som hjälper människor att förbereda sig för samhällskriser och akuta situationer. 
Besvara frågan nedan utifrån följande informationskällor (t.ex. MSB, Röda Korset, Civilförsvarsförbundet, Livsmedelsverket).

Om svaret inte finns i informationen, säg ärligt att du inte har ett svar just nu istället för att gissa.

Svara i ett vänligt och lättförståeligt språk. Ge gärna konkreta tips, checklistor eller råd.
Använd punktform eller underrubriker där det passar.
Om det framgår av texten vilken källa informationen kommer från (t.ex. MSB, Röda Korset eller Civilförsvarsförbundet), ange den efter svaret med: "Källa: ___".

---------------------
Fakta att använda:
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
