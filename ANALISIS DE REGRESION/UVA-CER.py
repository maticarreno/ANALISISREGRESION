import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import json

# Añadir Token de https://estadisticasbcra.com/api/registracion
token = "BEARER "

endpoint_cer = "cer"
endpoint_uva = "uva"

def get_data(endpoint):
    url = "https://api.estadisticasbcra.com/" + endpoint
    headers = {"Authorization": token}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  

        if response.status_code == 200:
            data_json = response.json()
            return data_json
        else:
            print(f"Error al obtener datos desde la API ({endpoint})")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud HTTP: {e}")
        return None
    
def analisis_regresion():
    data_cer = get_data(endpoint_cer)
    data_uva = get_data(endpoint_uva)
    fechas_cer = [item['d'] for item in data_cer]
    valores_cer = [item['v'] for item in data_cer]
    fechas_uva = [item['d'] for item in data_uva]
    valores_uva = [item['v'] for item in data_uva]
    df_cer = pd.DataFrame({'Fecha': fechas_cer, 'CER': valores_cer})
    df_uva = pd.DataFrame({'Fecha': fechas_uva, 'Valor_UVA': valores_uva})
    df = df_cer.merge(df_uva, on='Fecha', how='outer')
    df.fillna(0, inplace=True)
    X = df[['Valor_UVA']]
    y = df['CER']

    model = LinearRegression()
    model.fit(X, y)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Valor_UVA', y='CER', data=df)
    sns.lineplot(x='Valor_UVA', y=model.predict(X), data=df, color='red')
    plt.xlabel('Valor_UVA')
    plt.ylabel('CER')
    plt.title('Análisis de Regresión CER / UVA')
    plt.show()

if __name__ == '__main__':
    analisis_regresion()