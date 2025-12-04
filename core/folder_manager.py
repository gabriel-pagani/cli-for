from server.connection import server_request, close_connection
from core.data_extractor import data_extractor
from core.data_formatter import data_formatter
from core.bot import bot
import time
import os


FOLDER = r'\\serverfile\users\Tecnologia\Softwares\Windows\CliFor\automation\assets\pdfs'


def get_codes() -> dict:
    query = """
        SELECT
            'F' + RIGHT('00000' + CAST((CAST(SUBSTRING((SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'F%' AND CODCOLIGADA in (1,5,6) ORDER BY DATACRIACAO DESC, CODCFO DESC), 2, 5) AS INT) + 1) AS VARCHAR), 5) AS COD_FOR,
            'C' + RIGHT('00000' + CAST((CAST(SUBSTRING((SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'C%' AND CODCOLIGADA in (1,5,6) ORDER BY DATACRIACAO DESC, CODCFO DESC), 2, 5) AS INT) + 1) AS VARCHAR), 5) AS COD_CLI
    """
    try:
        codes = server_request(query=query)
        close_connection()
        return codes
    except Exception:
        return None

def process_file(file: str, codes: dict) -> None:
    absolute_path = os.path.join(FOLDER, file)

    raw_data = data_extractor(absolute_path)
    formatted_data = data_formatter(raw_data)

    insc_est = file.lower().replace('.pdf', '').replace('c', '').replace('f', '')

    if file.upper().startswith('F'):
        bot(formatted_data=formatted_data, clifor=codes['COD_FOR'], insc_est=insc_est)
    elif file.upper().startswith('C'):
        bot(formatted_data=formatted_data, clifor=codes['COD_CLI'], insc_est=insc_est)

    try:
        os.remove(absolute_path)
    except Exception:
        None

def monitor_folder() -> None:
    try:
        files = os.listdir(FOLDER)
        valid_files = [f for f in files if f.lower().endswith('.pdf') and (f.lower().startswith('c') or f.lower().startswith('f'))]
        
        print("Automação iniciada....")
        
        for index, file in enumerate(valid_files, 1):
            codes = get_codes()
            if (file.lower().endswith('.pdf') and (file.lower().startswith('c') or file.lower().startswith('f'))):
                process_file(file=file, codes=codes)
                print(f"Arquivo {index} de {len(valid_files)} processado")
        
        print("Automação finalizada. Pressione Enter para fechar...")
        input()

    except Exception:
        None
