import streamlit as st
from retriever import retrieve_context
from generator import generate_answer
from profile_handler import load_profile

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
profile = load_profile()

with st.expander("Visa din beredskapsprofil"):
    if profile:
        st.markdown(
            "<div style='background-color:#f4f4f4;padding:15px;border-radius:5px;'>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<b>Hushåll:</b> {profile.get('household_size')}", unsafe_allow_html=True
        )
        st.markdown(
            f"<b>Boendeform:</b> {profile.get('housing_type')}", unsafe_allow_html=True
        )

        husdjur = "Ja" if profile.get("has_pets") else "Nej"
        st.markdown(f"<b>Husdjur:</b> {husdjur}", unsafe_allow_html=True)

        elberoende = "Ja" if profile.get("electricity_dependent") else "Nej"
        st.markdown(f"<b>Elberoende:</b> {elberoende}", unsafe_allow_html=True)

        ort = profile.get("location") or "Ej angiven"
        st.markdown(f"<b>Ort:</b> {ort}", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Ingen profil hittades. Skapa en i terminalversionen.")

# -------- FRÅGESTÄLLNING --------
st.subheader("Ställ en fråga")

question = st.text_area("Formulera din fråga nedan:", height=100)

if st.button("Skicka"):
    if question.strip():
        with st.spinner("Letar efter relevant information..."):
            profile_context = (
                (
                    f"Användarens beredskapsprofil:\n"
                    f"- Hushåll: {profile.get('household_size')}\n"
                    f"- Boendeform: {profile.get('housing_type')}\n"
                    f"- Husdjur: {profile.get('has_pets')}\n"
                    f"- Elberoende: {profile.get('electricity_dependent')}\n"
                    f"- Ort: {profile.get('location')}\n\n"
                )
                if profile
                else ""
            )

            context = retrieve_context(question)
            full_context = profile_context + context
            answer = generate_answer(question, full_context)

        st.success("AI:s svar:")
        st.markdown(answer)
    else:
        st.warning("Du måste skriva en fråga innan du kan skicka.")
