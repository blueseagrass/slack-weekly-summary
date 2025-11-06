# fetches last 7 days of messages from Slack channel
# bundles into a text block
# Sends to chatgpt to summarize/format
# Posts the summary back to Slack (can change destination channel later)

import os
from datetime import datetime, timedelta, timezone
from slack_sdk import WebClient
from dotenv import load_dotenv
from openai import OpenAI 
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

# environment variables from .env
load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
PROJECT_CHANNEL_ID = os.getenv("PROJECT_CHANNEL_ID")
SUMMARY_CHANNEL_ID = os.getenv("SUMMARY_CHANNEL_ID", PROJECT_CHANNEL_ID)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Init Slack and OpenAI clients
slack_client = WebClient(token=SLACK_BOT_TOKEN)
ai_client = OpenAI(api_key=OPENAI_API_KEY)

# Fetch last N days of messages from Slack
def fetch_messages(channel_id, days=7, limit=200):
    # get timestamp for 7 days ago
    oldest = (datetime.now(timezone.utc) - timedelta(days=days)).timestamp()

     # Slack API fetches message history
    resp = slack_client.conversations_history(
        channel=channel_id,
        oldest=str(oldest),
        limit=limit,
    )
    # return only big list of messages
    return resp["messages"]

# strip channel text into gpt-readable format
def build_channel_text(messages):
    lines = []
    # reverse so oldest messages get read first
    for m in reversed(messages):
        text = m.get("text", "").strip()
        if not text:
            continue
        user = m.get("user", "someone")
        ts = m.get("ts", "")
        lines.append(f"[{user} @ {ts}]: {text}")
    #join all lines into big block
    big_text = "\n".join(lines)
    # optional cap:don't send too much data
    return big_text[:8000]


# Ask Chatgpt to produce weekly update summary
# based on the block of messages
def ask_gpt_for_update(channel_text):
    # Fill the placeholder with actual Slack text
    user_prompt = USER_PROMPT_TEMPLATE.format(channel_text=channel_text)

    try:
        response = ai_client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4, # apparentally lower = more factual and colder lol
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"*AI summary unavailable:* {e}"

# post back to Slack in whatever channel
def post_to_slack(channel_id, text):
    slack_client.chat_postMessage(channel=channel_id, text=text)

def main():
    #get last 7 days
    messages = fetch_messages(PROJECT_CHANNEL_ID)
    #Build readable text
    channel_text = build_channel_text(messages)
    #LLM summary
    summary_markdown = ask_gpt_for_update(channel_text)
    #post in desired channel
    post_to_slack(SUMMARY_CHANNEL_ID, summary_markdown)

if __name__ == "__main__":
    main()
