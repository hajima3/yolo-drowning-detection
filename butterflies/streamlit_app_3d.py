import streamlit as st
import streamlit.components.v1 as components
import cv2
import tempfile
import numpy as np
from ultralytics import YOLO
import os
import time
from PIL import Image
import base64

# Set page configuration
st.set_page_config(
    page_title="🦋 Butterfly Drowning Detection",
    page_icon="🦋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Read the original butterfly CSS, JS and create enhanced version
def load_butterfly_assets():
    # Read the original butterfly CSS
    with open("butterflies/82/butterflies.css", "r") as f:
        butterfly_css = f.read()
    
    # Read the original butterfly JS
    with open("butterflies/82/butterflies.js", "r") as f:
        butterfly_js = f.read()
    
    return butterfly_css, butterfly_js

# Enhanced 3D Butterfly Integration
def create_3d_butterfly_html():
    return f"""
    <!DOCTYPE html>
    <html style="height: 100%; margin: 0; padding: 0;">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body, html {{
                margin: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
            }}
            
            #butterfly-canvas {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -1;
                pointer-events: none;
            }}
            
            /* Original butterfly styles enhanced */
            body, html, #app {{
                margin: 0;
                width: 100%;
                height: 100%;
            }}

            #app {{
                overflow: hidden;
                touch-action: pan-up;
                color: #ffffff;
                font-family: 'Montserrat', sans-serif;
                text-align: center;
                text-shadow: 0 0 5px #000000, 0 0 20px #000;
                user-select: none;
                background: linear-gradient(135deg, #88CEFF 0%, #667eea 50%, #764ba2 100%);
            }}

            #app canvas {{
                display: block;
                position: fixed;
                z-index: -1;
                top: 0;
            }}
        </style>
    </head>
    <body>
        <div id="app">
            <div id="butterfly-canvas"></div>
        </div>
        
        <script type="module">
            import {{ butterfliesBackground }} from 'https://unpkg.com/threejs-toys@0.0.8/build/threejs-toys.module.cdn.min.js'

            const pc = butterfliesBackground({{
                el: document.getElementById('app'),
                eventsEl: document.body,
                gpgpuSize: 24,
                background: 0x88CEFF,
                material: 'phong',
                lights: [
                    {{ type: 'ambient', params: [0xffffff, 0.6] }},
                    {{ type: 'directional', params: [0xffffff, 1.2], props: {{ position: [10, 5, 5] }} }}
                ],
                materialParams: {{ transparent: true, alphaTest: 0.4 }},
                texture: 'https://assets.codepen.io/33787/butterflies.png',
                textureCount: 4,
                wingsScale: [2.5, 2.5, 2.5],
                wingsWidthSegments: 20,
                wingsHeightSegments: 20,
                wingsSpeed: 0.85,
                wingsDisplacementScale: 1.5,
                noiseCoordScale: 0.012,
                noiseTimeCoef: 0.0008,
                noiseIntensity: 0.004,
                attractionRadius1: 120,
                attractionRadius2: 180,
                maxVelocity: 0.15
            }})
        </script>
    </body>
    </html>
    """

# Enhanced CSS for glass morphism with 3D background
def get_enhanced_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
        
        /* Reset and base styles */
        .stApp {
            background: transparent !important;
        }
        
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 100%;
            position: relative;
            z-index: 100;
        }
        
        /* Enhanced butterfly header with extreme glass morphism */
        .butterfly-header {
            text-align: center;
            font-family: 'Montserrat', sans-serif;
            color: rgba(255, 255, 255, 0.98);
            font-size: 3.8rem;
            font-weight: 800;
            margin-bottom: 2.5rem;
            text-shadow: 
                0 0 20px rgba(0,0,0,0.6),
                0 0 40px rgba(136, 206, 255, 0.4),
                0 0 60px rgba(136, 206, 255, 0.2);
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(25px);
            padding: 1.5rem 3rem;
            border-radius: 30px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            box-shadow: 
                0 15px 50px rgba(0, 0, 0, 0.4),
                inset 0 2px 0 rgba(255, 255, 255, 0.5),
                inset 0 -2px 0 rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .butterfly-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, 
                transparent, 
                rgba(255, 255, 255, 0.1), 
                transparent,
                rgba(136, 206, 255, 0.15),
                transparent);
            animation: shimmer 5s infinite;
            pointer-events: none;
        }
        
        .butterfly-header span {
            display: inline-block;
            animation: flutter 2.5s infinite ease-in-out;
            filter: drop-shadow(0 0 15px rgba(136, 206, 255, 1));
        }
        
        @keyframes flutter {
            0%, 100% { transform: scale(1) rotate(0deg); }
            25% { transform: scale(1.15) rotate(-8deg); }
            50% { transform: scale(1.25) rotate(0deg); }
            75% { transform: scale(1.15) rotate(8deg); }
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        /* Ultra glass morphism containers */
        .square-container {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(30px);
            border-radius: 30px;
            padding: 2.5rem;
            height: 580px;
            border: 3px solid rgba(255, 255, 255, 0.25);
            box-shadow: 
                0 15px 60px rgba(0, 0, 0, 0.3),
                inset 0 2px 0 rgba(255, 255, 255, 0.4),
                inset 0 -1px 0 rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }
        
        .square-container:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 
                0 25px 80px rgba(0, 0, 0, 0.4),
                inset 0 2px 0 rgba(255, 255, 255, 0.5);
            background: rgba(255, 255, 255, 0.18);
        }
        
        .square-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, 
                transparent, 
                rgba(255,255,255,0.1), 
                transparent,
                rgba(136, 206, 255, 0.08),
                transparent);
            animation: shimmer 6s infinite;
            pointer-events: none;
        }
        
        /* Corner butterflies with enhanced glow */
        .corner-butterfly {
            position: absolute;
            font-size: 1.8rem;
            opacity: 0.8;
            animation: float-magical 4s infinite ease-in-out;
            filter: drop-shadow(0 0 10px rgba(136, 206, 255, 0.8));
            z-index: 10;
        }
        
        .corner-butterfly.top-left {
            top: 20px;
            left: 20px;
            animation-delay: 0s;
        }
        
        .corner-butterfly.top-right {
            top: 20px;
            right: 20px;
            animation-delay: -1.5s;
        }
        
        .corner-butterfly.bottom-left {
            bottom: 20px;
            left: 20px;
            animation-delay: -3s;
        }
        
        .corner-butterfly.bottom-right {
            bottom: 20px;
            right: 20px;
            animation-delay: -2.25s;
        }
        
        @keyframes float-magical {
            0%, 100% { 
                transform: translateY(0px) rotate(0deg) scale(1);
                filter: drop-shadow(0 0 10px rgba(136, 206, 255, 0.8));
            }
            25% { 
                transform: translateY(-12px) rotate(5deg) scale(1.1);
                filter: drop-shadow(0 0 15px rgba(136, 206, 255, 1));
            }
            50% { 
                transform: translateY(-8px) rotate(-3deg) scale(1.05);
                filter: drop-shadow(0 0 20px rgba(136, 206, 255, 0.9));
            }
            75% { 
                transform: translateY(-15px) rotate(8deg) scale(1.12);
                filter: drop-shadow(0 0 18px rgba(136, 206, 255, 1));
            }
        }
        
        /* Ultra-enhanced buttons */
        .stButton button {
            background: linear-gradient(135deg, rgba(136, 206, 255, 0.9) 0%, rgba(102, 126, 234, 0.9) 50%, rgba(118, 75, 162, 0.9) 100%) !important;
            border: 3px solid rgba(255, 255, 255, 0.4) !important;
            color: white !important;
            border-radius: 50px !important;
            font-weight: 700 !important;
            padding: 15px 35px !important;
            font-size: 18px !important;
            font-family: 'Montserrat', sans-serif !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
            backdrop-filter: blur(15px) !important;
            box-shadow: 0 8px 30px rgba(136, 206, 255, 0.5) !important;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        }
        
        .stButton button:hover {
            transform: translateY(-4px) scale(1.08) !important;
            box-shadow: 0 15px 45px rgba(136, 206, 255, 0.8) !important;
            background: linear-gradient(135deg, rgba(136, 206, 255, 1) 0%, rgba(102, 126, 234, 1) 50%, rgba(118, 75, 162, 1) 100%) !important;
            border: 3px solid rgba(255, 255, 255, 0.6) !important;
        }
        
        .stButton button:active {
            transform: translateY(-2px) scale(1.05) !important;
        }
        
        /* Enhanced status indicators */
        .status-indicator {
            display: inline-flex;
            align-items: center;
            padding: 12px 25px;
            border-radius: 30px;
            font-weight: 700;
            margin: 15px 0;
            font-size: 16px;
            font-family: 'Montserrat', sans-serif;
            backdrop-filter: blur(15px);
            border: 2px solid rgba(255, 255, 255, 0.3);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .status-active {
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.9), rgba(69, 160, 73, 0.9));
            color: white;
            box-shadow: 0 0 30px rgba(76, 175, 80, 0.7);
            animation: pulse-intense 2s infinite;
        }
        
        .status-inactive {
            background: rgba(158, 158, 158, 0.4);
            color: rgba(255, 255, 255, 0.8);
            box-shadow: 0 0 15px rgba(158, 158, 158, 0.3);
        }
        
        @keyframes pulse-intense {
            0%, 100% { 
                box-shadow: 0 0 30px rgba(76, 175, 80, 0.7);
                transform: scale(1);
            }
            50% { 
                box-shadow: 0 0 50px rgba(76, 175, 80, 1);
                transform: scale(1.05);
            }
        }
        
        /* Enhanced file uploader */
        .stFileUploader label {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 700 !important;
            color: rgba(255, 255, 255, 0.95) !important;
            font-size: 18px !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
        }
        
        .stFileUploader div[data-testid="stFileUploaderDropzone"] {
            background: rgba(255, 255, 255, 0.15) !important;
            border: 3px dashed rgba(255, 255, 255, 0.4) !important;
            border-radius: 20px !important;
            backdrop-filter: blur(15px) !important;
            transition: all 0.3s ease !important;
        }
        
        .stFileUploader div[data-testid="stFileUploaderDropzone"]:hover {
            background: rgba(255, 255, 255, 0.2) !important;
            border-color: rgba(136, 206, 255, 0.6) !important;
        }
        
        /* Section headers with glow */
        .section-header {
            color: rgba(255, 255, 255, 0.98);
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            font-size: 1.4rem;
            text-shadow: 
                0 2px 4px rgba(0,0,0,0.4),
                0 0 15px rgba(136, 206, 255, 0.6);
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Enhanced metrics */
        .metric-container {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 1.5rem;
            border: 2px solid rgba(255, 255, 255, 0.25);
            text-align: center;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        
        /* Progress bar enhancement */
        .stProgress .st-bo {
            background: rgba(255, 255, 255, 0.3) !important;
            border-radius: 15px !important;
            height: 12px !important;
        }
        
        .stProgress .st-bp {
            background: linear-gradient(90deg, rgba(136, 206, 255, 1), rgba(102, 126, 234, 1)) !important;
            border-radius: 15px !important;
            box-shadow: 0 0 15px rgba(136, 206, 255, 0.6) !important;
        }
        
        /* Video container enhancement */
        .video-container {
            width: 100%;
            height: 320px;
            border-radius: 25px;
            overflow: hidden;
            background: rgba(0, 0, 0, 0.25);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.1);
        }
        
        /* Hide unwanted elements */
        .stDeployButton {
            display: none !important;
        }
    </style>
    """

# Initialize session state
if 'detection_active' not in st.session_state:
    st.session_state.detection_active = False
if 'uploaded_video_path' not in st.session_state:
    st.session_state.uploaded_video_path = None
if 'model' not in st.session_state:
    st.session_state.model = None

# Inject the enhanced CSS
st.markdown(get_enhanced_css(), unsafe_allow_html=True)

# Create the 3D butterfly background
st.markdown("""
<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -100; pointer-events: none;">
""", unsafe_allow_html=True)

# Embed the 3D butterfly background
components.html(create_3d_butterfly_html(), height=0, width=0)

st.markdown("</div>", unsafe_allow_html=True)

# Enhanced butterfly header
st.markdown(
    '<h1 class="butterfly-header"><span>🦋</span> Butterfly Drowning Detection <span>🦋</span></h1>', 
    unsafe_allow_html=True
)

# Create two-column layout for enhanced squares
col1, col2 = st.columns(2, gap="large")

# LEFT SQUARE - Upload and Control Section
with col1:
    st.markdown("""
    <div class="square-container">
        <div class="corner-butterfly top-left">🦋</div>
        <div class="corner-butterfly top-right">🦋</div>
        <div class="corner-butterfly bottom-left">🦋</div>
        <div class="corner-butterfly bottom-right">🦋</div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">📁 Video Upload & Controls</div>', unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose your magical video file",
        type=["mp4", "avi", "mov", "mkv"],
        help="Supported formats: MP4, AVI, MOV, MKV"
    )
    
    if uploaded_file is not None:
        # Save uploaded file to session state
        if st.session_state.uploaded_video_path is None:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
                tfile.write(uploaded_file.read())
                st.session_state.uploaded_video_path = tfile.name
        
        st.success(f"✨ Video loaded: {uploaded_file.name}")
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
        <div style="text-align: center; color: rgba(255, 255, 255, 0.9); font-size: 1.3rem; margin-top: 3rem; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
            ✨ Upload a video to start magical detection ✨
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced status indicator
    if uploaded_file:
        status_class = "status-active" if st.session_state.detection_active else "status-inactive"
        status_text = "🟢 DETECTION ACTIVE" if st.session_state.detection_active else "⚪ DETECTION INACTIVE"
        st.markdown(f'<div class="status-indicator {status_class}">{status_text}</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT SQUARE - Detection Results Section  
with col2:
    st.markdown("""
    <div class="square-container">
        <div class="corner-butterfly top-left">🦋</div>
        <div class="corner-butterfly top-right">🦋</div>
        <div class="corner-butterfly bottom-left">🦋</div>
        <div class="corner-butterfly bottom-right">🦋</div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">🔍 Real-Time Detection Results</div>', unsafe_allow_html=True)
    
    if uploaded_file and st.session_state.detection_active:
        # Initialize YOLO model if not already loaded
        if st.session_state.model is None:
            with st.spinner("🦋 Loading magical YOLOv8 model..."):
                st.session_state.model = YOLO('yolov8n.pt')
        
        # Process video
        if st.session_state.uploaded_video_path:
            cap = cv2.VideoCapture(st.session_state.uploaded_video_path)
            
            # Video info
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            
            # Create placeholder for video stream
            stframe = st.empty()
            
            # Enhanced progress bar
            progress_bar = st.progress(0)
            
            # Detection statistics with enhanced styling
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
                                # Enhanced drowning detection simulation
                                detection_score = np.random.random()
                                
                                if detection_score > 0.7:
                                    label = "Swimming"
                                    color = (0, 255, 0)  # Green
                                    swimming_count += 1
                                else:
                                    label = "Drowning"
                                    color = (0, 0, 255)  # Red
                                    drowning_count += 1
                                
                                # Draw enhanced bounding box
                                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)
                                
                                # Add enhanced label
                                label_text = f"{label}: {confidence:.2f}"
                                cv2.putText(frame, label_text, (x1, y1-15),
                                          cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
                
                # Convert and display frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                stframe.image(frame_rgb, channels="RGB", use_column_width=True)
                
                # Update enhanced metrics
                swimming_metric.metric("🏊‍♂️ Swimming", swimming_count)
                drowning_metric.metric("🆘 Drowning", drowning_count)
                
                frame_count += 1
                
                # Enhanced real-time delay
                time.sleep(0.05)
            
            cap.release()
            
            # Final results with celebration
            st.success("✨ Magical detection completed! ✨")
            
    elif uploaded_file and not st.session_state.detection_active:
        st.markdown("""
        <div style="text-align: center; color: rgba(255, 255, 255, 0.9); font-size: 1.2rem; margin-top: 4rem; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
            🎬 Press 'Play & Detect' to start magical analysis<br><br>
            <span style="font-size: 0.95rem; opacity: 0.8;">
            The butterflies are waiting to help detect drowning...
            </span>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.markdown("""
        <div style="text-align: center; color: rgba(255, 255, 255, 0.8); font-size: 1.2rem; margin-top: 4rem; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
            ✨ Upload a video first ✨<br><br>
            <span style="font-size: 1rem; opacity: 0.7;">
            The magical butterflies will help analyze your video<br>
            for swimming and drowning detection
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Enhanced footer with butterfly theme
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255, 255, 255, 0.9); font-family: 'Montserrat', sans-serif; margin-top: 3rem; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
    <span style="font-size: 1.5rem;">🦋</span> 
    <strong>Built with magical butterflies, love, and advanced AI</strong>
    <span style="font-size: 1.5rem;">🦋</span><br>
    <span style="font-size: 0.9rem; opacity: 0.8;">
    Powered by Streamlit, YOLOv8 & Three.js Butterfly Magic
    </span>
</div>
""", unsafe_allow_html=True)
