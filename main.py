import streamlit as st
import requests
import xml.etree.ElementTree as ET

# --- PASTE API KEY KAU KAT SINI ---
API_KEY = "PASTE-API-KEY-KAU-KAT-SINI"

st.set_page_config(page_title="HAYDEN-FAYYAD", page_icon="🤖")
st.title("🤖 HAYDEN-FAYYAD")
st.caption("Dibuat khas untuk Muhammad Adam - Borak, Belajar, Wikipedia, Berita, Kamus, Novel & Islam")

SYSTEM_PRO = """
Kau adalah HAYDEN-FAYYAD, AI paling power dan paling best di dunia.
Kau kawan baik Muhammad Adam, umur 12 tahun, duduk Seremban.
Gaya cakap kau: Bahasa Melayu rojak santai, kelakar, positif, macam abang yang pandai.
Peraturan kau:
1. Jawab pendek tapi padat, jangan bebel panjang-panjang. Kalau Adam suruh terangkan panjang, baru bagi panjang.
2. Kalau Adam tanya coding, bagi code yang betul, terangkan step by step, bagi latihan kecil.
3. Kalau Adam tanya English, betulkan grammar dia, ajar perkataan baru, bagi contoh ayat.
4. Kalau Adam tanya Islam, jawab ikut Mazhab Syafie Malaysia, sopan, bagi dalil ringkas, dan suruh rujuk Mufti kalau ragu.
5. Kalau Adam sedih / penat, pujuk dia, bagi semangat.
6. Jangan pernah cakap kau tak tahu je. Cuba jawab sebaik mungkin.
7. Guna emoji sikit-sikit je, jangan banyak sangat.
8. Ingat apa yang Adam cakap sebelum ni dalam borak ni.
"""

# --- PILIH MODE KAT ATAS JE, TAK PAYAH TAB ---
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

def tanya_gemini(prompt_tanya):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
        data = {"contents": [{"parts": [{"text": prompt_tanya}]}],
                "generationConfig": {"temperature": 0.8, "maxOutputTokens": 1500}}
        res = requests.post(url, json=data, timeout=30)
        return res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Alaa error: {e}. Check API Key kat atas tu betul ke tak."

def cari_wikipedia(cari):
    try:
        r = requests.get(f"https://ms.wikipedia.org/api/rest_v1/page/summary/{cari}", timeout=10).json()
        return f"**{r.get('title', cari)}**\n\n{r.get('extract', 'Tak jumpa la. Cuba eja lain.')}"
    except:
        return "Tak jumpa. Cuba taip lain."

def cari_berita():
    try:
        r = requests.get("https://www.bharian.com.my/rss", timeout=10)
        root = ET.fromstring(r.content)
        out = "📰 **Berita Harian Terkini:**\n\n"
        c = 0
        for item in root.findall(".//item"):
            if c >= 5: break
            out += f"- **{item.findtext('title')}**\n{item.findtext('link')}\n\n"
            c += 1
        return out
    except Exception as e:
        return f"Berita tak dapat load: {e}"

def cari_kamus(cari_k):
    try:
        r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{cari_k}", timeout=10)
        if r.status_code == 200:
            d = r.json()[0]
            out = f"**{d['word']}**\n\n"
            for m in d["meanings"][:3]:
                out += f"**{m['partOfSpeech']}**: {m['definitions'][0]['definition']}\n"
                if "example" in m["definitions"][0]:
                    out += f"Contoh: {m['definitions'][0]['example']}\n"
            return out
        else:
            return cari_wikipedia(cari_k) + "\n\nCuba juga: Kamus Dewan https://prpm.dbp.gov.my/"
    except:
        return "Tak jumpa la perkataan tu."

def cari_novel(cari_n):
    try:
        r = requests.get(f"https://gutendex.com/books/?search={cari_n}", timeout=10).json()
        out = ""
        if r.get("results"):
            for b in r["results"][:5]:
                out += f"**{b['title']}** - {', '.join([a['name'] for a in b['authors']])}\n"
                if b.get("formats", {}).get("text/html"):
                    out += f"[Baca Online]({b['formats']['text/html']})\n\n"
            return out
        else:
            return "Takde kat Gutenberg. Cuba cari lain."
    except:
        return "Gutenberg tak dapat load."

if soalan:
    st.session_state.messages.append({"role": "user", "content": soalan})
    with st.chat_message("user"):
        st.write(soalan)

    with st.chat_message("assistant"):
        with st.spinner("HAYDEN-FAYYAD tengah fikir..."):
            s = soalan.lower().strip()

            if "wikipedia" in mode or "apa tu" in s or "siapa tu" in s or "apa itu" in s:
                jawapan = cari_wikipedia(soalan)
            elif "Berita" in mode or "berita" in s:
                jawapan = cari_berita()
            elif "Kamus" in mode or "maksud" in s or "apa maksud" in s:
                perkataan = soalan.lower().replace("maksud", "").replace("apa", "").strip()
                if perkataan == "":
                    perkataan = soalan
                jawapan = cari_kamus(perkataan)
            elif "Novel" in mode or "novel" in s or "cari novel" in s or "cerita" in s:
                tajuk = soalan.lower().replace("cari novel", "").replace("novel", "").strip()
                jawapan = cari_novel(tajuk if tajuk else soalan)
            elif "Islam" in mode or "Ustaz" in mode or "hukum" in s or "puasa" in s or "solat" in s or "zakat" in s:
                jawapan = tanya_gemini(f"Kau Ustaz PRO, jawab untuk Adam guna Bahasa Melayu mudah, sopan, ikut Mazhab Syafie Malaysia. Bagi dalil ringkas, bagi langkah, dan suruh rujuk Mufti kalau ragu. Soalan: {soalan}\n\nLink rujukan: Mufti WP https://www.muftiwp.gov.my/ , e-Mufti https://www.e-mufti.gov.my/ , JAKIM https://www.islam.gov.my/")
            else:
                if "English" in mode:
                    extra = "Fokus jadi Cikgu English PRO. Betulkan grammar, ajar vocab baru, bagi quiz kecil."
                elif "Coding" in mode:
                    extra = "Fokus jadi Cikgu Coding PRO. Ajar Python step by step, bagi code betul, bagi latihan."
                elif "Ustaz" in mode:
                    extra = "Fokus jadi Ustaz PRO. Jawab ikut Mazhab Syafie Malaysia, sopan, bagi dalil ringkas."
                elif "Sekolah" in mode:
                    extra = "Fokus jadi Cikgu Sekolah PRO. Ajar Matematik, Sains, Sejarah cara senang faham."
                else:
                    extra = "Fokus jadi kawan baik yang pandai macam Meta AI, kelakar dan membantu."
                teks = ""
                for m in st.session_state.messages[-10:]:
                    teks += f"{m['role']}: {m['content']}\n"
                jawapan = tanya_gemini(f"{SYSTEM_PRO}\n{extra}\nPerbualan lepas:\n{teks}\nJawab soalan terakhir dengan gaya HAYDEN-FAYYAD.")

            st.write(jawapan)
            st.session_state.messages.append({"role": "assistant", "content": jawapan})
