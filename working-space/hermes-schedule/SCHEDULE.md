# Hermes Schedule

This file tracks your schedule, cross-referenced with your Google Calendar.
Last updated: 2026-05-16

---

## User Profile

- **Name:** Heigatvu
- **Timezone:** GMT+7 (Ho Chi Minh City)
- **Role:** Master's student + developer + YouTube creator + piano learner

---

## User Schedule (GMT+7)

### Weekdays

| Time               | Block                             | Content                                   |
| ------------------ | --------------------------------- | ----------------------------------------- |
| 7:00 AM            | Wake up / Morning routine         | —                                         |
| 8:00 AM – 3:00 PM  | **Work**                          | See active work below                     |
| 12:00 PM – 1:00 PM | **Daily English**                 | (inside work block — fixed)               |
| 3:00 PM            | **Healthy Recipe Cron**           | Dinner tonight + breakfast/lunch tomorrow |
| 3:00 PM – 8:00 PM  | Buffer / rest / exercise / social | Protected — do not schedule work here     |
| 8:00 PM – 12:00 AM | **Study**                         | See study topics below                    |
| 12:00 AM – 7:00 AM | **Sleep**                         | Never schedule anything here              |

### Weekends

- Morning (before 10 AM): fully free — do not schedule
- Rest, review, social
- Light review sessions allowed if user requests
- No hard deadlines should land on weekends unless user explicitly sets them

---

## Active Work (Weekdays 8 AM – 3 PM)

Priority order — Hermes allocates time to these based on deadlines:

1. **Master presentation** — highest priority when deadline is within 14 days
2. **VIBE proposal** — high priority, check deadline in `~/masters/deadlines/tracker.md`
3. **DLD/SSD research design** — medium priority
4. **BME proceeding** — medium priority
5. **Academic document** — ongoing, fill remaining work slots

---

## Study Topics (Weekdays 8 PM – 12 AM)

**Specific topics are tracked in the learning tracker:**
`/home/heigatvu/MyFile/my-project/my-assistance/working-space/learning/tracker.md`

Hermes reads this file on every `/daily-brief` to tell you exactly what to study.

Courses and their calendar slots:

- **DSP Coursera** — Monday/Wednesday/Friday 20:00–22:00
- **AI VIETNAM** — Monday/Wednesday/Friday 22:00–00:00
- **Speech Processing** — Tuesday/Thursday 20:00–22:00
- **English** — Tuesday/Thursday 22:00–00:00 (supplement to 12–1 PM daily block)
- **Statistics Book** — Saturday 20:00–22:00

---

## Agent Rules

### Hard constraints — never violate

- **Sleep block:** 12 AM – 7 AM — nothing scheduled here, ever
- **Weekend mornings:** before 10 AM — fully free
- **3 PM – 8 PM weekdays:** rest/buffer — do not schedule unless user explicitly asks
- **Daily English 12–1 PM:** fixed — do not move or overlap

### Work window

- Agent may suggest or schedule tasks between **10 AM – 11 PM** only
- Preferred deep work window: **8 AM – 12 PM** (focus tasks: writing, coding, research)
- Preferred light tasks window: **2 PM – 3 PM** (admin, review, email)
- Study window: **8 PM – 12 AM**

### Google Calendar rules

- **Always check** calendar for existing events before adding anything (8 AM – 11 PM range)
- **Never overwrite** events already in the calendar
- **Show proposed schedule** to user before creating events — wait for approval
- Events marked "personal" or "rest" are untouchable
- Cross-reference `~/masters/deadlines/tracker.md` when allocating work sessions

---

## Cron Jobs

### 1. Daily schedule — 10 AM every day

Send to Telegram:

```
Good morning. Here is your schedule for today:
- Pull today's Google Calendar events
- List active work tasks ranked by deadline
- Suggest time blocks for each work task within the 8 AM–3 PM window
- Flag any deadline within 7 days as urgent
- Remind of study topic for tonight (8 PM–12 AM)
```

### 2. Gmail summary — 11 AM, 4 PM, 10 PM every day

Send to Telegram:

```
Gmail summary for [time]:
- New important emails since last summary
- Any emails needing a reply today
- Flag anything related to academic deadlines or project updates
```

### 3. Healthy Vietnamese recipe — 3 PM every day

Send to Telegram:

```
3 PM meal planning:
- Suggest one healthy Vietnamese dinner recipe for tonight (simple, under 45 min cook time)
- Suggest breakfast for tomorrow (quick, nutritious)
- Suggest lunch for tomorrow (can be prepped tonight)
Keep suggestions varied — avoid repeating the same recipe within 7 days.
```

### 4. Daily optimization review — 10 PM every day

Send to Telegram:

```
End-of-day review:
- What was completed today vs planned?
- Any deadlines moved or added?
- Adjust tomorrow's schedule if needed
- Suggest one study topic for the remaining time tonight (until 12 AM)
- One sentence: what to focus on first thing tomorrow morning
```

### 5. Weekly planning — Sunday 8 PM

Send to Telegram:

```
Weekly planning for the coming week:
- Read /home/heigatvu/MyFile/my-project/my-assistance/working-space/hermes-schedule/deadlines/tracker.md for upcoming deadlines
- Read /home/heigatvu/MyFile/my-project/my-assistance/working-space/lab-run/tracker.md for dev project status (flag stale >4 days)
- Read /home/heigatvu/MyFile/my-project/my-assistance/working-space/lab-run/*/docs/journal.md for dev project session logs
- Read /home/heigatvu/MyFile/my-project/my-assistance/working-space/learning/tracker.md for learning progress
- Read /home/heigatvu/MyFile/my-project/my-assistance/working-space/hermes-schedule/youtube/pipeline.md for content pipeline
- Check Google Calendar for fixed commitments next week
- Propose a work allocation plan (which project gets which work slots)
- Allocate morning deep-work slots for the most-stale active project
- Flag any week with 2+ deadlines as high-pressure and suggest what to defer
```

---

## Priority Matrix

When two tasks compete for the same slot, use this order:

1. Academic deadline within 7 days → always wins
2. Academic deadline within 14 days → high priority
3. Active dev project with a blocker → schedule next available slot
4. YouTube (only if no academic deadline within 7 days)
5. Study rotation → fills remaining evening slots
6. Piano practice → minimum 20 min/day, flexible time, evening preferred

---

## Deadlines Reference

Hermes reads this file combined with:

- `/home/heigatvu/MyFile/my-project/my-assistance/working-space/hermes-schedule/deadlines/tracker.md` — academic deadlines
- `/home/heigatvu/MyFile/my-project/my-assistance/working-space/learning/tracker.md` — learning progress (what to study tonight)
- `/home/heigatvu/MyFile/my-project/my-assistance/working-space/lab-run/*/docs/journal.md` — dev project status
- `/home/heigatvu/MyFile/my-project/my-assistance/working-space/hermes-schedule/youtube/pipeline.md` — content pipeline
- Google Calendar — fixed commitments

---

## Notes for Hermes

- User is based in Ho Chi Minh City (GMT+7). Always use GMT+7 for all times.
- When suggesting recipes, keep them Vietnamese and healthy. Avoid repeating within 7 days.
- When summarizing Gmail, be concise — 5 lines max per summary unless something is urgent.
- Always ask for approval before creating, editing, or deleting Google Calendar events.
- If a deadline is missed or a session was skipped, log it and suggest how to recover — don't just reschedule blindly.

Last updated: 2026-05-18
