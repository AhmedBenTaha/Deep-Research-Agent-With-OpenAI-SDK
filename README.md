# Deep Research Agent

A small Gradio app that turns a research question into a multi-step research workflow. It uses OpenAI Agents SDK agents to plan searches, gather web results, write a Markdown report, and deliver the report by email (or Pushover).

## How it works

1. The planner creates a set of search queries (4 by default).
2. A search agent uses the Agents SDK web search tool for each query.
3. The writer combines the gathered summaries into a detailed report.
4. The email agent formats and sends the report using the configured notification method.

The Gradio interface streams progress updates and then displays the completed report. A trace link is also shown for each run.

## Requirements

- Python 3.10 or newer
- A Groq API key for the planning and report-writing agents
- An OpenAI API key for the built-in web search agent
- SMTP credentials for email delivery, or Pushover credentials when using push notifications

## Setup

From this directory, create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in this directory. For email delivery, configure:

```dotenv
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
EMAIL_ADDRESS=you@example.com
EMAIL_APP_PASSWORD=your_smtp_app_password
EMAIL_SMTP_SERVER=smtp.gmail.com
USE_EMAIL=true
```

Email is sent to the address in `EMAIL_ADDRESS`. Use an SMTP app password where your email provider requires one; do not commit `.env` or share API keys.

To send notifications through Pushover instead, set `USE_EMAIL=false` and add:

```dotenv
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_application_token
```

Optional model and search-count settings:

```dotenv
DEFAULT_MODEL_NAME=openai/gpt-oss-120b
OPENAI_MODEL_NAME=gpt-4o
NUM_SEARCHES=4
```

`DEFAULT_MODEL_NAME` is used by the Groq-backed planner and writer. `OPENAI_MODEL_NAME` selects the search agent model.

## Run

```bash
python app.py
```

Open the local URL printed by Gradio, enter a research question, and select **Investigate**. The first run requires the API and notification credentials above.

## Project files

- `app.py` — Gradio user interface
- `research_manager.py` — coordinates planning, search, writing, and delivery
- `planner_agent.py` — creates the search plan
- `search_agent.py` — searches the web and summarizes results
- `writer_agent.py` — produces the final report
- `email_agent.py` — prepares and sends the notification
- `messanger.py` — SMTP and Pushover delivery helpers
- `styles.py` — interface styling and examples

## Notes

- Search queries are run concurrently, so the number of searches affects runtime and API usage.
- Reports are generated from the gathered search summaries. Review citations and important claims before relying on a report.
- The application emits an OpenAI platform trace URL for each research run.

