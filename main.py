import streamlit as st
import socket
import urllib.parse
import requests
from datetime import datetime, timezone, timedelta

try:
    from zoneinfo import ZoneInfo
    ZON_MY = ZoneInfo("Asia/Kuala_Lumpur")
except:
    ZON_MY = timezone(timedelta(hours=8))

from pekerja import bos_hayden, simpan_belajar
from pengetahuan import cari_pengetahuan, HAYDEN_INFO, CARA_JAWAB

st.set_page_config(page_title="Hayden 1", page_icon="🤖")
st.title("🤖 Hayden 1")
st.caption("Tanya Hayden 1 apa-apa")

def ada_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

OFFLINE = not ada_internet()

def waktu_malaysia():
    s = datetime.now(ZON_MY)
    hari = {"Monday":"Isnin","Tuesday":"Selasa","Wednesday":"Rabu","Thursday":"Khamis","Friday":"Jumaat","Saturday":"Sabtu","Sunday":"Ahad"}
    bulan = {"January":"Januari","February":"Februari","March":"Mac","April":"April","May":"Mei","June":"Jun","July":"Julai","August":"Ogos","September":"September","October":"Oktober","November":"November","December":"Disember"}
    return f"Hari {hari.get(s.strftime('%A'))}, {s.day} {bulan.get(s.strftime('%B'))} {s.year}, pukul {s.strftime('%I:%M %p')}"

WAKTU_MY = waktu_malaysia()

# ===== LETAK PASSWORD KAU KAT SINI JE =====
API_KEY = "PASTE-PASSWORD-KAU-KAT-SINI"
NEWS_API_KEY = ""

client = None
gemini_error = ""
# AMBIL YANG ELOK JE - 2 NI JE
MODEL_FIX = ["gemini-2.5-flash", "gemini-2.0-flash"]
MODEL_CUBA = []

if API_KEY and API_KEY != "PASTE-PASSWORD-KAU-KAT-SINI" and not OFFLINE:
    try:
        from google import genai
        client = genai.Client(api_key=API_KEY)
        MODEL_CUBA = MODEL_FIX.copy()
    except Exception as e:
        gemini_error = str(e)
        MODEL_CUBA = MODEL_FIX.copy()

def tanya_gemini(prompt):
    global gemini_error
    if OFFLINE or not client:
        return None
    for nama_model in MODEL_CUBA:
        try:
            res = client.models.generate_content(model=nama_model, contents=prompt)
            if res.text:
                st.session_state["model_jaya"] = nama_model
                return res.text.strip()
        except Exception as e:
            gemini_error = str(e)
            continue
    return None

def buat_imej_url(prompt_imej):
    p = urllib.parse.quote(prompt_imej)
    return f"https://image.pollinations.ai/prompt/{p}?width=1024&height=1024&nologo=true"

if "chat" not in st.session_state:
    st.session_state.chat = []
if "guna_gemini" not in st.session_state:
    st.session_state.guna_gemini = 0
if "model_jaya" not in st.session_state:
    st.session_state.model_jaya = "-"

with st.sidebar:
    if OFFLINE:
        st.warning("📴 OFFLINE")
    else:
        st.success("🌐 ONLINE")
    st.write(WAKTU_MY)
    st.write(f"Dah guna Gemini: {st.session_state.guna_gemini} kali")
    if st.button("Padam Memory / Topik Baru"):
        st.session_state.chat = []
        st.rerun()
    st.code(gemini_error if gemini_error else "Tiada error")

for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        if m.get("type") == "image":
            st.image(m["text"], caption=m.get("caption", ""))
        else:
            st.write(m["text"])

tanya = st.chat_input("Tanya Hayden 1 apa-apa... / buat imej ...")

if tanya:
    st.session_state.chat.append({"role": "user", "text": tanya})
    with st.chat_message("user"):
        st.write(tanya)
    with st.chat_message("assistant"):
        with st.spinner("Hayden 1 tengah fikir..."):
            t_lower = tanya.lower().strip()
            kata_imej = ["buat imej", "buat gambar", "buatkan gambar", "buatkan imej", "lukis", "gambar", "buat poster", "buat logo"]
            nak_imej = any(k in t_lower for k in kata_imej)
            if nak_imej:
                if OFFLINE:
                    jawapan = "Aku offline sekarang, tak boleh buat imej."
                    st.write(jawapan)
                    st.session_state.chat.append({"role": "assistant", "text": jawapan})
                else:
                    prompt_imej = tanya
                    for k in kata_imej:
                        prompt_imej = prompt_imej.lower().replace(k, "").strip()
                    if prompt_imej == "":
                        prompt_imej = "kucing comel"
                    url_imej = buat_imej_url(prompt_imej)
                    st.write("OK, ni imej untuk: " + prompt_imej)
                    st.image(url_imej, caption=prompt_imej)
                    st.session_state.chat.append({"role": "assistant", "text": "OK, ni imej untuk: " + prompt_imej})
                    st.session_state.chat.append({"role": "assistant", "text": url_imej, "type": "image", "caption": prompt_imej})
            elif t_lower.startswith("ajar aku"):
                try:
                    bahagian = tanya.split("|", 3)
                    kod_bos = bahagian[1].strip()
                    soalan_baru = bahagian[2].strip()
                    jawapan_baru = bahagian[3].strip()
                    if kod_bos == "ADAM-BOS":
                        simpan_belajar(soalan_baru, jawapan_baru)
                        jawapan = "Ok, dah simpan."
                    else:
                        jawapan = "Eh, kod salah."
                except:
                    jawapan = "Format: ajar aku | ADAM-BOS | soalan | jawapan"
                st.write(jawapan)
                st.session_state.chat.append({"role": "assistant", "text": jawapan})
            else:
                jawapan = bos_hayden(tanya)
                if jawapan == "TAK_TAHU" and OFFLINE:
                    jawapan = "Aku offline sekarang, soalan ni aku tak belajar lagi."
                if jawapan == "TAK_TAHU":
                    cari = cari_pengetahuan(tanya, NEWS_API_KEY)
                    if cari:
                        jawapan = cari
                if jawapan == "TAK_TAHU" and client and not OFFLINE:
                    history = st.session_state.chat[-7:-1]
                    teks_history = ""
                    for h in history:
                        if h.get("type") == "image":
                            continue
                        peranan = "User" if h["role"] == "user" else "HAYDEN"
                        teks_history = teks_history + peranan + ": " + h["text"] + "\n"
                    prompt = CARA_JAWAB + "\nInfo: " + HAYDEN_INFO + "\nWAKTU SEBENAR SEKARANG DI MALAYSIA: " + WAKTU_MY + "\nPERBUALAN SEBELUM NI:\n" + teks_history + "\nSoalan terbaru: " + tanya
                    hasil = tanya_gemini(prompt)
                    if hasil:
                        jawapan = hasil
                        simpan_belajar(tanya, hasil)
                        st.session_state.guna_gemini = st.session_state.guna_gemini + 1
                    else:
                        jawapan = "GEMINI ERROR: " + gemini_error
                if jawapan == "TAK_TAHU":
                    jawapan = "Aku tak tahu lagi yang ni."
                st.write(jawapan)
                st.session_state.chat.append({"role": "assistant", "text": jawapan})
