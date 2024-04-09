import telebot, json, time
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
    with open('searchHistory.json', 'w') as file:
        json.dump(data, file)

bot = telebot.TeleBot(TOKEN)

def arranque():
    message = bot.send_message(users["id"], "Iniciando Sistemas")
    time.sleep(3)
    
    message = bot.edit_message_text("Sistemas en línea", message.chat.id)
    bot.edit_message_text("🤖", message.chat.id)
    


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
            pos = 14
            try:
                if search[1] not in history["history"]:
                    history["history"].append(search[1])
                    pos = len(history["history"])-1
                    actualizar_historial(history)
                else:
                    pos = history["history"].index(search[1])
            except Exception as e:
                print(f'Error: {e}')
            
            try:
                keyboard = telebot.types.InlineKeyboardMarkup()
                
                a = 0
                for content in text[0]['arr_content']:
                    a+=1
                    contenido = f'{pos}_ {a}'
                    button = telebot.types.InlineKeyboardButton(content,callback_data=contenido)
                    keyboard.add(button)
                bot.send_message(message.chat.id, f'Tabla de Contenido',reply_markup=keyboard)
            except Exception as e:
                try:
                    bot.send_message(message.chat.id, f'La infomacion no tiene soporte para Busqueda dinamica en estos momentos... Disculpe las molestias {text[0]["content"]}')
                except Exception as e:
                    bot.send_message(message.chat.id, f'La infomacion no tiene soporte para Busqueda dinamica en estos momentos... Disculpe las molestias')
    
    else:
        bot.send_message(message.chat.id, 'Lo siento pero no puedes usar este bot en este momento')



@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    data = call.data.split('_ ')
    history = obtener_historial()
    history = history["history"][int(data[0])]
    busqueda = wiki.search(history)
    busqueda = busqueda[int(data[1])]
    # print(f'Historial {history}')

    bot.send_message(call.from_user.id, f'''<b>{busqueda['title']}</b>
{busqueda['content']}''',parse_mode='html')

if __name__ == '__main__':
    arranque()
    try:
        bot.infinity_polling()
    except:
        bot.send_message(users['id'], """ Hubo un problema grave en la ejecución de Jarvis """)
        print("Jarvis no pudo ser iniciado")
    bot.send_message(users['id'], "Servidor Apagado, para seguir usando es necesario volver a ponerlo en línea")