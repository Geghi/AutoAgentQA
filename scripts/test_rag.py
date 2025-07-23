import argparse
from dotenv import load_dotenv
from app.agents.rag import rag_pipeline

load_dotenv()

def main():
    """
    Main function to test the RAG pipeline.
    """
    parser = argparse.ArgumentParser(description="Test the RAG pipeline.")
    parser.add_argument(
        "query",
        type=str,
        help="The query to send to the RAG pipeline.",
    )
    args = parser.parse_args()

    answer = rag_pipeline(args.query)

    print("Query:")
    print(args.query)
    print("\nAnswer:")
    print(answer)

if __name__ == "__main__":
    main()
