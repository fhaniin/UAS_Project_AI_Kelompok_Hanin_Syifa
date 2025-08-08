

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scheduler import load_imams, run_ga

st.title("🕌 Penjadwalan Imam Masjid Otomatis (Algoritma Genetika)")

st.sidebar.markdown("### Upload Data Imam (CSV)")
uploaded_file = st.sidebar.file_uploader("Upload file CSV", type="csv")

if uploaded_file:
    with open("imams.csv", "wb") as f:
        f.write(uploaded_file.read())
    st.success("File berhasil diupload!")

    imam_data = load_imams("imams.csv")

    st.markdown("### Parameter Algoritma Genetika")
    pop_size = st.slider("Ukuran Populasi", 10, 100, 30)
    n_gen = st.slider("Jumlah Generasi", 10, 200, 50)
    cross_rate = st.slider("Tingkat Crossover", 0.1, 1.0, 0.8)
    mut_rate = st.slider("Tingkat Mutasi", 0.01, 1.0, 0.05)

    if st.button("Jalankan Optimasi"):
        best, score, history, hari_list, shalat_list = run_ga(pop_size, n_gen, cross_rate, mut_rate, imam_data)
        st.success(f"Fitness Terbaik: {score}")

        jadwal = []
        for i in range(len(best)):
            hari = hari_list[i // len(shalat_list)]
            shalat = shalat_list[i % len(shalat_list)]
            jadwal.append({"Hari": hari, "Shalat": shalat, "Imam": best[i]})
        df = pd.DataFrame(jadwal)
        st.dataframe(df.pivot(index="Hari", columns="Shalat", values="Imam"))

        st.markdown("### Evolusi Fitness")
        fig, ax = plt.subplots()
        ax.plot(history, label="Fitness Terbaik")
        ax.set_xlabel("Generasi")
        ax.set_ylabel("Fitness")
        ax.legend()
        st.pyplot(fig)
