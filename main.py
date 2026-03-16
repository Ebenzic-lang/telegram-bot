import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# =============================
# CONFIGURATION
# =============================

BOT_TOKEN = "8540733828:AAF5YcwK7zca9S5aM_Q-lr_pot3j0dlB6LY"

CHANNEL_USERNAME = "@Chealseanews"

PLAY_LINK = "https://yourtrackinglink.com/play"
OFFER_LINK = "https://yourtrackinglink.com/offer"

# =============================
# LOGGING
# =============================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# =============================
# START COMMAND
# =============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("🔓 I Joined (Unlock)", callback_data="unlock")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "👋 *Welcome!*\n\n"
        "Get access to *exclusive drops + winner alerts*.\n\n"
        "*Step 1/2:* Join our channel to unlock."
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# =============================
# VERIFY MEMBERSHIP
# =============================

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    try:

        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)

        if member.status in ["member", "administrator", "creator"]:

            keyboard = [
                [InlineKeyboardButton("🎰 Play Now", url=PLAY_LINK)],
                [InlineKeyboardButton("🎁 Today's Offer", callback_data="offer")],
                [InlineKeyboardButton("💬 Support", url="https://t.me/your_support")]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                "🎉 *Unlocked!*\n\nStep *2/2*: Continue to the site.",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )

        else:

            keyboard = [
                [InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
                [InlineKeyboardButton("🔓 Try Unlock Again", callback_data="unlock")]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            text = (
                "❌ *Not subscribed yet.*\n\n"
                "Join the channel to unlock."
            )

            await query.edit_message_text(
                text,
                parse_mode="Markdown",
                reply_markup=reply_markup
            )

    except Exception as e:
        logger.error(e)
        await query.message.reply_text("⚠️ Error checking subscription.")

# =============================
# OFFER BUTTON
# =============================

async def offer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🎰 Play Now", url=PLAY_LINK)]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "🎁 *Today's Special Offer*\n\n"
        "Limited-time opportunity available today."
    )

    await query.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# =============================
# MAIN
# =============================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_membership, pattern="unlock"))
    app.add_handler(CallbackQueryHandler(offer, pattern="offer"))

    print("Bot is running...")

    app.run_polling()

if __name__ == "__main__":
    main()
