# Hermes Schedule — Setup Guide

Run through this once to get everything connected. After this, the crons run automatically.

---

## Step 1: Connect Google Calendar and Gmail via MCP

In any Hermes session:

```
Connect to Google Calendar MCP at https://calendarmcp.googleapis.com/mcp/v1 and Gmail MCP at https://gmailmcp.googleapis.com/mcp/v1. Save both connections to memory so they're available in every session.
```

Test the connection:

```
Read my Google Calendar for today and list all events.
```

```
Summarize my last 5 Gmail emails.
```

If both return real data, you're connected.

---

## Step 2: Load your schedule into Hermes memory

```bash
cd /home/heigatvu/MyFile/my-project/my-assistance/working-space/hermes-schedule
hermes
```

Paste:

```
Read SCHEDULE.md fully. Save all constraints, rules, time blocks, and priorities to memory. Confirm what you've saved.
```

Check the output — make sure Hermes correctly understood:

- Sleep block (12 AM – 7 AM)
- Rest block (3 PM – 8 PM weekdays)
- Work window (8 AM – 3 PM weekdays)
- Study window (8 PM – 12 AM weekdays)
- Weekend rules

---

## Step 3: Register all cron jobs

Paste each of these one at a time, confirm each works before moving to the next.

### Cron 1: Daily schedule at 10 AM

```
Set up a cron: every day at 10 AM (GMT+7), read SCHEDULE.md, check Google Calendar for today's events, list my active work tasks ranked by deadline from /home/heigatvu/MyFile/my-project/my-assistance/working-space/hermes-schedule/deadlines/tracker.md, suggest time blocks for the work window (8 AM–3 PM), flag any deadline within 7 days, and remind me of tonight's study topic. Send to Telegram.
```

### Cron 2: Gmail summary at 11 AM, 4 PM, 10 PM

```
Set up a cron: every day at 11 AM, 4 PM, and 10 PM (GMT+7), summarize new important Gmail emails since the last summary. Flag anything urgent or deadline-related. Keep it to 5 lines max unless something is critical. Send to Telegram.
```

### Cron 3: Healthy Vietnamese recipe at 3 PM

```
Set up a cron: every day at 3 PM (GMT+7), suggest one healthy Vietnamese dinner recipe for tonight (under 45 min cook time), one quick breakfast for tomorrow, and one lunch for tomorrow that can be prepped tonight. Never repeat a recipe suggested in the last 7 days — check memory for recent suggestions. Send to Telegram.
```

### Cron 4: Daily optimization review at 10 PM

```
Set up a cron: every day at 10 PM (GMT+7), review what was completed today vs the morning plan, check if any deadlines shifted, suggest adjustments to tomorrow's schedule, recommend one study topic for the remaining time tonight, and give one sentence on what to focus on first tomorrow morning. Send to Telegram.
```

### Cron 5: Weekly planning on Sunday at 8 PM

```
Set up a cron: every Sunday at 8 PM (GMT+7), read /home/heigatvu/MyFile/my-project/my-assistance/working-space/hermes-schedule/deadlines/tracker.md, the last entry in /home/heigatvu/MyFile/my-project/my-assistance/working-space/lab-run/*/docs/journal.md, /home/heigatvu/MyFile/my-project/my-assistance/working-space/hermes-schedule/youtube/pipeline.md, and next week's Google Calendar. Propose a work allocation plan for the week — which project gets which mornings. Flag any week with 2+ deadlines as high-pressure and suggest what to defer. Send to Telegram.
```

---

## Step 4: Test the calendar scheduling flow

This is the most important one to test manually before trusting it.

```
Based on SCHEDULE.md and my Google Calendar, propose a schedule for tomorrow. Show me the proposed time blocks before adding anything to the calendar. Wait for my approval.
```

Review what it proposes. Check:

- Does it respect the sleep block?
- Does it respect the 3 PM–8 PM rest window?
- Does it prioritize by deadline correctly?
- Does it ask for approval before touching the calendar?

If yes on all — approve, and it creates the events.

---

## Step 5: Protect your rest blocks in Google Calendar

Before relying on Hermes for scheduling, manually create these as recurring "busy" events in Google Calendar so they're protected even if Hermes forgets a rule:

- **Sleep:** 12 AM – 7 AM daily (recurring)
- **Rest/buffer:** 3 PM – 8 PM weekdays (recurring)
- **Weekend morning free:** Saturday + Sunday 7 AM – 10 AM (recurring)

This is a safety net — even if a prompt goes wrong, your calendar physically blocks those slots.

---

## Daily usage (once set up)

Everything runs automatically via crons. You only need to open Hermes manually when:

- Adding a new deadline: `Add to deadline tracker: [project] — [task] due [date]`
- Rescheduling something: `Move tomorrow's DLD session to Thursday — I have a conflict`
- Checking status: `What's my most urgent deadline right now?`
- Requesting a recipe swap: `Skip the recipe today, suggest something different tomorrow`

---

## Troubleshooting

**Crons not firing:** check that Hermes is running as a background service (`hermes service status`). If not: `hermes service start`.

**Calendar not updating:** re-test the MCP connection with `Read my Google Calendar for today`.

**Wrong timezone:** remind Hermes: `All times are GMT+7. Ho Chi Minh City. Update memory.`

**Recipe repeating:** `Clear recipe memory and start fresh. Here are recipes to avoid this week: [list]`
