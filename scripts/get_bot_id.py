import os
from slack_sdk import WebClient
from dotenv import load_dotenv

load_dotenv()

# Replace with your actual Bot User OAuth Token or ensure it's in your .env file
# It's recommended to load it from .env as SLACK_BOT_TOKEN
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")

if not slack_bot_token:
    print("Error: SLACK_BOT_TOKEN not found in .env file or environment variables.")
    print("Please ensure your .env file has SLACK_BOT_TOKEN=xoxb-YOUR_TOKEN_HERE")
else:
    client = WebClient(token=slack_bot_token)
    try:
        response = client.auth_test()
        bot_user_id = response["user_id"]
        print(f"Your SLACK_BOT_USER_ID is: {bot_user_id}")
        print(f"Add this to your .env file: SLACK_BOT_USER_ID={bot_user_id}")
    except Exception as e:
        print(f"Error calling Slack API: {e}")
        print("Please ensure your SLACK_BOT_TOKEN is correct and has the necessary permissions (e.g., `auth:read`).")

