# RPA Extrator Faturas (DOC9)

Este repositório contém o código-fonte em **Python** que realiza a automação para:
- Ler todas as páginas de uma tabela no site [https://rpachallengeocr.azurewebsites.net/](https://rpachallengeocr.azurewebsites.net/).
- Capturar apenas as faturas cuja data de vencimento já passou ou vence hoje.
- Faz o download dos faturas.
- Gerar um arquivo .CSV com: Número da Fatura, Data da Fatura e URL da Fatura.

## Sumário
1. [Tecnologias Utilizadas](#tecnologias-utilizadas)
2. [Configuração e Instalação](#configuração-e-instalação)
3. [Execução](#execução)
4. [Decisões Técnicas](#decisões-técnicas)
5. [Otimizações de Performance](#otimizações-de-performance)
6. [Como Usar](#como-usar)

---

## Tecnologias Utilizadas
- **Python 3.9+**
- [Selenium](https://pypi.org/project/selenium/)
- [Requests](https://pypi.org/project/requests/)
- [ChromeDriver](https://chromedriver.chromium.org/downloads) (compatível com sua versão do Google Chrome)

---

## Configuração e Instalação

1. **Clonar o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/desafio-doc9.git
   cd desafio-doc9

2. **Instalar dependências:**
   pip install -r requirements.txt

## Execução
**No diretório principal (onde está o main.py), execute:**
  python src/main.py
  
**"Caso esteja usando ambiente virtual, lembre-se de ativá-lo antes."**

## Decisões Técnicas
- Selenium para automação de navegação:
- Usado por permitir clicar em botões "Next" e extrair dados de tabelas dinâmicas.
- Requests para download dos arquivos:
- Mais simples e eficiente que fazer download direto via Selenium.

**Estrutura de pastas:**
- src/ para isolar o código.
- faturas/ (gerada dinamicamente) para armazenar os PDFs/JPGs baixados e o CSV final.

## Otimizações de Performance
- utilização do webdriver_manager (já incluso nas dependências) para instalação automática do ChormeDriver.
- Headless Chrome: o Chrome é iniciado sem interface gráfica, reduzindo uso de recursos.
- Paginação: só carrega a próxima página quando a anterior já foi processada.
- Download Sequencial: dado o volume esperado, não foi necessário paralelismo. Para grande escala (Futuro), será possível usar Threads ou Async IO.

## Como Usar
**Após a execução, o script:**
- Navega pelas páginas do site.
- Coleta as faturas cujo vencimento = data atual.
- Salva os arquivos na pasta faturas.
- Gera o arquivo faturas.csv dentro da mesma pasta.
- Verifique o conteúdo da pasta faturas. Você deverá encontrar: arquivos .pdf ou .jpg (conforme a extensão do link).
- O arquivo faturas.csv com colunas: Número da Fatura, Data da Fatura e URL da Fatura.