import datetime
import glob
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from nasajon.util.repetir_exception import RepetirException


class ItauService:

    def __init__(self, codigo, senha):
        self.codigo = codigo
        self.senha = senha

        # Código para tentar rodar chrome dentro do docker com alpine e para testes locais
        # self.chrome_driver_path = os.getenv(
        #     'chrome_driver_path', '/usr/lib/chromium/chromedriver')
        self.remote_chrome = os.getenv(
            'remote_chrome', 'http://chrome:4444/wd/hub')
        self.folder_extrato = os.getenv(
            'folder_extrato', '/var/www/html/downloads')

        if(self.remote_chrome[-1] == "/"):
            self.remote_chrome = self.remote_chrome[:-1]

        if(self.folder_extrato[-1] == "/"):
            self.folder_extrato = self.folder_extrato[:-1]

    def baixar_extrato(self, id: str):
        # Calculando 60 dias atrás:
        data_extrato = datetime.datetime.now() - datetime.timedelta(days=60)
        profile = {"download.default_directory": "/home/seluser/Downloads/" + id}
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", profile)
        # Carregando o driver de comunicação com o chrome:
        driver = webdriver.Remote(
            self.remote_chrome, desired_capabilities=options.to_capabilities())

        # Código para tentar rodar chrome dentro do docker com alpine e para testes locais
        # chrome_options = webdriver.ChromeOptions()
        # profile = {
        #     "download.default_directory": "F:\\Trabalho\\PastasContabeis\\downloads\\" + id}
        # chrome_options.add_experimental_option("prefs", profile)
        # driver = webdriver.Chrome(
        #     self.chrome_driver_path, chrome_options=chrome_options)
        try:
            # Abrindo o site do banco do brasil:
            driver.get('https://www.itau.com.br/')

            # Aguardando para não dar erro de execução:
            time.sleep(5)

            # Achando a seleção por tipo de acesso:
            botao_tipo_acesso = driver.find_element_by_id('menuTypeAccess')
            botao_tipo_acesso.click()
            time.sleep(1)

            # Achando a opção "código operador":
            tipo_codigo_operador = driver.find_element_by_xpath(
                '//li[@data-select-form="codigo-operador"]')
            tipo_codigo_operador.click()
            time.sleep(1)

            # Digitando o código do operador:
            input_operador = driver.find_element_by_id('codOp')
            input_operador.send_keys(self.codigo + '\n')

            # Aguardando para não dar erro de execução:
            time.sleep(5)

            # Recuperando as teclas da senha:
            teclas_senha = driver.find_elements_by_xpath(
                '//a[@id="campoTeclado"]')
            for digito_senha in self.senha:
                for tecla_senha in teclas_senha:
                    if (digito_senha in tecla_senha.text):
                        tecla_senha.click()

            # Recuperando a tecla "acessar"
            tecla_acessar = driver.find_element_by_id('acessar')
            tecla_acessar.click()

            # Aguardando para não dar erro de execução:
            time.sleep(10)

            # Recuperando o radio button de acesso básico
            radio_basico = driver.find_element_by_id('rdBasico')
            radio_basico.click()

            # Recuperando o botao "continuar"
            botao_continuar = driver.find_element_by_id('btn-continuar')
            botao_continuar.click()

            # Aguardando para não dar erro de execução:
            time.sleep(5)

            # Fechando o modal, se houver:
            try:
                botao_fechar = driver.find_element_by_xpath(
                    '//area[@alt="Fechar"]')
                if (botao_fechar != None):
                    botao_fechar.click()
            except:
                pass

            time.sleep(1)

            # Recuperando o botão "ver extrato"
            botao_ver_extrato = driver.find_element_by_xpath(
                '//a[@aria-label="ver extrato"]')
            botao_ver_extrato.click()
            time.sleep(10)

            # Recuperando o botão "salvar em outros formatos"
            driver.switch_to.frame(1)
            botao_formatos = driver.find_element(
                By.CSS_SELECTOR, "tr:nth-child(12) .linkBoxLateral")
            botao_formatos.click()

            # Aguardando para não dar erro de execução:
            time.sleep(5)

            # Recuperando o radio button do forato OFX:
            radio_ofx = driver.find_element_by_id('OFX')
            radio_ofx.click()

            time.sleep(2)

            # Preenchendo o campo dia:
            input_dia = driver.find_element_by_id('Dia')
            input_dia.send_keys("{:02d}".format(data_extrato.day))

            time.sleep(2)

            # Preenchendo o campo mes:
            input_mes = driver.find_element_by_id('Mes')
            input_mes.send_keys("{:02d}".format(data_extrato.month))

            time.sleep(2)

            # Preenchendo o campo ano:
            input_ano = driver.find_element_by_id('Ano')
            input_ano.send_keys(str(data_extrato.year))

            time.sleep(2)

            # Clicando no botão "continuar"
            botao_continuar = driver.find_element_by_xpath(
                '//img[@class="TRNinputBTN"]')
            botao_continuar.click()

            time.sleep(2)

        except Exception as err:
            raise RepetirException(err)

        finally:
            # Fechando o browser:
            driver.quit()

        # Aguardando o download:
        time.sleep(5)

        # Recuperando o últio arquivo da pasta de downloads:
        lista_downloads = glob.glob(self.folder_extrato + '/' + id + '/*.ofx')
        extrato = max(lista_downloads, key=os.path.getctime)

        # Imprimindo o path do extrato:
        return extrato
