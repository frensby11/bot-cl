import requests  
import time  

# URL de la página que quieres mantener activa  
url = "https://dashboard.render.com/web/srv-crsmhobtq21c73dh0afg"  # Cambia esta URL por la de tu instancia  

# Intervalo de tiempo entre peticiones en segundos  
intervalo = 10  # Puedes ajustar este valor según sea necesario  

try:  
    while True:  
        # Realiza la petición a la página  
        response = requests.get(url)  

        # Imprime el estado de la respuesta  
        print(f"Petición realizada. Estado: {response.status_code}")  

        # Espera el tiempo definido antes de la próxima petición  
        time.sleep(intervalo)  

except KeyboardInterrupt:  
    print("Detenido por el usuario.")
