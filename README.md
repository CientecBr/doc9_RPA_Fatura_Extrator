# RPA Extrator Faturas (DOC9)

Este reposit�rio cont�m o c�digo-fonte em **Python** que realiza a automa��o para:
- Ler todas as p�ginas de uma tabela no site [https://rpachallengeocr.azurewebsites.net/](https://rpachallengeocr.azurewebsites.net/).
- Capturar apenas as faturas cuja data de vencimento j� passou ou vence hoje.
- Faz o download dos faturas.
- Gerar um arquivo .CSV com: N�mero da Fatura, Data da Fatura e URL da Fatura.

## Sum�rio
1. [Tecnologias Utilizadas](#tecnologias-utilizadas)
2. [Configura��o e Instala��o](#configura��o-e-instala��o)
3. [Execu��o](#execu��o)
4. [Decis�es T�cnicas](#decis�es-t�cnicas)
5. [Otimiza��es de Performance](#otimiza��es-de-performance)
6. [Como Usar](#como-usar)

---

## Tecnologias Utilizadas
- **Python 3.9+**
- [Selenium](https://pypi.org/project/selenium/)
- [Requests](https://pypi.org/project/requests/)
- [ChromeDriver](https://chromedriver.chromium.org/downloads) (compat�vel com sua vers�o do Google Chrome)

---

## Configura��o e Instala��o

1. **Clonar o reposit�rio**:
   ```bash
   git clone https://github.com/seu-usuario/desafio-doc9.git
   cd desafio-doc9

2. **Instalar depend�ncias:**
   pip install -r requirements.txt

## Execu��o
**No diret�rio principal (onde est� o main.py), execute:**
  python src/main.py
  
**"Caso esteja usando ambiente virtual, lembre-se de ativ�-lo antes."**

## Decis�es T�cnicas
- Selenium para automa��o de navega��o:
- Usado por permitir clicar em bot�es "Next" e extrair dados de tabelas din�micas.
- Requests para download dos arquivos:
- Mais simples e eficiente que fazer download direto via Selenium.

**Estrutura de pastas:**
- src/ para isolar o c�digo.
- faturas/ (gerada dinamicamente) para armazenar os PDFs/JPGs baixados e o CSV final.

## Otimiza��es de Performance
- utiliza��o do webdriver_manager (j� incluso nas depend�ncias) para instala��o autom�tica do ChormeDriver.
- Headless Chrome: o Chrome � iniciado sem interface gr�fica, reduzindo uso de recursos.
- Pagina��o: s� carrega a pr�xima p�gina quando a anterior j� foi processada.
- Download Sequencial: dado o volume esperado, n�o foi necess�rio paralelismo. Para grande escala (Futuro), ser� poss�vel usar Threads ou Async IO.

## Como Usar
**Ap�s a execu��o, o script:**
- Navega pelas p�ginas do site.
- Coleta as faturas cujo vencimento = data atual.
- Salva os arquivos na pasta faturas.
- Gera o arquivo faturas.csv dentro da mesma pasta.
- Verifique o conte�do da pasta faturas. Voc� dever� encontrar: arquivos .pdf ou .jpg (conforme a extens�o do link).
- O arquivo faturas.csv com colunas: N�mero da Fatura, Data da Fatura e URL da Fatura.