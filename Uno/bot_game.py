import asyncio
from telegram import Update, Bot, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
from Player import Player
from Game import Game
import os

TOKEN = "6880900785:AAH_4ftHZLP8MNJW5Ta-LZJl-jCoUL4goFg"
IMAGE_DIRECTORY = "CardsImage"  # Added directory path for card images
IMAGE_DIRECTORY = "CardsImage"  # Added directory path for card images

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    if 'players' not in context.bot_data:
        context.bot_data['players'] = []
    if len(context.bot_data['players']) < 2:
        player_name = update.message.from_user.first_name
        context.bot_data['players'].append(Player(player_name, chat_id))
        await update.message.reply_text(f"Welcome, {player_name}! You have been added to the game.")
        if len(context.bot_data['players']) == 2:
            await update.message.reply_text("Two players have joined. The game will start now!")
            await start_game(context.bot, context.bot_data['players'])
    else:
        await update.message.reply_text("The game already has two players.")

async def start_game(bot: Bot, players: list):
    game = Game(bot, *players)
    await game.play()

def main():
    # Create the application
    application = Application.builder().token(TOKEN).build()

    # Add command handler for /start
    application.add_handler(CommandHandler("start", start))

    # Run the application with polling
    application.run_polling()

if __name__ == '__main__':
    main()