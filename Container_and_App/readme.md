# instruções para o container

coloque todos os arquivos no mesmo diretório.
exemplo: (`\etc\c2_server`)

execute o comando:

```
docker compose up -d
```

Assim o conteiner vai ficar rodando em segundo plano e capturando os dados, com o terminal liberado para uso.
Caso queira ver os logs de recebimento você pode usar o comando:
 
```
docker compose logs -f
```