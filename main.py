
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("API_KEY")
TWELVE_DATA_URL = "https://api.twelvedata.com/price"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /lot [тикер] [депозит] [риск %] [стоп-лосс в пунктах]")

def get_price(symbol):
    params = {"symbol": symbol, "apikey": API_KEY}
    response = requests.get(TWELVE_DATA_URL, params=params)
    data = response.json()
    return float(data["price"])

def calculate_lot(price, deposit, risk_percent, stop_loss_points, contract_size=1, point_value=0.01):
    risk_amount = deposit * (risk_percent / 100)
    lot_size = risk_amount / (stop_loss_points * point_value)
    return round(lot_size, 2)

async def lot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper()
        deposit = float(context.args[1])
        risk = float(context.args[2])
        stop_loss = float(context.args[3])

        price = get_price(symbol)
        lot = calculate_lot(price, deposit, risk, stop_loss)
        await update.message.reply_text(f"Цена {symbol}: {price}\nРассчитанный лот: {lot} лота")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lot", lot))
    app.run_polling()

if __name__ == "__main__":
    main()
