import os
import logging
from dotenv import load_dotenv # Import the dotenv library
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# --- Load Environment Variables from .env file ---
# This line looks for a .env file in the current directory and loads its variables
# into the environment, making them accessible via os.environ.get()
load_dotenv()
# Note: If a variable is already set in your system's environment,
# load_dotenv() usually won't override it by default.

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Retrieve Configuration from Environment Variables ---
# Now os.environ.get() will find the variables loaded from the .env file
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")

# --- Validate Configuration ---
# Check if the required environment variables were successfully loaded.
if not SLACK_BOT_TOKEN:
    logging.error("Error: SLACK_BOT_TOKEN not found. Make sure it's defined in your .env file.")
    exit(1)

if not SLACK_CHANNEL_ID:
    logging.error("Error: SLACK_CHANNEL_ID not found. Make sure it's defined in your .env file.")
    exit(1)

# --- Message Payload Definition (Same as before) ---
did_you_know_message_1 = {
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "💡 Did You Know? Getting Started with Gemini!",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Welcome to our *Did You Know* series on using Gemini at work! 🎉\n\nLet's start with the absolute basics:"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Tip #1: Just Ask Clearly!* \n\nYou don't need special codes or complex instructions to begin. Simply ask Gemini a clear, straightforward question just like you might ask a colleague."
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Try it out!* Ask Gemini something like:\n• `Explain what [a common work term or concept] means in simple terms.`\n• `What are the main steps to [a simple process]?`\n• `Draft a short, polite email asking for [something simple].`"
            }
            # Optional: Add an accessory image
            # "accessory": {
            #   "type": "image",
            #   "image_url": "YOUR_IMAGE_URL_HERE",
            #   "alt_text": "Illustration representing asking a question"
            # }
        },
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "✨ *Gemini Tip #1 | Keep it simple to start!*"
                }
            ]
        }
    ]
}

# --- Function to Post Message (Same as before) ---
def post_message_to_slack(client: WebClient, channel_id: str, blocks: list, fallback_text: str):
    """
    Posts a message with Block Kit blocks to a specified Slack channel.

    Args:
        client: An instance of slack_sdk.WebClient.
        channel_id: The ID of the target Slack channel.
        blocks: A list of Block Kit blocks defining the message structure.
        fallback_text: Plain text summary used for notifications.
    """
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            blocks=blocks,
            text=fallback_text
        )
        logging.info(f"Message posted successfully to channel {channel_id} (Timestamp: {response['ts']})")
    except SlackApiError as e:
        logging.error(f"Error posting message to channel {channel_id}: {e.response['error']}")
        logging.error(f"Full error response: {e.response}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

# --- Main Execution Block (Same as before) ---
if __name__ == "__main__":
    logging.info("Script started. Initializing Slack WebClient...")
    slack_client = WebClient(token=SLACK_BOT_TOKEN)

    logging.info(f"Attempting to post 'Did You Know #1' message to channel {SLACK_CHANNEL_ID}...")
    fallback = "💡 Did You Know? Tip #1: Just Ask Clearly!"

    post_message_to_slack(
        client=slack_client,
        channel_id=SLACK_CHANNEL_ID,
        blocks=did_you_know_message_1["blocks"],
        fallback_text=fallback
    )

    logging.info("Script finished.")