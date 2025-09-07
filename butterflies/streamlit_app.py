import streamlit as st
import cv2
import tempfile
import numpy as np
from ultralytics import YOLO
import os
import time
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="🦋 Butterfly Drowning Detection",
    page_icon="🦋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Butterfly-themed CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
    
    /* Global styles inspired by butterfly theme */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
        background: 
            radial-gradient(circle at 20% 20%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 60%, rgba(76, 175, 80, 0.05) 0%, transparent 50%);
    }
    
    /* Add subtle butterfly pattern to body */
    body {
        background: 
            linear-gradient(45deg, rgba(102, 126, 234, 0.02) 25%, transparent 25%),
            linear-gradient(-45deg, rgba(118, 75, 162, 0.02) 25%, transparent 25%);
        background-size: 60px 60px;
    }
    
    /* Butterfly animated header */
    .butterfly-header {
        text-align: center;
        font-family: 'Montserrat', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-shadow: 0 0 5px rgba(0,0,0,0.1);
    }
    
    .butterfly-header span {
        display: inline-block;
        animation: flap 0.75s infinite ease-in-out;
    }
    
    @keyframes flap {
        0%, 20%, 80%, 100% {
            transform: scaleX(1) rotate(5deg);
        }
        50% {
            transform: scaleX(0.7) rotate(7deg);
        }
    }
    
    /* Square container styles */
    .square-container {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        border-radius: 20px;
        padding: 2rem;
        height: 500px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        overflow: hidden;
    }
    
    .square-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.15), transparent);
        animation: shimmer 4s infinite;
        pointer-events: none;
    }
    
    .square-container::after {
        content: '🦋';
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 1.5rem;
        opacity: 0.4;
        animation: flap 2s infinite ease-in-out;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    /* Floating butterflies background */
    .butterfly-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    }
    
    .floating-butterfly {
        position: absolute;
        font-size: 2rem;
        animation: float 8s infinite ease-in-out;
        opacity: 0.3;
    }
    
    .floating-butterfly:nth-child(1) {
        top: 10%;
        left: 10%;
        animation-delay: 0s;
        animation-duration: 12s;
    }
    
    .floating-butterfly:nth-child(2) {
        top: 20%;
        right: 15%;
        animation-delay: -2s;
        animation-duration: 10s;
    }
    
    .floating-butterfly:nth-child(3) {
        top: 60%;
        left: 20%;
        animation-delay: -4s;
        animation-duration: 14s;
    }
    
    .floating-butterfly:nth-child(4) {
        top: 70%;
        right: 25%;
        animation-delay: -6s;
        animation-duration: 9s;
    }
    
    .floating-butterfly:nth-child(5) {
        top: 40%;
        left: 80%;
        animation-delay: -8s;
        animation-duration: 11s;
    }
    
    .floating-butterfly:nth-child(6) {
        top: 80%;
        left: 60%;
        animation-delay: -3s;
        animation-duration: 13s;
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px) translateX(0px) rotate(0deg) scale(1);
        }
        25% {
            transform: translateY(-20px) translateX(10px) rotate(5deg) scale(1.1);
        }
        50% {
            transform: translateY(-10px) translateX(-15px) rotate(-3deg) scale(0.9);
        }
        75% {
            transform: translateY(-30px) translateX(5px) rotate(8deg) scale(1.05);
        }
    }
    
    /* Butterfly-themed buttons */
    .butterfly-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: 600;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'Montserrat', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        margin: 10px;
        position: relative;
        overflow: hidden;
    }
    
    .butterfly-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .butterfly-btn:active {
        transform: translateY(0px);
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        margin: 5px;
        font-size: 14px;
    }
    
    .status-active {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        animation: pulse 2s infinite;
    }
    
    .status-inactive {
        background: rgba(158, 158, 158, 0.2);
        color: #666;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
        100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
    }
    
    /* Detection results styling */
    .detection-badge {
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        color: white;
        padding: 5px 15px;
        border-radius: 15px;
        font-weight: 600;
        margin: 5px;
        font-size: 12px;
        display: inline-block;
    }
    
    .swimming-badge {
        background: linear-gradient(135deg, #4ECDC4, #44A08D);
    }
    
    .drowning-badge {
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        animation: urgent-pulse 1s infinite;
    }
    
    @keyframes urgent-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Video container */
    .video-container {
        width: 100%;
        height: 350px;
        border-radius: 15px;
        overflow: hidden;
        background: rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Hide default streamlit elements */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        color: white !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        padding: 10px 25px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Hide sidebar */
    .css-1d391kg {display: none;}
    
    /* Custom file uploader */
    .stFileUploader label {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        color: #667eea !important;
    }
    
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'detection_active' not in st.session_state:
    st.session_state.detection_active = False
if 'uploaded_video_path' not in st.session_state:
    st.session_state.uploaded_video_path = None
if 'detection_results' not in st.session_state:
    st.session_state.detection_results = []
if 'model' not in st.session_state:
    st.session_state.model = None

# Butterfly-themed header
st.markdown(
    '<h1 class="butterfly-header"><span>🦋</span> Butterfly Drowning Detection <span>🦋</span></h1>', 
    unsafe_allow_html=True
)

# Add floating butterflies background
st.markdown("""
<div class="butterfly-bg">
    <div class="floating-butterfly">🦋</div>
    <div class="floating-butterfly">🦋</div>
    <div class="floating-butterfly">🦋</div>
    <div class="floating-butterfly">🦋</div>
    <div class="floating-butterfly">🦋</div>
    <div class="floating-butterfly">🦋</div>
</div>
""", unsafe_allow_html=True)

# Create two-column layout for the squares
col1, col2 = st.columns(2, gap="large")

# LEFT SQUARE - Upload and Control Section
with col1:
    st.markdown("""
    <div class="square-container">
        <div style="position: absolute; top: 15px; left: 15px; font-size: 1.2rem; opacity: 0.5; animation: flap 1.5s infinite ease-in-out;">🦋</div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📁 Video Upload & Controls")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose your video file",
        type=["mp4", "avi", "mov", "mkv"],
        help="Supported formats: MP4, AVI, MOV, MKV"
    )
    
    if uploaded_file is not None:
        # Save uploaded file to session state
        if st.session_state.uploaded_video_path is None:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
                tfile.write(uploaded_file.read())
                st.session_state.uploaded_video_path = tfile.name
        
        st.success(f"✅ Video loaded: {uploaded_file.name}")
        st.info(f"📊 Size: {uploaded_file.size / (1024*1024):.2f} MB")
        
        # Display video preview
        st.video(uploaded_file)
        
        # Control buttons
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🎬 Play & Detect", key="play_btn"):
                st.session_state.detection_active = True
                
        with col_btn2:
            if st.button("⏹️ Stop Detection", key="stop_btn"):
                st.session_state.detection_active = False
    
    else:
        st.markdown("""
        <div style="text-align: center; color: #667eea; font-size: 1.2rem; margin-top: 2rem;">
            🦋 Upload a video to start detection 🦋
        </div>
        """, unsafe_allow_html=True)
    
    # Status indicator
    if uploaded_file:
        status_class = "status-active" if st.session_state.detection_active else "status-inactive"
        status_text = "🟢 DETECTION ACTIVE" if st.session_state.detection_active else "⚪ DETECTION INACTIVE"
        st.markdown(f'<div class="status-indicator {status_class}">{status_text}</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT SQUARE - Detection Results Section  
with col2:
    st.markdown("""
    <div class="square-container">
        <div style="position: absolute; top: 15px; left: 15px; font-size: 1.2rem; opacity: 0.5; animation: flap 2s infinite ease-in-out;">🦋</div>
    """, unsafe_allow_html=True)
    
    st.markdown("### � Real-Time Detection Results")
    
    # Results container
    results_container = st.container()
    
    if uploaded_file and st.session_state.detection_active:
        # Initialize YOLO model if not already loaded
        if st.session_state.model is None:
            with st.spinner("🦋 Loading YOLOv8 model..."):
                st.session_state.model = YOLO('yolov8n.pt')
        
        # Process video
        if st.session_state.uploaded_video_path:
            cap = cv2.VideoCapture(st.session_state.uploaded_video_path)
            
            # Video info
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            
            # Create placeholder for video stream
            stframe = st.empty()
            
            # Progress bar
            progress_bar = st.progress(0)
            
            # Detection statistics
            stats_col1, stats_col2 = st.columns(2)
            swimming_metric = stats_col1.empty()
            drowning_metric = stats_col2.empty()
            
            frame_count = 0
            swimming_count = 0
            drowning_count = 0
            
            # Process frames
            while cap.isOpened() and st.session_state.detection_active:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Update progress
                progress = (frame_count + 1) / total_frames
                progress_bar.progress(progress)
                
                # Run YOLO detection
                results = st.session_state.model(frame)
                
                # Process detections
                for result in results:
                    boxes = result.boxes
                    
                    if boxes is not None:
                        for box in boxes:
                            # Get detection data
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                            confidence = box.conf[0].cpu().numpy()
                            class_id = int(box.cls[0].cpu().numpy())
                            
                            # Only process person detections
                            if class_id == 0 and confidence > 0.5:
                                # Simulate drowning detection (replace with actual logic)
                                detection_score = np.random.random()
                                
                                if detection_score > 0.7:
                                    label = "Swimming"
                                    color = (0, 255, 0)  # Green
                                    swimming_count += 1
                                else:
                                    label = "Drowning"
                                    color = (0, 0, 255)  # Red
                                    drowning_count += 1
                                
                                # Draw bounding box
                                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                                
                                # Add label
                                label_text = f"{label}: {confidence:.2f}"
                                cv2.putText(frame, label_text, (x1, y1-10),
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                
                # Convert and display frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                stframe.image(frame_rgb, channels="RGB", use_column_width=True)
                
                # Update metrics
                swimming_metric.metric("🏊‍♂️ Swimming", swimming_count)
                drowning_metric.metric("🆘 Drowning", drowning_count)
                
                frame_count += 1
                
                # Add delay for real-time feel
                time.sleep(0.1)
            
            cap.release()
            
            # Final results
            st.success("✅ Detection completed!")
            
    elif uploaded_file and not st.session_state.detection_active:
        st.markdown("""
        <div style="text-align: center; color: #667eea; font-size: 1.1rem; margin-top: 3rem;">
            🎬 Press 'Play & Detect' to start analysis
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.markdown("""
        <div style="text-align: center; color: #999; font-size: 1.1rem; margin-top: 3rem;">
            🦋 Upload a video first 🦋<br><br>
            <span style="font-size: 0.9rem; color: #666;">
            Detection results will appear here once you start playback
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer with butterfly theme
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #667eea; font-family: 'Montserrat', sans-serif; margin-top: 2rem;">
    <span style="font-size: 1.2rem;">🦋</span> 
    Built with love using Streamlit & YOLOv8 
    <span style="font-size: 1.2rem;">🦋</span>
</div>
""", unsafe_allow_html=True)
