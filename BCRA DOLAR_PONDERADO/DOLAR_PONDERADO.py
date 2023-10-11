import requests
import pandas as pd
import matplotlib.pyplot as plt

#Token de https://estadisticasbcra.com/api/registracion
token = "BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjg1MDk0OTQsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJjYXJyZW5vZ3VpbGxlcm1vQGhvdG1haWwuY29tIn0.jngLsi4DcQZCZxC-0qhjdfY5yBBaDd79wmqlWHYc32fqXXlGWSj9IMaXrH7KDzO4jSNPRlYZ5aYf10Xkc7iqEw"

def get_data(endpoint):
    url = "https://api.estadisticasbcra.com/" + endpoint
    headers = {"Authorization": token}
    data_json = requests.get(url, headers=headers).json()
    data = pd.DataFrame(data_json)
    data.set_index("d", inplace=True, drop=True)
    x = str(data.tail(1)).split(" ")
    return x[-1]
 
def dolar_ponderado(base_monetaria, leliq, lebac, reserva_internacional):
    return (int(base_monetaria) + int(leliq) + int(lebac)) / int(reserva_internacional)
  
base_monetaria = get_data("base")
leliq = get_data("leliq")
lebac = get_data("lebac")
reserva_internacional = get_data("reservas")
 
print((dolar_ponderado(base_monetaria, leliq, lebac, reserva_internacional)))
