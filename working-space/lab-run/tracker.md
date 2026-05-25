# Project Tracker (lab-run)

Last updated: 2026-05-18

Projects are in `/home/heigatvu/MyFile/my-project/my-assistance/working-space/lab-run/`

---

## ADReSSo-feature-extraction-en

Git: [b413324] finish late fusion

| Field | Value |
|-------|-------|
| What it is | Alzheimer's speech feature extraction pipeline (ADReSSo dataset) |
| Status | 🔄 Active — fusion pipeline done |
| Last session | b413324 — finish late fusion (early + late fusion both implemented) |
| Key files | `src/feature_extraction_pipeline.py`, `src/model_feature_pipeline.py`, `src/traditionalApproach/` |
| Next steps | Evaluate fusion models, run on full dataset |

---

## speech-analysis-for-you

Git: [677d213] change to run with a lot of file

| Field | Value |
|-------|-------|
| What it is | Speech analysis tool — clapperboard detection / audio processing |
| Status | 🔄 Active — batch processing working |
| Last session | 677d213 — change to run with a lot of file |
| Next steps | — |

---

## How to update

Tell Hermes:

```
Update project tracker: <project> — completed <task>, next <task>
```

Or edit this file directly.

## How Hermes uses this

- `/project-status` — reads this file to show all project health at once
- `/start-project <name>` — reads this file + git log to tell you where to pick up
- `/end-project-session <name>` — updates this file after you finish coding
