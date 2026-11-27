import streamlit as st
import socket
import urllib.parse
import json
import os
from datetime import datetime, timezone, timedelta

try:
    from zoneinfo import ZoneInfo
    ZON_MY = ZoneInfo("Asia/Kuala_Lumpur")
except:
    ZON_MY = timezone(timedelta(hours=8))

st.set_page_config(page_title="Hayden 1", page_icon="🤖")
st.title("🤖 Hayden 1")
st.caption("Tanya Hayden 1 apa-apa")

# ===== SEMUA FUNGSI PEKERJA LETAK DALAM NI JE, TAK PAYAH FILE LAIN =====
FAIL_BELAJAR = "belajar.json"

def load_belajar():
    if os.path.exists(FAIL_BELAJAR):
        try:
            with open(FAIL_BELAJAR, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def simpan_belajar(soalan, jawapan):
    data = load_belajar()
    data[soalan.lower().strip()] = jawapan
    try:
        with open(FAIL_BELAJAR, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def bos_hayden(tanya):
    n = tanya.lower().strip()
    if n.startswith("we "):
        n = n[3:].strip()
    if n.startswith("wei "):
        n = n[4:].strip()
    if n in ["hi", "hai", "hello", "hey", "salam", "assalamualaikum", "assalamualaikum wbt", "selamat pagi", "selamat malam", "selamat petang"]:
        if "assalamualaikum" in n or n == "salam":
            return "Waalaikumsalam! 😄 Apa cerita?"
        return "Woi! Ada ni. Apa cerita? 😄"
    if "siapa kau" in n or "kau siapa" in n or "ko siapa" in n or "nama kau" in n:
        return "Aku Hayden 1. Bos aku Adam dari Seremban. Kau pulak siapa?"
    if "siapa bos" in n or "bos kau" in n:
        return "Bos aku Adam dari Seremban."
    if "nama pekerja" in n or "senarai pekerja" in n or "siapa pekerja" in n:
        return "Aku ada 7000 pekerja. Yang paling rapat: Aiman, Aisyah, Hafiz, Nadia, Faris, Sofia, Daniel, Mira, Irfan, Zara."
    if "berapa pekerja" in n or "pekerja kau" in n:
        return "Aku ada 7000 pekerja dalam sistem."
    if "apa khabar" in n or "khabar" in n or "sihat" in n:
        return "Aku sihat je! Kau pulak sihat ke?"
    data = load_belajar()
    if n in data:
        return data[n]
    for k, v in data.items():
        if k in n or n in k:
            return v
    return "TAK_TAHU"

# ===== WAKTU MALAYSIA =====
def waktu_malaysia():
    s = datetime.now(ZON_MY)
    hari = {"Monday":"Isnin","Tuesday":"Selasa","Wednesday":"Rabu","Thursday":"Khamis","Friday":"Jumaat","Saturday":"Sabtu","Sunday":"Ahad"}
    bulan = {"January":"Januari","February":"Februari","March":"Mac","April":"April","May":"Mei","June":"Jun","July":"Julai","August":"Ogos","September":"September","October":"Oktober","November":"November","December":"Disember"}
    return f"Hari {hari.get(s.strftime('%A'))}, {s.day} {bulan.get(s.strftime('%B'))} {s.year}, pukul {s.strftime('%I:%M %p')}"
WAKTU_MY = waktu_malaysia()

def ada_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False
OFFLINE = not ada_internet()

# ===== PASSWORD KAU KAT SINI =====
API_KEY = "PASTE-PASSWORD-KAU-KAT-SINI"

client = None
gemini_error = ""
MODEL_FIX = ["gemini-2.5-flash", "gemini-2.0-flash"]

if API_KEY and API_KEY != "PASTE-PASSWORD-KAU-KAT-SINI" and not OFFLINE:
    try:
        from google import genai
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        gemini_error = str(e)

def tanya_gemini(prompt):
    if OFFLINE or not client:
        return None
    for nama_model in MODEL_FIX:
        try:
            res = client.models.generate_content(model=nama_model, contents=prompt)
            if res.text:
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

with st.sidebar:
    if OFFLINE:
        st.warning("📴 OFFLINE")
    else:
        st.success("🌐 ONLINE")
    st.write(WAKTU_MY)
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
                if jawapan == "TAK_TAHU" and client and not OFFLINE:
                    prompt = f"Kamu HAYDEN. Bos = Adam dari Seremban. Pekerja = 7000 orang. Jawab panjang, kelakar, santai. WAKTU: {WAKTU_MY}. Soalan: {tanya}"
                    hasil = tanya_gemini(prompt)
                    if hasil:
                        jawapan = hasil
                        simpan_belajar(tanya, hasil)
                    else:
                        jawapan = "GEMINI ERROR: " + gemini_error
                if jawapan == "TAK_TAHU":
                    jawapan = "Aku tak tahu lagi yang ni."
                st.write(jawapan)
                st.session_state.chat.append({"role": "assistant", "text": jawapan})
