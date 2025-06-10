import streamlit as st
import time

def breathing_exercise():
    st.title("🧘 Breathing Coach")
    st.write("Follow the animation to breathe.")
    phases = [("Inhale", 4), ("Hold", 4), ("Exhale", 4)]
    for _ in range(3):
        for phase, secs in phases:
            st.subheader(phase)
            for i in range(secs, 0, -1):
                st.write(f"{i} seconds...")
                time.sleep(1)
