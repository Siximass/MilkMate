import os
import requests
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials


def connect_sheet():
    load_dotenv()

    sheet_id = os.getenv("GOOGLE_SHEETS_ID")
    if not sheet_id:
        raise RuntimeError("ไม่พบ GOOGLE_SHEETS_ID ในไฟล์ .env")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = Credentials.from_service_account_file(
        "service-account.json",
        scopes=scopes,
    )

    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.sheet1

    return worksheet


def send_telegram_message(message: str):
    load_dotenv()

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("ยังไม่ได้ตั้งค่า TELEGRAM_BOT_TOKEN หรือ TELEGRAM_CHAT_ID ใน .env")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
    }

    response = requests.post(url, json=payload, timeout=10)

    if response.status_code == 200:
        print("ส่งรายงานไป Telegram สำเร็จ")
    else:
        print("ส่ง Telegram ไม่สำเร็จ")
        print(response.text)


def create_report():
    worksheet = connect_sheet()
    records = worksheet.get_all_records()

    if not records:
        return "ยังไม่มีข้อมูลยอดขายบริการใน Google Sheet"

    total_sales = 0
    total_quantity = 0
    service_counter = {}

    for row in records:
        service = row["menu"]
        quantity = int(row["quantity"])
        total = float(row["total"])

        total_sales += total
        total_quantity += quantity

        if service not in service_counter:
            service_counter[service] = 0
        service_counter[service] += quantity

    best_service = max(service_counter, key=service_counter.get)

    report = f"""
🚗 Car Care Morning Report by Carey

ยอดขายรวมทั้งหมด: {total_sales:.2f} บาท
จำนวนบริการที่ขายได้: {total_quantity} รายการ
บริการขายดี: {best_service} ({service_counter[best_service]} รายการ)

สรุปโดย Carey: วันนี้ยอดขายบริการของร้าน Car Care ถูกบันทึกเรียบร้อยแล้ว พร้อมใช้วิเคราะห์และวางแผนโปรโมชันต่อได้เลย
""".strip()

    return report


def main():
    try:
        report = create_report()
        print(report)
        send_telegram_message(report)
    except Exception as error:
        print("เกิดข้อผิดพลาด:")
        print(error)


if __name__ == "__main__":
    main()