# XAUUSD Forex Factory News Calendar

A rolling Apple Calendar subscription for **USD High and Medium** Forex Factory events with **30-minute reminders**. Times are stored in UTC so Apple Calendar displays correct UK GMT/BST times.

## Setup
1. Open **Actions > Update Forex Calendar > Run workflow** to test the data download.
2. In **Settings > Actions > General**, grant **Read and write permissions** to GITHUB_TOKEN if commits fail.
3. In **Settings > Pages**, choose **Deploy from a branch**, branch **main**, folder **/(root)**, and Save.
4. Subscribe in Apple Calendar: **File > New Calendar Subscription**, using:
   https://robertkis1.github.io/forex-factory-gold-calendar/xauusd_news.ics
5. Set subscription auto-refresh to daily, if offered. Test reminders on your devices.

The workflow runs daily at 06:20 UTC, but Forex Factory's unofficial weekly export may be blocked or rate-limited. Check Actions failures. The calendar accumulates upcoming events as they are published, **not a guaranteed year of events in advance**. Alerts on subscribed calendars may be ignored by Apple Calendar; verify before relying on them for trading. Public repository and calendar contents are visible to anyone.

Source: https://nfs.faireconomy.media/ff_calendar_thisweek.ics. Respect the source's terms of use and rate limits.
