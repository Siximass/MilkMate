import os
import sys
from dotenv import load_dotenv
from google import genai


def generate_captions(menu_name: str, price: str) -> str:
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError("ไม่พบ GOOGLE_API_KEY กรุณาใส่ API key ในไฟล์ .env ก่อน")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a marketing copywriter for a milk and drink shop named Milk Mate.
The shop AI assistant is named Matey.

Create 3 Instagram captions in Thai for this menu.

Menu: {menu_name}
Price: {price} baht

Requirements:
- Output in Thai
- Friendly and casual tone
- Suitable for a milk/drink shop
- Do not make medical claims
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
        print('python caption.py "โกโก้ภูเขาไฟ" 50')
        return

    menu_name = sys.argv[1]
    price = sys.argv[2]

    try:
        captions = generate_captions(menu_name, price)
        print("\n=== Milk Mate Caption Generator ===\n")
        print(captions)
    except Exception as error:
        print("เกิดข้อผิดพลาด:")
        print(error)


if __name__ == "__main__":
    main()