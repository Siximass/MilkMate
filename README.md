# Milk Mate Caption Generator

โปรเจกต์นี้เป็น Caption Generator สำหรับร้าน Milk Mate  
ใช้ Python ร่วมกับ Gemini API เพื่อสร้างแคปชัน Instagram สำหรับเมนูเครื่องดื่ม 3 รูปแบบ ได้แก่ Cute, Minimal และ Gen-Z

## Project Info

- Shop name: Milk Mate
- AI assistant name: Matey
- Main file: `caption.py`
- Language: Python
- API: Gemini API

## Features

- รับชื่อเมนูและราคาเป็น input
- สร้างแคปชันภาษาไทย 3 สไตล์
  - Cute
  - Minimal
  - Gen-Z
- เก็บ API Key ไว้ในไฟล์ `.env`
- ใช้ `.gitignore` เพื่อป้องกันไม่ให้ secret หลุดขึ้น GitHub

## Installation

ติดตั้ง dependencies:

```bash
pip install -r requirements.txt