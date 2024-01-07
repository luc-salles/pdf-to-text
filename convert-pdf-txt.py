#!/usr/bin/python3
from pdf2image import convert_from_path
from PIL import Image
import glob
import pytesseract
import os
###### necessario sudo apt install python3-tesserocr
##### PDF PARA IMAGEM
def pdfs_to_images(input_folder, output_folder):
    # Certifique-se de que o diretório de saída exista
    os.makedirs(output_folder, exist_ok=True)

    # Listar todos os arquivos PDF no diretório de entrada
    pdf_files = glob.glob(os.path.join(input_folder, '*.pdf'))

    for pdf_path in pdf_files:
        # Criar uma pasta específica para cada PDF no diretório de saída
        pdf_folder_name = os.path.splitext(os.path.basename(pdf_path))[0]
        pdf_output_folder = os.path.join(output_folder, pdf_folder_name)
        os.makedirs(pdf_output_folder, exist_ok=True)

        # Converter páginas PDF em imagens usando pdf2image
        images = convert_from_path(pdf_path, output_folder=pdf_output_folder, fmt='png', thread_count=1)

#######

##### IMG para TXT

def extrair_texto_e_salvar_arquivo(imagem, caminho_do_tesseract, caminho_do_arquivo_saida):
    # Configurar o caminho do Tesseract
    pytesseract.pytesseract.tesseract_cmd = caminho_do_tesseract

    # Abrir a imagem usando a biblioteca Pillow
    imagem_pillow = Image.open(imagem)

    # Extrair o texto usando a biblioteca pytesseract
    texto_extraido = pytesseract.image_to_string(imagem_pillow, lang='por')

    # Salvar o texto em um arquivo de texto
    with open(caminho_do_arquivo_saida, 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(texto_extraido)

def processar_todas_as_imagens_no_diretorio(diretorio_entrada, diretorio_saida, caminho_do_tesseract):
    # Certifique-se de que o diretório de saída exista
    os.makedirs(diretorio_saida, exist_ok=True)

    # Listar todos os subdiretórios no diretório de entrada
    subdiretorios = [nome for nome in os.listdir(diretorio_entrada) if os.path.isdir(os.path.join(diretorio_entrada, nome))]

    # Iterar sobre cada subdiretório
    for subdiretorio in subdiretorios:
        # Construir caminhos completos para entrada e saída
        diretorio_entrada_completo = os.path.join(diretorio_entrada, subdiretorio)
        diretorio_saida_completo = os.path.join(diretorio_saida, subdiretorio)

        # Certifique-se de que o diretório de saída exista para este subdiretório
        os.makedirs(diretorio_saida_completo, exist_ok=True)

        # Listar todos os arquivos .png no subdiretório de entrada
        arquivos = os.listdir(diretorio_entrada_completo)
        imagens_png = [arquivo for arquivo in arquivos if arquivo.lower().endswith('.png')]

        # Iterar sobre cada imagem .png
        for imagem in imagens_png:
            # Construir caminhos completos para a imagem e o arquivo de saída
            caminho_da_imagem = os.path.join(diretorio_entrada_completo, imagem)
            caminho_do_arquivo_saida = os.path.join(diretorio_saida_completo, f"{os.path.splitext(imagem)[0]}.txt")

            # Extrair texto e salvar em um arquivo para cada imagem
            extrair_texto_e_salvar_arquivo(caminho_da_imagem, caminho_do_tesseract, caminho_do_arquivo_saida)


pdfs_to_images('PDF', 'IMG')

# Substitua 'TXT' pelo nome do diretório onde os arquivos de texto serão salvos
processar_todas_as_imagens_no_diretorio('IMG', 'TXT', '/usr/bin/tesseract')

