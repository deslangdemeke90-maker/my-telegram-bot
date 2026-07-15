:import telebot
from telebot import types
import sqlite3

# የአንተ ቦት መለያ ቁጥር (Token)
BOT_TOKEN = "8873576144:AAGdtQLg53UcRTJKT51jhNPhj3aFe4TX--Y" 
bot = telebot.TeleBot(BOT_TOKEN)8774424248

# የመረጃ ቋት (Database) ማስተካከያ
DB_NAME = "bot_database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # የተጠቃሚዎችን ሂሳብ መረጃ የሚይዝ ሰንጠረዥ መፍጠር
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0.0
        )
    ''')
    conn.commit()
    conn.close()

# የተጠቃሚውን ቀሪ ሂሳብ ለማግኘት
def get_balance(user_id)
