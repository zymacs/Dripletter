# Dripletter

A PDF book drip service to increase likelihood for reading through huge books by emailing smaller portions on a user defined schedule.

## Description

Dripletter splits PDF files into configurable chunks and automatically emails them on a schedule you define. Define your schedule using natural language phrases like:

- `"Every day at 10:00pm"`
- `"Every Mon, Tue, Wed at 6:00"`

The app uses system cron to manage scheduled broadcasts, SQLite for tracking deliveries, and Gmail SMTP for sending emails.

## How It Works

1. **Search & Select** — Find a PDF in your documents folder
2. **Configure** — Set page range, chunk size, and who receives it
3. **Schedule** — Define when emails are sent using natural language
4. **Automate** — Cron handles sending; the app tracks delivery status in the database

## Requirements

- Python 3.7+
- Unix/Linux system (uses system cron)
- Gmail account with app password enabled

## Installation

```bash
# Clone the repository
git clone https://github.com/kithenry/Dripletter.git
cd Dripletter

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

First run will prompt you to create `config.py` with these settings:

```
System user:          # Your Linux username
Sender email:         # Gmail address sending the emails
Sender app password:  # Google app password (not your regular password)
Documents location:   # Full path to folder containing PDFs (e.g., /home/user/Books)
Default split size:   # Default pages per email chunk (default: 5)
Default recipients:   # Email addresses to receive broadcasts
```

**Getting a Google App Password:**
1. Enable 2-factor authentication on your Google account
2. Visit [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Follow the prompts to setup the password.
4. Copy the 16-character app password

## Usage

```bash
python main.py
```

You'll be prompted to:

1. **Search for a file** — Enter a search term to find your PDF
2. **Confirm pages** — Opens PDF so you can set start/end pages (optional)
3. **Set chunk size** — How many pages per email
4. **Name the broadcast** — A short alias for this book (e.g., "dune")
5. **Set schedule** — When to send emails (e.g., `"Every Saturday at 7:21pm"`)

The app then:
- Splits the PDF into chunks in `{working_dir}/{book_name}/`
- Creates a database table to track delivery status
- Adds a cron job to run `broadcaster.py` on your schedule

## Dependencies

- **pymupdf** — PDF manipulation and splitting
- **python-crontab** — Create and manage cron jobs
- **sqlalchemy** — Database ORM (SQLite)

## File Structure

```
main.py              Entry point; handles setup and PDF splitting
broadcaster.py       Cron job that sends queued emails
mailer.py            Gmail SMTP sender
splitter.py          PyMuPDF wrapper for splitting PDFs
scheduler.py         Cron job manager (python-crontab wrapper)
cronconverter.py     Parses natural language to cron syntax
db_manager.py        SQLite database operations
file_manager.py      File search in documents folder
config.py            Generated on first run with your settings
cds.db              SQLite database tracking broadcasts
```

## Current Limitations

- **Unix/Linux only** — Requires system cron (future: platform-independent scheduler)
- **Fixed chunk sizes** — All emails for a broadcast have same page count
- **No pause/resume** — Must delete folder and database table to stop
- **Manual management** — No CLI to modify schedules after creation
- **No book covers** — Emails contain only PDF pages
- **Command-line only** — No web or GUI interface yet

## Database Schema

Each broadcast creates a table `{alias}_table` with:

```sql
id                  (INTEGER PRIMARY KEY)
file_name           (TEXT)
file_path           (TEXT)
send_status         (TEXT) — 'pending', 'sent', 'failed'
send_date           (TEXT)
broadcast_frequency (TEXT) — e.g., "Every day at 10:00pm"
planned_send_time   (TEXT) — parsed from frequency
```

## Troubleshooting

**"Document not found"**
- Ensure PDF is in the folder specified in config.py
- Check folder permissions

**"xdg-open: command not found"**
- Not available on all systems; the app tries to open the PDF for preview but continues without it

**"Cron job not running"**
- Verify cron daemon is active: `systemctl status cron`
- Check that the system user in config.py matches your actual username

**"Emails not sending"**
- Verify Gmail app password (not your regular password)
- Confirm 2FA is enabled on Google account
- Check logs in `cds_logs.txt`

## License

MIT License — see [LICENSE](LICENSE) file

## Contributing

Pull requests welcome. See [Issues](https://github.com/kithenry/Dripletter/issues) for areas needing work.
