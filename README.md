# XAUUSD Forex Factory News Calendar

A rolling Apple Calendar subscription for **USD High and Medium** Forex Factory events with **30-minute reminders**. Times are stored in UTC so Apple Calendar displays correct UK GMT/BST times.

## Live status dashboard

Open **https://robertkis1.github.io/forex-factory-gold-calendar/** to see the latest GitHub Actions run, its freshness, whether the public ICS is accessible, and how many future events it contains. The dashboard checks every five minutes while open; it is not an independent background monitoring service. GitHub Actions can occasionally delay or skip scheduled runs.

## Automated failure alerts

An independent watchdog workflow runs hourly at minute 43 UTC. It checks:
- The latest updater run occurred within the last three hours and did not fail.
- The public GitHub Pages ICS is accessible and has a valid calendar envelope.
- It reports the number of upcoming events, but does not treat zero future events as a failure.

If a check fails, the watchdog creates a GitHub Issue named **[Calendar Monitor] Automation or feed problem** (or comments on the existing open issue) and marks its own workflow run as failed. It automatically closes the issue when checks recover.

**To receive emails:** enable GitHub Actions failure emails in [GitHub notification settings](https://github.com/settings/notifications), verify your notification email, and enable email delivery for participating/watching repository issue notifications if you want issue alerts. Email delivery depends on your GitHub preferences; GitHub issues are not an independent mail service. The watchdog itself is a scheduled GitHub Action and therefore may also be delayed or skipped.

## Setup
1. Open **Actions > Update Forex Calendar > Run workflow** to test the data download.
2. In **Settings > Actions > General**, grant **Read and write permissions** to GITHUB_TOKEN if commits fail.
3. In **Settings > Pages**, choose **Deploy from a branch**, branch **main**, folder **/(root)**, and Save.
4. Subscribe in Apple Calendar: **File > New Calendar Subscription**, using:
   https://robertkis1.github.io/forex-factory-gold-calendar/xauusd_news.ics
5. Set subscription auto-refresh to every 15 minutes, if offered. Test reminders on your devices.

The workflow is scheduled hourly at minute 17 UTC, but Forex Factory's unofficial weekly export may be blocked or rate-limited. Check Actions failures. The calendar accumulates upcoming events as they are published, **not a guaranteed year of events in advance**. Alerts on subscribed calendars may be ignored by Apple Calendar; verify before relying on them for trading. Public repository and calendar contents are visible to anyone.

Source: https://nfs.faireconomy.media/ff_calendar_thisweek.ics. Respect the source's terms of use and rate limits.
