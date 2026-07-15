import telebot
from telebot import types
import sqlite3

# የአንተ ቦት መለያ ቁጥር (Token)
BOT_TOKEN = "8873576144:AAGdTQLg53UcRTJKT51jh8774424248"
bot = telebot.TeleBot(BOT_TOKEN)

# የመረጃ ቋት (Database) ማስተካከል
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

# ቦቱ ሲነሳ የመረጃ ቋቱን ያዘጋጃል
init_db()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # ተጠቃሚው ቀድሞ በመረጃ ቋቱ ውስጥ ካለ ማረጋገጥ፣ ከሌለ መመዝገብ
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    
    if user is None:
        cursor.execute("INSERT INTO users (user_id, balance) VALUES (?, ?)", (user_id, 0.0))
        conn.commit()
        balance = 0.0
    else:
        balance = user[0]
        
    conn.close()
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_balance = types.KeyboardButton("💰 የእኔ ሂሳብ (Balance)")
    btn_earn = types.KeyboardButton("💸 ማግኘት (Earn)")
    markup.add(btn_balance, btn_earn)
    
    bot.reply_to(message, "እንኳን ወደ ቦቱ በደህና መጡ! ከታች ያሉትን አማራጮች በመጠቀም መስራት ይችላሉ።", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    
    if message.text == "💰 የእኔ ሂሳብ (Balance)":
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        balance = user[0] if user else 0.0
        bot.reply_to(message, f"የአሁኑ ሂሳብዎ: {balance} ብር ነው ጠቅላላ")
        
    elif message.text == "💸 ማግኘት (Earn)":
        # እዚህ ጋር ተጠቃሚው የሚሰራበትን ተግባር ማከል ትችላለህ
        bot.reply_to(message, "ማስታወቂያዎችን በማየት ወይም ጓደኞችን በመጋበዝ ገንዘብ ማግኘት ይችላሉ!")

# ቦቱን ማስነሳት
if __name__ == "__main__":
    print("ቦቱ እየሰራ ነው...")
    bot.infinity_polling()
