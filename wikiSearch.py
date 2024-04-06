import wikipedia
import telebot

TOKEN = '6954388294:AAE25G81cYl1FuYr8U2wrDB4r_yOeskLaN4'
bot = telebot.TeleBot(TOKEN)

def search(search):

    try:
        wikipedia.set_lang("es")

        page = wikipedia.page(search)

        texto = page.content

        text = f"Titulo: {page.title}\nContenido: \n{texto}"

    except wikipedia.exceptions.DisambiguationError as e:
        return ["La busqueda es ambigua, por favor sé más espécifico"]
    except wikipedia.exceptions.PageError as e:
        return ["Tonto, la pagina no existe?"]
    except:
        return ["Parece que hay un error desconocido"]
    
    text = text.split('\n\n')
    tabla = [{
        'id' : 0,
        'title' : 'Tabla de Contenido',
        'content' : '',
        'arr_content' : []}]
    id = 1
    for content in text:
        if '==' in content:

            while '===' in content:
                content = content.replace('===', '==')
            content = content.split('==')
            content[0] = id
            id+=1
            if content[2] == "":
                continue
            tabla.append({
                'id': content[0],
                'title' : content[1],
                'content' : content[2]})
            
            tabla[0]["arr_content"].append(content[1])
            tabla[0]['content']+=f'\n-{str(content[1])}'

    return tabla


# datas = search('animal')

# for data in datas[0]["arr_content"]:
#     print(f'{type(data)}: {data}')