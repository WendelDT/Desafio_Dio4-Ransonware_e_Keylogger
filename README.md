# Documentação Técnica: Simulação de Keylogger e Exfiltração via C2

## 1. Escopo do Projeto
Este projeto documenta o desenvolvimento e a implementação de um **keylogger** para fins educacionais, simulando um cenário real de ataque e exfiltração de dados em um ambiente controlado.

* **Objetivo:** Capturar inputs de teclado e exfiltrar os dados para um servidor remoto via protocolo HTTP.
* **Diferencial:** Implementação de um servidor de Comando e Controle (C2) centralizado em substituição ao envio tradicional por e-mail.

## 2. Topologia do Laboratório
O ambiente foi construído utilizando a plataforma **PNETLab**, replicando a infraestrutura da empresa fictícia "Tabajiros".

* **Gateway/Firewall:** MikroTik RouterOS.
* **Networking:** Switch L2 Cisco.
* **Endpoints Alvos:** 2x Windows 10 e 1x Windows Server 2008.
* **Infraestrutura de Ataque:** * **Kali Linux:** Utilizado para desenvolvimento e entrega do payload.
    * **Debian 12 (C2 Server):** Host do servidor de recebimento de dados.

![Topologia da Rede](images/labfoto.png)

## 3. Arquitetura do Servidor C2 (Command & Control)
O servidor C2 atua como o *listener* do ataque.
* **Tecnologias:** Desenvolvido em **Python** com o micro-framework **Flask**.
* **Deployment:** Implementado via **Docker Compose**, garantindo isolamento e facilidade de replicação.
* **Exfiltração:** O servidor processa requisições `POST` contendo os logs de teclas capturadas, simulando tráfego HTTP legítimo para evitar detecção básica por firewalls.

## 4. Desenvolvimento e Vetores de Infecção
O artefato malicioso (Keylogger) foi compilado como um executável independente (`.exe`) através do **PyInstaller**.

### Possíveis Vetores de Entrega (Simulados):
* **Engenharia Social:** Phishing via e-mail com técnicas de *File Binding* (fusão do executável com PDFs ou imagens).
* **Exploração de Vulnerabilidades:** Execução remota via **Meterpreter** após comprometimento inicial do host.

## 5. Análise de Execução e Detecção
Nesta fase, validamos o comportamento do artefato no endpoint "Vendas".

![Execução do Binário](images/keylogger1.png)

### Perspectiva de Defesa (Blue Team):
* **Processos:** Monitoramento do *Task Manager* em busca de processos suspeitos ou masquerading (nomes de processos legítimos).
* **Rede:** Identificação de persistência através de conexões ativas com o comando `netstat -a`.
* **Firewall:** Monitoramento da tabela de conexões no MikroTik para identificar comunicações anômalas na porta 80/443 destinadas a IPs externos não catalogados.

![Monitoramento de Processos](images/keylogger2.png)

## 6. Resultados e Logs de Captura
O teste foi validado através da inserção de strings aleatórias no host alvo, simulando a captura de credenciais ou comunicações sensíveis.

![Simulação de Input](images/keylogger4.png)

### Verificação de Recebimento (C2):
O servidor C2 registrou com sucesso as requisições provenientes do IP do host "Vendas", armazenando o conteúdo em formato `.txt`.

![Logs de Recebimento](images/keylogger3.png)
![Visualização do Log - Servidor](images/keylogger6.png)

## 7. Arquivos
Em /keylogger se encontram os seguintes arquivos disponiveis:
* **keyloger source**: código fonte compactado (ideal para ser baixado no Windows, visto que o antivirus por criar alertas e excluir o código).
* **keylogger**: código fonte. 
* **keylogger_32**: arquivo .exe. compilado para rodar em windows 32bits.

## 8. Conclusão e Mitigação
Compreendido o funcionamento do keylogger, um malware que captura as informações digitadas no teclado e as envia para um servidor ou email remoto, e como isso pode ser danoso para uma empresa, principalmente se capturar logins e senhas sensiveis.

A maioria dos malwares exploram a engenharia social, e as falhas humanas. Para que uma empresa tenha boa segurança não basta apenas o time de T.I ter um bom treinamento, é necessário treinamentos constantes também com outros setores da empresa, desde a secretária que possa abrir um email até o diretor, ambos podem expor a empresa a vulnerabilidades.

**Recomendações de Segurança:**
1.  **Hardening de Endpoint:** Restrição de execução de binários não assinados.
2.  **Segurança de Rede:** Implementação de inspeção SSL/TLS para identificar tráfego C2 mascarado como HTTP.
3.  **Treinamento Anti-Phishing:** Fortalecimento da cultura de segurança para mitigar vetores de engenharia social.
