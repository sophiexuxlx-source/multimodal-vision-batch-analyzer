import os
import glob
import json
import random
import csv
import io
import tempfile
import cv2
import pandas as pd
import streamlit as st
from PIL import Image

import image_utils
import api_client
import use_cases
import batch_analyzer

INSTAGRAM_PHOTOS_DIR = r"c:\AI Builder & AI Architect\AI Study\AI Builders\Project 2 Downloading Imagines from an Instagram Account\photos"

# Page Config
st.set_page_config(
    page_title="Multimodal Vision AI Explorer",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.3rem;
        color: #1E88E5;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #546E7A;
        margin-bottom: 1.5rem;
    }
    .card {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 1.2rem;
        border-left: 5px solid #1E88E5;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# App Title & Subtitle
st.markdown('<div class="main-header">🖼️ Multimodal Vision AI Explorer</div>', unsafe_allow_html=True)

# Load Instagram photos list
@st.cache_data
def load_photos():
    return batch_analyzer.get_all_photos(INSTAGRAM_PHOTOS_DIR)

ig_photos = load_photos()

# Helper for Video Keyframe Extraction
def extract_mp4_keyframes(video_bytes, num_keyframes=4):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(video_bytes)
        tmp_path = tmp.name
    
    cap = cv2.VideoCapture(tmp_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    keyframes = []
    
    if total_frames > 0:
        step = max(1, total_frames // num_keyframes)
        for i in range(0, total_frames, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                keyframes.append(Image.fromarray(frame_rgb))
            if len(keyframes) >= num_keyframes:
                break
    cap.release()
    try:
        os.remove(tmp_path)
    except Exception:
        pass
    return keyframes

# Sidebar: Image Source Selection
st.sidebar.header("📁 Image Selection")
source_option = st.sidebar.radio(
    "Choose Image Source:",
    [
        "🖼️ Instagram Dataset (911 Photos)", 
        "📁 Project 4 Workspace Folder",
        "📤 Upload Custom Image (Drag & Drop)", 
        "🎨 Synthetic Test Image"
    ]
)

selected_image_path = None
selected_pil_image = None
image_title = ""

if source_option == "🖼️ Instagram Dataset (911 Photos)":
    if ig_photos:
        col_side1, col_side2 = st.sidebar.columns([3, 1])
        with col_side2:
            if st.button("🎲 Random"):
                st.session_state["selected_index"] = random.randint(0, len(ig_photos) - 1)
        
        if "selected_index" not in st.session_state:
            st.session_state["selected_index"] = 0
            
        selected_index = st.sidebar.number_input(
            "Photo Index (1-911):",
            min_value=1,
            max_value=len(ig_photos),
            value=st.session_state["selected_index"] + 1,
            step=1
        ) - 1

        selected_image_path = ig_photos[selected_index]
        image_title = os.path.basename(selected_image_path)
        
        # Search by filename
        search_query = st.sidebar.text_input("🔍 Search Filename (e.g. 629224241):")
        if search_query:
            matches = [(i, p) for i, p in enumerate(ig_photos) if search_query.lower() in os.path.basename(p).lower()]
            if matches:
                selected_index = matches[0][0]
                selected_image_path = matches[0][1]
                image_title = os.path.basename(selected_image_path)
                st.sidebar.success(f"Matched Photo #{selected_index + 1}")
            else:
                st.sidebar.warning(f"No photo found matching: '{search_query}'")
    else:
        st.sidebar.error("Instagram dataset directory not found.")

elif source_option == "📁 Project 4 Workspace Folder":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    valid_exts = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp4", ".mov", ".avi", ".mkv")
    workspace_files = [
        f for f in os.listdir(project_dir) 
        if os.path.isfile(os.path.join(project_dir, f)) and f.lower().endswith(valid_exts)
    ]
    
    if workspace_files:
        # Default to nambrowncarbon_geos5_20260720.mp4 if present
        default_idx = 0
        for i, fname in enumerate(workspace_files):
            if "nambrowncarbon" in fname.lower():
                default_idx = i
                break
                
        selected_filename = st.sidebar.selectbox("Select file in Project 4 folder:", workspace_files, index=default_idx)
        selected_image_path = os.path.join(project_dir, selected_filename)
        image_title = selected_filename
        
        file_ext = os.path.splitext(selected_filename)[1].lower()
        if file_ext in [".mp4", ".mov", ".avi", ".mkv"]:
            st.sidebar.info("🎬 MP4 Video detected. Extracting keyframes...")
            with open(selected_image_path, "rb") as vf:
                v_bytes = vf.read()
            gif_frames = extract_mp4_keyframes(v_bytes, num_keyframes=4)
            if gif_frames:
                selected_pil_image = gif_frames
                st.sidebar.success(f"[OK] Extracted {len(gif_frames)} keyframes from video!")
        elif file_ext == ".gif":
            try:
                pil_img = Image.open(selected_image_path)
                if getattr(pil_img, "is_animated", False) and pil_img.n_frames > 1:
                    n_frames = pil_img.n_frames
                    step = max(1, n_frames // 4)
                    gif_frames = []
                    for i in range(0, n_frames, step):
                        pil_img.seek(i)
                        gif_frames.append(pil_img.copy().convert("RGB"))
                    selected_pil_image = gif_frames
                else:
                    selected_pil_image = pil_img.convert("RGB")
            except Exception as e:
                st.sidebar.error(f"Error loading GIF: {e}")
    else:
        st.sidebar.warning("No media files found in Project 4 workspace folder.")

elif source_option == "📤 Upload Custom Image (Drag & Drop)":
    uploaded_file = st.sidebar.file_uploader(
        "Upload an Image, GIF, or MP4 Video:", 
        type=["jpg", "jpeg", "png", "webp", "gif", "mp4", "mov", "avi", "mkv"]
    )
    if uploaded_file is not None:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        image_title = uploaded_file.name

        if file_ext in [".mp4", ".mov", ".avi", ".mkv"]:
            st.sidebar.info("🎬 Video file detected. Extracting keyframes using OpenCV...")
            v_bytes = uploaded_file.read()
            gif_frames = extract_mp4_keyframes(v_bytes, num_keyframes=4)
            if gif_frames:
                selected_pil_image = gif_frames  # List of keyframe Images
                st.sidebar.success(f"[OK] Extracted {len(gif_frames)} keyframes!")
            else:
                st.sidebar.error("Could not extract frames from video.")
        else:
            try:
                pil_img = Image.open(uploaded_file)
                # Check if animated GIF
                if getattr(pil_img, "is_animated", False) and pil_img.n_frames > 1:
                    st.sidebar.info(f"🎞️ Animated GIF detected ({pil_img.n_frames} frames). Extracting keyframes...")
                    n_frames = pil_img.n_frames
                    step = max(1, n_frames // 4)
                    gif_frames = []
                    for i in range(0, n_frames, step):
                        pil_img.seek(i)
                        gif_frames.append(pil_img.copy().convert("RGB"))
                    selected_pil_image = gif_frames
                else:
                    selected_pil_image = pil_img.convert("RGB")
            except Exception as e:
                st.sidebar.error(f"Could not load file: {e}")

elif source_option == "🎨 Synthetic Test Image":
    sample_path = "sample_image.png"
    if not os.path.exists(sample_path):
        image_utils.create_sample_image(sample_path)
    selected_image_path = sample_path
    image_title = "sample_image.png (Geometric Shapes & Text)"

# Main Layout: Two Columns
col_img, col_analysis = st.columns([1, 1.2])

with col_img:
    st.subheader("📸 Active Image / Sequence Preview")
    if isinstance(selected_pil_image, list):
        st.info(f"🎞️ Animated Sequence ({len(selected_pil_image)} Keyframes Extracted)")
        cols_grid = st.columns(len(selected_pil_image))
        for idx, kf in enumerate(selected_pil_image):
            with cols_grid[idx]:
                st.image(kf, caption=f"Frame #{idx+1}", use_container_width=True)
        img_to_process = selected_pil_image
    elif selected_pil_image is not None:
        st.image(selected_pil_image, caption=image_title, use_container_width=True)
        img_to_process = selected_pil_image
    elif selected_image_path is not None and os.path.exists(selected_image_path):
        img_to_process = Image.open(selected_image_path)
        st.image(img_to_process, caption=image_title, use_container_width=True)
        st.caption(f"**Path:** `{selected_image_path}`")
    else:
        st.info("Please select or upload an image from the sidebar.")
        img_to_process = None

with col_analysis:
    st.subheader("⚡ AI Multimodal Analysis")
    
    if img_to_process is not None:
        tab1, tab2, tab3, tab4 = st.tabs([
            "📝 Description & Q&A", 
            "🏷️ Web Alt-Text", 
            "🔍 Object Recognition", 
            "📊 Batch Exporter"
        ])
        
        # Tab 1: Description & Q&A
        with tab1:
            st.markdown("### Image Description & Custom Q&A")
            custom_q = st.text_input("Ask a custom question about this photo (or leave blank for full description):")
            
            if st.button("🚀 Analyze Image", key="btn_desc"):
                with st.spinner("Analyzing with Gemini 3.6 Flash..."):
                    try:
                        res = use_cases.generate_image_description(img_to_process, custom_question=custom_q if custom_q else None)
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown(res)
                        st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {e}")

        # Tab 2: Alt-Text Generation
        with tab2:
            st.markdown("### Web Accessibility Alt-Text Generation")
            st.caption("Generates WCAG-compliant HTML alt-text under 125 characters.")
            
            if st.button("✨ Generate Alt-Text", key="btn_alt"):
                with st.spinner("Generating alt-text..."):
                    try:
                        alt = use_cases.generate_alt_text(img_to_process)
                        st.success("Alt-Text Successfully Generated!")
                        st.code(f'<img src="{image_title}" alt="{alt}" />', language="html")
                        st.info(f"**Alt-Text:** {alt} ({len(alt)} chars)")
                    except Exception as e:
                        st.error(f"Error: {e}")

        # Tab 3: Object Recognition (JSON)
        with tab3:
            st.markdown("### Structured Object Recognition (JSON)")
            st.caption("Identifies objects, counts, categories, and colors in pure JSON.")
            
            if st.button("🔍 Detect Objects", key="btn_obj"):
                with st.spinner("Detecting objects..."):
                    try:
                        obj_json = use_cases.detect_objects(img_to_process)
                        st.json(obj_json)
                    except Exception as e:
                        st.error(f"Error: {e}")

        # Tab 4: Batch Exporter
        with tab4:
            st.markdown("### 📊 Bulk Dataset Batch Exporter")
            st.caption("Automatically analyze N photos from your 911 Instagram collection and download CSV / JSON reports.")
            
            batch_count = st.slider("Select number of photos to batch analyze:", min_value=1, max_value=20, value=3)
            
            if st.button("⚡ Run Batch Export Job", key="btn_batch"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                selected_batch = random.sample(ig_photos, min(batch_count, len(ig_photos)))
                results = []
                
                for idx, photo_path in enumerate(selected_batch, 1):
                    fn = os.path.basename(photo_path)
                    status_text.text(f"Processing photo {idx}/{len(selected_batch)}: {fn}...")
                    
                    try:
                        desc = use_cases.generate_image_description(photo_path)
                        alt_text = use_cases.generate_alt_text(photo_path)
                        objs_json = use_cases.detect_objects(photo_path)
                        
                        results.append({
                            "file_name": fn,
                            "alt_text": alt_text,
                            "description": desc,
                            "detected_objects": ", ".join([o.get("name", "") for o in objs_json.get("objects", [])])
                        })
                    except Exception as e:
                        st.warning(f"Error processing {fn}: {e}")
                    
                    progress_bar.progress(idx / len(selected_batch))
                
                status_text.success("Batch Analysis Complete!")
                df_results = pd.DataFrame(results)
                st.dataframe(df_results, use_container_width=True)
                
                # Download CSV Button
                csv_buffer = io.StringIO()
                df_results.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="📥 Download CSV Report",
                    data=csv_buffer.getvalue(),
                    file_name="batch_analysis_results.csv",
                    mime="text/csv"
                )
