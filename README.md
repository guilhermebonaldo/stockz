## Project Organization

    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.ipynb       <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         1-1-jqp-initial-data-exploration.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    |
    └── src                <- Source code for use in this project.
        |
        ├── __init__.py        <- Script calling functions of make_dataset.py, build_features.py 
        |                         and predict_model.py, run to execute the entire pipeline
        │
        ├── make_dataset.py    <- Script to download or generate data
        │
        ├── build_features.py  <- Script to turn raw data into features for modeling
        │
        ├── predict_model.py   <- Script to use trained models to make predictions
        │                          
        ├── train_model.py     <- Script to train models
        │
        │
        └── visualize.py  <- Scripts to create exploratory and results oriented visualizations
       


---------------

## Detailed information

------------------


### Data

1. Don't ever edit your raw data, especially not manually, and especially not in Excel. 
2. Don't overwrite your raw data. 
3. Don't save multiple versions of the raw data. 
4. Treat the data (and its format) as immutable. The code you write should move the raw data through a pipeline to your final analysis. 
5. You shouldn't have to run all of the steps every time you want to make a new figure (see Analysis is a DAG), but anyone should be able to reproduce the final products with only the code in src and the data in data/raw.

Also, if data is immutable, it doesn't need source control in the same way that code does. Therefore, by default, the data folder is included in the .gitignore file. If you have a small amount of data that rarely changes, you may want to include the data in the repository. Github currently warns if files are over 50MB and rejects files over 100MB. Some other options for storing/syncing large data include AWS S3 with a syncing tool (e.g., s3cmd), Git Large File Storage, Git Annex, and dat.





------------------

### Models

This directory is the place where serialized models go to. files could be in the formats ```.pickle``` , ```.hdf5``` , ```.h5``` , and others.

In this directory can be saved ```MLFlow experiments``` too.


------------------

### Notebooks

Since notebooks are challenging objects for source control (e.g., diffs of the json are often not human-readable and merging is near impossible), we recommended not collaborating directly with others on Jupyter notebooks, they must be used only in development phase, not in production. The code developed in the notebooks that will run in production must be transferred to ```.py``` files.

**Naming convention:** We use the format ```<step>-<version>-<ghuser>-<description>.ipynb``` (e.g., 1-1-ggb-visualize-distributions.ipynb).


Refactor the good parts. Don't write code to do the same task in multiple notebooks. If it's a data preprocessing task, put it in the pipeline at src/data/make_dataset.py and load data from data/interim. If it's useful utility code, refactor it to src.

To load functions from the src files in the notebook:

```python
# OPTIONAL: Load the "autoreload" extension so that code can change
%load_ext autoreload

# OPTIONAL: always reload modules so that as you change code in src, it gets loaded
%autoreload 2

from src.data import make_dataset
```

------------------

### Requirements

The first step in reproducing an analysis is always reproducing the computational environment it was run in. You need the same tools, the same libraries, and the same versions to make everything play nicely together.

One effective approach to this is use virtualenv. By listing all of your requirements in the repository (we include a ```requirements.txt``` file) you can easily track the packages needed to recreate the analysis. Here is a good workflow:



### 1. Gerenciamento do ambiente de desenvolvimento 

 

Por conta da escolha do Python como principal linguagem de programação utilizada nos projetos de ciência de dados dentro da Tenbu, optou-se por utilizar o pacote conda presente na suíte de ferramentas Anaconda, como ferramenta para instalação de novas bibliotecas e pacotes, assim como para gerenciar os ambientes utilizados para cada projeto. Abaixo segue discriminado as atividades que serão necessárias para dar andamento a um projeto junto com especificações de como realizá-las. 

 

#### 1.1. Criação de um novo ambiente 

 

Após a estruturação dos diretórios padrão da Tenbu que irá suportar os arquivos e artefatos de um novo projeto é momento de começar a programar. Para isso é essencial que se tenha um ambiente limpo, leve e isolado, ou seja, sem bibliotecas de terceiros que possam comprometer o desempenho ou influenciar o desenvolvimento do projeto atual. Para criar este novo ambiente utilizando o conda basta se localizar no diretório do projeto e digitar: 

 
~~~~
conda create -n {nome-do-projeto} python=3.6
~~~~
 

Com isso, o conda criará um ambiente com somente as bibliotecas básicas para programar em Python. Após esse passo será necessário ativar o ambiente, para assim instalar as ferramentas necessárias e fazer uso do ambiente de fato. Para isso basta digitar no terminal: 

 
~~~~
conda activate {nome-do-projeto}
~~~~
 

Caso já tenha esquecido o nome do ambiente que você acabou de dar, é possível listar todos os ambientes presentes no sistema operacional. Basta digitar: 

 
~~~~
conda env list
~~~~

 

Com o ambiente ativo no seu terminal, já é possível instalar pacotes através do conda ou pip e todas as bibliotecas estarão presentes apenas para quem utiliza este ambiente. 

 

#### 1.2. Adicionar ambiente ao Jupyter Notebooks 

 

Atualmente em projetos de ciência de dados é bastante comum o uso do desenvolvimento iterativo proporcionado pelos notebooks para realizar os experimentos estatísticos e de machine learning, e por conta disso, naturalmente é desejado o uso dos ambientes junto ao notebook. Para tal será necessário a criação de um novo kernel dentro do Jupyter Notebook. Para realizar esta tarefa, com o ambiente ativado, vide topico 1.1, basta instalar o pacote ipykernel do python pelo conda e adicionar o ambiente, segue o código: 

 
~~~~
conda install -c anaconda ipykernel 
python -m ipykernel install --user --name={nome-do-ambiente} 
~~~~
 

A partir disso, poderá ser escolhido qual ambiente utilizar ao criar um novo notebook, por conta disso é preciso de uma certa atenção para identificar qual kernel você deseja que o notebook faça uso. 

 

#### 1.3. Exportar um ambiente já existente 

 

Chegará o momento que será necessário salvar o estado do desenvolvimento do projeto, seja para realizar um backup de segurança ou seja para repassar para um colega continuar o seu trabalho. Para isso, além dos códigos gerados é necessário ter uma réplica do ambiente que os desenvolveu, dado que os códigos possam exigir algumas bibliotecas hipsters que poucas almas utilizam e quem for pegar o seu código para dar continuidade precisar ter os mesmos insumos para chegar onde você chegou. Com ajuda do conda você pode exportar o seu ambiente para um arquivo .yaml onde ficará descrito todas os pacotes e suas respectivas versões, possibilitando dessa maneira que outro conda possa importá-lo. Segue o código para tal: 

~~~~
conda env export > environment.yml
~~~~

Colocando este arquivo junto a raiz do projeto e o repassando junto ao seu código para o seu versionador favorito (GitHub, GitLab, GitBucket), você já estará realizando seu papel de bom programador dando os insumos necessários para futuras almas perdidas que precisarão utilizar o que você já realizou. 

#### 1.4. Importar ambiente 

Eventualmente o destino há de colocar você na posição de utilizar ou continuar o código de outra pessoa. Se esta pessoa que escreveu o código leu este artigo e encarecidamente seguiu as orientações aqui descritas, esta será uma tarefa um pouco menos dolorosa para você. Após ter clonado o repositório desejado, ou somente em posse do arquivo .yaml, basta digitar o código a seguir: 

~~~~
conda {nome-do-seu-ambiente} create -f environment.yml
~~~~

Após isso o ambiente desejado já estará presente no seu computador e você desejará realizar os passos do tópico 1.2 

 

#### 1.5. Excluir ambiente

 

Como tudo que é bom um dia acaba, projetos acabam, ou pelo menos deveriam, mas isso não acontece com os ambientes. Por conta disso você precisa se responsabilizar em remover estes ambientes para evitar o consumo de recursos do computador, ou somente para não transformar o seu computador em um cemitério de pacotes python. Para tal basta listar os ambientes que você tem, escolher qual deseja excluir e executar o seguinte código: 

 
~~~~
conda {nome-do-ambiente} list
conda remove --name {nome-do-ambiente} --all
~~~~
 

Após isso, seu você e seu computador estarão livres deste ambiente, assim como seu TOC por deixar as coisas organizadas, entretanto você percebera que o kernel do Jupyter Notebook criado a partir deste ambiente não terá sumido, para tal você pode executar os seguintes códigos para listar e remover o kernel desejado: 

 
~~~~
jupyter kernelspec list 
jupyter kernelspec uninstall {nome-do-kernel}
~~~~

Esse é o básico a respeito de gerenciamento de ambientes em python, mas se você precisar de alguma funcionalidade a mais pode acessar a documentação oficial do conda ou procurar no StackOverflow como todo mundo já faz. 

#### 1.6. Utilizar um ambiente nos notebooks:

~~~
Kernel > Change Kernel > <env_selecionado>
~~~

--------------

### Env

You really don't want to leak your AWS secret key or Postgres username and password on Github. Enough said — see the Twelve [Factor App principles](https://12factor.net/config) on this point. Here's one way to do this:

Store your secrets and config variables in the special file ```.env``` file in the project root folder. Thanks to the .gitignore, this file should never get committed into the version control repository. Here's an example:

```python
# example .env file
DATABASE_URL=postgres://username:password@localhost:5432/dbname
AWS_ACCESS_KEY=myaccesskey
AWS_SECRET_ACCESS_KEY=mysecretkey
OTHER_VARIABLE=something
```


***Use a package to load these variables automatically.***

You should use a package called ```python-dotenv``` to load up all the entries in this file as environment variables so they are accessible with os.environ.get. Here's an example snippet adapted from the python-dotenv documentation:

```python
import os
from dotenv import load_dotenv, find_dotenv

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables
load_dotenv(dotenv_path)

database_url = os.environ.get("DATABASE_URL")
other_variable = os.environ.get("OTHER_VARIABLE")
```

------------------

### Src

It is important to use as much logs as possible here, in order to have visibility of the process.

1. ```make_dataset.py``` is the script to download or generate data, make joins and drop features

2. ```build_features.py``` is the script to turn raw data into features for modeling, here are applied Feature Engineering functions developed by Tenbu's excelence team or others.

3. ```train_model.py``` is the script to  train models. This must contain the training of the best model and its hyperparameters, obtained in the modeling notebook. Be careful using grid search here, this may not go well in production.

4. ```predict_model.py``` is the script to  use trained models to make predictions

5. ```__init__.py``` is the Script calling functions of ```make_dataset.py```, ```build_features.py``` and ```predict_model.py```. Run to execute the entire pipeline. This will be the script called in production.


------------------

## Github conection and code versioning

### 1. Sincronizando arquivos com o GitHub 

Após a criação do ambiente para a execução do projeto, é preciso que a estrutura de pastas esteja de acordo com os padrões estabelecidos, seguindo hierarquias de diretórios e nomenclaturas de arquivos. 
Outra parte muito importante para manutenção da evolução do projeto é o versionamento. Nesse caso é utilizado o GitHub como repositório e ferramenta de versionamento do projeto. Logo, é preciso saber quais comandos e quando utilizá-los para sincronizar as pastas locais com o repositório GitHub. 

#### 1.1 Criando um repositorio no GitHub
O primeiro passo é crar um repositorio no GitHub para o projeto (pedir à pessoa controladora do GitHub Tenbu para criar)

#### 1.2. Adicionando ao GitHub 

Após a criação do repositório local do projeto, é preciso que o mesmo seja vinculado ao repositório do GitHub. Para fazer isso, é necessário abrir o terminal do servidor através do software PuTTY, entrar na pasta do projeto e executar o seguinte comando: 

~~~~
git init
~~~~

Adicionar os arquivos do repositorio local

~~~~
git add .
~~~~


#### 1.3. Commitando as alterações 

Para que as alterações realizadas nos notebooks sejam devidamente salvas, juntamente com uma breve mensagem explicativa da alteração, o seguinte comando deverá ser executado: 

~~~~
git commit –m “mensagem” 
~~~~

#### 1.4. Criando o vinculo com o GitHub

~~~~
git remote add origin <remote-repository-URL>
~~~~

Para verificar:
~~~~
git remote -v
~~~~


#### 1.5. Empurrando para o repositório 

Logo que as alterações forem salvas, os diretórios do projeto estão prontos para serem armazenados no repositório do GitHub. Para executar tal ação, é necessário rodar o seguinte comando: 

~~~~
git push -f origin master 
~~~~

#### 1.6. Pegando a versão mais atual do GitHub 

Sempre que o colaborador precisar pegar algum arquivo ou diretório do GitHub, isso podendo acontecer caso outro colaborador tenha feito alterações e salvado uma versão mais atual, é preciso sincronizar os arquivos locais com os mais atuais do repositório. Isso é feito através do seguinte comando: 

~~~~
git pull
~~~~

#### 1.7. Copiando um repositório

Caso você queira fazer uma cópia de um repositório e todo seu conteúdo para seu um outro repositório, é possível fazê-lo através do seguinte comando: 

~~~~
git clone
~~~~


```python

```
