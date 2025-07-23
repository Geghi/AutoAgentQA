import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.ingestion.index import get_document_names

load_dotenv()

print(get_document_names())