import re
import time
from link.app.link import Link


class Func:

    def get_cnpjs(link: Link) -> list[str]:
        """
        Extrai os CNPJs listados no menu select2 aberto.
        Retorna uma lista de strings contendo apenas os CNPJs.
        """
        # Aguarda o menu <ul> do select2 ser exibido
        xpath_ul = "//ul[contains(@class,'select2-results__options') and @role='listbox']"
        link.wait_element_clickable(xpath_ul)

        # Captura todos os <li> dentro do menu
        items = link.find_elements(f"{xpath_ul}/li")

        cnpjs: list[str] = []

        for item in items:
            text = item.text.strip()
            match = re.match(r"(\d{14})", text)
            if match:
                cnpjs.append(match.group(1))

        if not cnpjs:
            raise RuntimeError("Nenhum CNPJ encontrado no select2 aberto.")
        #print(cnpjs)

        return cnpjs

    def login(link:Link, login:str, passwd:str) -> list[str]:

        link.open_link()
        link.maximize()

        link.wait_element_clickable("//input[@id='userLogin']")
        link.send_keys("//input[@id='userLogin']",login)
        link.click_element("//button[@id='submitUserLoginIdentifier_area']") 
        link.wait_element_clickable("//input[@id='password']")
        link.send_keys("//input[@id='password']",passwd)
        link.click_element("//button[@id='next']")
        link.wait_element_clickable("//span[@id='select2-Pluto_2C9E1DB33ED130C2013ED2AC65C034CA__SELECTED_client_code-container']")
        link.click_element("//span[@id='select2-Pluto_2C9E1DB33ED130C2013ED2AC65C034CA__SELECTED_client_code-container']")

        cnpjs = Func.get_cnpjs(link)
        print(cnpjs)

        return cnpjs
    
    def extract_file(link:Link, cnpjs: list[str]) -> None:

        for i in cnpjs:
            link.wait_element_clickable("//span[@id='select2-Pluto_2C9E1DB33ED130C2013ED2AC65C034CA__SELECTED_client_code-container']")
            link.click_element("//span[@id='select2-Pluto_2C9E1DB33ED130C2013ED2AC65C034CA__SELECTED_client_code-container']")
            link.click_element("//input[@aria-label='Search']")
            print("AQUI")
        
            link.send_keys("//input[@aria-label='Search']",i)

            time.sleep(100)
            

link = Link(
url = 'https://www.tep.edenred.com/portal/tep/login/',
sleep =1,
driver='Chrome',
headless=False,
prod=False
)
login = "susana.silva@jofege.com.br"
passwd = "Gi120319*"

cnpjs = Func.login(link, login, passwd)
Func.extract_file(link, cnpjs)


# TENTAR EXTRAIR O CODIGO QUE TERMINA A LINHA ABAIXO 
"""            //li[@id='select2-Pluto_2C9E1DB33ED130C2013ED2AC7BC039F9__SELECTED_client_code-result-xtyp-265304']
            //li[@id='select2-Pluto_2C9E1DB33ED130C2013ED2AC7BC039F9__SELECTED_client_code-result-342o-257441']"""


