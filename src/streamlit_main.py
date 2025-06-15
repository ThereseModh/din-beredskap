import streamlit as st
from retriever import retrieve_context
from generator import generate_answer
from profile_handler import get_current_profile
import json
from pathlib import Path

# Konfigurerar sidlayout och titel
st.set_page_config(page_title="Din Beredskap", layout="wide")

# Laddar in anpassad CSS
with open("src/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initiera visningsläge
if "view" not in st.session_state:
    st.session_state.view = "question"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidhuvud och introduktion
st.markdown(
    """
<div style='background-color:#0B3C5D;padding:2.5rem 1rem;border-radius:18px;margin-bottom:2rem;text-align:center;'>
    <h1 style='color:#fff;font-size:42px;font-weight:700;margin-bottom:0.3em;font-family:Segoe UI, sans-serif;'>Din Beredskap 🧰</h1>
    <p style='color:#f0f0f0;font-size:17px;margin-bottom:0.3em;font-family:Segoe UI, sans-serif;'>
        En AI-baserad rådgivare för hemberedskap och krishantering
    </p>
    <p style='color:#cfd6df;font-size:15.5px;max-width:700px;margin:auto;font-family:Segoe UI, sans-serif;'>
        Ställ frågor om krisberedskap, naturkatastrofer, skyddsrum, checklistor och mer.<br>
        AI:n ger konkreta råd baserade på tillförlitliga källor och din personliga beredskapsprofil.
    </p>
</div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='menu-buttons'>", unsafe_allow_html=True)
# Skapar en ensam kolumn för att centrera knappen horisontellt
(col1,) = st.columns([1])

with col1:
    if st.button("🛠️ Skapa/Redigera profil"):
        st.session_state.view = "profile"


st.markdown("</div>", unsafe_allow_html=True)

# === HUVUDVY: Användaren kan ställa en fråga till AI:n och se scenarier ===
if st.session_state.view == "question":
    col1, col2 = st.columns([1, 2])

    with col1:
        with st.expander("\U0001f464 Din beredskapsprofil"):
            profile = get_current_profile()
            if profile:
                st.markdown(
                    """
                    <div class="profilrad">
                        <p><strong>Hushåll:</strong> {} personer</p>
                        <p><strong>Barn:</strong> {} st</p>
                        <p><strong>Boendeform:</strong> {}</p>
                        <p><strong>Plats:</strong> {}</p>
                        <p><strong>Bil:</strong> {}</p>
                        <p><strong>Husdjur:</strong> {}</p>
                        <p><strong>Brunn:</strong> {}</p>
                        <p><strong>Ved:</strong> {}</p>
                        <p><strong>Elberoende:</strong> {}</p>
                        <p><strong>Ort:</strong> {}</p>
                    </div>
                """.format(
                        profile.get("household_size"),
                        profile.get("num_children"),
                        profile.get("housing_type"),
                        profile.get("area_type"),
                        "Ja" if profile.get("has_car") else "Nej",
                        "Ja" if profile.get("has_pets") else "Nej",
                        "Ja" if profile.get("has_private_well") else "Nej",
                        "Ja" if profile.get("has_wood_heating") else "Nej",
                        "Ja" if profile.get("electricity_dependent") else "Nej",
                        profile.get("location") or "Ej angiven",
                    ),
                    unsafe_allow_html=True,
                )
            else:
                st.info("Ingen profil hittades. Gå till Redigera profil.")

    with col2:
        st.markdown(
            "<div class='section-title'>Ställ din fråga</div>", unsafe_allow_html=True
        )
        with st.form("question_form", clear_on_submit=True):
            question = st.text_area("Vad vill du veta?", height=100)
            submitted = st.form_submit_button("Skicka fråga")

        # Om en fråga har skickats in, generera svar baserat på användarens profil + dokumentkontekst
        if submitted and question.strip():
            profile_input = get_current_profile()
            with st.spinner("AI:n analyserar frågan..."):
                profile_context = """Användarens profil:
                - Hushåll: {}
                - Barn: {}
                - Boendeform: {}
                - Plats: {}
                - Bil: {}
                - Husdjur: {}
                - Brunn: {}
                - Ved: {}
                - Elberoende: {}
                - Ort: {}""".format(
                    profile_input.get("household_size"),
                    profile_input.get("num_children"),
                    profile_input.get("housing_type"),
                    profile_input.get("area_type"),
                    "Ja" if profile_input.get("has_car") else "Nej",
                    "Ja" if profile_input.get("has_pets") else "Nej",
                    "Ja" if profile_input.get("has_private_well") else "Nej",
                    "Ja" if profile_input.get("has_wood_heating") else "Nej",
                    "Ja" if profile_input.get("electricity_dependent") else "Nej",
                    profile_input.get("location") or "Ej angiven",
                )
                context = retrieve_context(question)
                answer = generate_answer(question, context + profile_context)
            st.session_state.chat_history.append((question, answer))
            st.rerun()

        st.markdown(
            "<div class='scenario-heading'>Krisscenarier</div>", unsafe_allow_html=True
        )
        st.markdown("<div class='scenario-grid'>", unsafe_allow_html=True)

        scenarios = {
            "\U0001f50c Strömavbrott": "Hur förbereder jag mig för ett längre strömavbrott?",
            "\U0001f30a Översvämning": "Vad bör jag tänka på vid översvämning?",
            "\U0001f525 Brand": "Hur förbereder jag mig för en brand i hemmet?",
            "\U0001f96b Matbrist": "Hur kan jag förbereda mig för brist på mat?",
            "\U0001f4a7 Vattenbrist": "Vad gör jag om dricksvattnet slutar fungera?",
            "\u26a0\ufe0f Krigshot": "Vad behöver jag vid krigshot eller allvarlig samhällskris?",
            "\u2744\ufe0f Extrem kyla": "Hur håller jag mig varm utan el under vintern?",
            "\U0001f392 Evakuering": "Vad bör jag packa om jag måste evakuera?",
        }

        # Skapar knappar för fördefinierade krisscenarier med automatiska frågor
        for i, (label, prompt) in enumerate(scenarios.items()):
            if st.button(label, key=f"scenario_{i}"):
                profile_input = get_current_profile()
                with st.spinner("AI:n sammanställer ett svar..."):
                    context = retrieve_context(prompt)
                    profile_context = json.dumps(
                        profile_input, indent=2, ensure_ascii=False
                    )
                    answer = generate_answer(prompt, context + profile_context)
                st.session_state.chat_history.append((prompt, answer))
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.chat_history:
        st.markdown(
            "<div class='section-title'>Frågeflöde</div>", unsafe_allow_html=True
        )
        for q, a in reversed(st.session_state.chat_history):
            st.markdown(
                f"""
                <div class="chat-block">
                    <p><strong>Du:</strong> {q}</p>
                    <div class="chat-answer">{a}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# === PROFILVY: Användaren kan skapa eller redigera sin beredskapsprofil ===
elif st.session_state.view == "profile":
    PROFILE_PATH = Path("data/profile.json")

    # Tillbaka-knapp
    if st.button("🔙 Tillbaka"):
        st.session_state.view = "question"
        st.rerun()

    st.markdown(
        "<h4 class='section-title'>Redigera din beredskapsprofil</h4>",
        unsafe_allow_html=True,
    )
    profile_form = get_current_profile()

    with st.form("profile_form"):
        household_size = st.number_input(
            "Hur många personer finns i hushållet?",
            min_value=1,
            step=1,
            value=profile_form.get("household_size", 1),
        )
        num_children = st.number_input(
            "Hur många av dessa är barn?",
            min_value=0,
            max_value=household_size,
            step=1,
            value=profile_form.get("num_children", 0),
        )
        housing_type = st.selectbox(
            "Bor du i hus eller lägenhet?",
            ["Hus", "Lägenhet"],
            index=0 if profile_form.get("housing_type") == "Hus" else 1,
        )
        area_type = st.selectbox(
            "Bor du i tätort eller på landsbygden?",
            ["Tätort", "Landsbygd"],
            index=0 if profile_form.get("area_type") == "Tätort" else 1,
        )
        has_car = (
            st.radio(
                "Har du bil?",
                ["Ja", "Nej"],
                index=0 if profile_form.get("has_car") else 1,
            )
            == "Ja"
        )
        has_pets = (
            st.radio(
                "Har du husdjur?",
                ["Ja", "Nej"],
                index=0 if profile_form.get("has_pets") else 1,
            )
            == "Ja"
        )
        has_private_well = (
            st.radio(
                "Har du egen brunn?",
                ["Ja", "Nej"],
                index=0 if profile_form.get("has_private_well") else 1,
            )
            == "Ja"
        )
        has_wood_heating = (
            st.radio(
                "Har du möjlighet till vedeldning?",
                ["Ja", "Nej"],
                index=0 if profile_form.get("has_wood_heating") else 1,
            )
            == "Ja"
        )
        electricity_dependent = (
            st.radio(
                "Är någon elberoende?",
                ["Ja", "Nej"],
                index=0 if profile_form.get("electricity_dependent") else 1,
            )
            == "Ja"
        )
        location = st.text_input(
            "Ange din ort (frivilligt):", value=profile_form.get("location", "")
        )

        if st.form_submit_button("Spara profil"):
            new_profile = {
                "household_size": household_size,
                "num_children": num_children,
                "housing_type": housing_type,
                "area_type": area_type,
                "has_car": has_car,
                "has_pets": has_pets,
                "has_private_well": has_private_well,
                "has_wood_heating": has_wood_heating,
                "electricity_dependent": electricity_dependent,
                "location": location,
            }
            PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
            with PROFILE_PATH.open("w", encoding="utf-8") as f:
                json.dump(new_profile, f, indent=2, ensure_ascii=False)
            st.success("Profilen har sparats!")
            st.session_state.view = "question"
            st.rerun()
