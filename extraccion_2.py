# El codigo anterior no analizo todos los partidos asi que usamos otro metodo
from selenium import webdriver
from selenium.webdriver.edge.service import Service
import pandas as pd
import time

# Los años de la copa america
years = [1975, 1979, 1983, 1987, 1989, 1991, 1993, 1995, 1997, 1999, 2001, 2004, 2007, 2011, 2015, 2016, 2019, 2021]

# Cuando importamos selenium hay que descargar un driver segun el navegador que se use
path = "C:/Users/hitak/Downloads/edgedriver_win64/msedgedriver.exe"
service = Service(executable_path=path)
driver = webdriver.Edge(service=service)


def get_dates(year):
    # se accede a la web de wikipedia usando el año
    web = f"https://en.wikipedia.org/wiki/{year}_Copa_Am%C3%A9rica"
    driver.get(web)
    # se busca los partidos de la copa america usando el xpath y la clase del html
    matches = driver.find_elements(by='xpath', value='//tr[@style="font-size:90%"] | //tr[@itemprop="name"]')

    local = []
    resultado = []
    visitante = []

    for match in matches:
        # se obtiene el nombre del equipo local, visitante y el resultado desde el html
        local.append(match.find_element(by='xpath', value='./td[1] | th[1]').text)
        resultado.append(match.find_element(by='xpath', value='./td[2] | th[2]').text)
        visitante.append(match.find_element(by='xpath', value='./td[3] | th[3]').text)

    # se crea un diccionario con los datos obtenidos
    dict_fotball = {'Home': local, 'Away': visitante, 'Score': resultado}
    df_fotball = pd.DataFrame(dict_fotball)
    df_fotball['year'] = year
    time.sleep(2)
    return df_fotball

copaAmerica = [get_dates(year) for year in years]
driver.quit()
df_copaAmerica = pd.concat(copaAmerica, ignore_index=True)
df_copaAmerica.to_csv("america_worldcup_missing_data.csv", index=False)