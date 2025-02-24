import streamlit as st
import pandas as pd
from simulation import MCS # Import der Simulation

from PIL import Image
import numpy as np
import time
import base64

# Seite auf wide setzen
st.set_page_config(layout="wide")

# ---------------------------------
# Daten laden
# ---------------------------------
prob_df = pd.read_csv("Data/Prob_df.csv")


infos = pd.read_csv("Data/Player_infos.csv")

Surfaces = ["Hard", "Clay", "Grass"]
TournamentType = ["GrandSlam", "Masters", "Others"]

# ------------------------------------
# Globales Styling (Schwarz/Weiß)
# ------------------------------------
global_styles = """
<style>
/* Seitenhintergrund in Weiß */
[data-testid="stAppViewContainer"] {
    background-color: #FFFFFF;
}
/* Sidebar-Hintergrund in Weiß */
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
}
/* Überschriften in Schwarz */
h1, h2, h3, h4, h5, h6 {
    color: #000000;
}
/* Standard-Text in Schwarz */
body, p, div, label, span {
    color: #000000;
    margin: 0;
    padding: 0;
}
/* Button anpassen: heller Hintergrund, weiße Schrift */
div.stButton > button {
    background-color: #B9BBB6; 
    color: #FFFFFF;
    font-weight: bold;
    border: none;
    padding: 10px 20px;
}
div.stButton > button:hover {
    background-color: #4682B4;
}
</style>
"""
st.markdown(global_styles, unsafe_allow_html=True)

# ------------------------------------
# Spezifisches Styling für Selectboxen
# ------------------------------------
selectbox_styles = """
<style>
[data-baseweb="select"] div[role="combobox"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #000000 !important;
}
[data-baseweb="menu"] {
    background-color: #FFFFFF !important;
}
[data-baseweb="menu"] [role="option"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}
</style>
"""
st.markdown(selectbox_styles, unsafe_allow_html=True)

# ------------------------------------
# Header: Bild als Hintergrund
# ------------------------------------
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")

image_path = "Images/header.jpg"
img_base64 = get_base64_of_bin_file(image_path)

header_html = f"""
<div style="
    width: 100%;
    height: 300px; 
    background-image: url('data:image/jpeg;base64,{img_base64}');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
">
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# ------------------------------------
# Titel (zentriert)
# ------------------------------------
st.markdown("<h1 style='text-align: center;'>Tennis Match Simulation</h1>", unsafe_allow_html=True)

# ------------------------------------
# Layout: Links Eingaben, Rechts Spielerinfos + Ergebnis
# ------------------------------------
col_left, col_right = st.columns([1, 2])

# Linke Spalte: Eingaben
with col_left:
    st.subheader("Please select:")

    # Liste der Spielernamen
    player_names = list(prob_df["Player_Name"].unique())

    # Spieler 1
    player1_options = ["Select Player 1"] + player_names
    Player1 = st.selectbox("", options=player1_options, key="p1", label_visibility="collapsed")

    # Spieler 2
    player2_options = ["Select Player 2"] + player_names
    Player2 = st.selectbox("", options=player2_options, key="p2", label_visibility="collapsed")

    # Surface
    surface_options = ["Select Surface"] + Surfaces
    Surface = st.selectbox("", options=surface_options, key="surf", label_visibility="collapsed")

    # Tournament
    tournament_options = ["Select Tournament"] + TournamentType
    Tournament = st.selectbox("", options=tournament_options, key="tourn", label_visibility="collapsed")

    # Simulationsknopf
    simulate_button = st.button("Start the simulation")

# --- Rechte Spalte: Aufteilung in 3 Spalten (links: Spieler 1, Mitte: Matchergebnis, rechts: Spieler 2) ---
with col_right:
    col_left_r, col_center_r, col_right_r = st.columns([1, 1, 1])

    # Helper: Use the same function to embed images as Base64 in HTML
    def embed_image_html(image_path, width):
        img_b64 = get_base64_of_bin_file(image_path)
        return f"<img src='data:image/png;base64,{img_b64}' width='{width}px'>"

    # Spieler 1: Bild, Infos und Platzhalter für den Pokal
    with col_left_r:
        if Player1 != "Select Player 1":
            p1_data = infos[infos["Player_Name"] == Player1].iloc[0]
            # Build HTML with centered image and info
            player1_image_path = f"Images/Players/{Player1}.png"
            player1_html = f"""
            <div style="text-align: center;">
                {embed_image_html(player1_image_path, 150)}
                <p style="text-align: center; margin: 0; padding: 0;">
                    <strong>{Player1}</strong><br>
                    Age: {p1_data.get('Age', 'N/A')}<br>
                    Pro Since: {p1_data.get('Pro_since', 'N/A')}<br>
                    ATP Rank: {p1_data.get('ATPRank', 'N/A')}<br>
                    Elo Rank: {p1_data.get('EloRank', 'N/A')}<br>
                    Elo Points: {p1_data.get('EloPoints', 'N/A')}
                </p>
            </div>
            """
            st.markdown(player1_html, unsafe_allow_html=True)
        else:
            st.info("Please select Player 1")
        trophy_placeholder1 = st.empty()  # For later trophy

    # Mittlere Spalte: Platzhalter für das Matchergebnis
    with col_center_r:
        # Adjust vertical space so the result aligns with trophy images
        st.markdown("<div style='height: 300px;'></div>", unsafe_allow_html=True)
        match_result_placeholder = st.empty()

    # Spieler 2: Bild, Infos und Platzhalter für den Pokal
    with col_right_r:
        if Player2 != "Select Player 2":
            p2_data = infos[infos["Player_Name"] == Player2].iloc[0]
            player2_image_path = f"Images/Players/{Player2}.png"
            player2_html = f"""
            <div style="text-align: center;">
                {embed_image_html(player2_image_path, 150)}
                <p style="text-align: center; margin: 0; padding: 0;">
                    <strong>{Player2}</strong><br>
                    Age: {p2_data.get('Age', 'N/A')}<br>
                    Pro Since: {p2_data.get('Pro_since', 'N/A')}<br>
                    ATP Rank: {p2_data.get('ATPRank', 'N/A')}<br>
                    Elo Rank: {p2_data.get('EloRank', 'N/A')}<br>
                    Elo Points: {p2_data.get('EloPoints', 'N/A')}
                </p>
            </div>
            """
            st.markdown(player2_html, unsafe_allow_html=True)
        else:
            st.info("Please select Player 2")
        trophy_placeholder2 = st.empty()

# --------------------------------
# Simulation: Wird beim Klick auf den Button in der linken Spalte gestartet
# --------------------------------
if simulate_button:
    with st.spinner('Quiet please...'):
        # Validierung
        if Player1 == "Select Player 1" or Player2 == "Select Player 2":
            st.error("Please select both players before starting the simulation.")
        elif Surface == "Select Surface" or Tournament == "Select Tournament":
            st.error("Please select surface and tournament type.")
        elif Player1 == Player2:
            st.error("Please choose two different players.")
        else:
            # Berechnung der Wahrscheinlichkeit&MCS
            match_result = MCS(Player1,Player2,Surface,Tournament)
            # Aktualisierung des zentralen Platzhalters in der rechten Spalte (mittlere Spalte)
            match_result_placeholder.markdown(f"""
                <div style='text-align:center;margin-top:30px;'>
                    <h3>Match Result</h3>
                    <p><strong>Set Distribution:</strong> {match_result[1][0]} : {match_result[1][1]}</p>
                    <p><strong>The winner is:</strong> {match_result[0]} 🎉</p>
                </div>
            """, unsafe_allow_html=True)

        # Trophy (Pokal) zentriert im Gewinnerbereich anzeigen
            trophy_path = "Images/Pokal.jpg"
            if match_result[0] == Player1:
                trophy_placeholder1.markdown(f"""
                    <div style="text-align: center;">
                        <img src="data:image/jpeg;base64,{get_base64_of_bin_file(trophy_path)}" width="150">
                    </div>
                """, unsafe_allow_html=True)
            elif match_result[0] == Player2:
                trophy_placeholder2.markdown(f"""
                    <div style="text-align: center;">
                        <img src="data:image/jpeg;base64,{get_base64_of_bin_file(trophy_path)}" width="150">
                    </div>
                """, unsafe_allow_html=True)