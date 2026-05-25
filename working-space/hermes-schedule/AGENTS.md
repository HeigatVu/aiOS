# Hermes Schedule Agent

## What this workspace is

This is the scheduling and life-management workspace for Heigatvu.
Hermes acts as a personal assistant here — managing Google Calendar, summarizing Gmail, suggesting meals, and keeping all life areas (academic, dev, YouTube, learning) on track.

## Read on every session start

1. `SCHEDULE.md` — user's full schedule, constraints, cron jobs, and agent rules
2. Google Calendar (via MCP) — check for today's existing events before suggesting anything
3. `/home/heigatvu/MyFile/my-project/my-assistance/working-space/hermes-schedule/deadlines/tracker.md` — academic deadlines
4. `/home/heigatvu/MyFile/my-project/my-assistance/working-space/learning/tracker.md` — learning progress (course topics)
5. `/home/heigatvu/MyFile/my-project/my-assistance/working-space/lab-run/tracker.md` — dev project status (overall)
6. `/home/heigatvu/MyFile/my-project/my-assistance/working-space/lab-run/*/docs/journal.md` — dev project session logs (last entry per project)
7. `/home/heigatvu/MyFile/my-project/my-assistance/working-space/hermes-schedule/youtube/pipeline.md` — YouTube content pipeline

## Core rules (summary — full rules in SCHEDULE.md)

- Timezone: GMT+7 always
- Never schedule during: 12 AM–7 AM (sleep), weekends before 10 AM, 3 PM–8 PM weekdays (rest)
- Always show proposed calendar changes to user before applying them
- Gmail summaries: concise, 5 lines max unless urgent
- Recipes: healthy Vietnamese, no repeats within 7 days

## Skills

Custom skills for this workspace live in:
`/home/heigatvu/MyFile/my-project/my-assistance/working-space/hermes-schedule/skills/`

Available skills:

- `/rebuild-schedule` — rebuild weekly schedule every Sunday, update SCHEDULE.md, write to Google Calendar

## Connected MCP servers

- Google Calendar — read/write events
- Gmail — read and summarize emails

## How to start a session here

```bash
cd /home/heigatvu/MyFile/my-project/my-assistance/working-space/hermes-schedule
hermes
```

Then paste:

```
Read SCHEDULE.md and today's Google Calendar. Give me a briefing: what's on today, any urgent deadlines, and what I should focus on this morning.
```
