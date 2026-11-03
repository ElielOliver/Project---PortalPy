from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv

def obter_dados_portal():
    load_dotenv()
    usuario = os.getenv("UVV_USUARIO")
    senha = os.getenv("UVV_SENHA")

    # Configuração para rodar invisível
    opcoes = Options()
    opcoes.add_argument("--headless=new")
    opcoes.add_argument("--window-size=1920,1080")
    
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico, options=opcoes)
    
    dados_extraidos = {
        "notificacoes": [],
        "atividades": [],
        "boletim": []
    }

    try:
        navegador.get("https://aluno.uvv.br/")
        time.sleep(2)

        # Login
        navegador.find_element(By.ID, "Matricula").send_keys(usuario)
        navegador.find_element(By.ID, "Password").send_keys(senha)
        navegador.find_element(By.CLASS_NAME, "portal-login-submit").click()
        time.sleep(10) 

        # 1. Extrai Notificações
        notificacoes = navegador.find_elements(By.CSS_SELECTOR, ".box-mensagem ul li a")
        for noti in notificacoes:
            try:
                elemento_data = noti.find_element(By.CSS_SELECTOR, "span.pull-right")
                texto_data = elemento_data.text
                data_formatada = texto_data.replace("\n", " ").strip()
                titulo = noti.text.replace(texto_data, "").strip()
                if titulo: 
                    dados_extraidos["notificacoes"].append({"titulo": titulo, "data": data_formatada})
            except:
                if noti.text.strip():
                    dados_extraidos["notificacoes"].append({"titulo": noti.text.strip(), "data": ""})

        # 2. Extrai Atividades Pendentes
        try:
            navegador.find_element(By.XPATH, "//*[contains(text(), 'Calendário de Atividades')]").click()
            time.sleep(5) 
            
            eventos = navegador.find_elements(By.CSS_SELECTOR, ".fc-content")
            
            for evento in eventos:
                texto_evento = evento.text.strip().replace("\n", " | ")
                if not texto_evento:
                    continue
                    
                evento.click()
                time.sleep(1.5) 
                
                texto_pagina = navegador.find_element(By.TAG_NAME, "body").text
                
                if "Data de entrega da atividade:" not in texto_pagina:
                    dados_extraidos["atividades"].append(texto_evento)
                    
                botao_fechar = navegador.find_element(By.XPATH, "//button[contains(text(), 'Fechar')]")
                botao_fechar.click()
                time.sleep(1)
                
        except Exception as e:
            print(f"Erro ao extrair as atividades: {e}")

        # 3. Extrai Boletim
        try:
            navegador.find_element(By.XPATH, "//*[contains(text(), 'Boletins')]").click()
            time.sleep(5) 
            
            linhas_tabela = navegador.find_elements(By.TAG_NAME, "tr")
            for linha in linhas_tabela:
                colunas = linha.find_elements(By.TAG_NAME, "td")
                
                if len(colunas) == 12:
                    disciplina = colunas[2].text.strip()
                    av1 = colunas[3].text.strip()
                    tf1 = colunas[4].text.strip()
                    resultado = colunas[11].text.strip()
                    
                    if av1 == "-": av1 = "N/A"
                    if tf1 == "-": tf1 = "0"
                    
                    dados_extraidos["boletim"].append({
                        "disciplina": disciplina,
                        "av1": av1,
                        "tf1": tf1,
                        "status": resultado
                    })
        except Exception as e:
            print(f"Erro ao extrair o boletim: {e}")
        
    except Exception as e:
        print(f"Erro ao tentar encontrar os elementos: {e}")
        
    finally:
        navegador.quit() 
        return dados_extraidos

# Bloco para testar apenas o scraper diretamente (opcional)
if __name__ == "__main__":
    print(obter_dados_portal())