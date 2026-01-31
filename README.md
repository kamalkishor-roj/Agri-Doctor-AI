# 🌿 Agri-Doctor: AI-Powered Crop Disease Detective

![Python](https://img.shields.io/badge/Python-3.10-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Groq](https://img.shields.io/badge/AI-Llama3-purple)

## Overview
**Agri-Doctor** is an end-to-end AI application designed to assist farmers in early detection and treatment of crop diseases. Agriculture is the backbone of many economies, yet farmers lose significant yields annually due to untreated or misdiagnosed plant diseases.

This project bridges the gap between complex technology and the farm field. By simply uploading a photo of a leaf, the system identifies the specific disease and—crucially—provides an instant, actionable prescription (chemical and organic) using a Large Language Model (LLM).

## Key Features
* **Multi-Crop Support:** Specialized diagnosis for **Rice, Sugarcane, Tomato, and Grapes**.
* **Hybrid AI Architecture:**
    * **Vision:** A fine-tuned **MobileNetV2** (CNN) model to classify 23 distinct disease classes.
    * **Language:** Integrated **Groq API (Llama-3-70b)** to generate human-readable medical advice, treatment steps, and prevention tips.
* **Smart Logic Filter:** Implements a custom probability filter to eliminate confusion between visually similar crops (e.g., Rice vs. Sugarcane leaves).
* **Interactive Chat:** Users can ask follow-up questions to the "AI Doctor" (e.g., *"Is this pesticide safe for pets?"*) and get context-aware answers.

## 🛠️ Tech Stack
* **Deep Learning:** TensorFlow, Keras (Transfer Learning with MobileNetV2).
* **Generative AI:** Groq API (Llama 3.3 Versatile).
* **Web Framework:** Streamlit (Python).
* **Image Processing:** PIL (Python Imaging Library), NumPy.

## 📊 Dataset & Model Results
The model was trained on a curated dataset combining the **Plant Village Dataset** and custom web-scraped images for Rice and Sugarcane.
* **Total Classes:** 23 (Including healthy and diseased states).
* **Training Accuracy:** ~80% (after fine-tuning top layers).
* **Validation Accuracy:** ~78%.
* **Optimization:** Uses `tf.data.AUTOTUNE` for high-performance data pipelines and data augmentation (rotation, zoom, contrast) to handle real-world field conditions.

## How It Works
1. **Select Crop:** User selects the crop type (Rice, Tomato, etc.) from the sidebar.
2. **Upload Image:** User uploads a photo of the affected leaf.
3. **AI Diagnosis:**
    * The **CNN Model** analyzes the texture/shape to find the disease (e.g., *Early Blight*).
    * The **Logic Filter** ensures the diagnosis matches the selected crop type.
4. **Prescription:** The **LLM (Groq)** receives the diagnosis and writes a custom treatment plan (Cause, Medicine, Prevention).

## 📱 App Demo

**1. Disease Diagnosis & Medical Prescription**
![Diagnosis Result](screenshots/diagnosis.png)

**2. AI Doctor Chat Interface**
![Chat Interface](screenshots/chat.png)

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.8+
* A free [Groq API Key](https://console.groq.com/keys)

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/Agri-Doctor.git](https://github.com/your-username/Agri-Doctor.git)
cd Agri-Doctor

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Set Up API Key (Securely)

Create a `.streamlit` folder and a `secrets.toml` file to store your key safely.

**Windows:**

```bash
mkdir .streamlit
notepad .streamlit/secrets.toml

```

**Inside `secrets.toml`, paste your key:**

```toml
GROQ_API_KEY = "gsk_your_key_here"

```

### 4. Run the App

```bash
python -m streamlit run app.py

```

## 📂 Project Structure

```text
Agri-Doctor/
├── MultiCrop_Doctor_v1.keras    # The trained AI Brain (CNN)
├── app.py                       # Main Streamlit Application
├── requirements.txt             # List of dependencies
├── README.md                    # Project Documentation
├── screenshots/                 # Images for README
│   ├── diagnosis.png
│   └── chat.png
└── .streamlit/                  # Hidden folder for secrets
    └── secrets.toml             # API Key storage (Do not upload to GitHub)

```

## Future Scope

* **Offline Mode:** Convert the model to TensorFlow Lite for a mobile Android app.
* **Local Language Support:** Add Hindi/Regional language support for wider accessibility in rural India.
* **Fertilizer Calculator:** Add a tool to calculate NPK requirements based on crop stage.

## Contributing

Contributions are welcome! Please fork this repository and submit a Pull Request.







