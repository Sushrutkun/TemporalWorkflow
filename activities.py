# activities.py
import asyncio
import logging

from temporalio import activity

from temporal_workflow.constants import last_msg_id, dot_aware_channel
from temporal_workflow.fetch_channel_messages import fetch_channel_messages
from temporal_workflow.helper import (
    create_gemini_prompt,
    call_gemini_api,
    parse_gemini_response,
    write_structured_output,
    get_new_last_msg_id, call_add_job_api, filter_latest_msgs,
)
from temporal_workflow.mongo_client import get_mongo_client

logging.basicConfig(level=logging.INFO)


@activity.defn
async def fetch_from_mongo() -> int:
    client = get_mongo_client()
    db = client["test"]
    collection = db["teleMsgs"]
    logging.info(f"Connecting to {db} database and {collection} collection")

    doc = collection.find_one({'channelName': dot_aware_channel})
    lastMsgId = doc.get(last_msg_id) if doc and last_msg_id in doc else None
    logging.info(f"Fetched lastMsgId: {lastMsgId}")
    return int(lastMsgId)


@activity.defn
async def fetch_from_telegram_channel(min_id: int) -> list:
    logging.info(f"Fetched last MinId: {min_id}")
    messages = await fetch_channel_messages(min_id)
    write_structured_output(messages,"messages.json")
    return messages


@activity.defn
async def filter_with_gemini(data1: list, min_id: int) -> list:
    data2 = filter_latest_msgs(data1, min_id)
    prompt = create_gemini_prompt(data2)
    output = await asyncio.to_thread(call_gemini_api, prompt)
    logging.info(f"Fetched RESPONSE: {output}")
    data = parse_gemini_response(output)

    client = get_mongo_client()
    db = client["test"]
    collection = db["teleMsgs"]
    collection.update_one(
        {'channelName': dot_aware_channel},
        {"$set": {last_msg_id: str(get_new_last_msg_id(data2,min_id))}}
    )
    write_structured_output(data)
    return data


@activity.defn
async def post_jobs_to_hyreme(data: list) -> None:
    logging.info(f"Posting {len(data)} jobs to HyreMe")
    if len(data) == 0:
        return
    resp = call_add_job_api(data)
    logging.info(f"{resp}")
