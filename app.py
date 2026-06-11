import streamlit as st
import os
import tempfile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(
    page_title="Meme Gacor 🔥",
    page_icon="🔥",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
.stApp { background: #0d0d0d; color: #f0f0f0; }
h1, h2, h3 { color: #FFC857 !important; }
.stButton > button {
    background: #FFC857; color: #0d0d0d; font-weight: 700;
    border: none; border-radius: 8px; padding: 0.6rem 1.4rem;
    font-family: 'Space Grotesk', sans-serif; font-size: 1rem;
}
.stButton > button:hover { background: #ffdb8a; transform: translateY(-1px); }
hr { border-color: #2a2a2a; }
.generate-btn > button {
    width: 100%; padding: 1rem; font-size: 1.2rem;
    background: #FFC857; border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔥 Meme Gacor Generator")
st.markdown("Upload gambar + audio → langsung jadi video siap kirim WA")
st.markdown("---")

# ── UPLOAD ───────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📸 Gambar")
    uploaded_file = st.file_uploader(
        "JPG / PNG / WEBP",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)

with col2:
    st.markdown("### 🎙️ Audio")
    uploaded_audio = st.file_uploader(
        "MP3 / WAV / OGG",
        type=["mp3", "wav", "ogg", "m4a"],
        key="audio_up",
        label_visibility="collapsed"
    )
    if uploaded_audio:
        st.audio(uploaded_audio)

st.markdown("---")

caption_text = st.text_input(
    "✏️ Caption di video (opsional)",
    placeholder="Misal: Pertamax naik lagi bro 😭"
)

st.markdown("---")

# ── GENERATE ─────────────────────────────────────────────────────────
ready = uploaded_file is not None and uploaded_audio is not None

if not ready:
    st.info("⬆️ Upload gambar dan audio dulu baru bisa generate")
else:
    if st.button("🎬 Generate Video", use_container_width=True):
        with st.spinner("Lagi render video..."):
            try:
                import moviepy.editor as mpe
                import numpy as np

                with tempfile.TemporaryDirectory() as tmp:
                    # ── Siapkan gambar ──────────────────────────────
                    img = Image.open(uploaded_file).convert("RGB")

                    # Resize ke 720p max
                    max_w = 1280
                    if img.width > max_w:
                        ratio = max_w / img.width
                        img = img.resize((max_w, int(img.height * ratio)), Image.LANCZOS)

                    # Pastikan dimensi genap (wajib buat codec h264)
                    w = img.width if img.width % 2 == 0 else img.width - 1
                    h = img.height if img.height % 2 == 0 else img.height - 1
                    img = img.resize((w, h), Image.LANCZOS)

                    draw = ImageDraw.Draw(img)

                    # Caption bar bawah
                    if caption_text:
                        try:
                            font_cap = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
                        except:
                            font_cap = ImageFont.load_default()
                        bar_h = 55
                        draw.rectangle([0, h - bar_h, w, h], fill=(0, 0, 0, 210))
                        draw.text((16, h - bar_h + 10), caption_text, fill=(255, 200, 87), font=font_cap)

                    # Tombol play overlay di tengah
                    try:
                        font_play = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44)
                    except:
                        font_play = ImageFont.load_default()

                    play_text = "▶ Putar"
                    # Shadow + background pill
                    btn_w, btn_h = 200, 60
                    cx, cy = w // 2, h // 2
                    draw.rounded_rectangle(
                        [cx - btn_w//2, cy - btn_h//2, cx + btn_w//2, cy + btn_h//2],
                        radius=30, fill=(0, 0, 0, 180), outline=(255, 200, 87), width=3
                    )
                    # Teks tengah
                    bbox = draw.textbbox((0, 0), play_text, font=font_play)
                    tw = bbox[2] - bbox[0]
                    th = bbox[3] - bbox[1]
                    draw.text((cx - tw//2, cy - th//2 - 4), play_text, fill=(255, 200, 87), font=font_play)

                    # Simpan gambar
                    img_path = os.path.join(tmp, "frame.jpg")
                    img.save(img_path, quality=92)

                    # ── Siapkan audio ───────────────────────────────
                    ext = os.path.splitext(uploaded_audio.name)[1] or ".mp3"
                    audio_path = os.path.join(tmp, f"audio{ext}")
                    with open(audio_path, "wb") as f:
                        f.write(uploaded_audio.getvalue())

                    # ── Render video ────────────────────────────────
                    audio_clip = mpe.AudioFileClip(audio_path)
                    duration = audio_clip.duration

                    img_clip = (mpe.ImageClip(img_path)
                                .set_duration(duration)
                                .set_audio(audio_clip))

                    video_path = os.path.join(tmp, "meme_gacor.mp4")
                    img_clip.write_videofile(
                        video_path,
                        fps=1,
                        codec="libx264",
                        audio_codec="aac",
                        logger=None
                    )

                    with open(video_path, "rb") as f:
                        video_bytes = f.read()

                st.success("✅ Video siap!")
                st.video(video_bytes)
                st.download_button(
                    "⬇️ Download MP4",
                    data=video_bytes,
                    file_name="meme_gacor.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )

            except ImportError:
                st.error("❌ moviepy belum diinstall. Tambahin `moviepy` ke requirements.txt lalu restart app.")
            except Exception as e:
                st.error(f"❌ Gagal render: {e}")

# ── FOOTER ───────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#555; font-size:0.8rem; padding:0.5rem 0">
    Made with 😂 by IZFA · Cuma buat gabut, jangan serius
</div>
""", unsafe_allow_html=True)
