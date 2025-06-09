import streamlit as st
from retriever import retrieve_context
from generator import generate_answer
from profile_handler import get_current_profile
import json
from pathlib import Path


# -------- GLOBALT TEMA & SIDHUVUD --------
st.set_page_config(page_title="Din Beredskap", layout="centered")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def load_css(filename):
    css_path = Path(__file__).parent / filename
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")

st.markdown(
    "<div class='title'>Din Beredskap – AI-assistent för hemberedskap och krishantering</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class='subtitle'>
        Ställ frågor om krisberedskap, naturkatastrofer, skyddsrum, checklistor och mer.
        AI:n ger konkreta råd baserade på tillförlitliga källor och din personliga beredskapsprofil.
    </div>
    <hr>
    """,
    unsafe_allow_html=True,
)


# -------- PROFILSEKTION --------

with st.expander("Visa din beredskapsprofil"):
    profile_view = get_current_profile()
    if profile_view:
        st.markdown(
            f"""
            <div class="profilrad">
                <p><strong>Hushåll:</strong> {profile_view.get("household_size")} personer</p>
                <p><strong>Varav barn:</strong> {profile_view.get("num_children")} st</p>
                <p><strong>Boendeform:</strong> {profile_view.get("housing_type")}</p>
                <p><strong>Plats:</strong> {profile_view.get("area_type")}</p>
                <p><strong>Har bil:</strong> {"Ja" if profile_view.get("has_car") else "Nej"}</p>
                <p><strong>Husdjur:</strong> {"Ja" if profile_view.get("has_pets") else "Nej"}</p>
                <p><strong>Egen brunn:</strong> {"Ja" if profile_view.get("has_private_well") else "Nej"}</p>
                <p><strong>Vedeldning:</strong> {"Ja" if profile_view.get("has_wood_heating") else "Nej"}</p>
                <p><strong>Elberoende:</strong> {"Ja" if profile_view.get("electricity_dependent") else "Nej"}</p>
                <p><strong>Ort:</strong> {profile_view.get("location") or "Ej angiven"}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Ingen profil hittades. Du kan skapa en här nedan.")


# === Redigera och spara profil ===
PROFILE_PATH = Path("data/profile.json")

with st.expander("Redigera din beredskapsprofil"):
    st.markdown("Ändra och spara din profil nedan:")
    profile_form = get_current_profile()

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
        options=["Hus", "Lägenhet"],
        index=0 if profile_form.get("housing_type") == "Hus" else 1,
    )
    area_type = st.selectbox(
        "Bor du i tätort eller på landsbygden?",
        options=["Tätort", "Landsbygd"],
        index=0 if profile_form.get("area_type") == "Tätort" else 1,
    )
    has_car = (
        st.radio(
            "Har du bil?",
            options=["Ja", "Nej"],
            index=0 if profile_form.get("has_car") else 1,
        )
        == "Ja"
    )
    has_pets = (
        st.radio(
            "Har du husdjur?",
            options=["Ja", "Nej"],
            index=0 if profile_form.get("has_pets") else 1,
        )
        == "Ja"
    )
    has_private_well = (
        st.radio(
            "Har du egen brunn?",
            options=["Ja", "Nej"],
            index=0 if profile_form.get("has_private_well") else 1,
        )
        == "Ja"
    )
    has_wood_heating = (
        st.radio(
            "Har du möjlighet till vedeldning?",
            options=["Ja", "Nej"],
            index=0 if profile_form.get("has_wood_heating") else 1,
        )
        == "Ja"
    )
    electricity_dependent = (
        st.radio(
            "Är någon elberoende (tex medicinsk utrustning)?",
            options=["Ja", "Nej"],
            index=0 if profile_form.get("electricity_dependent") else 1,
        )
        == "Ja"
    )
    location = st.text_input(
        "Ange din ort (frivilligt):", value=profile_form.get("location", "")
    )

    if st.button("Spara profil"):
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

# -------- FRÅGESTÄLLNING --------


for i, (q, a) in enumerate(st.session_state.chat_history, 1):
    st.markdown(
        f"""
    <div class="chat-block">
        <p><strong>Fråga {i}:</strong> {q}</p>
        <p><strong>AI:s svar:</strong></p>
        <div class="chat-answer">{a}</div>
    </div>
    <hr>
    """,
        unsafe_allow_html=True,
    )


with st.form("question_form", clear_on_submit=True):
    st.markdown("<h4 class='section-title'>Ställ en fråga</h4>", unsafe_allow_html=True)
    question = st.text_area("Formulera din fråga nedan:", height=100, key="question")

    submitted = st.form_submit_button("Skicka")

if submitted:
    if question.strip():
        profile_input = get_current_profile()

        with st.spinner("Letar efter relevant information..."):
            profile_context = (
                f"Användarens beredskapsprofil:\n"
                f"- Hushåll: {profile_input.get('household_size')} personer\n"
                f"- Varav barn: {profile_input.get('num_children')} st\n"
                f"- Boendeform: {profile_input.get('housing_type')}\n"
                f"- Plats: {profile_input.get('area_type')}\n"
                f"- Har bil: {'Ja' if profile_input.get('has_car') else 'Nej'}\n"
                f"- Husdjur: {'Ja' if profile_input.get('has_pets') else 'Nej'}\n"
                f"- Egen brunn: {'Ja' if profile_input.get('has_private_well') else 'Nej'}\n"
                f"- Vedeldning: {'Ja' if profile_input.get('has_wood_heating') else 'Nej'}\n"
                f"- Elberoende: {'Ja' if profile_input.get('electricity_dependent') else 'Nej'}\n"
                f"- Ort: {profile_input.get('location') or 'Ej angiven'}\n\n"
            )

            context = retrieve_context(question)
            answer = generate_answer(question, context + profile_context)

        st.session_state.chat_history.append((question, answer))
        st.rerun()

    else:
        st.warning("Du måste skriva en fråga innan du kan skicka.")
