import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import asyncio
import re
from app.agents.rag import rag_pipeline

# Load environment variables from .env file
load_dotenv()

async def main():
    # Read questions from file
    with open("tests/questions/questions.txt", "r") as f:
        questions = [re.sub(r"^\d+\.\s*", "", line.strip()) for line in f.readlines() if line.strip() and line.strip()[0].isdigit()]
    
    # Initialize results list
    results = []
    # Iterate through questions and call RAG pipeline
    for question in questions:
        answer = rag_pipeline(question)
        time.sleep(1)
        results.append(f"Question: {question}\\nAnswer: {answer}\\n\\n")

    # Save results to file
    with open("qa_results.txt", "w") as f:
        f.writelines(results)

if __name__ == "__main__":
    asyncio.run(main())
