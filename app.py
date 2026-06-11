import streamlit as st
import os
import subprocess
import tempfile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(
    page_title="BUAT SERU-SERUAN AJA",
    page_icon="🔥",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Work+Sans:wght@400;500;700&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"], .stApp {
    font-family: 'Work Sans', -apple-system, Helvetica, sans-serif;
    background: #FAFAFA !important;
    color: #0A0A0A;
}

/* ── Header ── */
.vb-header {
    border-bottom: 3px solid #0A0A0A;
    padding-bottom: 16px;
    margin-bottom: 32px;
}
.vb-overline {
    font-family: 'Work Sans', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #EF4444;
    margin-bottom: 6px;
}
.vb-title {
    font-family: 'Archivo Black', Impact, 'Arial Black', sans-serif;
    font-size: 56px;
    font-weight: 400;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: #0A0A0A;
    margin: 0;
}
.vb-sub {
    font-family: 'Work Sans', sans-serif;
    font-size: 16px;
    color: #525252;
    margin-top: 8px;
    line-height: 1.7;
}

/* ── Section label ── */
.vb-section {
    font-family: 'Work Sans', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #0A0A0A;
    border-left: 3px solid #EF4444;
    padding-left: 10px;
    margin-bottom: 12px;
    margin-top: 32px;
}

/* ── Upload card ── */
.vb-card {
    background: #FAFAFA;
    border: 2px solid #E5E5E5;
    padding: 24px;
    margin-bottom: 0;
}
.vb-card:hover { border-color: #0A0A0A; }

/* ── Status box ── */
.vb-status-ok {
    border: 2px solid #16A34A;
    background: #F0FDF4;
    color: #16A34A;
    font-family: 'Work Sans', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 6px 14px;
    display: inline-block;
    margin-top: 8px;
}
.vb-status-wait {
    border: 2px solid #D4D4D4;
    background: #F5F5F5;
    color: #A3A3A3;
    font-family: 'Work Sans', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 6px 14px;
    display: inline-block;
    margin-top: 8px;
}

/* ── Divider ── */
.vb-divider {
    border: none;
    border-top: 2px solid #0A0A0A;
    margin: 32px 0;
}

/* ── Streamlit overrides ── */
.stFileUploader {
    border: 2px solid #D4D4D4 !important;
    background: #FAFAFA !important;
    border-radius: 0 !important;
    padding: 16px !important;
}
.stFileUploader:hover { border-color: #0A0A0A !important; }

.stTextInput > div > div > input {
    border: 2px solid #D4D4D4 !important;
    border-radius: 0 !important;
    background: #FAFAFA !important;
    color: #0A0A0A !important;
    font-family: 'Work Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 8px 14px !important;
    height: 44px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #0A0A0A !important;
    box-shadow: 0 0 0 2px #FAFAFA, 0 0 0 4px #0A0A0A !important;
}
.stTextInput label {
    font-family: 'Work Sans', sans-serif !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: #0A0A0A !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #0A0A0A !important;
    color: #FAFAFA !important;
    border: 2px solid #0A0A0A !important;
    border-radius: 0 !important;
    font-family: 'Work Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 10px 24px !important;
    transition: background 0.15s, border-color 0.15s !important;
}
.stButton > button:hover {
    background: #EF4444 !important;
    border-color: #EF4444 !important;
    transform: none !important;
}

.stDownloadButton > button {
    background: #0A0A0A !important;
    color: #FAFAFA !important;
    border: 2px solid #0A0A0A !important;
    border-radius: 0 !important;
    font-family: 'Work Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 10px 24px !important;
}
.stDownloadButton > button:hover {
    background: #EF4444 !important;
    border-color: #EF4444 !important;
}

/* ── Alert ── */
.stAlert {
    border-radius: 0 !important;
    border-left: 4px solid #EF4444 !important;
    background: #FEF2F2 !important;
    font-family: 'Work Sans', sans-serif !important;
}
.stSuccess {
    border-left: 4px solid #16A34A !important;
    background: #F0FDF4 !important;
}

/* ── Footer ── */
.vb-footer {
    border-top: 2px solid #0A0A0A;
    padding-top: 16px;
    margin-top: 48px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.vb-footer-brand {
    font-family: 'Archivo Black', sans-serif;
    font-size: 14px;
    letter-spacing: -0.01em;
    color: #0A0A0A;
}
.vb-footer-note {
    font-family: 'Work Sans', sans-serif;
    font-size: 12px;
    color: #A3A3A3;
}

hr { border-top: 1px solid #E5E5E5 !important; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────────────────────
st.markdown("""
<div class="vb-header">
    <div class="vb-overline">Di Bawa · Santai Aje</div>
    <div class="vb-title">UNTUK<br>SERU-SERUAN AJE</div>
    <div class="vb-sub">Upload gambar + audio — generate jadi satu video, kirim ke WA.</div>
</div>
""", unsafe_allow_html=True)

def check_ffmpeg():
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
        return result.returncode == 0
    except:
        return False

# ── UPLOAD ───────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="vb-section">01 — Gambar</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "JPG / PNG / WEBP",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)
        st.markdown('<div class="vb-status-ok">✓ Gambar siap</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="vb-status-wait">Belum diupload</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="vb-section">02 — Audio</div>', unsafe_allow_html=True)
    uploaded_audio = st.file_uploader(
        "MP3 / WAV / OGG / M4A",
        type=["mp3", "wav", "ogg", "m4a"],
        key="audio_up",
        label_visibility="collapsed"
    )
    if uploaded_audio:
        st.audio(uploaded_audio)
        st.markdown('<div class="vb-status-ok">✓ Audio siap</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="vb-status-wait">Belum diupload</div>', unsafe_allow_html=True)

# ── CAPTION ──────────────────────────────────────────────────────────
st.markdown('<div class="vb-section">03 — Caption</div>', unsafe_allow_html=True)
caption_text = st.text_input(
    "CAPTION DI VIDEO (OPSIONAL)",
    placeholder="Misal: Pertamax naik lagi bro 😭"
)

st.markdown('<hr class="vb-divider">', unsafe_allow_html=True)

# ── GENERATE ─────────────────────────────────────────────────────────
ready = uploaded_file is not None and uploaded_audio is not None

if not ready:
    st.markdown("""
    <div style="border: 2px solid #D4D4D4; padding: 24px; background: #F5F5F5;
                font-family: 'Work Sans', sans-serif; color: #525252; font-size: 14px;">
        Upload gambar dan audio dulu — tombol generate akan muncul otomatis.
    </div>
    """, unsafe_allow_html=True)
else:
    if st.button("▶ GENERATE VIDEO", use_container_width=True):
        if not check_ffmpeg():
            st.error("ffmpeg tidak ditemukan. Pastikan packages.txt sudah ada di repo.")
        else:
            with st.spinner("Rendering..."):
                try:
                    with tempfile.TemporaryDirectory() as tmp:

                        # ── Siapkan gambar ──────────────────────────
                        img = Image.open(uploaded_file).convert("RGB")
                        max_w = 1280
                        if img.width > max_w:
                            ratio = max_w / img.width
                            img = img.resize((max_w, int(img.height * ratio)), Image.LANCZOS)
                        w = img.width - (img.width % 2)
                        h = img.height - (img.height % 2)
                        img = img.resize((w, h), Image.LANCZOS)

                        draw = ImageDraw.Draw(img)

                        # Caption bar bawah — hitam solid ala editorial
                        if caption_text:
                            try:
                                font_cap = ImageFont.truetype(
                                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
                            except:
                                font_cap = ImageFont.load_default()
                            bar_h = 60
                            draw.rectangle([0, h - bar_h, w, h], fill=(10, 10, 10, 230))
                            # Garis merah aksen kiri
                            draw.rectangle([0, h - bar_h, 5, h], fill=(239, 68, 68))
                            draw.text((20, h - bar_h + 14), caption_text,
                                      fill=(250, 250, 250), font=font_cap)

                        # Overlay play button — square, VoiceBox style
                        try:
                            font_play = ImageFont.truetype(
                                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
                        except:
                            font_play = ImageFont.load_default()

                        play_text = "▶  PUTAR"
                        btn_w, btn_h_px = 220, 64
                        cx, cy = w // 2, h // 2
                        # Background hitam solid — no radius, VoiceBox
                        draw.rectangle(
                            [cx - btn_w//2, cy - btn_h_px//2,
                             cx + btn_w//2, cy + btn_h_px//2],
                            fill=(10, 10, 10, 210)
                        )
                        # Border merah kiri 4px (pull-quote style)
                        draw.rectangle(
                            [cx - btn_w//2, cy - btn_h_px//2,
                             cx - btn_w//2 + 4, cy + btn_h_px//2],
                            fill=(239, 68, 68)
                        )
                        # Border putih keseluruhan
                        draw.rectangle(
                            [cx - btn_w//2, cy - btn_h_px//2,
                             cx + btn_w//2, cy + btn_h_px//2],
                            outline=(250, 250, 250), width=2
                        )
                        bbox = draw.textbbox((0, 0), play_text, font=font_play)
                        tw = bbox[2] - bbox[0]
                        th = bbox[3] - bbox[1]
                        draw.text((cx - tw//2 + 4, cy - th//2),
                                  play_text, fill=(250, 250, 250), font=font_play)

                        img_path = os.path.join(tmp, "frame.png")
                        img.save(img_path)

                        # ── Simpan audio ────────────────────────────
                        ext = os.path.splitext(uploaded_audio.name)[1] or ".mp3"
                        audio_path = os.path.join(tmp, f"audio{ext}")
                        with open(audio_path, "wb") as f:
                            f.write(uploaded_audio.getvalue())

                        # ── Render ffmpeg ───────────────────────────
                        video_path = os.path.join(tmp, "meme_gacor.mp4")
                        cmd = [
                            "ffmpeg", "-y",
                            "-loop", "1", "-i", img_path,
                            "-i", audio_path,
                            "-c:v", "libx264",
                            "-tune", "stillimage",
                            "-c:a", "aac", "-b:a", "192k",
                            "-pix_fmt", "yuv420p",
                            "-shortest",
                            "-movflags", "+faststart",
                            video_path
                        ]
                        result = subprocess.run(cmd, capture_output=True, timeout=120)

                        if result.returncode != 0:
                            st.error("ffmpeg error:")
                            st.code(result.stderr.decode())
                        else:
                            with open(video_path, "rb") as f:
                                video_bytes = f.read()

                            st.success("Video siap.")
                            st.video(video_bytes)
                            st.download_button(
                                "⬇ DOWNLOAD MP4",
                                data=video_bytes,
                                file_name="meme_gacor.mp4",
                                mime="video/mp4",
                                use_container_width=True
                            )

                except Exception as e:
                    st.error(f"Error: {e}")

# ── FOOTER ───────────────────────────────────────────────────────────
st.markdown("""
<div class="vb-footer">
    <span class="vb-footer-brand">MEME GACOR</span>
    <span class="vb-footer-note">Made by IZFA · Cuma buat gabut, jangan serius</span>
</div>
""", unsafe_allow_html=True)
