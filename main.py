from typing import Final
from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes
from core.decoder import Decoder
from core.product import Product
import numpy as np
import cv2


TOKEN: Final = '8513421764:AAEVqZAMNfKS_ZJsFBztLL5fBXa0X72jiBQ'
BOT_USERNAME: Final ='@FoodTruthBot'
decoder=Decoder()

PRODUCT_METHODS={1 : Product.get_name_and_brand,
                 2 : Product.get_allergens,
                 3 : Product.get_calories,
                 4 : Product.get_is_vegan_info,
                 5 : Product.get_is_halal_or_kosher,
                 6 : Product.get_is_gluten_free,
                 7 : Product.get_nutrition_score}

#Commands
async def start_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! thanks for using me! I am a food barcode scanner!")

async def help_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am a food barcode scanner, send me a picture of your food with a clear barcode to start :)")

async def menu_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    menu_str = "reply with a number from the list below to get the info you want\n"
    menu_str+= "1 : Name and Brand\n"
    menu_str += "2 : Allergens\n"
    menu_str += "3 : Calories\n"
    menu_str += "4 : Vegan/Vegatarian Status\n"
    menu_str += "5 : Halal/Kosher Status\n"
    menu_str += "6 : Gluten Status\n"
    menu_str += "7 : Nutrition Score\n"

    await update.message.reply_text(menu_str)

    

#Responses and Utils

#TODO: put in a seperate utils file
async def get_numpy_image(update):
    image = update.message.photo[-1]
    file = await image.get_file()
    image_bytes = await file.download_as_bytearray()
    image_np = np.frombuffer(image_bytes, np.uint8)
    image_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    return image_np


def handle_response(text: str, product: Product)->str:
    response = ""

    if text.isdigit() and 0 < int(text) <= len(PRODUCT_METHODS):
        choice = int(text)
        response = PRODUCT_METHODS[choice](product)
    else:
        response = "invalid message please refer to menu command!"

    return response
        
# Handlers

async def handle_image_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image= await get_numpy_image(update)
    
    try:
        barcode=decoder.decode(image)
    except ValueError as error:
        print(error)
        await update.message.reply_text("Barcode not found in the picture, Try again!")
        return
    

    try:
        product=Product(barcode)
    except ValueError as error:
        print(error)
        await update.message.reply_text(error)
        return

    context.user_data['product']=product

    await update.message.reply_text("Barcode found,to get the menu for the product information use menu command")
    
    

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_product = context.user_data.get('product',None)
    if not user_product:
        await update.message.reply_text("please send a picture of a food product with its barcode clear!")
        return
    
    message_type = update.message.chat.type #type of message: group or private chat
    text = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME,'').strip()
            response=handle_response(new_text,user_product)
        else:
            return
    
    else:
        response = handle_response(text,user_product)
    
    print('Bot:',response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update: {update} caused error {context.error}')





if __name__=='__main__':
    print('Starting bot')
    app=Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('menu',menu_command))

    #Messages

    app.add_handler(MessageHandler(filters.PHOTO,handle_image_message))
    app.add_handler(MessageHandler(filters.TEXT,handle_message))


    #Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)



        
        


    
    
