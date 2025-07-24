from typing import List

def format_rag_response_as_blocks(response_data: dict) -> list:
    """
    Formats the RAG pipeline response into Slack Block Kit format.

    Args:
        response_data: A dictionary from rag_pipeline with "answer" and "groundings".

    Returns:
        A list of Slack blocks.
    """
    answer = response_data.get("answer", "No answer found.")
    groundings = response_data.get("groundings", [])

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": answer
            }
        }
    ]

    if groundings:
        groundings_text = "\n".join([f"• <https://{source}|{source}>" for source in groundings])
        blocks.append({"type": "divider"})
        blocks.append(
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Sources:*\n{groundings_text}"
                    }
                ]
            }
        )
    
    blocks.append({"type": "divider"})
    blocks.append(
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Helpful 👍",
                        "emoji": True
                    },
                    "value": "feedback_helpful",
                    "action_id": "feedback_helpful_button"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Not Helpful 👎",
                        "emoji": True
                    },
                    "value": "feedback_not_helpful",
                    "action_id": "feedback_not_helpful_button",
                    "style": "danger"
                }
            ]
        }
    )

    return blocks
