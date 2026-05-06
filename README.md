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

**Requisitos**

- Python 3.8+
- Bibliotecas: `requests`, `beautifulsoup4`

Instalação rápida:

```bash
python -m pip install --user requests beautifulsoup4
```

**Como executar**

1. Abrir um terminal na pasta do projeto.
2. Executar:

```bash
python Crawler.py
```

Seguir as prompts para inserir a `URL de partida` e o limite de páginas (ou escolher modo ilimitado).

**O que o crawler faz**

- Respeita `robots.txt` (se não for possível ler, não procede).
- Identifica-se com o User-Agent `CrawlerBot`.
- Evita visitar a mesma página duas vezes.
- Extrai o título da página e todos os links (`<a href>`).
- Introduz um `sleep` de 1 segundo entre pedidos para não sobrecarregar o servidor.
- Guarda os resultados em JSON em: `dump_<site>/resultado.json` (por exemplo `dump_example.com/resultado.json`).
