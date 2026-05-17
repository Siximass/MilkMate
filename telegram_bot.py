import os
import re
import time
import requests
from dotenv import load_dotenv
from google import genai


MODEL = "gemini-2.5-flash"


def get_env():
    load_dotenv()

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    google_api_key = os.getenv("GOOGLE_API_KEY")

    if not bot_token:
        raise RuntimeError("ไม่พบ TELEGRAM_BOT_TOKEN ในไฟล์ .env")

    if not google_api_key:
        raise RuntimeError("ไม่พบ GOOGLE_API_KEY ในไฟล์ .env")

    return bot_token, google_api_key


def send_message(bot_token: str, chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
    }

    response = requests.post(url, json=payload, timeout=15)

    if response.status_code != 200:
        print("ส่งข้อความไม่สำเร็จ:")
        print(response.text)


def generate_captions(service_name: str, price: str, google_api_key: str) -> str:
    client = genai.Client(api_key=google_api_key)

    prompt = f"""
You are a marketing copywriter for a car wash and car care shop named Car Care.
The shop AI assistant is named Carey.

Create 3 Instagram captions in Thai for this car wash service or promotion.

Service/Promotion: {service_name}
Price: {price} baht

Requirements:
- Output in Thai
- Friendly and casual tone
- Suitable for a car wash / car care shop
- Focus on cleanliness, shine, convenience, easy price, and customer trust
- Do not make exaggerated claims
- Do not mention that AI wrote it
- Create exactly 3 styles:
  1. Cute
  2. Minimal
  3. Gen-Z
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    return response.text


def parse_caption_command(text: str):
    """
    รองรับคำสั่ง:
    แคปชั่น ล้างรถเก๋ง 120
    ขอแคปชั่น ล้างรถกระบะ 150
    caption Premium Shine 450
    """

    text = text.strip()

    patterns = [
        r"^แคปชั่น\s+(.+?)\s+(\d+)$",
        r"^ขอแคปชั่น\s+(.+?)\s+(\d+)$",
        r"^caption\s+(.+?)\s+(\d+)$",
    ]

    for pattern in patterns:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            service_name = match.group(1).strip()
            price = match.group(2).strip()
            return service_name, price

    return None, None


def handle_message(bot_token: str, google_api_key: str, message: dict):
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()

    if not text:
        return

    if text in ["/start", "เริ่ม"]:
        welcome = """
สวัสดีค่ะ ฉันคือ Carey ผู้ช่วย AI ของร้าน Car Care 🚗

พิมพ์คำสั่งแบบนี้เพื่อสร้างแคปชัน:
แคปชั่น ล้างรถเก๋ง 120
ขอแคปชั่น แพ็กเกจ Premium Shine 450

หรือพิมพ์:
help
""".strip()
        send_message(bot_token, chat_id, welcome)
        return

    if text.lower() in ["help", "/help", "วิธีใช้"]:
        help_text = """
วิธีใช้ Carey Caption Bot 🚗

พิมพ์:
แคปชั่น ชื่อบริการ ราคา

ตัวอย่าง:
แคปชั่น ล้างรถเก๋ง 120
แคปชั่น ล้างรถกระบะ 150
ขอแคปชั่น แพ็กเกจ Premium Shine 450
caption Rain Protection 499

Carey จะสร้างแคปชัน 3 สไตล์ให้:
1. Cute
2. Minimal
3. Gen-Z
""".strip()
        send_message(bot_token, chat_id, help_text)
        return

    service_name, price = parse_caption_command(text)

    if not service_name or not price:
        reply = """
Carey ยังไม่เข้าใจคำสั่งค่ะ 🥺

ลองพิมพ์แบบนี้นะคะ:
แคปชั่น ล้างรถเก๋ง 120
ขอแคปชั่น แพ็กเกจ Premium Shine 450
""".strip()
        send_message(bot_token, chat_id, reply)
        return

    send_message(
        bot_token,
        chat_id,
        f"กำลังสร้างแคปชันสำหรับ {service_name} ราคา {price} บาทให้ค่ะ 🚗✨",
    )

    try:
        captions = generate_captions(service_name, price, google_api_key)

        reply = f"""
🚗 Car Care Caption by Carey

บริการ/โปรโมชัน: {service_name}
ราคา: {price} บาท

{captions}
""".strip()

        send_message(bot_token, chat_id, reply)

    except Exception as error:
        error_text = str(error)

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text or "quota" in error_text.lower():
            send_message(
                bot_token,
                chat_id,
                "ตอนนี้ Gemini API ใช้งานเกินโควตาชั่วคราวค่ะ กรุณารอสักครู่แล้วลองใหม่อีกครั้งนะคะ",
            )
        else:
            send_message(
                bot_token,
                chat_id,
                "เกิดข้อผิดพลาดในการสร้างแคปชันค่ะ กรุณาลองใหม่อีกครั้งนะคะ",
            )

        print("เกิดข้อผิดพลาด:")
        print(error)


def main():
    bot_token, google_api_key = get_env()

    print("Carey Telegram Bot กำลังทำงาน...")
    print("พิมพ์ใน Telegram ได้เลย เช่น: แคปชั่น ล้างรถเก๋ง 120")
    print("กด Ctrl + C เพื่อหยุดบอท")

    offset = None

    while True:
        try:
            url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
            params = {
                "timeout": 30,
                "offset": offset,
            }

            response = requests.get(url, params=params, timeout=40)
            data = response.json()

            if not data.get("ok"):
                print("getUpdates ไม่สำเร็จ:")
                print(data)
                time.sleep(3)
                continue

            for update in data.get("result", []):
                offset = update["update_id"] + 1

                message = update.get("message")
                if message:
                    handle_message(bot_token, google_api_key, message)

        except KeyboardInterrupt:
            print("\nหยุด Carey Telegram Bot แล้ว")
            break

        except Exception as error:
            print("เกิดข้อผิดพลาดใน loop:")
            print(error)
            time.sleep(3)


if __name__ == "__main__":
    main()