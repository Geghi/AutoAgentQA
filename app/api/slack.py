from fastapi import APIRouter, Request, HTTPException, Depends
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from app.core.config import config
from app.services.slack_service import SlackService
from app.agents.rag import rag_pipeline
from app.utils.logger import logger

router = APIRouter()

# Initialize Slack App
slack_app = AsyncApp(
    token=config.SLACK_BOT_TOKEN,
    signing_secret=config.SLACK_SIGNING_SECRET,
)
slack_handler = AsyncSlackRequestHandler(slack_app)

@slack_app.event("app_mention")
async def handle_app_mention(event: dict, say): # Changed body to event and removed SlackEvent(**body)
    logger.info(f"App mention event received: {event}")
    text = event["text"]
    channel_id = event["channel"]
    user_id = event["user"]

    # Remove bot mention from the text
    mention_id = f"<@{config.SLACK_BOT_USER_ID}>"
    query = text.replace(mention_id, "").strip()

    if not query:
        await say(f"Hi <@{user_id}>! Please ask me a question after mentioning me.")
        return

    try:
        response_text = rag_pipeline(query)
        await say(response_text)
    except Exception as e:
        logger.error(f"Error handling app mention: {e}", exc_info=True)
        await say(f"Sorry <@{user_id}>, I encountered an error trying to answer your question. Please try again later.")

@slack_app.event("message")
async def handle_message_events(event: dict, say):
    logger.info(f"Message event received: {event}")
    # Check if it's a direct message (IM)
    if event.get("channel_type") == "im":
        text = event["text"]
        user_id = event["user"]

        if not text:
            await say(f"Hi <@{user_id}>! Please ask me a question.")
            return

        try:
            response_text = rag_pipeline(text)
            await say(response_text)
        except Exception as e:
            logger.error(f"Error handling direct message: {e}", exc_info=True)
            await say(f"Sorry <@{user_id}>, I encountered an error trying to answer your question. Please try again later.")

@router.post("/slack/events")
async def slack_events(req: Request):
    # Slack URL verification challenge
    request_body = await req.json()
    if "challenge" in request_body:
        return request_body["challenge"]
    return await slack_handler.handle(req)

@router.get("/slack/install")
async def install(req: Request):
    return await slack_handler.handle(req)

@router.get("/slack/oauth_redirect")
async def oauth_redirect(req: Request):
    return await slack_handler.handle(req)
