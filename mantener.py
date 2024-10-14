import requests  
import time  

# URL de la página que quieres mantener activa  
url = "https://mantener-servidores.onrender.com"  # Cambia esta URL por la de tu instancia  
url2 = "https://bot-cl.onrender.com"

# Intervalo de tiempo entre peticiones en segundos  
intervalo = 10  # Puedes ajustar este valor según sea necesario  

try:  
    while True:  
        # Realiza la petición a la página  
        response = requests.get(url)
        response2 = requests.get(url2)

        # Imprime el estado de la respuesta  
        print(f"Petición realizada. Estado: {response.status_code}")  
        print(f"Petición realizada. Estado: {response2.status_code}")  

        # Espera el tiempo definido antes de la próxima petición  
        time.sleep(intervalo)  

except KeyboardInterrupt:  
    print("Detenido por el usuario.")
