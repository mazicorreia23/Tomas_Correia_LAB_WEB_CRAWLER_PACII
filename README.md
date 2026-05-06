Este é um script simples para navegação automática em páginas web (crawling). O objetivo é explorar um endereço inicial, extrair títulos e links de cada página encontrada e guardar os dados de forma organizada.

## Funcionalidades

* Navegação recursiva a partir de um URL inicial.
* Extração de títulos de páginas e mapeamento de links.
* Respeito pelas regras do ficheiro `robots.txt` de cada site.
* Controlo de fluxo com intervalos aleatórios entre pedidos para evitar sobrecarga nos servidores.
* Exportação automática dos resultados para ficheiros JSON.
* Suporte para interrupção manual (Ctrl+C) sem perda de dados.

## Requisitos

Para correr este script, é necessário ter o Python instalado e as seguintes bibliotecas:

* `requests`: Para realizar os pedidos HTTP.
* `beautifulsoup4`: Para processar o HTML das páginas.
* 

## Estrutura dos ficheiros de saída

Após a execução, serão gerados três ficheiros na pasta de destino:

* **sucesso.json** : Contém o URL, o título e a lista de links encontrados em cada página visitada com sucesso.
* **erros.json** : Registo de páginas que não puderam ser acedidas, incluindo o código de erro ou falha de rede.
* **mapa_relacoes.json** : Um mapa simplificado que liga cada URL visitada a todos os links que ela contém.
