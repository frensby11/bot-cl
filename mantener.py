import requests  
import time  

# URL de la página que quieres mantener activa  
url = "https://dashboard.render.com/web/srv-crsmhobtq21c73dh0afg"  # Cambia esta URL por la de tu instancia  
url2 = "https://dashboard.render.com/web/srv-cs5d42t6l47c73f3lnf0/deploys/dep-cs5d5kl6l47c73f3m5bg"

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
