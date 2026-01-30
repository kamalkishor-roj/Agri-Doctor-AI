import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from groq import Groq

# ==========================================
# 1. CONFIGURATION & SECRETS
# ==========================================
st.set_page_config(
    page_title="Agri-Doctor AI",
    page_icon="🌿",
    layout="wide"
)

# --- SECRETS MANAGEMENT (GITHUB SAFE) ---
# Instead of pasting the key here, we read it from a hidden file.
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("❌ Missing API Key! Please create a `.streamlit/secrets.toml` file.")
    st.stop()

# Configure Groq Client
client = Groq(api_key=GROQ_API_KEY)

# --- MODEL LOADING ---
@st.cache_resource
def load_model():
    # Load your local Keras model
    try:
        return tf.keras.models.load_model('Agri_Doctor_Final.keras')
    except Exception as e:
        st.error(f"Error loading model file: {e}")
        return None

model = load_model()

# Your Class Names (Exactly as trained)
CLASS_NAMES = [
    'Grape_Plant_from_Plant_Village_Dataset', # ❌ BAD LABEL (Index 0)
    'Grape___Black_rot', 
    'Grape___Esca_(Black_Measles)', 
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
    'Grape___healthy', 
    'Rice_Bacterial_leaf_blight', 
    'Rice_Brown_spot', 
    'Rice_Leaf_smut', 
    'Sugarcane_Healthy', 
    'Sugarcane_Mosaic', 
    'Sugarcane_RedRot', 
    'Sugarcane_Rust', 
    'Sugarcane_Yellow', 
    'Tomato_Bacterial_spot', 
    'Tomato_Early_blight', 
    'Tomato_Late_blight', 
    'Tomato_Leaf_Mold', 
    'Tomato_Septoria_leaf_spot', 
    'Tomato_Spider_mites_Two_spotted_spider_mite', 
    'Tomato_Target_Spot', 
    'Tomato_Tomato_YellowLeaf__Curl_Virus', 
    'Tomato_Tomato_mosaic_virus', 
    'Tomato_healthy'
]

# ==========================================
# 2. THE AI BRAIN (GROQ / LLAMA 3)
# ==========================================
def get_medical_advice(disease_name, crop_name):
    prompt = f"""
    You are an expert agriculturalist.
    The user has detected {disease_name} on their {crop_name} plant.
    Provide a concise report:
    1. **What is it?** (1 sentence explanation).
    2. **Treatment:** List 3 effective treatments.
    3. **Prevention:** One simple tip.
    Keep it professional but easy to understand.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful agriculture expert."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile", # The best free model currently
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"

# ==========================================
# 3. UI LAYOUT & LOGIC
# ==========================================
st.title("🌿 Agri-Doctor: AI Disease Detective")
st.markdown("---")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    crop_choice = st.selectbox("Select Your Crop:", ["Rice", "Sugarcane", "Tomato", "Grape"])
    st.info(f"Currently Analyzing: **{crop_choice}**")
    st.write("---")
    st.caption("Powered by MobileNetV2 & Llama 3")

# Main Interface
col1, col2 = st.columns([1, 1])

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    
    with col1:
        st.image(image, caption='Uploaded Leaf', use_container_width=True)
    
    with col2:
        if st.button('🔍 Analyze Leaf', type="primary"):
            with st.spinner('Dr. AI is examining the leaf...'):
                if model is None:
                    st.error("Model not loaded.")
                    st.stop()

                # VISION PREDICTION
                img_array = np.array(image.resize((224, 224)))
                img_array = tf.expand_dims(img_array, 0)
                predictions = model.predict(img_array)[0]
                
                # --- SMART LOGIC FILTER ---
                filtered_preds = []
                for i, score in enumerate(predictions):
                    label = CLASS_NAMES[i]
                    
                    # 1. Zero out "Wrong Crops"
                    if crop_choice.lower() not in label.lower():
                        filtered_preds.append(0.0)
                        continue
                        
                    # 2. 🚨 Zero out the "JUNK LABEL"
                    if label == 'Grape_Plant_from_Plant_Village_Dataset':
                        filtered_preds.append(0.0)
                    else:
                        filtered_preds.append(score)
                
                # Get Winner
                best_idx = np.argmax(filtered_preds)
                best_label = CLASS_NAMES[best_idx]
                confidence = filtered_preds[best_idx] * 100

                # DISPLAY RESULTS
                if confidence > 10:
                    st.success(f"**Diagnosis:** {best_label}")
                    st.metric("Confidence Score", f"{confidence:.1f}%")
                    
                    # Save context
                    st.session_state.diagnosis = best_label
                    st.session_state.crop = crop_choice
                    
                    # GET ADVICE
                    with st.spinner("Consulting the specialist..."):
                        advice = get_medical_advice(best_label, crop_choice)
                        st.markdown(advice)
                        # Save to chat history
                        st.session_state.messages.append({"role": "assistant", "content": advice})
                else:
                    st.error(f"⚠️ Unsure. This doesn't look like {crop_choice}.")
                    st.info("Try selecting a different crop in the sidebar.")

# ==========================================
# 4. CHAT INTERFACE
# ==========================================
st.markdown("---")
st.subheader("💬 Ask the Doctor")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a follow-up question (e.g., 'Is this organic?')"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Context-Aware Prompt
    if "diagnosis" in st.session_state:
        context = f"Context: User has {st.session_state.crop} with {st.session_state.diagnosis}. Answer: {prompt}"
    else:
        context = f"Answer this farming question: {prompt}"

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": context}],
                    model="llama-3.3-70b-versatile",
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")