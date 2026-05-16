import json
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

from agent_tools import TOOL_REGISTRY


CONFIDENCE_THRESHOLD = 0.7


def call_llm(user_input: str) -> dict:
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("ไม่พบ GOOGLE_API_KEY ในไฟล์ .env")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are Matey, an AI assistant for Milk Mate.

Your job is to choose the correct tool for the user's request.

Available tools:
1. log_sale
   - Use when the user wants to record a sale.
   - Required arguments:
     - menu: string
     - quantity: integer
     - price: number

2. get_yesterday_summary
   - Use when the user wants a sales summary or report.
   - No arguments required.

Return only valid JSON in this schema:
{{
  "action": "tool_name",
  "arguments": {{}},
  "confidence": 0.0,
  "reason": "short reason"
}}

Rules:
- Return JSON only. Do not include markdown.
- If the user wants to record a sale, use action "log_sale".
- If the user wants a report or sales summary, use action "get_yesterday_summary".
- If the user input is unclear, use low confidence.

User input:
{user_input}
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    # กันกรณี Gemini เผลอครอบ JSON ด้วย ```json
    text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


def dispatch_tool(plan: dict) -> dict:
    action = plan.get("action")
    arguments = plan.get("arguments", {})
    confidence = float(plan.get("confidence", 0))

    print("[trace] action:", action)
    print("[trace] confidence:", confidence)
    print("[trace] arguments:", arguments)

    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "ok": False,
            "error": "confidence too low",
            "plan": plan,
        }

    if action not in TOOL_REGISTRY:
        return {
            "ok": False,
            "error": f"unknown tool: {action}",
            "plan": plan,
        }

    tool_info = TOOL_REGISTRY[action]
    fn = tool_info["fn"]
    required_args = tool_info["args"]
    coerce = tool_info["coerce"]

    final_args = {}

    for arg_name in required_args:
        if arg_name not in arguments:
            return {
                "ok": False,
                "error": f"missing argument: {arg_name}",
                "plan": plan,
            }

        value = arguments[arg_name]

        if arg_name in coerce:
            value = coerce[arg_name](value)

        final_args[arg_name] = value

    result = fn(**final_args)

    return {
        "ok": True,
        "action": action,
        "result": result,
    }


def run_agent(user_input: str) -> dict:
    print("[trace] user_input:", user_input)

    plan = call_llm(user_input)

    print("[trace] plan:", plan)

    result = dispatch_tool(plan)

    print("[trace] result:", result)

    return result


def main():
    if len(sys.argv) < 2:
        print("วิธีใช้:")
        print('python agent_harness.py "บันทึกยอดขายโกโก้ภูเขาไฟ 2 แก้ว แก้วละ 50"')
        print('python agent_harness.py "สรุปรายงานยอดขายให้หน่อย"')
        return

    user_input = " ".join(sys.argv[1:])

    try:
        result = run_agent(user_input)
        print("\n=== Matey Agent Result ===")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as error:
        print("เกิดข้อผิดพลาด:")
        print(error)


if __name__ == "__main__":
    main()