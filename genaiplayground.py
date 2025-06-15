import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env for local testing
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("⚠️ API key not found. Make sure your .env file contains GOOGLE_API_KEY.")
    st.stop()

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-pro")

# Streamlit config
st.set_page_config(page_title="GenAI Playground", layout="wide")
st.title("🤖 Google Generative AI Playground")

# Sidebar settings
with st.sidebar:
    st.header("🛠️ Model Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.slider("Max Output Tokens", 100, 2048, 512)
    top_k = st.slider("Top-k", 1, 100, 40)
    top_p = st.slider("Top-p (Nucleus Sampling)", 0.0, 1.0, 0.9)
    user_prompt = st.text_area("System Instruction (Optional)", value="You are a helpful assistant.")

# Prompt area
prompt = st.text_area("💬 Enter your prompt here", height=200)

# Generate
if st.button("Generate"):
    if not prompt.strip():
        st.warning("Please enter a prompt first.")
    else:
        with st.spinner("Generating response..."):
            try:
                generation_config = genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    top_k=top_k,
                    top_p=top_p,
                )

                response = model.generate_content(
                    prompt,
                    generation_config=generation_config,
                    system_instruction=user_prompt if user_prompt.strip() else None
                )

                st.markdown("### ✨ Response")
                st.write(response.text)

            except Exception as e:
                st.error(f"🚨 Error: {e}")
