---
name: code-summary
description: Generates high-level repository steering files inside .agents/summary and AGENTS.md to minimize token drift.
---

# Skill: Code Summary

## Intent
Analyze the current repository's architecture, dependencies, and business domain to generate high-level steering documentation. This minimizes token overhead and structural drifting in future sessions.

## Protocol
1. Scan the repository to understand the core architecture, active modules, and technologies used.
2. Create or update an `AGENTS.md` file at the repository root mapping to the ASDLC open standard (Mission, Toolchain Registry, and Judgment Boundaries).
3. Generate or update the following three foundation steering files inside the `.agents/summary/` directory:
    - **product.md**: Detail the high-level purpose of the software, key business objectives, and targeted user types.
    - **tech.md**: List all frameworks, package managers, development tools, testing utilities, and infrastructure elements detected.
    - **structure.md**: Map out the high-level directory tree, file naming conventions, and layer separation boundaries.
4. Keep the summaries structural, concise, and focused on constraints that cannot be inferred immediately from clear code.
5. Notify the user with an asset list once execution completes.
6. If `AGENTS.md` or `.agents/summary` files already exist when this skill is invoked, re-scan the repository checking for inconsistencies and drift, then make any updates required to the markdown files.
