import os
import shutil
import csv

import utils

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

#SETUP

URL = 'https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-jurdica---cnpj'
BASE_DIR = f'{os.getcwd()}'
DOWNLOAD_PATH = f'{BASE_DIR}\estabelecimentos'
DATA_PATH =  f'{BASE_DIR}\dados'
DATA_MODEL = [
    'CNPJ_BASICO',
    'CNPJ_ORDEM',
    'CNPJ_DV',
    'IDENTIFICADOR',
    'NOME_FANTASIA',
    'SITUAÇÃO_CADASTRAL',
    'DATA_SITUACAO',
    'MOTIVO_SITUACAO',
    'NOME_CIDADE',
    'PAIS',
    'DATA_INÍCIO',
    'CNAE_PRINCIPAL',
    'CNAE_SECUNDARIO',
    'TIPO_LOGRADOURO',
    'LOGRADOURO',
    'NUMERO',
    'COMPLEMENTO',
    'BAIRRO',
    'CEP',
    'UF',
    'MUNICIPIO',
    'DDD1',
    'TELEFONE1',
    'DDD2',
    'TELEFONE2',
    'DDD_FAX',
    'FAX',
    'EMAIL',
    'SITUACAO_ESPECIAL',
    'DT_SITUACAO_ESPECIAL'
]

options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("prefs", {
  "download.default_directory": DOWNLOAD_PATH
  })
try:
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
except Exception as e:
    print('Falha ao localizar o google Chrome, por favor instale o navegador e tente novamente')

#mongo collection
collection = utils.collection

def create_dict(array):
    return dict(zip(DATA_MODEL, array))


def get_estabelecimentos(): # Download all 'ESTABELECIMENTOS' Files from https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-jurdica---cnpj
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-light btn-block m-1 dataset-btn botao-collapse-Recursos collapsed']"))).click()
        resources = driver.find_element(By.XPATH, "//div[@id='collapse-recursos']")
        resources_list = resources.find_elements(By.XPATH, './/div[@class="row flex mb-5"]')
        for i in resources_list:
            if 'Estabelecimento' in i.text:
                i.find_element(By.XPATH, './/button[@id="btnDownloadUrl"]').click()

        while True:
            if any('.crdownload' in n for n in os.listdir(DOWNLOAD_PATH)):
                continue
            else:
                break
        print('Download finalizado, iniciando descompactação dos arquivos')
        unzip_files()

    except Exception as e:
        print(utils.error_catch(e))

def unzip_files():
    try:
        for file in os.listdir(DOWNLOAD_PATH):
            file_path = f'{DOWNLOAD_PATH}\{file}'
            try:
                shutil.unpack_archive(file_path, DATA_PATH)
            except Exception as e:
                print(utils.error_catch(e))
    except Exception as e:
        print(utils.error_catch(e))
    else:
        print('Extraindo dados')
        extract_data()

def commit_datas(data):
    for d in data:
        if not collection.find_one({"CNPJ_BASICO": d["CNPJ_BASICO"]}): # Check if data exist on db | remove this if statement if you want to always update all entries
            x = collection.insert_one(d)

def extract_data():
    data_list = []
    print('extraindo dados. Isso pode demorar um pouco. (Você pode cancelar a qualquer momento caso não queira esperar o upload de todos os arquivos)')
    for file in os.listdir(DATA_PATH):
        with open(f'{DATA_PATH}\{file}') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for data in csv_reader:
                data_list.append(create_dict(data))
                if len(data_list) > 200: # Avoid memory overload. Disable or change the value if you pc can handle heavy process
                    commit_datas(data_list)
                    data_list = []
    print('Dados extraidos com sucesso, você pode verificar acessando diretamente no seu banco de dados ou executando o script export.py')



if __name__ == '__main__':
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)
    elif not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

    get_estabelecimentos()

