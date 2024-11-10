# JobWatcher Bot

🌐 *[English](README.md) | [Русский](README_RU.md) | [Українська](README_UA.md)*

JobWatcher is a Telegram bot designed to automatically gather and publish job vacancies from various sources, focusing on art, design, and other creative industries. The bot notifies users about new opportunities based on their interests and provides custom search and subscription options.

## ✨ Features

1. **🔍 Job Search and Filtering**:
   - Collects job data from multiple websites and APIs (see the list of sources below).
   - Filters vacancies by region (Ukraine, CIS countries, Poland, Canada).
   - Filters by categories, such as art, design, and creative industries.

2. **🧹 Analysis and Sorting**:
   - Removes duplicate job postings.
   - Shows only recent vacancies.
   - Standardizes job listings (title, company, description, requirements, contact information).

3. **📢 Publishing to Telegram**:
   - Automatically posts new job listings to primary and secondary channels: [ArtLeads](https://t.me/artleads) and [Distant Job](https://t.me/distant_job).
   - Regular updates up to 10 times per day.

4. **🔔 Custom User Notifications**:
   - Responds to user queries for job searches, including keyword and skill filters (e.g., "illustrator," "UI/UX designer").
   
5. **⚙️ Bot Management**:
   - Admin panel with commands for bot management.
   - Logs bot activity (published jobs, processed requests).

6. **💬 User Support**:
   - Allows users to subscribe to specific categories for job alerts.
   - `/help` command for bot instructions and guidance.

7. **🔗 Integration and Updates**:
   - API integration for supported job sites.
   - Adapts to changes on job listing websites.

## 🚀 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/progeroffline/jobwatcher.git
   cd jowatcher
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
   - Open `.env` and replace placeholders with your specific details, including `BOT_TOKEN` and `DATABASE_URL`.

4. **Run Database Migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Start the Bot**:
   ```bash
   cd src
   python3 -m bot
   ```

## 🌐 Job Sources

The bot collects job listings from the following websites (this list may change based on configuration):
- [Source 1](https://example.com)
- [Source 2](https://example.com)
- [Source 3](https://example.com)
- [Source 4](https://example.com)

*The complete list of sources and their configurations is available in the configuration file.*

## 🔑 Key Commands

- `/start` — Starts the bot and shows a welcome message.
- `/help` — Lists the bot's capabilities and commands.
- `/subscribe [category]` — Subscribes to notifications for new jobs in a specific category.
- `/unsubscribe [category]` — Cancels notifications for a specific category.
- `/search [keywords]` — Finds jobs that match specific keywords.

## 🤝 Contributing

Contributions are welcome! Open a pull request or create an issue to propose changes or suggest new features.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
