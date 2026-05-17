import os
import sys
from datetime import datetime
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


def log_sale(service: str, quantity: int, price: float):
    worksheet = connect_sheet()

    total = quantity * price
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [
        now,
        service,
        quantity,
        price,
        total,
    ]

    worksheet.append_row(row)

    print("บันทึกยอดขายบริการสำเร็จ")
    print(f"บริการ: {service}")
    print(f"จำนวน: {quantity}")
    print(f"ราคา: {price}")
    print(f"รวม: {total}")


def main():
    if len(sys.argv) < 4:
        print("วิธีใช้:")
        print('python sales_logger.py "ล้างรถเก๋ง" 2 120')
        print('python sales_logger.py "แพ็กเกจ Premium Shine" 1 450')
        return

    service = sys.argv[1]
    quantity = int(sys.argv[2])
    price = float(sys.argv[3])

    log_sale(service, quantity, price)


if __name__ == "__main__":
    main()