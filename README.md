## **Projeto Final Python**

Projeto final do curso de Python da CoderHouse. Esse projeto tem por objetivo desenvolver um pipeline de dados, onde foram realizados
a extração dos dados brutos via API, tratamento dos dados visando obter dados mais consistentes para serem analisados, a criação de um
banco de dados e o armazenamento das tabelas nesse banco. 

## :pencil: **Pré-requisitos**

:arrow_right: [Python 3](https://www.python.org/downloads/)

:arrow_right: [Visual Studio Code](https://code.visualstudio.com/download)

:heavy_exclamation_mark:É necessário baixar o arquivo [notificacao.py](https://github.com/iago-cord/Curso-Python/blob/main/Projeto%20Final/requirements.txt) e [funcoes.py](https://github.com/iago-cord/Curso-Python/blob/main/Projeto%20Final/funcoes.py) para que o código funcione corretamente. 

## :notebook_with_decorative_cover: Bibliotecas Utilizadas

As bibliotecas utilizadas no projeto estão disponiveis no arquivo [requirements.txt](https://github.com/iago-cord/Curso-Python/blob/main/Projeto%20Final/requirements.txt)
Nesse arquivo você pode conferir as bibliotecas e versões utilizadas. 

## :fuelpump: API's 

Para o desenvolvimento do projeto, foram utilizadas 3 bases de dados, disponibilizados pela **Brasil API**, que tem como como objetivo 
compilar dados sobre diversas áreas do pais. 
**Foram utilizadas 3 API's:**

:arrow_right: [**Corretoras**](https://brasilapi.com.br/api/cvm/corretoras/v1)

Fornece uma lista de todas as corretoras cadastradas na CVM, estando elas ativas ou canceladas. 

:arrow_right: [**Bancos**](https://brasilapi.com.br/api/banks/v1)

Fornece uma lista de todos os bancos operantes no Brasil.

:arrow_right: [**PIX**](https://brasilapi.com.br/api/pix/v1/participants)

Fornece uma lista de todos os bancos participantes do PIX no Brasil.

## :clipboard: Documentação

Este projeto está dividido em três arquivos, [Projeto Final.ipynb](https://github.com/iago-cord/Curso-Python/blob/main/Projeto%20Final/Projeto%20Final.ipynb) onde foi realizado a extração e a transformação dos dados, [notificação.py](https://github.com/iago-cord/Curso-Python/blob/main/Projeto%20Final/notificacao.py) que notifica se a importação da API obteve sucesso ou não e [funcoes.py](https://github.com/iago-cord/Curso-Python/blob/main/Projeto%20Final/funcoes.py) onde estão as funções utilizadas para a extração e transformação dos dados. 

## FUNÇÕES GERAIS

:arrow_right: **Importando tabelas das API's ->** função para importar as url's das API's recebe como parametro a url e retorna o request. 

**FUNÇÃO**

```
def importar (url):
    return requests.get(url)
```
**CHAMANDO A FUNÇÃO**
```
Extraindo a tabela banks da API
url = "https://brasilapi.com.br/api/banks/v1"

bancos = func.importar(url)
```
```
Extraindo a tabela corretoras da API
url = "https://brasilapi.com.br/api/cvm/corretoras/v1"

corretoras = func.importar(url)
```
```
Extraindo a tabela PIX da API
url = 'https://brasilapi.com.br/api/pix/v1/participants'

pix = requests.get(url)
```

:arrow_right: **Formato data ->** Foi usado o metodo **strftime** para transformar o objeto em string e formatar a data e hora no formato correto.

**FUNÇÃO**
```
def formato_datas():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
```
**CHAMANDO A FUNÇÃO**
```
data = func.formato_datas()
```

:arrow_right: **Salvando a tabela em uma variável ->** Essa função recebe como parametro a base de dados, verifica se o status code é igual a 200 e retorna a base passada como parametro no formato .json

**FUNÇÃO**
```
def salvar_tabela(base):
    if base.status_code == 200:
        return base.json()
```
**CHAMANDO A FUNÇÃO**
```
bancos_json = func.salvar_tabela(bancos) 
```
```
corretoras_json = func.salvar_tabela(corretoras) 
```
```
pix_json = func.salvar_tabela(pix) 
```

## FUNÇÕES DATAFRAME CORRETORAS 

:arrow_right: **Formatacao da coluna valor patrimonio** -> Foi utilizado o **Regex** para determinar a fomatacao, o metodo **format()** que vai receber a coluna a ser modificada. Depois criamos a função **formato_valor** que vai receber como  parametro o dataframe e a coluna, foi utilizado o **pd.to_numeric** para transformar o objeto em um numerico e depois o metodo **.apply** que recebeu a função formatar para aplicar a formatação a cada elemento da coluna.

**FUNÇÃO**
```
def formatar(valor):
    return "R${:,.2f}".format(valor)

def formato_valor(tabela,coluna):
    tabela[coluna] = pd.to_numeric(tabela[coluna])
    tabela[coluna] = tabela[coluna].apply(formatar)

```
**CHAMANDO A FUNÇÃO**
```
func.formato_valor(corretoras_full_renomeado,'Valor Patrimonio')
```
:arrow_right: **Formatacao das colunas com datas ->** Recebe como parametro o dataframe e a coluna a ser modificada, utiliza o metodo pd.to_datetime para transformar o dataframe em um objeto do tipo datetime, depois foi aplicado o metodo **dt.strftime** para formatar esse objeto.

**FUNÇÃO**

```
def formato_data(tabela, coluna):
    tabela[coluna] = pd.to_datetime(tabela[coluna])
    tabela[coluna] = tabela[coluna].dt.strftime('%d-%m-%Y')
```
**CHAMANDO A FUNÇÃO**

```
func.formato_data(corretoras_full_renomeado,'Data Registro')
```

➡️ **Alterando o nome das colunas ->** Passamos como parametro o dataframe, foi usado o metodo **set_axis** que recebeu como parametro as colunas a serem alteradas e o eixo(axis) 0 para linhas e 1 para colunas, no caso como foi alterado o nome da coluna definimos o **axis=1**

**FUNÇÃO**
```
def nome_colunas(tabela):
    return tabela.set_axis(['CNPJ', 'Tipo', 'Razão Social', 'Nome Comercial', 'Status', 'E-Mail', 'Telefone',
                          'CEP', 'Pais', 'UF', 'Municipio', 'Bairro', 'Complemento', 'Logradouro', 'Data Patrimonio', 
                          'Valor Patrimonio', 'Codigo CVM', 'Data Inicio', 'Data Registro'], axis=1)
```
**CHAMANDO A FUNÇÃO**

```
corretoras_full_renomeado = func.nome_colunas(corretoras_full)
```

:arrow_right: **Exclusão de colunas irrelevantes para a análise. ->** Recebe o dataframe como parametro, com o metodo **.drop** especificamos os nomes das colunas a serem dropadas, e o eixo de exclusão axis=1

**FUNÇÃO**

```
def exclusao_colunas(tabela):
     return tabela.drop(['Tipo','E-Mail', 'CEP', 'Complemento', 'Logradouro','Data Inicio',
                         'Data Patrimonio'], axis=1)
```

**CHAMANDO A FUNÇÃO**
```
corretoras_full_renomeado = func.nome_colunas(corretoras_full)
```

:arrow_right: **Ajustando o Formato do CNPJ ->** recebe o dataframe e a coluna como parametro, depois determinamos o padrão de CNPJ atraves do regex, o **str.replace** recebe o padrao para identificar e modificar os valores na coluna, em seguida os grupos identificados e a forma como eles vao ser separados(./-) e o **regex=true** para informar que se trata de uma expressão regular.

**FUNÇÃO**

```
def formato_cnpj(tabela,coluna):
    padrao = r'(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})'
    return tabela[coluna].str.replace(padrao, r'\1.\2.\3/\4-\5', regex = True
```
**CHAMANDO A FUNÇÃO**

```
corretoras_full_colunas['CNPJ'] = func.formato_cnpj(corretoras_full_colunas,'CNPJ')
```

:arrow_right: **Filtro telefone ->** Passamos como parametro o dataframe, a coluna e nesse caso o tamanho(length) da string a ser filtrada o metodo **str.len** faz a contagem do tamanho da string, e retorna os elementos da coluna que atendem o tamanho passado no parametro length. 

**FUNÇÃO** 
```
def filtro_str_len(tabela, coluna, length):
    return tabela[coluna].str.len() < length 

```
**CHAMANDO A FUNÇÃO**
```
filtro_tel =  func.filtro_str_len(corretoras_full_colunas,'Telefone',8) 
```

:arrow_right: **Adicionando o 3 em telefones que estavam faltando 1 numero  ->** Recebe de parametro o dataframe, o filtro e a coluna, o metodo **.loc** vai selecionar as linhas que atendem ao filtro e adicionar o numero 3 na frente desses numeros.

**FUNÇÃO** 
```
def ajuste_telefone(tabela, filtro, coluna):
    return '3'+ tabela.loc[filtro, coluna]
```

**CHAMANDO A FUNÇÃO**
```
corretoras_full_colunas.loc[filtro_tel, 'Telefone'] = func.ajuste_telefone(corretoras_full_colunas,filtro_tel,'Telefone')
```

:arrow_right: **Ajustando formato telefone ->** dataframe e coluna como parametro, depois definimos o padrao atraves do regex para identificar depois o **str.replace** recebe o padrao definido, a formatacao a ser aplicada e **regex=true** para informar que se trata de uma expressão regular

**FUNÇÃO** 

```
def formato_telefone(tabela, coluna):
    padrao_tel = r'(\d{4})(\d{4})'
    return tabela[coluna].str.replace(padrao_tel, r'\1-\2', regex=True)
``` 

**CHAMANDO A FUNÇÃO**

```
corretoras_full_colunas['Telefone'] = func.formato_telefone(corretoras_full_colunas, 'Telefone')
```

:arrow_right: **Funcao para filtrar string vazia ->** recebe como parametro dataframe, coluna e o tamanho da string. o metodo **str.len** faz a contagem e retorna o index da linha que atende a condição especificada.

**FUNÇÃO** 

```
def string_vazia(tabela, coluna, length):
    return tabela[ tabela[coluna].str.len() == length].index
``` 

**CHAMANDO A FUNÇÃO**

```
filtro_sem_tel = func.string_vazia(corretoras_full_colunas,'Telefone',1)

filtro_pais = func.string_vazia(corretoras_full_colunas,'Pais',1)

filtro_municipio = func.string_vazia(corretoras_full_colunas, 'Municipio', 0)

filtro_UF = func.string_vazia(corretoras_full_colunas,'UF',0)

filtro_bairro = func.string_vazia(corretoras_full_colunas,'Bairro',0)

filtro_nome_comercial = func.string_vazia(corretoras_full_colunas,'Nome Comercial',0)
``` 

:arrow_right: **Função drop de linhas ->** recebe como parametro o dataframe e o filtro anterior que retorna o index, o metodo **.drop** recebe o filtro como condição e dropa todas as linhas que atendem a condição do filtro baseado no index.

**FUNÇÃO** 

```
def drop_linhas(tabela, filtro):
    return tabela.drop(filtro)
``` 

**CHAMANDO A FUNÇÃO**

```
corretoras_full_colunas = func.drop_linhas(corretoras_full_colunas, filtro_sem_tel)

corretoras_full_colunas = func.drop_linhas(corretoras_full_colunas,filtro_pais)

corretoras_full_colunas = func.drop_linhas(corretoras_full_colunas,filtro_municipio)

corretoras_full_colunas = func.drop_linhas(corretoras_full_colunas,filtro_UF)

corretoras_full_colunas = func.drop_linhas(corretoras_full_colunas,filtro_bairro)

corretoras_full_colunas = func.drop_linhas(corretoras_full_colunas,filtro_nome_comercial)

corretoras_full_colunas = func.drop_linhas(corretoras_full_colunas,filtro_nome)

corretoras_full_colunas = func.drop_linhas(corretoras_full_colunas,filtro_valor)
``` 

:arrow_right: **Função filtrar caracteres especiais e valor zerado ->** recebe como parametro o dataframe, a coluna e o caracter a ser condicionado, depois retorna o index de todas as linhas que atendem a condicional.

**FUNÇÃO** 

```
def caracter_especial(tabela, coluna, condicional):
    return tabela[tabela[coluna] == condicional].index
``` 

**CHAMANDO A FUNÇÃO**

```
filtro_nome = func.caracter_especial(corretoras_full_colunas,'Nome Comercial','--')

filtro_valor = func.caracter_especial(corretoras_full_colunas,'Valor Patrimonio', 'R$0.00')
```

:arrow_right: **Filtrando as corretoras que estão em funcionamento**

```
corretoras_ativas = corretoras_full_colunas.loc[corretoras_full_colunas['Status'] =='EM FUNCIONAMENTO NORMAL']
```

:arrow_right: **Filtrando as corretoras que estão canceladas**

```
corretoras_canceladas = corretoras_full_colunas.loc[corretoras_full_colunas['Status'] =='CANCELADA']

``` 

:arrow_right: **Salvando os dados tratados no banco de dados e fechando a conexão**

```
corretoras_full_colunas.to_sql('Corretoras Tratado', corretoras_connect, if_exists='replace', index=False )
corretoras_ativas.to_sql('Corretoras Tratado Ativas', corretoras_connect, if_exists='replace', index=False )
corretoras_canceladas.to_sql('Corretoras Tratado Canceladas', corretoras_connect, if_exists='replace', index=False )
bancos_connect.close()
```
## FUNÇÕES DATAFRAME BANCOS 

:arrow_right: Funcao para alterar nome das colunas -> Passamos como parametro o dataframe, foi usado o metodo **set_axis** que recebeu como parametro as colunas a serem alteradas e o eixo(axis) 0 para linhas e 1 para colunas, no caso como foi alterado o nome da coluna passamos o **axis=1**

**FUNÇÃO** 

```
def altera_colunas(tabela):
    return tabela.set_axis(['ISPB', 'Nome', 'Código', 'Nome Completo'], axis=1)

``` 

**CHAMANDO A FUNÇÃO**

```
bancos_full_renomeado = func.altera_colunas(bancos_full)
``` 

:arrow_right: **Transformando as tabelas em um DataFrame** 

```
bancos_full = pd.DataFrame(bancos_json)
```

:arrow_right: **Excluindo linhas com a coluna code que possuem missing values**

```
bancos_full = bancos_full.dropna(subset=['code'])

```

:arrow_right: **Transformando os dados da coluna code de float para int**

```
bancos_full = bancos_full.astype({'code':int})
```
:arrow_right: **Alterando a coluna Nome Completo para deixar todos nomes em maiusculo**

```
bancos_full_renomeado['Nome Completo']=bancos_full_renomeado['Nome Completo'].str.upper()
```

:arrow_right: **Tratamento de Missing Values**

```
bancos_full_tratado = (bancos_full_renomeado.dropna())
```

:arrow_right: **Ordenação pela coluna Código**

```
bancos_full_tratado.sort_values('Código')
``` 
## FUNÇÕES DATAFRAME PIX 

:arrow_right: **Funcao para alterar o nome das colunas ->** Passamos como parametro o dataframe, foi usado o metodo **set_axis** que recebeu como parametro as colunas a serem alteradas e o eixo(axis) 0 para linhas e 1 para colunas, no caso como foi alterado o nome da coluna passamos o **axis=1**

**FUNÇÃO** 

```
def modifica_coluna(tabela):
    return tabela.set_axis(['ISPB', 'Nome', 'Nome Reduzido', 'Modalidade', 'Tipo', 'Inicio'], axis=1)

``` 

**CHAMANDO A FUNÇÃO**

```
pix_full_renomeado = func.modifica_coluna(pix_full)
```

:arrow_right: **Funcao para ajustar o formato de data hora da coluna inicio ->** Recebe como parametro o dataframe e a coluna a ser modificada, utiliza o metodo **pd.to_datetime** para transformar o dataframe em um objeto do tipo **datetime**, depois foi aplicado o metodo **dt.strftime** para formatar esse objeto.

**FUNÇÃO** 

```
def ajusta_datahora(tabela, coluna):
    return tabela[coluna].dt.strftime('%d-%m-%Y %H:%M')
``` 

**CHAMANDO A FUNÇÃO**

```
pix_full_renomeado['Inicio'] = func.ajusta_datahora(pix_full_renomeado,'Inicio')
```
