import json
import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from google import genai

from agent_tools import TOOL_REGISTRY


TRACE_FILE = "agent_trace.log"
MODEL = "gemini-2.5-flash"
CONFIDENCE_THRESHOLD = 0.7


def write_trace(event: str, data: dict) -> None:
    with open(TRACE_FILE, "a", encoding="utf-8") as file:
        record = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            **data,
        }
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def call_llm(user_input: str) -> dict:
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("ไม่พบ GOOGLE_API_KEY ในไฟล์ .env")

    client = genai.Client(api_key=api_key)

    system_instruction = """
คุณคือ Matey ผู้ช่วย AI ของร้าน Milk Mate

หน้าที่ของคุณคือแปลงคำสั่งภาษาไทยของผู้ใช้ให้เป็น JSON action เท่านั้น

เครื่องมือที่ใช้ได้:
1. log_sale
ใช้เมื่อผู้ใช้ต้องการบันทึกยอดขาย
รูปแบบ:
{
  "action": "log_sale",
  "args": {
    "menu": "ชื่อเมนู",
    "quantity": จำนวน,
    "price": ราคา
  },
  "confidence": 0.0,
  "reason": "เหตุผลสั้น ๆ"
}

2. get_yesterday_summary
ใช้เมื่อผู้ใช้ต้องการสรุปรายงานยอดขาย
รูปแบบ:
{
  "action": "get_yesterday_summary",
  "args": {},
  "confidence": 0.0,
  "reason": "เหตุผลสั้น ๆ"
}

ถ้าคำสั่งไม่ชัดเจน ให้ตอบ:
{
  "action": "unknown",
  "args": {},
  "confidence": 0.0,
  "reason": "ไม่เข้าใจคำสั่ง"
}

ตอบกลับเป็น JSON เท่านั้น ห้ามใส่ markdown ห้ามอธิบายเพิ่ม
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=f"{system_instruction}\n\nคำสั่ง: {user_input}",
    )

    raw = response.text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    write_trace("llm_response", {"raw": raw})

    return json.loads(raw)


def dispatch_tool(action_data: dict) -> dict:
    action = action_data.get("action")
    args = action_data.get("args", {})
    confidence = float(action_data.get("confidence", 0))

    write_trace(
        "parsed_action",
        {
            "action": action,
            "args": args,
            "confidence": confidence,
            "reason": action_data.get("reason", ""),
        },
    )

    if confidence < CONFIDENCE_THRESHOLD:
        result = {
            "status": "error",
            "message": "confidence ต่ำเกินไป จึงไม่เรียกใช้ tool",
        }
        write_trace("guardrail_reject", result)
        return result

    if action not in TOOL_REGISTRY:
        result = {
            "status": "error",
            "message": f"ไม่รู้จัก action: {action}",
        }
        write_trace("unknown_action", result)
        return result

    tool_info = TOOL_REGISTRY[action]
    fn = tool_info["fn"]
    required_args = tool_info["args"]
    coerce = tool_info["coerce"]

    final_args = {}

    try:
        for arg_name in required_args:
            if arg_name not in args:
                raise ValueError(f"missing argument: {arg_name}")

            value = args[arg_name]

            if arg_name in coerce:
                value = coerce[arg_name](value)

            final_args[arg_name] = value

        result = fn(**final_args)

        write_trace(
            "tool_result",
            {
                "action": action,
                "args": final_args,
                "result": result,
            },
        )

        return {
            "status": "success",
            "action": action,
            "result": result,
        }

    except (ValueError, TypeError) as error:
        result = {
            "status": "error",
            "message": str(error),
        }
        write_trace("tool_error", result)
        return result


def run_agent(user_input: str) -> dict:
    write_trace("user_input", {"message": user_input})

    action_data = call_llm(user_input)
    result = dispatch_tool(action_data)

    return result


def main():
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        result = run_agent(user_input)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print("Matey Agent พร้อมรับคำสั่ง (พิมพ์ 'exit' เพื่อออก)\n")

    while True:
        user_input = input("คุณ: ").strip()

        if user_input.lower() == "exit":
            break

        result = run_agent(user_input)
        print("Matey:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print()


if __name__ == "__main__":
    main()