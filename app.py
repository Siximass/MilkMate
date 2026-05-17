import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai

from rag_engine import RAGEngine


st.set_page_config(
    page_title="Carey | Car Care AI Assistant",
    page_icon="🚗",
    layout="wide",
)

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = "gemini-2.5-flash"

KB_PATH = Path(__file__).resolve().parent / "knowledge" / "carcare_kb.txt"


@st.cache_resource
def load_rag():
    return RAGEngine(str(KB_PATH))


rag = load_rag()


st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(56, 189, 248, 0.20), transparent 34%),
            radial-gradient(circle at bottom right, rgba(34, 197, 94, 0.10), transparent 32%),
            linear-gradient(135deg, #07111f 0%, #0f172a 48%, #111827 100%);
        color: #f8fafc;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 2rem;
    }

    .hero-card {
        background:
            linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(30, 41, 59, 0.9)),
            linear-gradient(90deg, rgba(125, 211, 252, 0.08), transparent);
        border: 1px solid rgba(186, 230, 253, 0.18);
        border-radius: 30px;
        padding: 34px 38px;
        box-shadow: 0 26px 76px rgba(0, 0, 0, 0.38);
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }

    .hero-card::after {
        content: "";
        position: absolute;
        right: -80px;
        top: -80px;
        width: 260px;
        height: 260px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.26), transparent 65%);
        border-radius: 50%;
    }

    .eyebrow {
        color: #7dd3fc;
        font-size: 14px;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .hero-title {
        font-size: 48px;
        line-height: 1.12;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 12px;
    }

    .hero-subtitle {
        font-size: 17px;
        color: #d1d5db;
        max-width: 790px;
        line-height: 1.75;
        margin-bottom: 22px;
    }

    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .badge {
        background: rgba(14, 165, 233, 0.16);
        border: 1px solid rgba(125, 211, 252, 0.34);
        color: #dff6ff;
        padding: 8px 14px;
        border-radius: 999px;
        font-size: 14px;
        font-weight: 650;
    }

    .section-title {
        font-size: 22px;
        font-weight: 850;
        color: #ffffff;
        margin: 26px 0 14px 0;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
        margin-bottom: 8px;
    }

    .stat-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.86));
        border: 1px solid rgba(186, 230, 253, 0.14);
        border-radius: 22px;
        padding: 18px;
        box-shadow: 0 14px 38px rgba(0, 0, 0, 0.25);
    }

    .stat-label {
        font-size: 13px;
        color: #a8c7d8;
        margin-bottom: 8px;
    }

    .stat-value {
        font-size: 24px;
        color: #ffffff;
        font-weight: 900;
        margin-bottom: 4px;
    }

    .stat-note {
        font-size: 13px;
        color: #86efac;
    }

    .service-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px;
        margin-bottom: 12px;
    }

    .service-card {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(186, 230, 253, 0.14);
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 16px 45px rgba(0, 0, 0, 0.26);
        min-height: 175px;
        position: relative;
        overflow: hidden;
    }

    .service-card::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #38bdf8, #86efac, #e5e7eb);
        opacity: 0.78;
    }

    .package-label {
        display: inline-block;
        background: rgba(56, 189, 248, 0.14);
        border: 1px solid rgba(125, 211, 252, 0.30);
        color: #dff6ff;
        font-size: 12px;
        font-weight: 800;
        padding: 5px 10px;
        border-radius: 999px;
        margin-bottom: 12px;
    }

    .service-card h3 {
        font-size: 18px;
        margin: 0 0 8px 0;
        color: #ffffff;
    }

    .service-card p {
        font-size: 14px;
        color: #d1d5db;
        margin: 0;
        line-height: 1.65;
    }

    .promo-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
        margin-bottom: 20px;
    }

    .promo-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.88), rgba(15, 23, 42, 0.86));
        border: 1px solid rgba(186, 230, 253, 0.14);
        border-radius: 22px;
        padding: 18px;
        box-shadow: 0 14px 36px rgba(0, 0, 0, 0.23);
    }

    .promo-card h4 {
        font-size: 16px;
        color: #bae6fd;
        margin: 0 0 8px 0;
    }

    .promo-card p {
        font-size: 13.5px;
        color: #e5e7eb;
        line-height: 1.55;
        margin: 0;
    }

    .workflow-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
        margin-bottom: 18px;
    }

    .workflow-card {
        background: rgba(8, 13, 23, 0.48);
        border: 1px solid rgba(186, 230, 253, 0.12);
        border-radius: 22px;
        padding: 18px;
        min-height: 130px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.22);
    }

    .workflow-step {
        width: 34px;
        height: 34px;
        border-radius: 999px;
        background: rgba(14, 165, 233, 0.20);
        border: 1px solid rgba(125, 211, 252, 0.35);
        color: #e0f2fe;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        margin-bottom: 12px;
    }

    .workflow-card h4 {
        font-size: 15.5px;
        color: #ffffff;
        margin: 0 0 7px 0;
    }

    .workflow-card p {
        font-size: 13.5px;
        color: #d1d5db;
        line-height: 1.55;
        margin: 0;
    }

    .chat-panel {
        background: rgba(8, 13, 23, 0.50);
        border: 1px solid rgba(186, 230, 253, 0.12);
        border-radius: 26px;
        padding: 18px 20px 8px 20px;
        margin-top: 12px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.28);
    }

    .hint-box {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(125, 211, 252, 0.18);
        border-radius: 22px;
        padding: 18px;
        margin-bottom: 16px;
        color: #d1d5db;
        line-height: 1.65;
    }

    .footer {
        margin-top: 28px;
        padding: 18px 20px;
        border-top: 1px solid rgba(186, 230, 253, 0.12);
        color: #9ca3af;
        font-size: 13.5px;
        text-align: center;
    }

    .footer strong {
        color: #e5e7eb;
    }

    [data-testid="stChatMessage"] {
        background: rgba(15, 23, 42, 0.82);
        border: 1px solid rgba(186, 230, 253, 0.12);
        border-radius: 20px;
        padding: 12px;
        margin-bottom: 14px;
    }

    .stButton > button {
        border-radius: 999px;
        border: 1px solid rgba(125, 211, 252, 0.34);
        background: rgba(14, 165, 233, 0.14);
        color: #e5e7eb;
        padding: 0.55rem 0.9rem;
        font-weight: 700;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border-color: rgba(186, 230, 253, 0.72);
        background: rgba(14, 165, 233, 0.25);
        color: #ffffff;
        transform: translateY(-1px);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #07111f 0%, #0f172a 100%);
        border-right: 1px solid rgba(186, 230, 253, 0.10);
    }

    @media (max-width: 900px) {
        .hero-title {
            font-size: 34px;
        }

        .hero-card {
            padding: 26px;
        }

        .stats-grid,
        .service-grid,
        .promo-grid,
        .workflow-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.markdown("## 🚗 Car Care")
    st.markdown("**Carey AI Assistant**")
    st.markdown("---")
    st.markdown("### 🕒 เวลาเปิดร้าน")
    st.write("08:00–18:00 น. ทุกวัน")
    st.markdown("### 💧 บริการยอดนิยม")
    st.write("ล้างรถ • ดูดฝุ่น • เคลือบสี • เคลือบกระจก")
    st.markdown("### 🎉 โปรเโมชั่น")
    st.write("Student Clean • Premium Friday • Rainy Care")
    st.markdown("### 🤖 ระบบ")
    st.write("RAG Chatbot + Gemini API")
    st.markdown("---")
    st.caption("Carey ตอบจาก knowledge base ของร้าน Car Care")


st.markdown(
    """
    <div class="hero-card">
        <div class="eyebrow">Clean Car, Easy Price</div>
        <div class="hero-title">🚗 Carey ผู้ช่วย AI ของ Car Care</div>
        <div class="hero-subtitle">
            ผู้ช่วยตอบคำถามเรื่องราคา แพ็กเกจ โปรโมชัน และการจองคิว
            สำหรับร้านล้างรถที่ดูสะอาด เป็นกันเอง และเริ่มต้นในราคาที่เข้าถึงได้
        </div>
        <div class="badge-row">
            <span class="badge">Friendly Service</span>
            <span class="badge">Easy Price</span>
            <span class="badge">RAG Chatbot</span>
            <span class="badge">Demo Day Ready</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">เปิดบริการ</div>
            <div class="stat-value">ทุกวัน</div>
            <div class="stat-note">08:00–18:00 น.</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">เริ่มต้นสบายกระเป๋า</div>
            <div class="stat-value">60฿</div>
            <div class="stat-note">ล้างมอเตอร์ไซค์</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">ใช้เวลาเร็วสุด</div>
            <div class="stat-value">15 นาที</div>
            <div class="stat-note">ขึ้นอยู่กับประเภทรถ</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">โปรสำหรับนักศึกษา</div>
            <div class="stat-value">10%</div>
            <div class="stat-note">Student Clean</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="section-title">แพ็กเกจแนะนำ</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="service-grid">
        <div class="service-card">
            <span class="package-label">เริ่มต้นง่าย</span>
            <h3>🧼 Basic Wash</h3>
            <p>ล้างภายนอก เช็ดแห้ง และทำความสะอาดล้อ เหมาะกับการดูแลรถประจำวันแบบรวดเร็ว</p>
        </div>
        <div class="service-card">
            <span class="package-label">ยอดนิยม</span>
            <h3>✨ Interior Clean</h3>
            <p>ดูดฝุ่น เช็ดคอนโซล เช็ดเบาะ และทำความสะอาดภายใน เหมาะกับรถที่ใช้งานทุกวัน</p>
        </div>
        <div class="service-card">
            <span class="package-label">แนะนำ</span>
            <h3>💙 Premium Shine</h3>
            <p>ล้างรถ ดูดฝุ่นภายใน และเคลือบเงาสีรถ ให้รถดูสะอาด เงา และน่าใช้งานขึ้น</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="section-title">โปรโมชันเด่น</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="promo-grid">
        <div class="promo-card">
            <h4>🎓 Student Clean</h4>
            <p>นักศึกษาลด 10% เมื่อแสดงบัตรนักศึกษา</p>
        </div>
        <div class="promo-card">
            <h4>🌧 Rainy Care</h4>
            <p>แพ็กเกจหน้าฝน Rain Protection ลดเหลือ 499 บาท</p>
        </div>
        <div class="promo-card">
            <h4>✨ Premium Friday</h4>
            <p>ทุกวันศุกร์ Premium Shine เหลือ 399 บาท</p>
        </div>
        <div class="promo-card">
            <h4>🚘 Couple Wash</h4>
            <p>ล้างรถ 2 คันในบิลเดียว ลดทันที 30 บาท</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="section-title">Carey ทำงานยังไง</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="workflow-grid">
        <div class="workflow-card">
            <div class="workflow-step">1</div>
            <h4>ลูกค้าถาม</h4>
            <p>พิมพ์คำถามเกี่ยวกับราคา แพ็กเกจ โปรโมชัน หรือการจองคิว</p>
        </div>
        <div class="workflow-card">
            <div class="workflow-step">2</div>
            <h4>ค้นข้อมูลร้าน</h4>
            <p>ระบบค้นหาข้อมูล Car Care ที่เกี่ยวข้องจาก knowledge base</p>
        </div>
        <div class="workflow-card">
            <div class="workflow-step">3</div>
            <h4>สร้างคำตอบ</h4>
            <p>Gemini ช่วยเรียบเรียงคำตอบภาษาไทยให้เข้าใจง่ายและเป็นกันเอง</p>
        </div>
        <div class="workflow-card">
            <div class="workflow-step">4</div>
            <h4>ตอบกลับทันที</h4>
            <p>Carey ตอบเหมือนผู้ช่วยหน้าร้าน โดยอ้างอิงจากข้อมูลจริงของร้าน</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="section-title">ลองถาม Carey</div>', unsafe_allow_html=True)

quick_questions = [
    "ร้านเปิดกี่โมง",
    "ล้างรถเก๋งราคาเท่าไหร่",
    "มีโปรนักศึกษาไหม",
    "รถสีดำควรเลือกแพ็กเกจไหน",
    "ช่วงหน้าฝนควรเลือกแพ็กเกจไหน",
    "ต้องจองคิวก่อนไหม",
    "รถเลอะโคลนคิดเพิ่มไหม",
    "มีแพ็กเกจอะไรบ้าง",
]

if "queued_prompt" not in st.session_state:
    st.session_state.queued_prompt = None

cols = st.columns(4)
for index, question in enumerate(quick_questions):
    with cols[index % 4]:
        if st.button(question, key=f"quick_{index}"):
            st.session_state.queued_prompt = question


st.markdown(
    """
    <div class="hint-box">
        💡 Carey จะตอบจากข้อมูลร้าน Car Care เท่านั้น หากไม่มีข้อมูลใน knowledge base
        ระบบจะตอบว่า <strong>ไม่ทราบจากข้อมูลร้านที่มีอยู่</strong> เพื่อลดการแต่งข้อมูลเอง
    </div>
    """,
    unsafe_allow_html=True,
)


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "สวัสดีค่ะ ฉันคือ Carey ผู้ช่วย AI ของร้าน Car Care ถามเรื่องราคา แพ็กเกจ โปรโมชัน หรือการจองคิวได้เลยค่ะ",
        }
    ]


def generate_answer(prompt: str) -> str:
    context_chunks = rag.search(prompt, top_k=4)
    context = "\n---\n".join(context_chunks)

    full_prompt = f"""
คุณคือ Carey ผู้ช่วย AI ของร้าน Car Care
ให้ตอบคำถามโดยอ้างอิงเฉพาะข้อมูลร้านด้านล่างเท่านั้น
ถ้าไม่พบข้อมูล ให้ตอบว่า "ไม่ทราบจากข้อมูลร้านที่มีอยู่"
ห้ามแต่งข้อมูลเอง

สไตล์การตอบ:
- ตอบเป็นภาษาไทย
- สุภาพ เป็นกันเอง เหมือนพนักงานหน้าร้าน
- ตอบให้ชัดเจน กระชับ และเข้าใจง่าย
- ถ้าเป็นเรื่องราคา เวลา หรือโปรโมชั่น ให้ตอบตัวเลขให้ชัดเจน

ข้อมูลร้าน:
{context}

คำถาม: {prompt}
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=full_prompt,
        )
        return response.text

    except Exception as e:
        error_text = str(e)

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text or "quota" in error_text.lower():
            return "ตอนนี้ระบบเรียกใช้งาน Gemini API เกินโควตาชั่วคราว กรุณารอสักครู่แล้วลองใหม่อีกครั้งค่ะ"

        return "เกิดข้อผิดพลาดในการเรียกใช้งาน AI กรุณาลองใหม่อีกครั้งค่ะ"


st.markdown('<div class="chat-panel">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

typed_prompt = st.chat_input("ถาม Carey เกี่ยวกับร้าน Car Care ได้เลย...")

prompt = None

if typed_prompt:
    prompt = typed_prompt
elif st.session_state.queued_prompt:
    prompt = st.session_state.queued_prompt
    st.session_state.queued_prompt = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    answer = generate_answer(prompt)

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)

st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    """
    <div class="footer">
        <strong>Carey by Car Care</strong> · Clean Modern RAG Chatbot · Built with Streamlit + Gemini
    </div>
    """,
    unsafe_allow_html=True,
)