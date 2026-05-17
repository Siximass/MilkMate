# Car Care AI Assistant

โปรเจกต์นี้เป็นระบบ AI สำหรับร้านล้างรถ **Car Care**  
โดยมีผู้ช่วย AI ชื่อ **Carey** ที่ช่วยตอบคำถามลูกค้า สร้างแคปชันโปรโมชัน และรองรับการต่อยอดเพื่อบันทึกยอดขายของบริการล้างรถ

## Project Info

- Business name: Car Care
- AI assistant name: Carey
- Domain: ร้านล้างรถ
- Main chatbot file: `app.py`
- RAG engine: `rag_engine.py`
- Knowledge base: `knowledge/carcare_kb.txt`
- Language: Python
- API: Gemini API
- UI: Streamlit
- Deploy: HuggingFace Spaces

## Features

### 1. RAG Chatbot

Carey สามารถตอบคำถามจาก knowledge base ของร้าน Car Care เช่น

- ราคาแพ็กเกจล้างรถ
- ประเภทบริการ
- บริการเสริม
- เวลาเปิดร้าน
- การจองคิว
- คำแนะนำช่วงหน้าฝน

ถ้าไม่มีข้อมูลใน knowledge base ระบบจะตอบว่าไม่ทราบจากข้อมูลร้านที่มีอยู่ เพื่อลดการแต่งข้อมูลเอง

### 2. Caption Generator

ใช้ Gemini API เพื่อช่วยสร้างแคปชันโปรโมตบริการของร้าน เช่น

- โปรล้างรถหน้าฝน
- โปรเคลือบสี
- โปรล้างภายใน
- โปรล้างรถมอเตอร์ไซค์

### 3. Sales Logger

สามารถต่อยอดเพื่อบันทึกยอดขายจากบริการต่าง ๆ เช่น

- ล้างรถเก๋ง
- ล้างรถกระบะ
- ดูดฝุ่นภายใน
- เคลือบสี
- ล้างห้องเครื่อง

## Installation

ติดตั้ง dependencies:

```bash
pip install -r requirements.txt