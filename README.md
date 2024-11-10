# JobWatcher

*[English](README.md) | [Русский](README_RU.md)*

A Telegram bot for automatically collecting and publishing job vacancies from various sources. This bot searches for jobs in art, design, and other creative industries, posting them in a Telegram channel and notifying users about new opportunities based on their preferences.

## Features

1. **Job Search and Filtering**:
   - Collects job data from various websites and APIs (see the list of sources below).
   - Filters vacancies by region (Ukraine, CIS countries, Poland, Canada).
   - Filters by categories, such as art, design, and creative industries.

2. **Analysis and Sorting**:
   - Removes duplicate job postings.
   - Filters only fresh vacancies.
   - Normalizes job data to a consistent format (title, company, description, requirements, contact information).

3. **Publishing to Telegram**:
   - Automatically publishes new job listings to main and additional channels: [ArtLeads](https://t.me/artleads) and [Distant Job](https://t.me/distant_job).
   - Periodically updates the channels (up to 10 times per day).

4. **Custom User Notifications**:
   - Searches for jobs based on user queries, including keyword and skill filters (e.g., "illustrator," "UI/UX designer").
   
5. **Bot Management**:
   - Admin panel for bot management through commands.
   - Logs bot activity (published jobs, processed requests).

6. **User Support**:
   - Subscription to notifications about new vacancies by selected categories.
   - `/help` command for bot usage instructions.

7. **Integration and Updates**:
   - API support for job sites (where available).
   - Adapts to changes on job listing websites.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/job-vacancy-bot.git
   cd job-vacancy-bot
   ```

2. **Set Up a Virtual Environment and Install Dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   - Copy `env-dist` to `.env`:
     ```bash
     cp env-dist .env
     ```
   - Fill in `.env` with your data, including `BOT_TOKEN`, `DATABASE_URL`, and other necessary settings.

4. **Run Database Migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Start the Bot**:
   ```bash
   python src/bot/__main__.py
   ```

## Job Sources

The bot collects job listings from the following websites (this list may change based on configuration):
- [Source 1](https://example.com)
- [Source 2](https://example.com)
- [Source 3](https://example.com)
- [Source 4](https://example.com)

*The full list and source configurations are available in the configuration file.*

## Key Commands

- `/start` — Starts the bot and displays a welcome message.
- `/help` — Provides information about bot capabilities and available commands.
- `/subscribe [category]` — Subscribes to notifications for new jobs in the chosen category.
- `/unsubscribe [category]` — Unsubscribes from notifications.
- `/search [keywords]` — Searches for jobs based on specified keywords.

## Contributing

New ideas and improvements are welcome. Feel free to open pull requests or create new issues.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
