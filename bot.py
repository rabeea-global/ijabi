# -*- coding: utf-8 -*-
# بوت إيجابي — خزّان استقبال الفيديوهات + سؤال وجواب آلي
# يحتاج مكتبة واحدة:  pip install python-telegram-bot
# ----------------------------------------------------------

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

# ===== ١) بدّل القيمتين التاليتين فقط =====
TOKEN = "ضع_توكن_البوت_هنا"              # تاخذه من BotFather
REVIEW_CHAT_ID = "ضع_id_قناة_المراجعة"   # قناتك الخاصة للمراجعة (مثال: -1001234567890)
# ==========================================

# نص الترحيب — نفس تعليمات الصفحة
WELCOME = (
    "أهلاً بيك في إيجابي 🌟\n\n"
    "الفكرة بسيطة: سجّل فيديو قصير (٥–١٥ ثانية) عمودي، "
    "وكول بصوتك: «آني إيجابي».\n"
    "بلهجتك، براحتك. مو إعلان، مو منتج — بس أنت وإيجابيتك.\n\n"
    "جاهز؟ سجّل الفيديو وارسله هنا 👇\n\n"
    "بإرسالك الفيديو، توافق على نشره علناً على صفحة إيجابي."
)

# أسئلة وأجوبة آلية (تظهر كأزرار)
FAQ = {
    "q1": "إيجابي منصّة تجمع الناس اللي يعلنون إيجابيتهم. مو إعلان، مو منتج — تعبير صادق وبس.",
    "q2": "صوّر نفسك تكول «آني إيجابي» — ٥–١٥ ثانية، عمودي، بلهجتك أو بالفصحى، براحتك.",
    "q3": "بعد المراجعة، يُنشر على صفحة إيجابي بالإنستغرام والفيسبوك.",
    "q4": "ما نطلب حساب ولا معلومات شخصية. ترسل الفيديو وبس. بالمشاركة توافق على النشر العلني.",
    "q5": "نراجع خلال ٢٤–٤٨ ساعة. إذا ناسب الطابع، يُنشر.",
}

def faq_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("شنو إيجابي؟", callback_data="q1")],
        [InlineKeyboardButton("شنو أصوّر؟", callback_data="q2")],
        [InlineKeyboardButton("وين يُنشر؟", callback_data="q3")],
        [InlineKeyboardButton("معلوماتي محفوظة؟", callback_data="q4")],
        [InlineKeyboardButton("متى يُنشر؟", callback_data="q5")],
    ])

# عند /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME, reply_markup=faq_keyboard())

# عند الضغط على زر سؤال
async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_text(FAQ.get(q.data, ""))

# عند وصول فيديو
async def got_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ١) ننسخ الفيديو إلى قناة المراجعة الخاصة بك
    try:
        await context.bot.copy_message(
            chat_id=REVIEW_CHAT_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id,
        )
    except Exception as e:
        print("review copy failed:", e)
    # ٢) نرد على المُرسِل
    await update.message.reply_text(
        "تم الاستلام ✓\n"
        "راح نراجع الفيديو، وإذا ناسب الطابع راح يُنشر على صفحة إيجابي. شكراً إلك 🌟"
    )

# أي رسالة نصية غير معروفة → نوجهه للفيديو
async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أرسل فيديو قصير تكول بيه «آني إيجابي» 🌟\n"
        "أو اضغط /start للتعليمات.",
        reply_markup=faq_keyboard()
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(faq))
    app.add_handler(MessageHandler(filters.VIDEO | filters.VIDEO_NOTE, got_video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))
    print("Ijabi bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
