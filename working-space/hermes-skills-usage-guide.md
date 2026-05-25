# Hermes Skills — Daily Usage Guide

How to use every skill in your setup, with exact commands and real examples.

---

## How to trigger skills

Three ways to run any skill:

**1. From terminal (at home or in a project folder)**
```bash
hermes
/skill-name [optional argument]
```

**2. From Telegram (anywhere, including phone)**
Just type the trigger phrase in your Hermes Telegram chat:
```
/daily-brief
start project audio-asr
youtube idea: how I use Hermes to manage my PhD
```

**3. Natural language (Hermes matches the trigger)**
You don't always need the slash command. If you say:
```
brief me on today
```
Hermes matches it to `/daily-brief` automatically.

---

## Quick reference card

| Skill | Command | When to use |
|---|---|---|
| Document manager | `/document-manager` | Find, search, draft any document |
| Daily brief | `/daily-brief` | Every morning — what's today |
| End of day | `/end-of-day` | Every evening — wrap up |
| Add deadline | `/add-deadline` | New task or deadline appears |
| YouTube idea | `/youtube-idea` | Any time inspiration hits |
| Rebuild schedule | `/rebuild-schedule` | Every Sunday evening |
| Start project | `/start-project [name]` | Before opening Claude Code |
| End project session | `/end-project-session [name]` | After closing Claude Code |
| Project status | `/project-status` | Check all projects at once |
| Code review | `/code-review [name]` | When you want a review |

---

# SKILL 1: Document Manager (existing)

Your existing skill — unchanged.

**Trigger phrases:**
```
find document about [topic]
search for [filename]
draft a document about [topic]
summarize [document name]
```

**Example uses:**
```
find my latest BME proceeding draft
search for anything related to VIBE proposal
draft an abstract for the DLD research paper
summarize the last academic document I saved
```

---

# SKILL 2: `/daily-brief`

Your morning orientation. Run this before you start work.

**Exact command:**
```
/daily-brief
```

**Trigger phrases:**
```
daily brief
morning brief
what's today
brief me on today
what do I have today
```

**What it outputs:**
- Today's Google Calendar events in order
- Your active work tasks ranked by deadline
- Suggested time blocks for the 8 AM–3 PM work window
- Anything due within 7 days flagged as urgent
- Tonight's suggested study topic
- One sentence: your top priority for the day

**Example real output:**
```
Good morning — Saturday, May 17

Today's calendar:
  09:00  Master presentation check-in with supervisor
  12:00  Daily English
  20:00  Study block — DSP Coursera

Work tasks (ranked by deadline):
  🔴 BME proceeding — submit draft — due in 3 days
  🟡 VIBE proposal — outline section 2 — due in 9 days
  ⚪ DLD research design — ongoing

Suggested morning blocks:
  08:00–10:00  BME proceeding (urgent)
  10:00–11:00  Meeting prep
  13:00–15:00  VIBE proposal

Top priority today: finish BME proceeding draft before the check-in.
```

**When to use:**
- Every weekday morning (runs automatically via cron at 10 AM)
- Any time you need to reorient mid-day

---

# SKILL 3: `/end-of-day`

Your evening wrap-up. Run this before 12 AM.

**Exact command:**
```
/end-of-day
```

**Trigger phrases:**
```
end of day
wrap up
daily review
what did I do today
close out today
```

**What it asks you:**
```
What did you complete today? What got pushed to tomorrow?
```

Answer in plain language:
```
Finished BME draft section 1 and 2. Pushed the conclusion to tomorrow. Didn't get to VIBE proposal at all.
```

**What it does after your answer:**
- Updates `deadlines/tracker.md` with new statuses
- Suggests adjustments to tomorrow's plan if things slipped
- Recommends one study topic for the remaining time tonight
- Sends a Telegram summary

**When to use:**
- Every weekday evening (runs automatically via cron at 10 PM)
- Run manually if your day ended unusually early or late

---

# SKILL 4: `/add-deadline`

Add a new deadline anytime — from terminal or Telegram.

**Exact command:**
```
/add-deadline
```

**Trigger phrases:**
```
add deadline
new deadline
I have a deadline
new submission
professor just gave me a deadline
```

**What it asks:**
```
1. Project name?
2. Task description?
3. Deadline date?
4. Priority? (high / medium / low)
5. Want a Google Calendar reminder 3 days before? (yes/no)
```

**Example from Telegram (quick format):**
```
add deadline: BME proceeding final submission — June 20 — high priority
```

Hermes fills in what it can and confirms before saving.

**What it saves to `deadlines/tracker.md`:**
```
| BME proceeding | Final submission | 2026-06-20 | 35 | high | in progress |
```

**When to use:**
- Immediately when supervisor gives you a new deadline
- When a project milestone is confirmed
- From your phone while in class or a meeting (Telegram works)

---

# SKILL 5: `/youtube-idea`

Capture a YouTube idea before you forget it.

**Exact command:**
```
/youtube-idea
```

**Trigger phrases:**
```
youtube idea
video idea
content idea
I want to make a video about
```

**Quick format (works from Telegram):**
```
youtube idea: "How I manage a PhD with Hermes Agent" — for developers who feel overwhelmed
```

**What it asks if you don't provide details:**
```
1. Title or working title?
2. Target audience?
3. Unique angle — what makes this different from existing videos?
```

**What it saves to `youtube/ideas/backlog.md`:**
```
## 2026-05-17 — How I manage a PhD with Hermes Agent
- Target audience: developers and master's students
- Unique angle: shows real skill files and real daily workflow, not theory
- Status: new
```

**When to use:**
- Any time an idea hits — from the shower, commute, mid-study
- Fastest from Telegram — one message and it's saved

---

# SKILL 6: `/rebuild-schedule`

Your Sunday evening ritual. Rebuilds the week.

**Exact command:**
```
/rebuild-schedule
```

**Trigger phrases:**
```
rebuild schedule
rebuild my schedule
sunday schedule
weekly rebuild
plan my week
```

**The flow:**
1. Hermes reads `SCHEDULE.md`, `deadlines/tracker.md`, Google Calendar
2. Asks you 5 questions (answer in one message):
   ```
   1. New deadlines or changes to existing ones?
   2. Tasks completed this week to remove?
   3. Priorities that shifted?
   4. Days/times next week to protect (rest, social, travel)?
   5. Anything else?
   ```
3. Shows you a proposed week plan — full table, Monday to Sunday
4. Waits for your approval or changes
5. Creates Google Calendar events after approval
6. Updates `SCHEDULE.md` with today's date
7. Sends Telegram confirmation

**Run every Sunday at 7 PM.** Google Calendar will remind you automatically (the skill creates this recurring reminder the first time you run it).

---

# SKILL 7: `/start-project`

Get oriented before you open Claude Code on a project.

**Exact command:**
```
/start-project [project-name]
```

**Examples:**
```
/start-project audio-asr
/start-project vibe-proposal
/start-project dsp-homework
```

**Trigger phrases:**
```
start project audio-asr
brief me on audio-asr
what's the status of vibe-proposal
I'm about to work on audio-asr
```

**What it outputs:**
```
Project: audio-asr
What it is: Automatic speech recognition system for Vietnamese audio, using Whisper + custom fine-tuning

Last session (2026-05-14):
  - Added data preprocessing pipeline
  - WER improved from 18% to 14% on test set

Open TODOs:
  - Fix tokenizer bug on sentence boundaries
  - Run evaluation on full dataset
  - Write up results section

Blockers:
  - None currently logged

Suggested focus today: fix the tokenizer bug first, then run evaluation

Architecture reminder:
  - Language: Python, PyTorch
  - Never touch: data/raw/ folder
  - Main entry point: src/train.py

→ Open Claude Code at:
  /home/heigatvu/MyFile/my-project/my-assistance/working-space/lab-run/audio-asr
```

**When to use:**
- Every time before opening Claude Code on a project
- When you haven't touched a project in a few days and need context back
- When switching between projects mid-day

---

# SKILL 8: `/end-project-session`

Log what you did after closing Claude Code.

**Exact command:**
```
/end-project-session [project-name]
```

**Examples:**
```
/end-project-session audio-asr
/end-project-session vibe-proposal
```

**Trigger phrases:**
```
end session audio-asr
log session for audio-asr
done coding on audio-asr
```

**What it asks you:**
```
1. Why did you make these changes? (reasoning, decisions)
2. What are the next steps for next session?
```

**Example answers:**
```
Why: Fixed the tokenizer bug — was splitting on periods inside abbreviations. Used regex lookahead instead.
Next steps: Run full evaluation, write results section, push to remote.
```

**What it writes to `docs/journal.md`:**
```
## 2026-05-17 15:30
### What changed
- Fixed tokenizer boundary detection (regex lookahead)
- Re-ran evaluation pipeline on test set

### Why
Fixed the tokenizer bug — was splitting on periods inside abbreviations.

### Next steps
- Run full evaluation on complete dataset
- Write results section
- Push to remote branch
```

**Shows you the entry before saving. You approve, then it saves.**

**When to use:**
- Every time you close Claude Code on a project
- Even short sessions — 20 minutes of work still deserves a log entry
- If you forgot to log yesterday, run it with "default to 1 day ago" and it still works

---

# SKILL 9: `/project-status`

A dashboard of all your lab-run projects at once.

**Exact command:**
```
/project-status
```

**Trigger phrases:**
```
project status
all projects
status board
what projects do I have
what am I working on
```

**Example output:**
```
Project Status Board — 2026-05-17

| Project          | Last touched  | Status                        | Next step                    |
|------------------|---------------|-------------------------------|------------------------------|
| audio-asr        | 2 days ago    | Evaluation pending            | Run full dataset eval        |
| vibe-proposal    | 5 days ago    | Section 2 in progress         | Finish outline               |
| dsp-homework     | 1 day ago     | Assignment 3 done             | Start assignment 4           |
| bme-proceeding   | ⚠️ 8 days ago | Draft started, stalled        | Resume — deadline in 3 days  |

⚠️ bme-proceeding has not been touched in 8 days and has a deadline in 3 days.
```

**When to use:**
- Monday morning after the weekly cron sends it to Telegram
- Any time you feel lost about where things stand
- Before a `/rebuild-schedule` to get an honest picture of project health

---

# SKILL 10: `/code-review`

Get a structured code review on your most-changed file.

**Exact command:**
```
/code-review [project-name]
```

**Examples:**
```
/code-review audio-asr
/code-review vibe-proposal
```

**Trigger phrases:**
```
code review audio-asr
review my code in audio-asr
review the latest changes in audio-asr
```

**What it does:**
1. Finds the file changed most in the last week (via `git log`)
2. Reads the file and the project's `AGENTS.md` conventions
3. Reviews for: bugs, unclear code, missing tests, style violations
4. If `hermes-agent-acp-skill` is installed: sends the same file to both Claude Code and Gemini and combines their perspectives

**Example output:**
```
Code review: src/tokenizer.py (audio-asr)
Reviewed against AGENTS.md conventions

BUGS
- Line 47: regex pattern doesn't handle Unicode Vietnamese characters — will miss sentence boundaries in test data

UNCLEAR CODE
- Line 83: variable name `tmp2` — rename to `boundary_positions`
- Function `process()` is doing 3 things — split into separate functions

MISSING TESTS
- No test for edge case: empty audio segment input
- No test for sentence boundary at end of file

STYLE
- Consistent with project style overall ✓

Saved to: lab-run/audio-asr/docs/reviews/2026-05-17-tokenizer.md
```

**When to use:**
- After any significant coding session
- Before pushing to a branch you'll share with others
- When something feels wrong but you can't place it
- Weekly code health check — pick one project each week

---

# Cron jobs (automatic — no action needed)

These run without you doing anything:

| Time | What runs | Where it arrives |
|---|---|---|
| Every weekday 10 AM | `/daily-brief` | Telegram |
| Every weekday 3 PM | Healthy Vietnamese recipe | Telegram |
| Every weekday 10 PM | `/end-of-day` | Telegram |
| Every Monday 9 AM | `/project-status` | Telegram |
| Every Sunday 7 PM | Reminder to run `/rebuild-schedule` | Telegram |
| Every day 11 AM, 4 PM, 10 PM | Gmail summary | Telegram |

You don't trigger these — they come to you.

---

# Using skills from Telegram (most common)

From your phone, you can run almost anything by typing naturally:

| What you want | Type in Telegram |
|---|---|
| Morning orientation | `daily brief` |
| Log an idea immediately | `youtube idea: [title] for [audience]` |
| Add a new deadline | `add deadline: [project] — [task] — [date]` |
| Check all projects | `project status` |
| Start a project | `start project audio-asr` |
| Log a session | `end session audio-asr` |
| Wrap up the day | `end of day` |

The most powerful mobile use: capturing ideas and deadlines the second they happen, before you forget.

---

# Common daily patterns

## Normal weekday

```
10:00 AM  [automatic] Daily brief arrives on Telegram — read it
10:15 AM  Type: "start project bme-proceeding" — get briefing
10:20 AM  cd lab-run/bme-proceeding && claude — do the work
12:00 PM  English break (calendar event)
 1:00 PM  Type: "end session bme-proceeding" — log the work
 3:00 PM  [automatic] Recipe arrives on Telegram
 8:00 PM  Study (DSP Coursera / AI VIETNAM / etc)
10:00 PM  [automatic] End-of-day arrives on Telegram — answer it
```

## When a new deadline lands (mid-class, meeting, anywhere)

```
[in Telegram] add deadline: VIBE proposal draft — June 5 — high
```
Saves immediately. Appears in tomorrow's daily brief.

## When an idea hits

```
[in Telegram] youtube idea: "How I survive a master's degree with AI tools" — for stressed grad students
```
Saved to backlog. Won't lose it.

## When you haven't touched a project in a week

```
/project-status
```
See which ones are stale. Use that to plan the coming week in `/rebuild-schedule`.

## Sunday evening (30 minutes)

```
7:00 PM  Google Calendar reminder fires
7:05 PM  cd ~/.hermes && hermes
7:06 PM  /rebuild-schedule
7:10 PM  Answer 5 questions
7:15 PM  Review proposed week plan
7:18 PM  Approve — calendar events created
7:20 PM  Done until next Sunday
```

---

# Tips for getting the most out of the skills

**Log every session, even short ones.** A 20-minute session that's logged is more valuable than a 3-hour session that isn't. Future you needs the context.

**Answer end-of-day honestly.** If you say "completed everything" when you didn't, the morning brief tomorrow will be wrong. Takes 2 minutes to be accurate.

**Use Telegram for captures, terminal for reviews.** Deadlines and ideas → Telegram (fast, anywhere). Code reviews and project briefings → terminal (you're at your desk anyway).

**Don't skip Sunday rebuild.** Even if the week went perfectly, rebuild anyway. It resets your calendar and updates `SCHEDULE.md`. A missed Sunday means a blind Monday.

**If a skill gives wrong output, fix it.** Open Claude Code at `~/.hermes` and ask it to patch the skill. Don't work around bad output — fix the source.
