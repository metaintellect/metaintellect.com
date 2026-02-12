---
title: "Media Collection"
subtitle: "A personal tool for managing a large physical media collection — 700 vinyl records, 2,200+ CDs, and 700 Blu-rays/DVDs — all searchable from one place."
description: "Full-stack app for cataloging 4,600+ physical media items — vinyl, CDs, SACDs, Blu-rays, and DVDs."
order: 2
status: "Live demo coming soon"
statsTitle: "The collection"
stats:
  - value: "~700"
    label: "vinyl records"
  - value: "2,200+"
    label: "CDs & SACDs"
  - value: "~700"
    label: "Blu-rays & DVDs"
  - value: "~1,000"
    label: "cassettes"
technologies:
  - "React 19"
  - "TypeScript"
  - "Vite 7"
  - "Tailwind CSS 4"
  - "TanStack Table"
  - "FastAPI"
  - "Python"
  - "SQLite + FTS5"
  - "Pydantic"
  - "Ruff"
  - "ESLint"
---

## What it does

Unifies data from Discogs (for music: vinyl, CDs, SACDs, cassettes) and Blu-ray.com (for video: 4K, Blu-ray, DVD) into a single searchable database. Tracks ownership status, purchase details, thumbnails, and provides full-text search across the entire collection — accent-insensitive and with prefix matching, which matters for large collections of ex-Yugoslav and Croatian releases.

## Background

With 4,600+ physical media items across multiple formats and sources, a unified tool was needed to search and manage the collection in one place. Discogs excels at music cataloging but does not handle video. Blu-ray.com excels at video but does not handle music. Neither supports purchase lifecycle tracking (owned → for sale → sold) in a unified way. This project delivers one tool that handles both.

The project was built entirely with AI assistance — the first React codebase, with no prior React experience. But "built with AI" does not mean "built instantly." There is no instant software. It is a growing, evolving thing that takes time to understand what is actually needed. AI tends to want to solve everything in one shot, but real software requires iteration — understanding the problem, pushing back on shortcuts, and letting the design evolve.

The value is not in generating code fast. It is in knowing what to ask for, recognizing when something is not right, and having the engineering judgment to steer the result toward something that actually works well.

## How it works

**Data import:** Python scripts parse CSV exports from Discogs and Blu-ray.com, clean the data (date formats, seller names, disambiguation suffixes), and load into a unified SQLite schema with source-specific extension tables.

**Search:** SQLite FTS5 with unicode61 tokenizer for accent-insensitive, diacritic-aware full-text search. Prefix matching so typing "kral" finds "Kraljevi" and "Kraljica."

**API:** FastAPI backend with Pydantic validation. CRUD for items, purchase tracking, for-sale/sold lifecycle, thumbnail management, and statistics.

**UI:** React 19 with TanStack Table v8 for sortable, filterable data display. Dark theme. Keyboard shortcuts (Ctrl+S to save, E for edit). Client-side filtering with server-side FTS for search.
