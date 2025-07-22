├── app/
│   ├── __init__.py
│   ├── main.py                  
│   ├── api/                      # API route definitions
│   │   ├── __init__.py
│   │   └── slack.py              # Slack events/webhook handling
│
│   ├── core/                    
│   │   ├── __init__.py
│   │   ├── config.py             
│   │   └── telemetry.py          # OpenTelemetry setup
│
│   ├── ingestion/               
│   │   ├── __init__.py
│   │   ├── loader.py             # Load documents from local/remote
│   │   ├── splitter.py           # Chunking logic
│   │   ├── embeddings.py         # Embedding model setup
│   │   └── index.py              # Build/rebuild Chroma index
│
│   ├── agents/                   
│   │   ├── __init__.py
│   │   ├── rag.py                # RAG pipeline via LangChain
│   │   ├── escalation.py         # Escalation logic & routing
│   │   └── memory.py             # Optional: long-term memory handling
│
│   ├── services/                 # Integration logic for external APIs
│   │   ├── __init__.py
│   │   ├── slack_service.py      # Slack client wrapper
│   │   ├── supabase_service.py   # Logging & feedback to Supabase
│   │   └── openai_service.py     # OpenAI API wrapper
│
│   ├── models/                   # Pydantic models and DB schemas
│   │   ├── __init__.py
│   │   ├── slack_events.py       # Slack event payloads
│   │   └── interaction.py        # Supabase interaction/feedback models
│
│   └── utils/                    # Utilities & common helpers
│       ├── __init__.py
│       └── logger.py
│
├── chroma/                       # Chroma DB files
│
├── data/                         # Raw document files
│
├── supabase/                     # Supabase setup or SQL scripts
│
├── scripts/                      # CLI tools, cron jobs, batch ingestion
│   └── run_ingest.py             # Run document ingestion manually
│
├── tests/                        
│
├── .env
├── .env.example
├── requirements.txt
├── README.md