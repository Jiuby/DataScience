# Se importan las librerias necesarias para realizar el web scraping y guardarlo :3
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Años de la copa america
year = [1975, 1979, 1983, 1987, 1989, 1991, 1993, 1995, 1997, 1999, 2001, 2004, 2007, 2011, 2015, 2016, 2019, 2021]



# Se crea una funcion para obtener los partidos de la copa america
def get_matches():
    # se accede a la pagina de wikipedia usando la url y el año y para acceder usando requests
    web = f"https://en.wikipedia.org/wiki/{year}_Copa_Am%C3%A9rica"
    respuesta = requests.get(web)
    # se obtiene el contenido de la pagina y lo convertimos en texto
    contenido = respuesta.text

    # se crea un objeto de la clase BeautifulSoup para poder manipular el contenido de la pagina
    soup = BeautifulSoup(contenido, "lxml")

    # buscamos algun patron desde el html que tengan los partidos
    matches = soup.find_all('div', class_='footballbox')

    home = []
    away = []
    score = []
    for match in matches:
        # se obtiene el nombre del equipo local, visitante y el resultado desde el html
        home.append(match.find('th', class_='fhome').get_text())
        away.append(match.find('th', class_='faway').get_text())
        score.append(match.find('th', class_='fscore').get_text())

    # se crea un diccionario con los datos obtenidos
    dict_fotball = {'Home': home, 'Away': away, 'Score': score}

    # se convierte el diccionario en un dataframe
    df_fotball = pd.DataFrame(dict_fotball)
    # se añade la columna del año
    df_fotball['year'] = year
    return df_fotball


copaAmerica = [get_matches(years) for years in year]

# se concatenan todos los dataframes en uno solo
df_copaAmerica = pd.concat(copaAmerica, ignore_index=True)
df_copaAmerica.to_csv("america_worldcup_historical_data.csv", index=False)
