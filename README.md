# AraonJR v2.0

Modernized Discord bot for server moderation and entertainment built with Discord.py 2.0+

## Features

- **Modern Discord Integration**: Built with Discord.py 2.0+ using Slash Commands
- **Advanced Music System**: High-quality music playback with interactive controls
- **Moderation Tools**: Ban, kick, unban, clear messages, and more
- **Fun Commands**: Various entertainment commands like slap, worth, poke, and more
- **Utility Features**: Wikipedia summaries, sentiment analysis, user info
- **Organized Codebase**: Well-structured with cogs for easy maintenance
- **Comprehensive Testing**: Unit tests to ensure stability

## Requirements

- Python 3.8 or higher
- Discord Bot Token - [Create one here](https://discord.com/developers/applications)
- Lavalink server for music playback (optional)

## Installation

### Standard Installation

```bash
# Clone the repository
git clone https://github.com/Araon/AraonJR.git
cd AraonJR

# Create and activate virtual environment (recommended)
python -m venv venv
# On Windows
venv\Scripts\activate  
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Using setup.py (Alternative)

```bash
pip install -e .
```

## Configuration

1. Create a `.env` file in the project root directory with the following content:

```
BOT_TOKEN=your_discord_bot_token_here
PREFIX=;  # Optional prefix for legacy commands
OWNER_ID=your_discord_user_id
TESTING_GUILD_ID=your_test_server_id  # For testing slash commands
```

## Running the Bot

```bash
python bot.py
```

## Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test file
python run_tests.py tests/test_wiki_utils.py
```

Or use pytest directly:

```bash
python -m pytest
```

## Project Structure

```
AraonJR/
├── bot.py                # Main bot file
├── cogs/                 # Command modules
│   ├── general.py        # General commands
│   ├── moderation.py     # Moderation commands
│   ├── music.py          # Music commands
│   ├── utility.py        # Utility commands
│   └── fun.py            # Fun commands
├── configs/              # Configuration files
│   └── config.py         # Bot configuration
├── utils/                # Utility functions
│   ├── bot_utils.py      # General bot utilities 
│   ├── sentiment_utils.py # Sentiment analysis
│   └── wiki_utils.py     # Wikipedia utilities
└── tests/                # Unit tests
```

## Legacy Support

This is a modernized version of the original AraonJR bot. While the focus is on new slash commands, we've maintained compatibility with most of the original functionality.

## Screenshots

![Menu](https://i.ibb.co/XYjB90j/araonjr.png)

## Author

[Araon](https://github.com/Araon)
