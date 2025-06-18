import streamlit as st
from recommend import recommend

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommender System")

movie_name = st.text_input("Enter a movie you like:")

if st.button("Recommend"):
    names, posters, summaries, reasons = recommend(movie_name)

    if not names:
        st.error("❌ Movie not found. Please enter an exact title from the dataset.")
    else:
        for i in range(len(names)):
            with st.container():
                cols = st.columns([1, 2])
                
                with cols[0]:
                    st.image(posters[i], use_container_width=True)

                with cols[1]:
                    st.subheader(f"🎥 {names[i]}")
                    st.markdown(f"**Summary:** {summaries[i]}")
                    st.markdown(f"<span style='color:#888; font-style: italic;'>🔍 {reasons[i]}</span>", unsafe_allow_html=True)

                st.markdown("---")
