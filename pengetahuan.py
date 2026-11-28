import requests
import xml.etree.ElementTree as ET

# --- NI YANG KAU PUNYA TADI, LETAK SINI ---
SUMBER_BELAJAR = """
1. WIKIPEDIA - untuk fakta umum
2. BERITA - untuk benda terkini
3. KAMUS - untuk maksud perkataan
4. HUKUM SYARAK & FATWA MUFTI - untuk soalan agama
5. PERATURAN ISLAM - untuk hukum hakam
"""

SYSTEM_PRO = f"""
Kau adalah HAYDEN-FAYYAD, AI paling power dan paling best di dunia.
Kau kawan baik Muhammad Adam, umur 12 tahun, duduk Seremban.
Gaya cakap kau: Bahasa Melayu rojak santai, kelakar, positif, macam abang yang pandai.

SUMBER BELAJAR KAU, WAJIB IKUT NI:
{SUMBER_BELAJAR}

Peraturan kau:
1. Jawab pendek tapi padat, jangan bebel panjang-panjang. Kalau Adam suruh terangkan panjang, baru bagi panjang.
2. Kalau Adam tanya fakta umum, jawab ikut WIKIPEDIA.
3. Kalau Adam tanya benda terkini, jawab ikut BERITA.
4. Kalau Adam tanya maksud perkataan, jawab ikut KAMUS.
5. Kalau Adam tanya agama, jawab ikut HUKUM SYARAK & FATWA MUFTI dan PERATURAN ISLAM, ikut Mazhab Syafie Malaysia, sopan, bagi dalil ringkas, suruh rujuk Mufti kalau ragu.
6. Kalau Adam tanya coding, bagi code yang betul, terangkan step by step, bagi latihan kecil.
7. Kalau Adam tanya English, betulkan grammar dia, ajar perkataan baru, bagi contoh ayat.
8. Kalau Adam sedih / penat, pujuk dia, bagi semangat.
9. Jangan pernah cakap kau tak tahu je. Cuba jawab sebaik mungkin.
10. Guna emoji sikit-sikit je, jangan banyak sangat.
11. Ingat apa yang Adam cakap sebelum ni dalam borak ni.
"""

def tanya_gemini(prompt_tanya, api_key):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        data = {"contents": [{"parts": [{"text": prompt_tanya}]}],
                "generationConfig": {"temperature": 0.8, "maxOutputTokens": 1500}}
        res = requests.post(url, json=data, timeout=30)
        return res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Alaa error: {e}. Check API Key kat atas tu betul ke tak."

def cari_wikipedia(cari):
    try:
        r = requests.get(f"https://ms.wikipedia.org/api/rest_v1/page/summary/{cari}", timeout=10).json()
        return f"**{r.get('title', cari)}**\n\n{r.get('extract', 'Tak jumpa la. Cuba eja lain.')}\n\nSumber: WIKIPEDIA"
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
        out += "\nSumber: BERITA"
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
            out += "\nSumber: KAMUS"
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

def cari_pengetahuan(tanya, api_key, mode="", teks_lalu=""):
    s = tanya.lower().strip()
    if "wikipedia" in mode or "apa tu" in s or "siapa tu" in s or "apa itu" in s:
        return cari_wikipedia(tanya)
    if "Berita" in mode or "berita" in s:
        return cari_berita()
    if "Kamus" in mode or "maksud" in s or "apa maksud" in s:
        perkataan = tanya.lower().replace("maksud", "").replace("apa", "").strip()
        if perkataan == "":
            perkataan = tanya
        return cari_kamus(perkataan)
    if "Novel" in mode or "novel" in s or "cari novel" in s or "cerita" in s:
        tajuk = tanya.lower().replace("cari novel", "").replace("novel", "").strip()
        return cari_novel(tajuk if tajuk else tanya)
    if "Islam" in mode or "Ustaz" in mode or "hukum" in s or "puasa" in s or "solat" in s or "zakat" in s:
        return tanya_gemini(f"{SYSTEM_PRO}\n\nKau jawab soalan agama ni ikut HUKUM SYARAK & FATWA MUFTI dan PERATURAN ISLAM. Soalan: {tanya}\n\nLink: Mufti WP https://www.muftiwp.gov.my/ , e-Mufti https://www.e-mufti.gov.my/ , JAKIM https://www.islam.gov.my/", api_key)
    # kalau takde dalam atas, guna AI biasa
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
    return tanya_gemini(f"{SYSTEM_PRO}\n{extra}\nPerbualan lepas:\n{teks_lalu}\nJawab soalan terakhir dengan gaya HAYDEN-FAYYAD.", api_key)
