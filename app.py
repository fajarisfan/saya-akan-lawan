import streamlit as st
import os
import tempfile
import base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

st.set_page_config(
    page_title="Meme Gacor 🔥",
    page_icon="🔥",
    layout="centered"
)

# ── CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

.main { background: #0d0d0d; }

.stApp {
    background: #0d0d0d;
    color: #f0f0f0;
}

h1, h2, h3 { color: #FFC857 !important; }

.stButton > button {
    background: #FFC857;
    color: #0d0d0d;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.4rem;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: #ffdb8a;
    transform: translateY(-1px);
}

.upload-box {
    border: 2px dashed #FFC857;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    background: #1a1a1a;
    margin-bottom: 1rem;
}

.audio-card {
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 1rem;
    cursor: pointer;
    transition: border-color 0.2s;
}
.audio-card:hover { border-color: #FFC857; }

.tag {
    display: inline-block;
    background: #FFC857;
    color: #0d0d0d;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    margin-right: 4px;
}

.preview-container {
    background: #1a1a1a;
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid #2a2a2a;
}

hr { border-color: #2a2a2a; }
</style>
""", unsafe_allow_html=True)

# ── AUDIO PRESETS ────────────────────────────────────────────────────
# Audio berupa URL dari file yang sudah dihosting atau base64
# Untuk demo: kita sediakan tombol pilih + teks quotes-nya
AUDIO_PRESETS = {
    "🏳️ Jokowi – Saya Sudah Lama Diam": {
        "file": "jokowi_diam.mp3",
        "quote": '"Saya sudah lama diam, tapi untuk kali ini saya akan lawan!"',
        "speaker": "Jokowi",
        "tag": "CLASSIC",
        "emoji": "🏳️"
    },
    "💪 Prabowo – Saya Sudah Lama Diam": {
        "file": "prabowo_diam.mp3",
        "quote": '"Saya sudah lama diam, tapi untuk kali ini saya akan lawan!"',
        "speaker": "Prabowo",
        "tag": "VIRAL",
        "emoji": "💪"
    },
    "🤝 Jokowi – Rakyat Jangan Diprovokasi": {
        "file": "jokowi_provokasi.mp3",
        "quote": '"Jangan mau diprovokasi, kita harus tetap bersatu!"',
        "speaker": "Jokowi",
        "tag": "BIJAK",
        "emoji": "🤝"
    },
    "🔥 Prabowo – Ojo Grusa Grusu": {
        "file": "prabowo_ojo.mp3",
        "quote": '"Ojo grusa grusu, ojo kesusu!"',
        "speaker": "Prabowo",
        "tag": "JAWA",
        "emoji": "🔥"
    },
}

# ── HEADER ───────────────────────────────────────────────────────────
st.markdown("# 🔥 Meme Gacor Generator")
st.markdown("Upload gambar + pilih audio = siap kirim ke WA")
st.markdown("---")

# ── STATE ────────────────────────────────────────────────────────────
if "selected_audio" not in st.session_state:
    st.session_state.selected_audio = None
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

# ── STEP 1: UPLOAD GAMBAR ────────────────────────────────────────────
st.markdown("### 📸 Step 1 — Upload Gambar")
uploaded_file = st.file_uploader(
    "Drag & drop atau klik untuk upload",
    type=["jpg", "jpeg", "png", "gif", "webp"],
    label_visibility="collapsed"
)

caption_text = st.text_input(
    "✏️ Caption (opsional)",
    placeholder="Misal: Pertamax naik lagi bro 😭",
    help="Teks ini akan ditampilin di atas gambar"
)

if uploaded_file:
    st.session_state.uploaded_image = uploaded_file
    img = Image.open(uploaded_file)
    
    # Resize preview
    max_w = 600
    if img.width > max_w:
        ratio = max_w / img.width
        new_h = int(img.height * ratio)
        img_preview = img.resize((max_w, new_h), Image.LANCZOS)
    else:
        img_preview = img
    
    # Tambahin caption kalau ada
    if caption_text:
        draw = ImageDraw.Draw(img_preview)
        # Background strip
        strip_h = 50
        draw.rectangle([0, 0, img_preview.width, strip_h], fill=(0, 0, 0, 200))
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        except:
            font = ImageFont.load_default()
        
        draw.text((12, 12), caption_text, fill=(255, 200, 87), font=font)
    
    st.image(img_preview, use_container_width=True)

st.markdown("---")

# ── STEP 2: PILIH AUDIO ──────────────────────────────────────────────
st.markdown("### 🎙️ Step 2 — Pilih Audio")
st.markdown("*Upload file audio lo sendiri, atau pakai preset di bawah:*")

# Upload audio sendiri
custom_audio = st.file_uploader(
    "Upload audio sendiri (MP3/WAV/OGG)",
    type=["mp3", "wav", "ogg", "m4a"],
    key="custom_audio",
    label_visibility="visible"
)

if custom_audio:
    st.session_state.selected_audio = {"type": "custom", "file": custom_audio, "name": custom_audio.name}
    st.success(f"✅ Audio '{custom_audio.name}' siap!")
    st.audio(custom_audio)

st.markdown("**— atau pilih preset —**")

# Grid preset audio
cols = st.columns(2)
preset_names = list(AUDIO_PRESETS.keys())

for i, preset_name in enumerate(preset_names):
    preset = AUDIO_PRESETS[preset_name]
    col = cols[i % 2]
    
    with col:
        is_selected = (
            st.session_state.selected_audio is not None and
            st.session_state.selected_audio.get("type") == "preset" and
            st.session_state.selected_audio.get("name") == preset_name
        )
        
        border_color = "#FFC857" if is_selected else "#333"
        bg_color = "#2a2200" if is_selected else "#1a1a1a"
        
        st.markdown(f"""
        <div style="background:{bg_color}; border:2px solid {border_color}; 
             border-radius:10px; padding:1rem; margin-bottom:0.5rem;">
            <div style="font-size:1.5rem">{preset['emoji']}</div>
            <div style="font-weight:700; font-size:0.9rem; color:#f0f0f0; margin:4px 0">
                {preset['speaker']}
            </div>
            <div style="background:#FFC857; color:#0d0d0d; font-size:0.65rem; 
                 font-weight:700; display:inline-block; padding:2px 6px; 
                 border-radius:4px; margin-bottom:6px">
                {preset['tag']}
            </div>
            <div style="font-size:0.78rem; color:#aaa; font-style:italic; line-height:1.4">
                {preset['quote']}
            </div>
            {'<div style="color:#FFC857; font-size:0.75rem; margin-top:6px">✓ DIPILIH</div>' if is_selected else ''}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"{'✓ Dipilih' if is_selected else 'Pilih'}", key=f"btn_{i}"):
            st.session_state.selected_audio = {
                "type": "preset",
                "name": preset_name,
                "data": preset
            }
            st.rerun()

st.markdown("---")

# ── STEP 3: PREVIEW & DOWNLOAD ───────────────────────────────────────
st.markdown("### 🎬 Step 3 — Preview & Download")

has_image = uploaded_file is not None
has_audio = st.session_state.selected_audio is not None

if not has_image and not has_audio:
    st.info("⬆️ Upload gambar dan pilih audio dulu ya")
elif not has_image:
    st.warning("📸 Gambar belum diupload")
elif not has_audio:
    st.warning("🎙️ Audio belum dipilih")
else:
    audio_info = st.session_state.selected_audio
    
    # Show preview
    col_img, col_info = st.columns([1, 1])
    
    with col_img:
        st.markdown("**Preview Gambar:**")
        img_display = Image.open(uploaded_file)
        if caption_text:
            draw = ImageDraw.Draw(img_display)
            strip_h = 60
            draw.rectangle([0, 0, img_display.width, strip_h], fill=(0, 0, 0, 200))
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
            except:
                font = ImageFont.load_default()
            draw.text((15, 15), caption_text, fill=(255, 200, 87), font=font)
        
        st.image(img_display, use_container_width=True)
    
    with col_info:
        st.markdown("**Audio Dipilih:**")
        if audio_info["type"] == "preset":
            preset = audio_info["data"]
            st.markdown(f"""
            <div style="background:#1a1a1a; border:1px solid #FFC857; border-radius:10px; padding:1rem;">
                <div style="font-size:2rem">{preset['emoji']}</div>
                <div style="font-weight:700; color:#FFC857">{preset['speaker']}</div>
                <div style="font-size:0.8rem; color:#aaa; font-style:italic; margin-top:8px">
                    {preset['quote']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#1a1a1a; border:1px solid #FFC857; border-radius:10px; padding:1rem;">
                <div style="font-size:2rem">🎵</div>
                <div style="font-weight:700; color:#FFC857">Custom Audio</div>
                <div style="font-size:0.8rem; color:#aaa; margin-top:8px">{audio_info['name']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("")
        st.markdown("**Cara pakai di WA:**")
        st.markdown("""
        1. Download gambar di bawah
        2. Download audio di bawah  
        3. Kirim gambar ke WA dulu
        4. Reply dengan audio
        
        *Atau gabungin jadi video (butuh ffmpeg)*
        """)
    
    st.markdown("---")
    
    # Download gambar
    col_d1, col_d2, col_d3 = st.columns(3)
    
    with col_d1:
        # Prepare final image
        img_final = Image.open(uploaded_file)
        if caption_text:
            draw = ImageDraw.Draw(img_final)
            strip_h = 60
            draw.rectangle([0, 0, img_final.width, strip_h], fill=(0, 0, 0, 200))
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
            except:
                font = ImageFont.load_default()
            draw.text((15, 15), caption_text, fill=(255, 200, 87), font=font)
        
        from io import BytesIO
        buf = BytesIO()
        img_final.save(buf, format="JPEG", quality=90)
        buf.seek(0)
        
        st.download_button(
            label="📷 Download Gambar",
            data=buf.getvalue(),
            file_name="meme_gacor.jpg",
            mime="image/jpeg",
            use_container_width=True
        )
    
    with col_d2:
        # Audio download
        if audio_info["type"] == "custom":
            audio_bytes = audio_info["file"].read()
            st.download_button(
                label="🎵 Download Audio",
                data=audio_bytes,
                file_name=audio_info["name"],
                mime="audio/mpeg",
                use_container_width=True
            )
        else:
            st.button("🎵 Audio (Upload dulu)", disabled=True, use_container_width=True)
    
    with col_d3:
        # Video gabungan dengan moviepy jika tersedia
        try:
            import moviepy.editor as mp
            can_video = True
        except:
            can_video = False
        
        if can_video and audio_info["type"] == "custom":
            if st.button("🎬 Gabung jadi Video", use_container_width=True):
                with st.spinner("Lagi bikin video..."):
                    try:
                        with tempfile.TemporaryDirectory() as tmp:
                            # Save image
                            img_path = os.path.join(tmp, "img.jpg")
                            img_final.save(img_path)
                            
                            # Save audio
                            audio_path = os.path.join(tmp, "audio.mp3")
                            audio_bytes_data = audio_info["file"].getvalue()
                            with open(audio_path, "wb") as f:
                                f.write(audio_bytes_data)
                            
                            # Create video
                            audio_clip = mp.AudioFileClip(audio_path)
                            duration = audio_clip.duration
                            
                            img_clip = mp.ImageClip(img_path).set_duration(duration)
                            img_clip = img_clip.set_audio(audio_clip)
                            img_clip = img_clip.resize(height=720)
                            
                            video_path = os.path.join(tmp, "output.mp4")
                            img_clip.write_videofile(video_path, fps=1, codec="libx264", 
                                                      audio_codec="aac", logger=None)
                            
                            with open(video_path, "rb") as f:
                                video_bytes = f.read()
                            
                            st.download_button(
                                "⬇️ Download Video MP4",
                                data=video_bytes,
                                file_name="meme_video.mp4",
                                mime="video/mp4"
                            )
                    except Exception as e:
                        st.error(f"Gagal bikin video: {e}")
        else:
            help_text = "Install moviepy dulu" if not can_video else "Upload audio custom dulu"
            st.button(f"🎬 Gabung Video", disabled=True, 
                     use_container_width=True, help=help_text)

# ── FOOTER ───────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#555; font-size:0.8rem; padding:1rem 0">
    Made with 😂 by IZFA · Cuma buat gabut, jangan serius
</div>
""", unsafe_allow_html=True)
