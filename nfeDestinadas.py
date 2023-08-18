from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import json
import time
import re


service = Service(ChromeDriverManager(version="latest").install())


def crawlerAgendarDestinadas(
    userNfeReceitaPr: str,
    passwordNfeReceitaPr: str,
    documentNumber: str,
    documentNumberOffice: str,
    initialDate: str,
    endDate: str,
    escritorioId: str,
    empresaId: str,
    razaoSocial: str
) -> dict:

    initialHour = '000000'
    endHour = '235959'
    cnpjFormatado = re.sub(r'^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$', r'\1.\2.\3/\4-\5', documentNumber)
    initialDateFormatted = re.sub(r'(\d{2})(\d{2})(\d{4})', r'\1/\2/\3', initialDate)
    endDateFormatted = re.sub(r'(\d{2})(\d{2})(\d{4})', r'\1/\2/\3', endDate)
    url = 'https://www.dfeportal.fazenda.pr.gov.br/dfe-portal/manterDownloadDFe.do?action=iniciar'

    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    page = webdriver.Chrome(service=service, options=chrome_options)    
    page.maximize_window()
    page.get(url)

    page.find_element(By.ID, 'cpfusuario').send_keys(userNfeReceitaPr)
    page.find_element(By.CSS_SELECTOR,
        'body > div.content > form.login-form.text-center > div:nth-child(3) > div > input').send_keys(
            passwordNfeReceitaPr)
    page.find_element(By.CSS_SELECTOR,
        'body > div.content > form.login-form.text-center > div.form-actions > button').click()

    time.sleep(3)    

    documentNumber_input = page.find_element(By.CSS_SELECTOR, '#ext-gen1081')
    time.sleep(1) 
    documentNumber_input.send_keys(cnpjFormatado)

    elemento = None
    
    page.find_element(By.CSS_SELECTOR, '#ext-gen1116').click()
    
    actions = ActionChains(page)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.perform()    
   
    page.find_element(By.CSS_SELECTOR, "#ext-gen1030").send_keys(initialDateFormatted)
    page.find_element(By.CSS_SELECTOR, "#ext-gen1030").send_keys(Keys.TAB)
    page.find_element(By.CSS_SELECTOR, "#ext-gen1022").send_keys(initialHour)
    page.find_element(By.CSS_SELECTOR, "#ext-gen1022").send_keys(Keys.TAB)
    page.find_element(By.CSS_SELECTOR, "#ext-gen1032").send_keys(endDateFormatted)
    page.find_element(By.CSS_SELECTOR, "#ext-gen1032").send_keys(Keys.TAB)
    page.find_element(By.CSS_SELECTOR, "#ext-gen1023").send_keys(endHour)
    time.sleep(1)

    page.find_element(By.CSS_SELECTOR, "#ucs20_BtnAgendar").click()
    time.sleep(2)
    
    try:
        elemento = page.find_element(By.ID, "component-1003")
        mensagem = elemento.text.strip()

        if "Este pedido de download DF-e já foi solicitado.<br>" in mensagem:
            print("Este pedido de download DF-e já foi solicitado.")
            page.quit()
            return {"Mensagem": "Este pedido de download DF-e já foi solicitado."}

        if "Agendamento não autorizado para este CNPJ." in mensagem:
            print("Agendamento não autorizado para este CNPJ.")
            
            splitDate = initialDate.split('/')
            formattedDate = splitDate[1] + '/' + splitDate[2]
            data_hora_atual = datetime.now()
            # Formatar a data e hora no formato desejado
            formato = "%d/%m/%Y %H:%M:%S"
            atualDate = data_hora_atual.strftime(formato)
            filterDate = f"{initialDateFormatted} 00:00:00 a {endDateFormatted} 23:59:59"

            print(atualDate)  # Saída no formato "01/08/2023 00:27:56"

            resultado_encontrado = {
                "filterDate": filterDate,
                "countInvoices": 'Não tem',
                "documentNumber": documentNumber,
                "docType": "Destinadas",
                "description": "Cnpj Não Autorizado",
                "escritorioId": escritorioId,
                "empresaId": empresaId,
                "requestNumber": "Não tem",
                "documentNumberOffice": documentNumberOffice,
                "processDate": "Não tem",
                "requestDate": atualDate,
                "referenceDate": formattedDate,
                "razaoSocial": razaoSocial,
                "urlFile": 'Não tem',
                "msg": "Agendamento não autorizado para este CNPJ.",
            }

            print("Resultado encontrado:")
            print(json.dumps(resultado_encontrado, indent=2, ensure_ascii=False).encode('utf-8').decode('utf-8'))
            page.quit()
            return resultado_encontrado 
       
        if "Não foram encontrados registros para os parâmetros informados." in mensagem:
            print("Não foram encontrados registros para os parâmetros informados")
            page.quit()
            return {"Mensagem": "Não foram encontrados registros para os parâmetros informados"}

    except:
        pass

    confere = f"{initialDate} 00:00:00 a {endDate} 23:59:59"

    tabela_selector = "table.x-grid-table.x-grid-table-resizer"
    linhas_selector = f"{tabela_selector} tbody tr:not(:first-child)"
    linhas = page.find_elements(By.CSS_SELECTOR, linhas_selector)

    resultados = []

    for linha in linhas:
        celulas_selector = "td"
        celulas = linha.find_elements(By.CSS_SELECTOR, celulas_selector)

        objeto_linha = {}

        time.sleep(1)

        for i, celula in enumerate(celulas, start=1):
            texto_celula = celula.text.strip()
            objeto_linha[f"coluna{i}"] = texto_celula

        resultados.append(objeto_linha)

        if objeto_linha["coluna3"] == confere and objeto_linha["coluna4"] == "Destinadas":

            status = objeto_linha["coluna10"].split('.')[0].strip()
            splitDate = initialDate.split('/')
            formattedDate = splitDate[1] + '/' + splitDate[2]

            resultado_encontrado = {
                "filterDate": objeto_linha["coluna3"],
                "countInvoices": 'Não tem',
                "documentNumber": documentNumber,
                "docType": objeto_linha["coluna4"],
                "description": status,
                "escritorioId": escritorioId,
                "empresaId": empresaId,
                "requestNumber": objeto_linha["coluna1"],
                "documentNumberOffice": documentNumberOffice,
                "processDate": objeto_linha["coluna9"],
                "requestDate": objeto_linha["coluna8"],
                "referenceDate": formattedDate,
                "razaoSocial": razaoSocial,
                "urlFile": 'Não tem',
                "msg": f"Agendamento Destinadas Cnpj: {documentNumber}, Realizado Com Sucesso",
            }

            print("Resultado encontrado:")
            print(json.dumps(resultado_encontrado, indent=2, ensure_ascii=False).encode('utf-8').decode('utf-8'))
            page.quit()
            return resultado_encontrado

    page.quit()
