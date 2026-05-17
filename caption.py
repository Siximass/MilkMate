import os
import sys
from dotenv import load_dotenv
from google import genai


def generate_captions(service_name: str, price: str) -> str:
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError("ไม่พบ GOOGLE_API_KEY กรุณาใส่ API key ในไฟล์ .env ก่อน")

    client = genai.Client(api_key=api_key)

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
- Focus on cleanliness, shine, convenience, and customer trust
- Do not make exaggerated claims
- Do not mention that AI wrote it
- Create exactly 3 styles:
  1. Cute
  2. Minimal
  3. Gen-Z
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text


def main():
    if len(sys.argv) < 3:
        print("วิธีใช้:")
        print('python caption.py "ล้างรถเก๋ง" 120')
        print('python caption.py "แพ็กเกจ Premium Shine" 450')
        return

    service_name = sys.argv[1]
    price = sys.argv[2]

    try:
        captions = generate_captions(service_name, price)
        print("\n=== Car Care Caption Generator ===\n")
        print(captions)
    except Exception as error:
        print("เกิดข้อผิดพลาด:")
        print(error)


if __name__ == "__main__":
    main()