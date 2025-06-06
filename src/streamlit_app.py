import streamlit as st
from retriever import retrieve_context
from generator import generate_answer
from profile_handler import get_current_profile
import json
from pathlib import Path


# -------- GLOBALT TEMA & SIDHUVUD --------
st.set_page_config(page_title="Din Beredskap", layout="centered")

st.markdown(
    """
    <h1 style='color:#0B3C5D;'>Din Beredskap – AI-assistent</h1>
    <p style='color:#333;font-size:16px;'>
        Ställ dina frågor om krisberedskap. AI:n söker i tillförlitliga källor och ger konkreta råd baserade på din profil.
    </p>
    <hr>
""",
    unsafe_allow_html=True,
)

# -------- PROFILSEKTION --------

with st.expander("Visa din beredskapsprofil"):
    profile_view = get_current_profile()
    if profile_view:
        st.markdown(
            f"<b>Hushåll:</b> {profile_view.get('household_size')} personer",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<b>Varav barn:</b> {profile_view.get('num_children')} st",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<b>Boendeform:</b> {profile_view.get('housing_type')}",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<b>Plats:</b> {profile_view.get('area_type')}", unsafe_allow_html=True
        )
        st.markdown(
            f"<b>Har bil:</b> {'Ja' if profile_view.get('has_car') else 'Nej'}",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<b>Husdjur:</b> {'Ja' if profile_view.get('has_pets') else 'Nej'}",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<b>Egen brunn:</b> {'Ja' if profile_view.get('has_private_well') else 'Nej'}",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<b>Vedeldning:</b> {'Ja' if profile_view.get('has_wood_heating') else 'Nej'}",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<b>Elberoende:</b> {'Ja' if profile_view.get('electricity_dependent') else 'Nej'}",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<b>Ort:</b> {profile_view.get('location') or 'Ej angiven'}",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
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
    has_car = st.checkbox("Har du bil?", value=profile_form.get("has_car", False))
    has_pets = st.checkbox("Har du husdjur?", value=profile_form.get("has_pets", False))
    has_private_well = st.checkbox(
        "Har du egen brunn?", value=profile_form.get("has_private_well", False)
    )
    has_wood_heating = st.checkbox(
        "Har du möjlighet till vedeldning?",
        value=profile_form.get("has_wood_heating", False),
    )
    electricity_dependent = st.checkbox(
        "Är någon elberoende (t ex medicinsk utrustning)?",
        value=profile_form.get("electricity_dependent", False),
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
st.subheader("Ställ en fråga")

question = st.text_area("Formulera din fråga nedan:", height=100)

if st.button("Skicka"):
    profile_input = get_current_profile()
    if question.strip():
        with st.spinner("Letar efter relevant information..."):
            profile_context = (
                (
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
                if profile_input
                else ""
            )

            context = retrieve_context(question)
            full_context = profile_context + context
            answer = generate_answer(question, full_context)

        st.success("AI:s svar:")
        st.markdown(answer)
    else:
        st.warning("Du måste skriva en fråga innan du kan skicka.")
