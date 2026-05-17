import requests
import time 
import yfinance as yf 
import os

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

#------------------------------------------------------------------------------  API  -----------------------------------------------------------------------


def obtener_precio(simbolo):
    try:
        ticker = yf.Ticker(simbolo)
        data = ticker.history(period="1d", interval="1m")

        if not data.empty:
            precio = data["Close"].iloc[-1]
            return float(precio)

        return None

    except Exception as e:
        print("Error obteniendo precio:", e)
        return None


#----------------------------------------------------------------------  GUARDA PERCIO  ---------------------------------------------------------------------

def guardar_datos(precio, accion):
    with open('precios.txt', 'a', encoding='UTF-8') as Pre:
        Pre.write(f'{accion}, {precio}\n')
        
        

#--------------------------------------------------------------------------  ENVIAR NOTIFICACION  -----------------------------------------------------------------
def enviar_alerta(mensaje):
    requests.post(WEBHOOK_URL, json={
        "content": mensaje
    })


#---------------------------------------------------------------------------  BOT  -----------------------------------------------------------------------------

acciones = ['META', 'SNDK', 'NVDA', 'MU']

rangos = {
    "META": {"bajo": 600, "alto": 620},
    "SNDK": {"bajo": 1350, "alto": 1450},
    "NVDA": {"bajo": 190, "alto": 240},
    "MU":   {"bajo": 690, "alto": 770}
}


estado = {accion: None for accion in acciones}

while True:
    for accion in acciones:
        precio = obtener_precio(accion)

        if precio is not None:
            guardar_datos(accion, precio)
            print(f"{accion}: {precio}")


            bajo = rangos[accion]["bajo"]
            alto = rangos[accion]["alto"]

            if precio <= bajo:
                nuevo_estado = 'bajo'

            elif precio >= alto:
                nuevo_estado = 'alto'

            else:
                nuevo_estado = 'neutral'
                
                
            

            # detectar cambio por acción
            if nuevo_estado != estado[accion]:
                mensaje = f"🚨 {accion} → {nuevo_estado} | Precio: {precio}"
                print(mensaje)
                enviar_alerta(mensaje)

                estado[accion] = nuevo_estado

        else:
            print(f"No se pudo obtener precio de {accion}")

    time.sleep(5)
    
    
