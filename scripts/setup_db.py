"""
Database initialization script for LLMinate RAG AI.
- Enables pgvector
- Creates Agents, Documents, Embeddings tables
- Creates vector index
- (Optionally) creates admin user
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

SCHEMA_SQL = """
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS agents (
    agent_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    model_config JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    status TEXT
);

CREATE TABLE IF NOT EXISTS documents (
    doc_id SERIAL PRIMARY KEY,
    agent_id INTEGER REFERENCES agents(agent_id),
    source_filename TEXT,
    uploaded_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS embeddings (
    chunk_id SERIAL PRIMARY KEY,
    doc_id INTEGER REFERENCES documents(doc_id),
    agent_id INTEGER REFERENCES agents(agent_id),
    vector vector(1536) NOT NULL,
    metadata JSONB
);

CREATE INDEX IF NOT EXISTS idx_embeddings_vector ON embeddings USING hnsw (vector vector_l2_ops);
"""

def get_engine() -> Engine:
    """
    Create a SQLAlchemy engine using the DATABASE_URL.
    """
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in environment variables.")
    return create_engine(DATABASE_URL)

def setup_database():
    """
    Run schema creation SQL to set up the database.
    """
    engine = get_engine()
    with engine.connect() as conn:
        for statement in SCHEMA_SQL.strip().split(';'):
            stmt = statement.strip()
            if stmt:
                conn.execute(text(stmt))
        conn.commit()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
