# Repo/Tool Card: Google Cloud Open Knowledge Format (OKF)

## Identity

- ID: google-open-knowledge-format
- Canonical URL: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/
- Type: reference
- Status: cataloged
- Inspection date: 2026-07-19

## What It Is

Open Knowledge Format (OKF) is an open, vendor-neutral format for a project knowledge bundle. It represents concepts such as database tables, views, datasets, metrics, APIs, playbooks, and join paths as Markdown files with YAML front matter and ordinary links.

## Why It May Be Useful

A project can use an OKF-style bundle as a stable context layer for database-aware agents. Instead of repeatedly reconstructing definitions from raw schemas, dashboards, and scattered documentation, an agent can read a reviewable data dictionary with links to related concepts.

This is an optional documentation and context pattern. It is not a database, database connector, access-control system, runtime dependency, or required component of every agent.

## Agent-Building Use Cases

- Describe tables, columns, views, metrics, owners, joins, data contracts, and freshness rules in versioned files.
- Give agents project-specific database context before they inspect raw database systems.
- Keep operational and data-quality notes alongside the code and make them reviewable by people.

## When To Consider

- A project has a durable database or analytics model that several agents or workflows must understand.
- Important context is scattered across SQL, dashboards, wikis, and senior engineers' knowledge.
- The team needs portable, Git-friendly documentation rather than another mandatory platform.

## When Not To Use

- The project has no durable data model or the knowledge bundle would immediately become stale.
- An existing authoritative catalog already meets the need and a duplicate would create drift.
- Sensitive metadata has not been classified and approved for storage in project files.

## Safety And Governance

- Never include credentials, raw private records, customer data, or unapproved schema details.
- An OKF document does not grant database access and must not be treated as proof that data is current.
- Assign an owner and freshness rule before an agent relies on a bundle for decisions.
- Validate the bundle against the authoritative schema and measure whether it improves the target workflow.

## Integration Gate

OKF is a cataloged option only. Select it for a specific project only after user approval, metadata classification, source-of-truth comparison, maintenance ownership, and a task-level evaluation. No Google Cloud, BigQuery, SDK, plugin, connector, or database migration is implied by this entry.

## Evidence Refs

- https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/
- https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf