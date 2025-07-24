from slack_sdk.web.async_client import AsyncWebClient
from app.core.config import config
from app.utils.logger import logger

class SlackService:
    def __init__(self):
        self.client = AsyncWebClient(token=config.SLACK_BOT_TOKEN)

    async def send_message(self, channel: str, text: str):
        try:
            response = await self.client.chat_postMessage(
                channel=channel,
                text=text
            )
            logger.info(f"Message sent to {channel}: {response['ts']}")
            return response
        except Exception as e:
            logger.error(f"Error sending message to Slack: {e}", exc_info=True)
            raise

    async def send_blocks(self, channel: str, blocks: list, text: str = "Assistant response"):
        try:
            response = await self.client.chat_postMessage(
                channel=channel,
                blocks=blocks,
                text=text  # Fallback text for notifications
            )
            logger.info(f"Block message sent to {channel}: {response['ts']}")
            return response
        except Exception as e:
            logger.error(f"Error sending block message to Slack: {e}", exc_info=True)
            raise

    async def get_user_info(self, user_id: str):
        try:
            response = await self.client.users_info(user=user_id)
            if response["ok"]:
                return response["user"]
            else:
                logger.error(f"Error getting user info for {user_id}: {response['error']}")
                return None
        except Exception as e:
            logger.error(f"Error fetching user info from Slack: {e}", exc_info=True)
            raise
