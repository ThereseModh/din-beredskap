import streamlit as st
from retriever import retrieve_context
from generator import generate_answer
from profile_handler import get_current_profile
import json
from pathlib import Path

# Konfigurerar sidlayout och titel
st.set_page_config(page_title="Din Beredskap", layout="wide")


# Laddar in anpassad CSS
def load_css(filename):
    css_path = Path(__file__).parent / filename
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style_new.css")

# Sidhuvud och introduktion
st.markdown(
    """
<div style='background-color:#184059;padding:1.5rem 1rem;border-radius:10px;margin-bottom:2rem;'>
    <h1 style='color:#fff;text-align:center;margin-bottom:0.2em;'>Din Beredskap 🧰</h1>
    <p style='color:#ddd;text-align:center;font-size:17px;'>
        En AI-baserad rådgivare för hemberedskap och krishantering
    </p>
    <p style='color:#cfd6df;text-align:center;font-size:15.5px;max-width:700px;margin:auto;'>
        Ställ frågor om krisberedskap, naturkatastrofer, skyddsrum, checklistor och mer. <br>
        AI:n ger konkreta råd baserade på tillförlitliga källor och din personliga beredskapsprofil.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# Skapar flikar: Fråga och Profil
tabs = st.tabs(["\U0001f4ac Ställ en fråga", "\U0001f4cb Skapa/redigera profil"])


# Flik 1: Frågeformulär och AI-svar
with tabs[0]:
    col1, col2 = st.columns([1, 2])

    # Visa användarens profil i vänsterkolumn
    with col1:
        with st.expander("\U0001f464 Visa din beredskapsprofil"):
            profile_view = get_current_profile()
            if profile_view:
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
                        profile_view.get("household_size"),
                        profile_view.get("num_children"),
                        profile_view.get("housing_type"),
                        profile_view.get("area_type"),
                        "Ja" if profile_view.get("has_car") else "Nej",
                        "Ja" if profile_view.get("has_pets") else "Nej",
                        "Ja" if profile_view.get("has_private_well") else "Nej",
                        "Ja" if profile_view.get("has_wood_heating") else "Nej",
                        "Ja" if profile_view.get("electricity_dependent") else "Nej",
                        profile_view.get("location") or "Ej angiven",
                    ),
                    unsafe_allow_html=True,
                )
            else:
                st.info("Ingen profil hittades. Du kan skapa en under fliken 'Profil'.")

    # Formulär för att ställa frågor
    with col2:
        st.markdown(
            "<h4 class='section-title'>Ställ en fråga till AI:n</h4>",
            unsafe_allow_html=True,
        )
        with st.form("question_form", clear_on_submit=True):
            question = st.text_area("Vad vill du veta?", height=100)
            submitted = st.form_submit_button("Skicka fråga")

        if submitted and question.strip():
            profile_input = get_current_profile()
            with st.spinner("Letar efter information..."):
                profile_context = f"""
                Användarens beredskapsprofil:
                - Hushåll: {profile_input.get("household_size")} personer
                - Barn: {profile_input.get("num_children")} st
                - Boendeform: {profile_input.get("housing_type")}
                - Plats: {profile_input.get("area_type")}
                - Bil: {"Ja" if profile_input.get("has_car") else "Nej"}
                - Husdjur: {"Ja" if profile_input.get("has_pets") else "Nej"}
                - Brunn: {"Ja" if profile_input.get("has_private_well") else "Nej"}
                - Ved: {"Ja" if profile_input.get("has_wood_heating") else "Nej"}
                - Elberoende: {"Ja" if profile_input.get("electricity_dependent") else "Nej"}
                - Ort: {profile_input.get("location") or "Ej angiven"}
                """
                context = retrieve_context(question)
                answer = generate_answer(question, context + profile_context)
            st.session_state.chat_history.append((question, answer))
            st.rerun()

        # Visa snabbval för scenarier
        st.markdown(
            "<hr style='margin-top:2.5rem;margin-bottom:1rem;'>", unsafe_allow_html=True
        )

        st.markdown(
            "<div class='scenario-heading'>Krisscenarier</div>", unsafe_allow_html=True
        )
        st.markdown(
            "<div class='scenario-subtext'>Klicka på ett scenario för att få AI-genererade, personligt anpassade råd.</div>",
            unsafe_allow_html=True,
        )

        scenario_prompts = {
            "🔌 Strömavbrott": "Hur förbereder jag mig för ett längre strömavbrott?",
            "🌊 Översvämning": "Vad bör jag tänka på vid översvämning?",
            "🔥 Brand": "Hur förbereder jag mig för en brand i hemmet?",
            "🥫 Matbrist": "Hur kan jag förbereda mig för brist på mat?",
            "💧 Vattenbrist": "Vad gör jag om dricksvattnet slutar fungera?",
            "⚠️ Krigshot": "Vad behöver jag vid krigshot eller allvarlig samhällskris?",
            "❄️ Extrem kyla": "Hur håller jag mig varm utan el under vintern?",
            "🎒 Evakuering": "Vad bör jag packa om jag måste evakuera?",
        }

        cols = st.columns(2)
        for i, (label, prompt) in enumerate(scenario_prompts.items()):
            with cols[i % 2]:
                st.markdown('<div class="scenario-button">', unsafe_allow_html=True)
                if st.button(label, key=f"scenario_{i}"):
                    profile_input = get_current_profile()
                    with st.spinner("AI:n sammanställer ett svar..."):
                        profile_context = (
                            "Användarens beredskapsprofil:\n"
                            + json.dumps(profile_input, indent=2, ensure_ascii=False)
                        )
                        context = retrieve_context(prompt)
                        answer = generate_answer(prompt, context + profile_context)
                    st.session_state.chat_history.append((prompt, answer))
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    # Visa historik av frågor och svar
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.session_state.chat_history:
        st.markdown(
            "<h4 class='section-title'>Ditt frågeflöde</h4>", unsafe_allow_html=True
        )

        for i, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
            st.markdown(
                f"""
            <div class="chat-block">
                <p><strong>Du:</strong> {q}</p>
                <p><strong>AI:</strong></p>
                <div class="chat-answer">{a}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )


# Flik 2: Redigera profil
with tabs[1]:
    PROFILE_PATH = Path("data/profile.json")
    st.markdown(
        "<h4 class='section-title'>Redigera din beredskapsprofil</h4>",
        unsafe_allow_html=True,
    )
    profile_form = get_current_profile()

    with st.form("profile_form"):
        # Formulärfält för varje profiluppgift
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

        # När användaren sparar formuläret
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
            st.rerun()
