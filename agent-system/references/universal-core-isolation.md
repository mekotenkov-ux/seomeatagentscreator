# Universal Core Isolation

The public agent-creation core must stay domain-neutral.

## What Belongs In The Core

- workflow contracts;
- artifact schemas;
- permission gates;
- context packaging rules;
- validation harnesses;
- package boundaries;
- adapter conformance;
- evidence and claim guards;
- skill-candidate lifecycle.

## What Does Not Belong

- client names;
- project URLs;
- provider-specific API defaults;
- SEO/GEO/YouTube-specific scoring rules;
- screenshots, logs, raw provider responses;
- examples copied from real private projects;
- hardcoded language/country/niche assumptions;
- domain-specific checkers in the universal acceptance gate.

## Contamination Check

Before release:

1. Build a list of forbidden literals from project manifests, examples, and private test runs.
2. Scan universal core files for those literals.
3. Allow only synthetic examples and explicitly anonymized fixtures.
4. Fail if package-specific lessons were placed in universal instructions instead of scoped references.

Domain lessons are useful, but only after they are generalized into a reusable mechanism.
