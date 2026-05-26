# ChimeraX Shared Posture

Last reviewed: 2026-05-15

ChimeraX is intentionally duplicated between CryoCore and Structure Factory.

## CryoCore Use

- map/model inspection
- density and model visual review
- scripted figure rendering
- reviewer-grade figure dossiers
- session files for operator spot-checks

## Structure Factory Use

- design and prediction atlas figures
- RFdiffusion/Boltz/Chai candidate visualization
- cross-lane synthesis figures
- public-safe demo rendering when the operator use context permits

## Policy

- Do not store installers, binaries, license IDs, or accepted-license notes in tracked files.
- Record noncommercial posture or commercial-license override per campaign before execution.
- Treat missing ChimeraX as a renderer-lane blocker only, with raw processing and model build continuing on the other lanes.
- Prefer manual/pre-staged installer handling when upstream download flows require interactive consent.
- Keep version strings synchronized across duplicated docs when a new source-backed audit happens.

## Current Local Contract

- Public posture: ChimeraX 1.11.
- Staged package posture observed in CryoCore preview work: 1.11.1 package on Ubuntu 22.04.
- Runtime class: gated renderer/review tool.
- Redistribution: none from this repo.
