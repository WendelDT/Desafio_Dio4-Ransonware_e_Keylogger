# Documentação Técnica: Simulação de Keylogger e Exfiltração via C2

## 1. Escopo do Projeto
Este projeto documenta o desenvolvimento e a implementação de um **keylogger** para fins educacionais, simulando um cenário real de ataque e exfiltração de dados em um ambiente controlado.
O Desafio consiste em criar um keylogger e fazer uma simulação da captura dos dados em um arquivo .txt. Como o desafio é flexivel resolvi mudar alguns parâmetros para que o ataque se parecesse com um ataque real de um caso do qual eu já trabalhei.

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
Ao invés de envia-las para uma conta de email, O keylogger as envia para um **servidor C2 (command-and-control)**, que para a simulação está localizado no proprio laborátorio, mas poderia muito bem ser uma **EC2** ou qualquer outra **VPS** escondida atrá de um IP da Cloudflare ou uma VPN.
O aplicativo que recebe os dados é um app de código em **Python**, utiliziando o **Flask** para hospeda-lo, ambos sobem no servidor com uma container, do qual eu utilizei **Docker Compose** para monta-lo.

O servidor C2 atua como o *listener* do ataque.
* **Tecnologias:** Desenvolvido em **Python** com o micro-framework **Flask**.
* **Deployment:** Implementado via **Docker Compose**, garantindo isolamento e facilidade de replicação.
* **Exfiltração:** O servidor processa requisições `POST` contendo os logs de teclas capturadas, simulando tráfego HTTP legítimo para evitar detecção básica por firewalls.

## 4. Desenvolvimento e Vetores de Infecção
O Keylogger foi enviado para o computador no formato de um executável, montado com a biblioteca **pyinstaller**, e enviado a maquina. Poderiamos utilziar técnicas como **engenharia social** utilziando, fundir esse excutavel a outro arquivo como um .PDF ou .PNG e envia-lo por email utilizando a ténica de **warp** ou **binder**, ou mesmo executa-lo através de uma invasão com o **meterpreter**.

### Possíveis Vetores de Entrega (Simulados):
* **Engenharia Social:** Phishing via e-mail com técnicas de *File Binding* (fusão do executável com PDFs ou imagens).
* **Exploração de Vulnerabilidades:** Execução remota via **Meterpreter** após comprometimento inicial do host.

## 5. Análise de Execução e Detecção
Nesta fase, validamos o comportamento do artefato no endpoint "Vendas".

Depois de executado podemos ver ele rodando no Task Mangener, Keyloggers mais profissionais e com boa ocultabilidade escondem seu nome, ou o trocam para o nome de outro programa conhecido, assim tornando mais complexo seu diagnostico. Uma maneira de diagsnoticar um Keylooger verificando as conexões abertas do dispositivo, isso pode ser feito com o comando `netstat -a`, ou nessa rede, olhando a tabel *firewall > connectinos* no Mikrotic, abertura de portas de SMTP, ou conexões suspeitas denunciam o keyloger, como esse está enviando as informações utilizando um POST via HTTP, pode ser confundido com navegador comum.

![Execução do Binário](images/keylogger1.png)

### Perspectiva de Defesa (Blue Team):
* **Processos:** Monitoramento do *Task Manager* em busca de processos suspeitos ou masquerading (nomes de processos legítimos).
* **Rede:** Identificação de persistência através de conexões ativas com o comando `netstat -a`.
* **Firewall:** Monitoramento da tabela de conexões no MikroTik para identificar comunicações anômalas na porta 80/443 destinadas a IPs externos não catalogados.

![Monitoramento de Processos](images/keylogger2.png)

## 6. Simulando entradas do usuário
Feito um teste digitando aleatóriamente no bloco de notas, simulando a digitação do usuário.

![Simulação de Input](images/keylogger4.png)

### Verificação de Recebimento (C2):
O servidor C2 registrou com sucesso as requisições provenientes do IP do host "Vendas", armazenando o conteúdo em formato `.txt`.

![Logs de Recebimento](images/keylogger3.png)
![Recebimento do Log - Servidor](images/keylogger5.png)

## 7. Resultados e Logs de Captura
Podemos abrir os logs de captuira direto no C2 ou baixa-los abri-los utilizando o notepad.

![Visualização do Log - Servidor](images/keylogger6.png)
![Visualização do Log - Servidor](images/keylogger7.png)

## 8. Arquivos
Em /keylogger se encontram os seguintes arquivos disponiveis:
* **keyloger source**: código fonte compactado (ideal para ser baixado no Windows, visto que o antivirus por criar alertas e excluir o código).
* **keylogger**: código fonte. 
* **keylogger_32**: arquivo .exe. compilado para rodar em windows 32bits.

## 9. Conclusão e Mitigação
Compreendido o funcionamento do keylogger, um malware que captura as informações digitadas no teclado e as envia para um servidor ou email remoto, e como isso pode ser danoso para uma empresa, principalmente se capturar logins e senhas sensiveis.

A maioria dos malwares começam explorando engenharia social e falhas humanas. Para que uma empresa tenha boa segurança não basta apenas o time de T.I ter um bom treinamento, é necessário também treinamentos constantes com outros setores da empresa, desde a secretária, que pode abrir um email com arquivo mailicioso, até o diretor, pois ambos podem expor a empresa a vulnerabilidades.

**Recomendações de Segurança:**
1.  **Hardening de Endpoint:** Restrição de execução de binários não assinados.
2.  **Segurança de Rede:** Implementação de inspeção SSL/TLS para identificar tráfego C2 mascarado como HTTP.
3.  **Treinamento Anti-Phishing:** Fortalecimento da cultura de segurança para mitigar vetores de engenharia social.
