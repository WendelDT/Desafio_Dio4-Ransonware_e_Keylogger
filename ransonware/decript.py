from cryptography.fernet import Fernet
import os

# 1. Carregar a chave que foi salva pelo ransomware
def carregar_chave():
    try:
        with open("chave.key", "rb") as chave_arquivo:
            return chave_arquivo.read()
    except FileNotFoundError:
        print("Erro: O arquivo 'chave.key' não foi encontrado. Não é possível descriptografar.")
        return None

# 2. Descriptografar um único arquivo
def descriptografar_arquivo(arquivo, chave):
    f = Fernet(chave)
    with open(arquivo, "rb") as file:
        dados_criptografados = file.read()
    
    try:
        # Reverte a criptografia
        dados_originais = f.decrypt(dados_criptografados)
        
        with open(arquivo, "wb") as file:
            file.write(dados_originais)
        return True
    except Exception as e:
        print(f"Falha ao descriptografar {arquivo}: {e}")
        return False

# 3. Encontrar arquivos na pasta alvo
def encontrar_arquivos(diretorio):
    lista = []
    for raiz, _, arquivos in os.walk(diretorio):
        for nome in arquivos:
            caminho = os.path.join(raiz, nome)
            # Ignora os scripts e a chave
            if nome not in ["ransonware.py", "decrypt.py", "chave.key", "mensagem_resgate.txt"]:
                lista.append(caminho)
    return lista

# 4. Função Principal
def main():
    diretorio_alvo = "TestFiles"
    
    chave = carregar_chave()
    if not chave:
        return

    arquivos = encontrar_arquivos(diretorio_alvo)
    
    print(f"Iniciando recuperação de arquivos em: {diretorio_alvo}...\n")
    
    for arquivo in arquivos:
        if descriptografar_arquivo(arquivo, chave):
            print(f"Recuperado: {arquivo}")
    
    # 5. Limpeza (Opcional)
    # Remove a mensagem de resgate após a recuperação
    caminho_resgate = os.path.join(diretorio_alvo, "mensagem_resgate.txt")
    if os.path.exists(caminho_resgate):
        os.remove(caminho_resgate)
        print("\nMensagem de resgate removida.")

    print("\nProcesso de descriptografia finalizado.")

if __name__ == "__main__":
    main()