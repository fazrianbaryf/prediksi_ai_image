import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import requests
from io import BytesIO
import time
import os

# --- Page Config ---
st.set_page_config(
    page_title="AI vs Human Art Detector",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for "Web-like" Feel ---
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(18, 18, 28) 0%, rgb(28, 28, 48) 90%);
        color: #ffffff;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(25, 25, 35, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Cards/Containers */
    .stCard {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        border: none;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 210, 255, 0.4);
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        border: 1px dashed rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        padding: 20px;
    }
    
    /* Results */
    .result-box {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        animation: fadeIn 1s ease-in;
    }
    
    .real-art {
        background: rgba(76, 175, 80, 0.2);
        border: 1px solid #4CAF50;
        color: #81c784;
    }
    
    .ai-art {
        background: rgba(244, 67, 54, 0.2);
        border: 1px solid #f44336;
        color: #e57373;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Model Loading ---
@st.cache_resource
def load_model():
    model_path_keras = 'model.keras'
    model_path_h5 = 'model.h5'
    
    path_to_use = None
    if os.path.exists(model_path_keras):
        path_to_use = model_path_keras
    elif os.path.exists(model_path_h5):
        path_to_use = model_path_h5
    else:
        return None

    try:
        model = tf.keras.models.load_model(path_to_use)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# --- App Structure ---

with st.sidebar:
    st.title("🤖 AI vs Human")
    st.markdown("---")
    st.markdown("### 📤 Input Source")
    
    upload_option = st.radio("Choose input method:", ("Upload Image", "Image URL"))
    
    image = None
    if upload_option == "Upload Image":
        uploaded_file = st.file_uploader("Drag & drop or browse", type=["jpg", "png", "jpeg", "webp"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            
    elif upload_option == "Image URL":
        url = st.text_input("Paste Image URL here")
        if url:
            try:
                response = requests.get(url)
                image = Image.open(BytesIO(response.content))
            except:
                st.error("Invalid URL or unable to load image.")

    st.markdown("---")
    st.info("💡 **Tip:** For best results, use high-quality images.")
    st.markdown("Made with ❤️ for Deep Learning")

# --- Main Content ---

st.markdown("<div style='text-align: center; margin-bottom: 40px;'><h1>🎨 Art Authenticator</h1><p style='font-size: 1.2rem; opacity: 0.8;'>Discover the origin of your masterpiece: Human Genius or Artificial Intelligence?</p></div>", unsafe_allow_html=True)

if model is None:
    st.error("⚠️ Model file not found! Please ensure 'model.keras' or 'model.h5' is in the directory.")
else:
    if image:
        # Display Image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🖼️ Your Image")
            st.image(image, use_container_width=True, caption="Input Image")
        
        with col2:
            st.markdown("### 🕵️ Analysis")
            
            if st.button("Analyze Art", key="analyze_btn"):
                with st.spinner("🔍 Examining nuances, brushstrokes, and noise patterns..."):
                    # Simulation for UX
                    time.sleep(1.5) 
                    
                    # Preprocessing
                    img = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
                    img_array = np.asarray(img)
                    img_array = img_array / 255.0  # Normalize if model expects [0,1]
                    img_array = np.expand_dims(img_array, axis=0) # Batch dimension

                    # Prediction
                    try:
                        prediction = model.predict(img_array)
                        score = prediction[0][0] # Assuming sigmoid output [0, 1]
                        
                        # Logic: 0 = AI, 1 = Real (adjust based on user's model)
                        # Typically keys are sorted alphabetically: AI vs Human -> AI=0, Human=1
                        
                        is_human = score > 0.5
                        confidence = score if is_human else 1 - score
                        
                        st.balloons() if is_human else None
                        
                        result_class = "real-art" if is_human else "ai-art"
                        result_text = "✨ Human Created" if is_human else "🤖 AI Generated"
                        icon = "🎨" if is_human else "💾"
                        
                        st.markdown(f"""
                        <div class="result-box {result_class}">
                            <div style="font-size: 3rem; margin-bottom: 10px;">{icon}</div>
                            <h2 style="margin:0; color: inherit;">{result_text}</h2>
                            <p style="font-size: 1.1rem; margin-top: 10px;">Confidence Score</p>
                            <h3 style="font-size: 2.5rem; color: inherit;">{confidence:.1%}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Extra metrics
                        st.markdown("### 📊 Detailed Composition")
                        st.progress(int(confidence * 100))
                        st.caption(f"Probability of being {result_text}")

                    except Exception as e:
                        st.error(f"Prediction Error: {e}")
            else:
                st.markdown("""
                <div class="stCard">
                    <h3>Ready to Scan?</h3>
                    <p>Click the button above to start the deep learning analysis.</p>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # Empty State
        st.markdown("""
        <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 300px; border: 2px dashed rgba(255,255,255,0.1); border-radius: 20px;'>
            <div style='font-size: 4rem; opacity: 0.5;'>🖼️</div>
            <p style='margin-top: 20px; font-size: 1.2rem; opacity: 0.6;'>Upload an image from the sidebar to begin</p>
        </div>
        """, unsafe_allow_html=True)

