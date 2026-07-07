# Repo/Tool Card: PaddlePaddle/PaddleOCR

## Identity

- ID: paddlepaddle-paddleocr
- Canonical URL: https://github.com/PaddlePaddle/PaddleOCR
- Type: library
- Status: cataloged
- Inspection date: 2026-07-07

## What It Is

OCR and document AI toolkit for converting PDFs and images into structured LLM-ready data such as JSON or Markdown, with multilingual recognition and document structure parsing.

## Why It May Be Useful

- Useful for agents that need to read screenshots, scans, PDFs, tables, forms, multilingual images, document layouts, and RAG inputs from visual sources.

## Agent-Building Use Cases

- Document ingestion layer for RAG or research agents.
- OCR step for screenshot/PDF processing workflows.
- Structured extraction from tables, formulas, seals, charts, and scanned documents.
- Potential MCP/document parsing reference because the repo contains an mcp_server folder.

## When To Consider

- When an agent must ingest PDFs, scanned documents, screenshots, tables, or multilingual visual text.
- When building document-to-Markdown/JSON pipelines for RAG or research workflows.
- When closed-source OCR is not acceptable or local processing is preferred.

## When Not To Use

- When the source is already clean text/HTML/Markdown.
- When target environment cannot support Python/model dependencies.
- When private document processing has no approved privacy/security policy.

## Implementation Shape

- Runtime/language: Python, PaddlePaddle, OCR models, optional JS bindings observed in repo tree
- Install/use pattern: Python OCR/document parsing toolkit with models and APIs; integration likely requires model download/runtime setup and document privacy policy.
- Requires permissions: package_install, model_download, local_file_read, private_document_access, possible_gpu_or_native_dependencies

## License And Maintenance

- License: Apache-2.0
- Maintainer: PaddlePaddle
- Recent activity: large active-looking repository; GitHub page showed 6,923 commits, issues, PRs, docs, tests, and multiple language docs
- Adoption signal: GitHub page showed 84.9k stars and 11k forks during inspection

## Risks And Unknowns

- OCR on private documents can expose sensitive data; needs explicit data handling rules.
- Model/runtime dependencies may be heavy; GPU/CPU, install size, and performance need validation.
- OCR outputs can be wrong; downstream agents need confidence, evidence refs, and human review for high-stakes documents.
- Do not treat benchmark or README claims as proof for a target document set without evals.

## Alternatives

- Tesseract
- docTR
- unstructured
- Marker
- cloud OCR APIs
- vision-language models

## Evidence Refs

- https://github.com/PaddlePaddle/PaddleOCR - GitHub page describes OCR/document AI conversion to structured LLM-ready JSON/Markdown and 100+ language support; inspected 2026-07-07.

## Integration Gate

This item is not integrated until a specific project selects it and passes license, security, runtime, validation, and rollback checks.
