import json
import os
import re

from dotenv import load_dotenv


def parse_gemini_response(output: dict) -> list:
    """
    Extracts and parses the JSON array from the Gemini API response.
    """
    text_block = output["candidates"][0]["content"]["parts"][0]["text"]
    json_str = re.sub(r"^```json\n|\n```$", "", text_block.strip())
    return json.loads(json_str)


def filter_latest_msgs(messages: list, min_id: int) -> list:
    """
    Filters messages to only include those with 'id' greater than min_id.
    """
    return [msg for msg in messages if msg.get('id', 0) > min_id]


def write_structured_output(data: list, filename: str = "structured_output.json"):
    """
    Writes the structured data to a JSON file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_gemini_prompt(data1: list) -> str:
    if not data1:
        return "The input list of job postings is empty. Return an empty JSON array: [] just return empty json array. Nothing else"

    return (
            "You are given a list of job postings extracted from a Telegram/WhatsApp channel in JSON format:\n"
            + str(data1)
            + "\nExtract and convert each posting into the following structured JSON format:\n"
              "{ 'company_name': '...', 'role': '...', 'batch': '...', 'stipend': '...', 'location': '...', 'apply_link': '...' }\n"
              "Rules:\n"
              "- If 'stipend' is missing, set it to 'N/A'.\n"
              "- If 'location' is missing, set it to 'N/A'.\n"
              "- If 'company_name' is missing or empty, exclude that posting from the output.\n"
              "- Return only the JSON array with structured data, no explanations.\n"
              "- If the input list is empty or all postings are invalid, return []."
    )


def call_gemini_api(prompt: str) -> dict:
    import requests
    load_dotenv()  # Only called when this function runs (in activity context)
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    resp = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
        headers={"X-goog-api-key": f"{gemini_api_key}", "Content-Type": "application/json"},
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=100
    )
    resp.raise_for_status()
    return resp.json()


def get_new_last_msg_id(messages: list, min_id: int) -> int:
    """
    Returns the highest 'id' value from a list of message dicts.
    """
    if len(messages) == 0:
        return min_id
    return max(msg.get('id', 0) for msg in messages if 'id' in msg)


def call_add_job_api(data: list):
    import requests
    load_dotenv()  # Only called when this function runs (in activity context)
    url = "https://hyreme-server.onrender.com/api/job"
    try:
        for job in data:
            resp = requests.post(url, json=job)
            resp.raise_for_status()
        return "Success"
    except requests.RequestException as e:
        return "Failed: " + str(e)
