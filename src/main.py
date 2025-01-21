import os
import csv
from datetime import datetime
import time
import requests

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():

    # Configuração do ChromeWebDriver
    options = webdriver.ChromeOptions()
    
    # Adicione o modo headless
    options.add_argument("--headless")

    # Instala e configura o ChromeDriver
    servico = Service(ChromeDriverManager().install())

    # Passe as opções ao criar o driver
    driver = webdriver.Chrome(service=servico, options=options)
    driver.maximize_window()

    try:
        # URL inicial
        url = "https://rpachallengeocr.azurewebsites.net/"
        driver.get(url)

        wait = WebDriverWait(driver, 15)

        # Garante que a tabela com ID "tableSandbox" está carregada
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#tableSandbox")))

        # Caminho da pasta de saida (Pega onde o Script Python iniciou)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "faturas")
        os.makedirs(output_dir, exist_ok=True)

        # Estrutura do arquivo .CSV
        csv_data = [["Numero da Fatura", "Data da Fatura", "URL da Fatura"]]

        # Função auxiliar para extrair os dados da tabela na página atual
        def extrair_dados_pagina():

            # Localiza a Tabela pelo CSS_SELETOR
            tbody = driver.find_element(By.CSS_SELECTOR, "table#tableSandbox tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            dados = []

            # Pecorre linha por linha
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) < 4:
                    continue
                
                # Mapeamento das colunas:
                numero_fatura   = cols[1].text.strip()  # ID
                data_fatura     = cols[2].text.strip()  # Due Date
                
                # Captura link do quarto <td>
                link_element = cols[3].find_element(By.TAG_NAME, "a")
                url_arquivo  = link_element.get_attribute("href")

                dados.append((numero_fatura, data_fatura, url_arquivo))
            return dados

        # Loop para percorrer todas as páginas até que o botão Next esteja desativado
        while True:
            # Extrai os dados da tabela
            pagina_dados = extrair_dados_pagina()

            # Processa cada linha
            for (numero_fatura, data_fatura, url_fatura) in pagina_dados:
                # Converter o data_vencimento no formato dd-mm-yyyy
                try:
                    data_vencimento_dt = datetime.strptime(data_fatura, "%d-%m-%Y")
                except ValueError:
                    # Se o data_vencimento mudar o formato para dd/mm/yyyy
                    data_vencimento_dt = datetime.strptime(data_fatura, "%d/%m/%Y")

                hoje = datetime.now()

                # Filtra para baixar o arquivo com o vencimento = hoje ou vencimento <= passado
                if data_vencimento_dt <= hoje:
                    extensao = os.path.splitext(url_fatura)[1] or ".pdf"

                    # Monta caminho do arquivo
                    nome_arquivo = f"{numero_fatura}{extensao}"
                    caminho_arquivo = os.path.join(output_dir, nome_arquivo)

                    # Faz o download da fatura
                    resp = requests.get(url_fatura)
                    with open(caminho_arquivo, "wb") as f:
                        f.write(resp.content)

                    # Adiciona a linha ao arquivo .CSV
                    csv_data.append([numero_fatura, data_fatura, url_fatura])

            # Tenta clicar em "Next" se não estiver desabilitado
            try:
                next_button = driver.find_element(By.ID, "tableSandbox_next")
                if "disabled" in next_button.get_attribute("class"):
                    # Se tiver disabled não há mais próxima página
                    break
                else:
                    # Clica para ir para a próxima página
                    next_button.click()

                    # Aguarda a tabela atualizar
                    time.sleep(2)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#tableSandbox tbody tr")))
            except:
                # Se der erro, para o processo e continua
                break

        # Gera o arquivo .CSV dentro da pasta "faturas"
        csv_file = os.path.join(output_dir, "faturas.csv")
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(csv_data)

        print(f"Processo concluído!")
        print(f"- Pasta de destino: {output_dir}")
        print(f"- CSV gerado em: {csv_file}")

    finally:
        # Fecha o navegador
        driver.quit()

if __name__ == "__main__":
    main()
