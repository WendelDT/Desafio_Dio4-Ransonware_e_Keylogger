from cryptography.fernet import Fernet
import os
import sys

# 1. Identificar o diretório dinamicamente (Script vs Executável)
if getattr(sys, 'frozen', False):
    DIRETORIO_ATUAL = os.path.dirname(sys.executable)
else:
    DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

def carregar_chave():
    caminho_chave = os.path.join(DIRETORIO_ATUAL, "chave.key")
    try:
        with open(caminho_chave, "rb") as chave_arquivo:
            return chave_arquivo.read()
    except FileNotFoundError:
        print("Erro: O arquivo 'chave.key' não foi encontrado no diretório atual.")
        return None

def descriptografar_arquivo(arquivo, chave):
    f = Fernet(chave)
    with open(arquivo, "rb") as file:
        dados_criptografados = file.read()
    
    try:
        dados_originais = f.decrypt(dados_criptografados)
        with open(arquivo, "wb") as file:
            file.write(dados_originais)
        return True
    except Exception as e:
        print(f"Falha ao descriptografar {arquivo}: {e}")
        return False

def encontrar_arquivos(diretorio):
    lista = []
    arquivos_ignorados = [
        "ransonware.py", "ransonware.exe", 
        "decript.py", "decript.exe", 
        "chave.key", "mensagem_resgate.txt"
    ]

    for raiz, _, arquivos in os.walk(diretorio):
        for nome in arquivos:
            caminho = os.path.join(raiz, nome)
            if nome.lower() not in arquivos_ignorados:
                lista.append(caminho)
    return lista

def main():
    chave = carregar_chave()
    if not chave:
        return

    arquivos = encontrar_arquivos(DIRETORIO_ATUAL)
    
    print(f"Iniciando recuperação de arquivos em: {DIRETORIO_ATUAL}...\n")
    
    for arquivo in arquivos:
        if descriptografar_arquivo(arquivo, chave):
            print(f"Recuperado: {arquivo}")
            
    caminho_resgate = os.path.join(DIRETORIO_ATUAL, "mensagem_resgate.txt")
    if os.path.exists(caminho_resgate):
        os.remove(caminho_resgate)
        print("\nMensagem de resgate removida.")

    print("\nProcesso de descriptografia finalizado.")

if __name__ == "__main__":
    main()