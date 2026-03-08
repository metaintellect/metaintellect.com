---
title: "NN-RAG"
subtitle: "Retrieval-Augmented Generation for Croatian legal documents from Narodne Novine — the Official Gazette of Croatia."
description: "A production-grade RAG system for searching 38,000+ Croatian legal documents with hybrid retrieval, reranking, and semantic caching."
order: 1
status: "Live demo coming soon"
demo: "https://nn.metaintellect.com"
statsTitle: "Numbers"
stats:
  - value: "38K+"
    label: "documents indexed"
  - value: "497"
    label: "tests"
  - value: "~60ms"
    label: "search latency"
  - value: "16yr"
    label: "of legal data"
technologies:
  - "Python"
  - "FastAPI"
  - "FAISS (HNSW)"
  - "BM25"
  - "Cross-encoder reranking"
  - "AWS Bedrock"
  - "Ollama"
  - "SQLite"
  - "BeautifulSoup"
  - "lemmagen3"
  - "n8n webhooks"
  - "Ruff"
  - "pytest"
---

## What it does

NN-RAG is a search and question-answering system for Croatian legal documents. It indexes ~38,500 documents published in Narodne Novine between 2010 and 2026 — laws, regulations, decisions, decrees — and lets you search them semantically or ask natural language questions with AI-generated answers citing specific legal sources.

## Background

The project began as a learning exercise — not from tutorials, but by building something real. An initial version explored RAG fundamentals; NN-RAG was then built from scratch in approximately 10 days of focused collaboration with AI.

The approach treats AI as an equal partner, not a code generator. Architecture thinking, engineering standards, and domain knowledge were brought to the project; the AI contributed implementation speed and breadth of knowledge. The real work was in the discussions: what approach to take, what trade-offs matter, and pushing back when shortcuts were suggested that wouldn't hold up.

Croatian legal documents present a strong challenge: morphologically complex language, strict legal structure (articles, paragraphs, chapters), cross-references between documents, and changes over time. Building good retrieval for this domain demonstrates mastery of the fundamentals.

## How it works

**Hybrid retrieval:** Combines dense vector search (FAISS/HNSW with nomic-embed-text or multilingual-e5-large embeddings) with sparse BM25 search, fused via Reciprocal Rank Fusion at 70/30 weighting.

**Legal-aware chunking:** Documents are split respecting Croatian legal structure — članak (article), stavak (paragraph), poglavlje (chapter) — at 500–1,500 characters with 10% overlap. Not naive text splitting.

**Query intelligence:** Croatian lemmatization, 48K synonym mappings, rule-based query expansion for common legal terms, and LLM-powered query rewriting when the initial retrieval confidence is low.

**Cross-encoder reranking:** Results are reranked using bge-reranker-v2-m3 or mxbai-rerank-large-v2 to improve precision after the initial retrieval.

**Semantic cache:** Queries with similarity ≥ 0.92 to previous queries are served from cache.

**Multi-index:** Separate indices for historical (2010–2025) and current (2026+) documents. The current index supports incremental updates without rebuilding.

**LLM answers:** Uses AWS Bedrock (Claude) or local Ollama for generating answers with source citations. Graceful fallback: if the LLM is unavailable, you still get search results with sources.
