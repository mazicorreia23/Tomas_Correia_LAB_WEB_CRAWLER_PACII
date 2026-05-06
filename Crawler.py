import requests
from bs4 import BeautifulSoup
import urllib.robotparser
from urllib.parse import urlparse, urljoin
import time
import json
import os

def verificar_permissao(url_alvo, agente):
    analise = urlparse(url_alvo)
    url_robots = f"{analise.scheme}://{analise.netloc}/robots.txt"
    
    leitor_robots = urllib.robotparser.RobotFileParser()
    leitor_robots.set_url(url_robots)
    try:
        leitor_robots.read()
        return leitor_robots.can_fetch(agente, url_alvo)
    except:
        return False

def crawler(url_inicial, max_paginas):
    meu_agente = "CrawlerBot"
    cabecalhos = {"User-Agent": meu_agente}
    
    historico = set()
    pendentes = [url_inicial]
    
    dados_extraidos = []

    print("--- INFO: Usa 'Ctrl + C' para encerrar e exportar os resultados ---")

    try:
        while pendentes and len(dados_extraidos) < max_paginas:
            url_atual = pendentes.pop(0)
            
            if url_atual in historico:
                continue
                
            historico.add(url_atual)

            total_progresso = "ILIMITADO" if max_paginas == float('inf') else max_paginas
            print(f"-> [{len(dados_extraidos) + 1}/{total_progresso}] Processando: {url_atual}")
            
            if not verificar_permissao(url_atual, meu_agente):
                print(f"   [!] Bloqueado por diretiva robots.txt")
                continue

            try:
                web_res = requests.get(url_atual, headers=cabecalhos, timeout=7)
                
                if web_res.status_code != 200:
                    continue

                sopa_html = BeautifulSoup(web_res.text, 'html.parser')
                if sopa_html.title and sopa_html.title.string:
                    titulo_pag = sopa_html.title.string.strip()
                else:
                    titulo_pag = "Título Indisponível"

                links_locais = extrair_links_da_pagina(sopa_html, url_atual, historico, pendentes)

                dados_extraidos.append({
                    "url": url_atual,
                    "titulo": titulo_pag,
                    "links": links_locais
                })

            except requests.exceptions.RequestException as erro:
                print(f"   [!] Falha de rede: {erro}")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n[PARAGEM FORÇADA] A preparar exportação")

    site_nome = urlparse(url_inicial).netloc or "extraido"
    caminho_base = os.path.dirname(os.path.abspath(__file__))
    pasta_final = os.path.join(caminho_base, f"dump_{site_nome}")

    os.makedirs(pasta_final, exist_ok=True)

    caminho_json = os.path.join(pasta_final, 'resultado.json')
    with open(caminho_json, 'w', encoding='utf-8') as ficheiro:
        json.dump(dados_extraidos, ficheiro, ensure_ascii=False, indent=4)

    print(f"\n--- OPERAÇÃO FINALIZADA ---")
    print(f"O ficheiro JSON foi gerado em: {caminho_json}")


def extrair_links_da_pagina(sopa_html, url_atual, historico, pendentes):
    links_locais = []

    for tag_a in sopa_html.find_all('a', href=True):
        link_absoluto = urljoin(url_atual, tag_a['href'])

        if not link_absoluto.startswith('http'):
            continue

        if link_absoluto not in links_locais:
            links_locais.append(link_absoluto)

        if link_absoluto not in historico and link_absoluto not in pendentes:
            pendentes.append(link_absoluto)

    return links_locais

if __name__ == "__main__":
    print("=== CRAWLER ===")

    entrada_url = input("URL de partida: ").strip()
    
    print("\nConfiguração de Escopo:")
    print("[1] Definir limite de páginas")
    print("[2] Modo Varredura Total (Ilimitado)")
    
    escolha = input("Opção: ").strip()
    
    if escolha == '2':
        limite = float('inf')
        print("Modo Ilimitado Ativo.")
    else:
        try:
            limite = int(input("Número de páginas: "))
        except:
            limite = 10
            print("Entrada inválida. Limite definido para 10.")

    crawler(entrada_url, limite)