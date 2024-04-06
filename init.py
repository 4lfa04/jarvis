import telebot, json
import wikiSearch as wiki

buttons = []
close_message_id = ''
TOKEN = '6954388294:AAE25G81cYl1FuYr8U2wrDB4r_yOeskLaN4'

def obtener_usuarios():
    with open('users.json') as file:
        return json.load(file)
users = obtener_usuarios()
def obtener_historial():
    with open('searchHistory.json') as file:
        return json.load(file)
def actualizar_historial(data):
    with open('searchHistory.json') as file:
        json.dump(data, file)

bot = telebot.TeleBot(TOKEN)

#Manejando COmando Start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # bot.set_message_reaction(message.chat.id)
    print(message)

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    bot.send_chat_action(message.chat.id, 'typing')
    close_message = bot.send_message(message.chat.id, "Cerrando Servidor")
    bot.stop_polling()


@bot.message_handler(func=lambda message: True)
def procesar_texto(message):
    if users['id'] == message.chat.id:
        reqText = message.text
        history = obtener_historial()
        if 'wiki' in reqText:
            search = reqText.split("wiki")
            text = wiki.search(search)
            # print(text)
            
            if not message.text in history["history"]:
                new_history = history["history"].append(message.text)
                print(new_history)
                # actualizar_historial(message.text)
            
            
            
            try:
                keyboard = telebot.types.InlineKeyboardMarkup()
                
                history_id = history["history"].index(message.text)
                for content in text[0]['arr_content']:

                    contenido = f'_{content}'
                    button = telebot.types.InlineKeyboardButton(content,callback_data=contenido)
                    keyboard.add(button)
                bot.send_message(message.chat.id, f'Tabla de Contenido',reply_markup=keyboard)
            except Exception as e:
                bot.send_message(message.chat.id, f'La infomacion No tiene soporte para Busqueda dinamica en estos momentos... Disculpe las molestias{text[0]["content"]}')
    
    else:
        bot.send_animation(message.chat.id, 'typing')
        bot.send_message(message.chat.id, 'Lo siento pero no puedes usar este bot en este momento')



@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    print(call.data)
    print(call.from_user.id)
    bot.send_message(call.from_user.id, call.data)
        
        

if __name__ == '__main__':
    bot.send_message(users["id"], "Iniciando Sistemas")
    # bot.set_my_commands()
    bot.send_message(users["id"], "Sistemas en linea")
    try:
        bot.infinity_polling()
    except:
        bot.send_message(users['id'], """ Hubo un problema grave en la ejecución de Jarvis """)
    bot.send_message(users['id'], "Servidor Apagado, para seguir usando es necesario volver a ponerlo en línea")