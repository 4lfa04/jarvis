import json, time
import telebot
import init

buttons = []
close_message_id = ''
TOKEN = '6954388294:AAE25G81cYl1FuYr8U2wrDB4r_yOeskLaN4'

bot = telebot.TeleBot(TOKEN)

def saveSleep(data):
    data = data.split(" ",1)
    original = ""
    with open("db/psicoDb.json") as file:
        original = json.load(file)
    with open("db/psicoDb.json", "w") as file:
        original["lista"].append({
            "fecha":time.strftime("%Y-%m-%d"),
            "hora":data[0],
            "info":data[1]
        })
        json.dump(original, file)

def saveNow(data):
    data = "Comiendo Pizza"
    with open("db/psicoDb.json") as file:
        original = json.load(file)
    with open("db/psicoDb.json", "w") as file:
        original["lista"].append({
            "fecha":time.strftime("%Y-%m-%d"),
            "hora":time.strftime("%H:%M"),
            "info":data
        })
        json.dump(original, file)

def clearSleep():
    with open("db/psicoDb.json", "w") as file:
        data = {"lista": []}
        json.dump(data, file)
    return "🗑 Historial reiniciado con <b>éxito</b>"

def getSleep():
    sueños = {}
    with open("db/psicoDb.json") as file:
        sueños = json.load(file)
    texto = "<b>📓 Historial de Episodios</b>\n"
    for sueño in sueños['lista']:
        texto+=f'{sueño["fecha"]} / {sueño["hora"]}: {sueño["info"]}\n'
    
    return texto

def getToday():
    sueños = {}
    fecha = time.strftime("%Y-%m-%d")
    with open("db/psicoDb.json") as file:
        sueños = json.load(file)
    texto = "<b>📓 Historial de Episodios de Hoy</b>\n"
    for sueño in sueños['lista']:
        print(f'Fecha: {sueño["fecha"]} : {fecha == sueño["fecha"]}')
        if sueño["fecha"] == fecha:
            texto+=f'{sueño["fecha"]} / {sueño["hora"]}: {sueño["info"]}\n'
    return texto

def handleOperation(message):
    bot.send_chat_action(message.chat.id, "typing")
    text = message.text
    data = 0
    if "addnow" in text.lower():
        mensaje = text.split(" ",1)
        saveNow(mensaje[1])
        data = "✅ Episodio guardado con <b>éxito</b>"
    elif "add" in text.lower():
        mensaje = text.split(" ", 1)
        saveSleep(mensaje[1])
        data = "✅ Episodio guardado con <b>éxito</b>"
    elif "gettoday" in text.lower():
        data = getToday()
    elif "get" in text.lower():
        data = getSleep()
    elif "clear" in text.lower():
        data = clearSleep()
    else:
        data = "❌ Lo siento, no entiendo lo que dices"
    bot.send_message(message.chat.id, data, parse_mode="html")