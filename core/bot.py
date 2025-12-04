import pyautogui
from core import smart_pyautogui
import pyperclip
import time
from server.connection import server_request, close_connection


def get_cnpj(cnpj: str) -> bool:
    query = f"SELECT * FROM FCFO WHERE CGCCFO = '{cnpj}'"
    try:
        response = server_request(query=query)
        close_connection()
        return bool(response)
    except Exception:
        None


def bot(formatted_data: dict, clifor: str, insc_est: str = None) -> None:
    if formatted_data['Situacao'] == 'BAIXADA' or formatted_data['Situacao'] == 'INAPTA':
        return
    
    if get_cnpj(formatted_data['Cnpj']):
        return

    pyautogui.PAUSE = 0.3

    smart_pyautogui.smart_click(image_path=r'\\serverfile\users\Tecnologia\Softwares\Windows\CliFor\automation\assets\images\menu.png')

    smart_pyautogui.smart_click(image_path=r'\\serverfile\users\Tecnologia\Softwares\Windows\CliFor\automation\assets\images\fechar.png')

    pyautogui.hotkey('ctrl', 'insert')

    smart_pyautogui.smart_press(key='tab', flag_path=r'\\serverfile\users\Tecnologia\Softwares\Windows\CliFor\automation\assets\images\cadastro_aberto.png')

    pyautogui.write(clifor)

    pyautogui.press('tab', presses=2)

    pyautogui.write(formatted_data['Nome Fantasia'].strip())

    pyautogui.press('tab')

    pyautogui.write(formatted_data['Nome Empresarial'].strip())

    # Seleciona a classificação e Categoria
    if 'C' in clifor.upper():
        smart_pyautogui.smart_click(image_path=r'\\serverfile\users\Tecnologia\Softwares\Windows\CliFor\automation\assets\images\cliente.png')

    if 'F' in clifor.upper():
        smart_pyautogui.smart_click(image_path=r'\\serverfile\users\Tecnologia\Softwares\Windows\CliFor\automation\assets\images\fornecedor.png')

    smart_pyautogui.smart_click(image_path=r'\\serverfile\users\Tecnologia\Softwares\Windows\CliFor\automation\assets\images\juridica.png')

    # Escreve o CPF/CNPJ
    pyautogui.press('tab')
    pyautogui.write(formatted_data['Cnpj'])

    # Tratamento da inscrição estadual
    if insc_est:
        pyautogui.press('tab', presses=3)
        if insc_est.isdigit():
            pyautogui.write(str(insc_est))
        pyautogui.press('tab', presses=8)
    else:
        pyautogui.press('tab', presses=11)

    # Preenche dados de endereço
    pyautogui.write(formatted_data['Cep'])
    pyautogui.press('tab')

    time.sleep(3)  # Espera o sistema processar o CEP
    pyautogui.click(x=1373, y=736)  # Fecha o menu
    pyautogui.click(x=1373, y=715)  # Fecha o menu

    # Preenche logradouro
    pyautogui.press('tab')
    pyautogui.write(formatted_data['Tipo Rua'])
    pyautogui.press('tab', presses=2)
    pyautogui.write(formatted_data['Nome Rua'])
    pyautogui.press('tab')

    # Número e complemento
    pyautogui.write(formatted_data['Numero'])
    pyautogui.press('tab', presses=3)

    pyautogui.write(formatted_data['Complemento'])
    pyautogui.press('tab')

    # Bairro
    pyautogui.write(formatted_data['Tipo Bairro'])
    pyautogui.press('tab', presses=2)
    pyautogui.write(formatted_data['Nome Bairro'])

    # UF e Município
    pyautogui.press('tab', presses=4)
    pyautogui.write(formatted_data['Uf'])

    pyautogui.press('tab', presses=4)
    pyperclip.copy(formatted_data['Municipio'])
    pyautogui.hotkey('ctrl', 'v')

    # Contatos
    pyautogui.press('tab', presses=4)
    pyautogui.write(formatted_data['Celular1'])
    pyautogui.press('tab')

    pyautogui.write(formatted_data['Celular2'])
    pyautogui.press('tab', presses=3)

    pyautogui.write(formatted_data['Email'])

    if insc_est and 'x' not in insc_est.lower():
        smart_pyautogui.smart_click(image_path=r'\\serverfile\users\Tecnologia\Softwares\Windows\CliFor\automation\assets\images\tributos.png')
        smart_pyautogui.smart_click(image_path=r'\\serverfile\users\Tecnologia\Softwares\Windows\CliFor\automation\assets\images\tipo_contribuinte.png')
        
        if 'I' in insc_est.upper():
            pyautogui.press('up')
            pyautogui.press('tab')
        elif insc_est.isdigit():
            pyautogui.press('up', presses=2)
            pyautogui.press('tab')

    # Salva o cadastro
    smart_pyautogui.smart_click(image_path=r'\\serverfile\users\Tecnologia\Softwares\Windows\CliFor\automation\assets\images\salvar.png')

    # Espera o cadastro terminar e fecha a aba
    smart_pyautogui.smart_click(x=114, y=168, flag_path=r'\\serverfile\users\Tecnologia\Softwares\Windows\CliFor\automation\assets\images\flag_filtro.png')
