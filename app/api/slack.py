from fastapi import APIRouter, Request, HTTPException, Depends
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from app.core.config import config
from app.services.slack_service import SlackService
from app.agents.rag import rag_pipeline
from app.utils.logger import logger
from app.utils.slack_formatter import format_rag_response_as_blocks

router = APIRouter()

# Initialize Slack App
slack_app = AsyncApp(
    token=config.SLACK_BOT_TOKEN,
    signing_secret=config.SLACK_SIGNING_SECRET,
)
slack_handler = AsyncSlackRequestHandler(slack_app)

@slack_app.event("app_mention")
async def handle_app_mention(event: dict, client):
    logger.info(f"App mention event received: {event}")
    text = event["text"]
    channel_id = event["channel"]
    user_id = event["user"]
    slack_service = SlackService()

    # Remove bot mention from the text
    mention_id = f"<@{config.SLACK_BOT_USER_ID}>"
    query = text.replace(mention_id, "").strip()

    if not query:
        await slack_service.send_message(channel_id, f"Hi <@{user_id}>! Please ask me a question after mentioning me.")
        return

    try:
        response_data = rag_pipeline(query)
        blocks = format_rag_response_as_blocks(response_data)
        await slack_service.send_blocks(channel=channel_id, blocks=blocks, text=response_data["answer"])
    except Exception as e:
        logger.error(f"Error handling app mention: {e}", exc_info=True)
        await slack_service.send_message(channel_id, f"Sorry <@{user_id}>, I encountered an error trying to answer your question. Please try again later.")

@slack_app.action("feedback_helpful_button")
async def handle_feedback_helpful(ack, body, client, logger):
    await ack()
    user_id = body["user"]["id"]
    channel_id = body["channel"]["id"]
    message_ts = body["message"]["ts"]
    original_blocks = body["message"]["blocks"]

    logger.info(f"User {user_id} marked response as helpful.")

    # Remove the actions block (buttons)
    updated_blocks = [block for block in original_blocks if block.get("type") != "actions"]

    # Add a confirmation text
    updated_blocks.append(
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"👍 Thanks for the feedback, <@{user_id}>!"
                }
            ]
        }
    )

    await client.chat_update(
        channel=channel_id,
        ts=message_ts,
        blocks=updated_blocks,
        text="Response marked as helpful."
    )

@slack_app.action("feedback_not_helpful_button")
async def handle_feedback_not_helpful(ack, body, client, logger):
    await ack()
    user_id = body["user"]["id"]
    channel_id = body["channel"]["id"]
    message_ts = body["message"]["ts"]
    original_blocks = body["message"]["blocks"]

    logger.info(f"User {user_id} marked response as not helpful.")

    # Remove the actions block (buttons)
    updated_blocks = [block for block in original_blocks if block.get("type") != "actions"]

    # Add a confirmation text
    updated_blocks.append(
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"👎 Thanks for the feedback, <@{user_id}>. We'll use this to improve."
                }
            ]
        }
    )

    await client.chat_update(
        channel=channel_id,
        ts=message_ts,
        blocks=updated_blocks,
        text="Response marked as not helpful."
    )

@slack_app.event("message")
async def handle_message_events(event: dict, client):
    logger.info(f"Message event received: {event}")
    # Check if it's a direct message (IM)
    if event.get("channel_type") == "im":
        text = event["text"]
        user_id = event["user"]
        channel_id = event["channel"]
        slack_service = SlackService()

        if not text:
            await slack_service.send_message(channel_id, f"Hi <@{user_id}>! Please ask me a question.")
            return

        try:
            response_data = rag_pipeline(text)
            blocks = format_rag_response_as_blocks(response_data)
            await slack_service.send_blocks(channel=channel_id, blocks=blocks, text=response_data["answer"])
        except Exception as e:
            logger.error(f"Error handling direct message: {e}", exc_info=True)
            await slack_service.send_message(channel_id, f"Sorry <@{user_id}>, I encountered an error trying to answer your question. Please try again later.")

@router.post("/slack/events")
async def slack_events(req: Request):
    # Handle the initial URL verification challenge from Slack
    if req.headers.get("content-type") == "application/json":
        try:
            body = await req.json()
            if body.get("challenge"):
                return body["challenge"]
        except Exception:
            # If JSON parsing fails, fall through to the handler
            pass

    # Let the Bolt handler process all other events (mentions, messages, actions)
    return await slack_handler.handle(req)

@router.get("/slack/install")
async def install(req: Request):
    return await slack_handler.handle(req)

@router.get("/slack/oauth_redirect")
async def oauth_redirect(req: Request):
    return await slack_handler.handle(req)
