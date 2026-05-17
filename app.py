import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai

from rag_engine import RAGEngine


load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = "gemini-2.5-flash"

KB_PATH = Path(__file__).resolve().parent / "knowledge" / "carcare_kb.txt"


@st.cache_resource
def load_rag():
    return RAGEngine(str(KB_PATH))


rag = load_rag()

st.title("🚗 Carey ผู้ช่วย AI ของ Car Care")
st.caption("ถามเรื่องแพ็กเกจล้างรถ ราคา บริการเสริม เวลาเปิดร้าน หรือการจองคิวได้เลย")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("ถามอะไรเกี่ยวกับร้าน Car Care ได้เลย..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    context_chunks = rag.search(prompt, top_k=3)
    context = "\n---\n".join(context_chunks)

    full_prompt = f"""
คุณคือ Carey ผู้ช่วย AI ของร้าน Car Care
ให้ตอบคำถามโดยอ้างอิงเฉพาะข้อมูลร้านด้านล่างเท่านั้น
ถ้าไม่พบข้อมูล ให้ตอบว่า "ไม่ทราบจากข้อมูลร้านที่มีอยู่"
ห้ามแต่งข้อมูลเอง

ข้อมูลร้าน:
{context}

คำถาม: {prompt}
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=full_prompt,
        )
        answer = response.text

    except Exception as e:
        error_text = str(e)

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text or "quota" in error_text.lower():
            answer = "ตอนนี้ระบบเรียกใช้งาน Gemini API เกินโควตาชั่วคราว กรุณารอสักครู่แล้วลองใหม่อีกครั้งค่ะ"
        else:
            answer = "เกิดข้อผิดพลาดในการเรียกใช้งาน AI กรุณาลองใหม่อีกครั้งค่ะ"

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)