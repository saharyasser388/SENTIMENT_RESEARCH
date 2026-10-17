---
name: study2-handover
description: Continue, audit, document, or deliver the SENTIMENT_RESEARCH Study 2 GPT-2 versus BERT GoEmotions work. Use when working in this repository on Study 2 results, local cleanup, reproducibility, Git commits, pushing the study branch, or opening its real GitHub pull request.
---

# Study 2 handover

Read [references/handover.md](references/handover.md) before changing Study 2.

## Workflow

1. Inspect `git status --short --branch`, `git log -5 --oneline`, configured remotes, and the relevant files. Treat the working tree as user-owned; review existing edits before changing or staging them.
2. Preserve Study 1. Do not alter its scripts, logs, or checkpoints unless the user explicitly requests it.
3. Preserve the published GoEmotions `train`, `valid`, and `test` splits, encoded class order, common maximum length 64, and validation Macro-F1 checkpoint policy.
4. Do not invent or silently recompute research results. Use the recorded logs or actual `*.results.json` artifacts. Do not use the test set for model selection.
5. Do not commit checkpoints, caches, virtual environments, or Python bytecode. If a `.pyc` is already tracked, remove it from the Git index rather than treating it as research output.
6. Run checks relevant to any change. Distinguish a failed check from an environment limitation.
7. Before committing, show or inspect the staged diff and ensure unrelated local changes are excluded. Use a concise action-oriented commit subject.
8. A PR is real only when the branch is pushed and GitHub returns a PR URL or number. Never describe locally prepared PR text as an opened PR. If authentication or a remote is missing, state the blocker and give the exact command the user must run.

## Definition of done

- The requested task is complete without modifying unrelated Study 1 work.
- Research claims match measured artifacts and logs.
- Relevant checks pass, or limitations are stated precisely.
- The working tree and commit/PR state are reported truthfully.
