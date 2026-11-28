import streamlit as st
from pekerja import bos_hayden, simpan_belajar
from pengetahuan import cari_pengetahuan

# --- PASTE API KEY KAU KAT SINI ---
API_KEY = "PASTE-API-KEY-KAU-KAT-SINI"

st.set_page_config(page_title="HAYDEN-FAYYAD", page_icon="🤖")
st.title("🤖 HAYDEN-FAYYAD")
st.caption("Dibuat khas untuk Muhammad Adam - Borak, Belajar, Wikipedia, Berita, Kamus, Novel & Islam")

mode = st.selectbox("HAYDEN-FAYYAD nak jadi apa hari ni?", ["🤖 HAYDEN-FAYYAD - Borak Macam Aku", "🇬🇧 Cikgu English PRO", "💻 Cikgu Coding PRO", "🕌 Ustaz PRO", "📚 Cikgu Sekolah PRO", "📚 Wikipedia", "📰 Berita", "📖 Kamus", "📕 Novel", "🕌 Islam"])

if st.button("🗑️ Padam Semua Borak"):
    st.session_state.messages = []
    st.rerun()

st.info("Tip: Taip je apa kau nak. Contoh: 'apa tu Hang Tuah', 'berita hari ni', 'maksud hello', 'cari novel Harry Potter', 'apa hukum puasa ganti'")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hai Adam! Aku HAYDEN-FAYYAD! Dah upgrade dah, lagi pandai macam Meta AI. Nak borak apa hari ni? Nak belajar coding ke English?"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

soalan = st.chat_input("Tanya HAYDEN-FAYYAD apa-apa...")

if soalan:
    st.session_state.messages.append({"role": "user", "content": soalan})
    with st.chat_message("user"):
        st.write(soalan)
    with st.chat_message("assistant"):
        with st.spinner("HAYDEN-FAYYAD tengah fikir..."):
            jawapan = bos_hayden(soalan)
            if jawapan == "TAK_TAHU":
                teks = ""
                for m in st.session_state.messages[-10:]:
                    teks += f"{m['role']}: {m['content']}\n"
                jawapan = cari_pengetahuan(soalan, API_KEY, mode, teks)
                if jawapan:
                    simpan_belajar(soalan, jawapan)
                else:
                    jawapan = "Aku tak tahu lagi yang ni."
            st.write(jawapan)
            st.session_state.messages.append({"role": "assistant", "content": jawapan})
