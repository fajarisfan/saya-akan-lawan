import streamlit as st
import os
import subprocess
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
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔥 Meme Gacor Generator")
st.markdown("Upload gambar + audio → langsung jadi video siap kirim WA")
st.markdown("---")

def check_ffmpeg():
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
        return result.returncode == 0
    except:
        return False

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
        if not check_ffmpeg():
            st.error("❌ ffmpeg tidak ditemukan di server ini.")
        else:
            with st.spinner("Lagi render video..."):
                try:
                    with tempfile.TemporaryDirectory() as tmp:

                        # ── Siapkan gambar ──────────────────────────
                        img = Image.open(uploaded_file).convert("RGB")

                        # Resize max 1280px lebar
                        max_w = 1280
                        if img.width > max_w:
                            ratio = max_w / img.width
                            img = img.resize((max_w, int(img.height * ratio)), Image.LANCZOS)

                        # Dimensi harus genap untuk h264
                        w = img.width - (img.width % 2)
                        h = img.height - (img.height % 2)
                        img = img.resize((w, h), Image.LANCZOS)

                        draw = ImageDraw.Draw(img)

                        # Caption bar bawah
                        if caption_text:
                            try:
                                font_cap = ImageFont.truetype(
                                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
                            except:
                                font_cap = ImageFont.load_default()
                            bar_h = 55
                            draw.rectangle([0, h - bar_h, w, h], fill=(0, 0, 0, 210))
                            draw.text((16, h - bar_h + 10), caption_text,
                                      fill=(255, 200, 87), font=font_cap)

                        # Overlay tombol play di tengah
                        try:
                            font_play = ImageFont.truetype(
                                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44)
                        except:
                            font_play = ImageFont.load_default()

                        play_text = "▶  Putar"
                        btn_w, btn_h = 210, 65
                        cx, cy = w // 2, h // 2
                        draw.rounded_rectangle(
                            [cx - btn_w//2, cy - btn_h//2, cx + btn_w//2, cy + btn_h//2],
                            radius=32, fill=(0, 0, 0, 175), outline=(255, 200, 87), width=3
                        )
                        bbox = draw.textbbox((0, 0), play_text, font=font_play)
                        tw = bbox[2] - bbox[0]
                        th = bbox[3] - bbox[1]
                        draw.text((cx - tw//2, cy - th//2 - 2), play_text,
                                  fill=(255, 200, 87), font=font_play)

                        # Simpan frame
                        img_path = os.path.join(tmp, "frame.png")
                        img.save(img_path)

                        # ── Simpan audio ────────────────────────────
                        ext = os.path.splitext(uploaded_audio.name)[1] or ".mp3"
                        audio_path = os.path.join(tmp, f"audio{ext}")
                        with open(audio_path, "wb") as f:
                            f.write(uploaded_audio.getvalue())

                        # ── Render dengan ffmpeg ────────────────────
                        video_path = os.path.join(tmp, "meme_gacor.mp4")
                        cmd = [
                            "ffmpeg", "-y",
                            "-loop", "1",
                            "-i", img_path,
                            "-i", audio_path,
                            "-c:v", "libx264",
                            "-tune", "stillimage",
                            "-c:a", "aac",
                            "-b:a", "192k",
                            "-pix_fmt", "yuv420p",
                            "-shortest",
                            "-movflags", "+faststart",
                            video_path
                        ]
                        result = subprocess.run(cmd, capture_output=True, timeout=120)

                        if result.returncode != 0:
                            st.error("❌ ffmpeg error:")
                            st.code(result.stderr.decode())
                        else:
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

                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ── FOOTER ───────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#555; font-size:0.8rem; padding:0.5rem 0">
    Made with 😂 by IZFA · Cuma buat gabut, jangan serius
</div>
""", unsafe_allow_html=True)
