# AraonJR Bot Setup Instructions

This guide will help you set up and run the modernized AraonJR Discord bot.

## Initial Setup

1. **Create a Virtual Environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Development Dependencies (for testing)**
   ```bash
   pip install pytest pytest-asyncio pytest-cov
   ```

4. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Edit `.env` with your Discord bot token and other settings
   ```bash
   # Create a copy of the example .env file
   copy .env.example .env
   # Edit the .env file with your preferred editor
   ```

## Running the Bot

1. **Start the Bot**
   ```bash
   python bot.py
   ```

2. **For Music Features**
   The bot requires a Lavalink server for music playback. You can either:
   - Set up your own Lavalink server
   - Use a public Lavalink server (change settings in the music cog)

## Testing

1. **Running Unit Tests**
   ```bash
   # Using pytest directly
   pytest

   # Or using the run_tests.py script
   python run_tests.py
   ```

## Key Features Added

1. **Modern Discord Integration**
   - Implemented slash commands using Discord.py 2.0+
   - Added proper permission handling
   - Enhanced embed usage for better readability

2. **Organized Codebase**
   - Implemented proper cog system
   - Separated utilities into modules
   - Improved error handling

3. **New and Enhanced Commands**
   - Modernized music system using Wavelink
   - Enhanced moderation commands with better feedback
   - Added utility commands like sentiment analysis and wiki searches
   - Reimplemented fun commands with better visuals

4. **Testing Framework**
   - Added unit tests for utilities and commands
   - Set up proper test configuration

## Bot Structure

The bot now follows a modern, modular structure:

- `bot.py` - Main entry point
- `cogs/` - Command modules
- `utils/` - Utility functions
- `configs/` - Configuration files
- `tests/` - Unit tests

## Troubleshooting

If you encounter any issues:

1. **Bot Won't Start**
   - Check that your `.env` file has the correct `BOT_TOKEN`
   - Ensure you have all dependencies installed

2. **Music Commands Not Working**
   - Verify that Lavalink is running and configured correctly
   - Check that the bot has permission to join and speak in voice channels

3. **Tests Failing**
   - Make sure all development dependencies are installed
   - Verify that you're running tests from the project root directory
