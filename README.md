## Slack Weekly Summary Bot
Summarizes the past 7 days of messages from a source Slack channel, 
writes a custom update using ChatGPT engine with a structured prompt, and posts back to a summary channel.

- Fetches last 7 days of Slack messages
- Summarizes them via GPT model
- Posts output back to Slack automatically
- Weekly scheduling can be set up with Github workflow actions

# Requirements
- Python 3.10 or newer
- Slack App with the following OAuth scopes:
  - `channels:history`
  - `groups:history`
  - `chat:write`
- OpenAI API key



## Setup:

# Clone repo
git clone https://github.com/<your-username>/slack-weekly-summary.git
cd slack-weekly-summary

## Create a virtual env
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# OR
.venv\Scripts\activate      # Windows

# Install dependancies
pip install -r requirements.txt



## Environment Setup:
## This project uses a .env file to store your API keys and Slack configuration.

# Copy the example file
cp .env.example .env

# Edit .env and replace placeholders
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
OPENAI_API_KEY=sk-your-openai-key
PROJECT_CHANNEL_ID=C1234567890
SUMMARY_CHANNEL_ID=C0987654321



## Usage
# Run the program locally:
python main.py

# Customize prompting
The summary format lives in prompts.py.
You can freely modify it — for example, change the tone, structure, or categories:

# Automate with GitHub Actions:
The included workflow .github/workflows/weekly.yml runs this script weekly.
TO configure:
- Push script to Github
- Add .env variables to Actions/Secrets
- By default, it runs every Thursday at 9:00 AM ET. Edit cron line in weekly.yml to change the time.