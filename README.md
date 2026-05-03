# Smart Factory Assistant (Agentic LLM System)

## Description

Smart Factory Assistant is an agentic AI system for industrial sensor analysis. It chains five specialised agents — sensor analysis, diagnosis, solution, optimization, and risk — over live sensor inputs (temperature, vibration, pressure, RPM). The Diagnosis Agent is grounded in domain knowledge through a Retrieval-Augmented Generation (RAG) layer backed by ChromaDB, and the entire pipeline is exposed through a Streamlit dashboard with live gauges, a radar overview, and per-agent expanders.

In short: **multi-agent AI + RAG + LLM-based reasoning + Streamlit UI**.

## Setup Instructions

```bash
pip install -r requirements.txt
python -m rag.ingest_docs
python -m streamlit run app.py
```

## Notes

- RAG ingestion (`python -m rag.ingest_docs`) **must be run once** before first use to build the ChromaDB knowledge base.
- The first run downloads a sentence-transformer embedding model (~80 MB). Subsequent runs are cached and start instantly.

## Features

- **Multi-agent architecture** — Sensor → Diagnosis → Solution → Optimization → Risk
- **RAG with ChromaDB** — domain documents retrieved per query, with source + similarity score
- **LLM-based reasoning** — prompt templates orchestrate agent decision-making
- **Streamlit dashboard** — live gauges, radar chart, risk indicator, per-agent expanders
- **Risk monitoring** — colour-coded HIGH / MEDIUM / LOW with actionable messaging
- **Evaluation system** — sensor case generator + evaluator for batch testing

## Project Structure

```
smart_factory_assistant/
├── app.py              # Streamlit entry point
├── main.py             # Pipeline orchestrator (run_pipeline)
├── agents/             # Sensor, Diagnosis, Solution, Optimization, Risk agents
├── rag/                # ChromaDB ingestion + retriever
├── data/               # Domain knowledge documents
├── prompts/            # LangChain prompt templates per agent
├── evaluation/         # Test-case generator + evaluator
├── ui/                 # Streamlit components, charts, styles
└── requirements.txt
```

## Team Roles

- **Lead Developer** — architecture, pipeline integration, code reviews
- **AI Engineer** — agent logic, prompt design, LLM reasoning
- **Data Engineer** — RAG ingestion, embedding pipeline, knowledge base
- **UI Developer** — Streamlit dashboard, Plotly charts, theming
- **Project Manager** — scope, milestones, team coordination
