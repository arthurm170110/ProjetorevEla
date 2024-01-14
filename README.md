# ProjetorevEla

    A covid-19 foi uma das maiores pandemias da história recente da humanidade causada
pelo novo coronavírus (SARS-CoV-2). Trata-se de uma infecção respiratória aguda
potencialmente grave e de distribuição global, que possui elevada transmissibilidade
entre as pessoas por meio de gotículas respiratórias ou contato com objetos e superfícies
contaminadas.

    Desde o primeiro caso (em 31 de dezembro de 2019) até 21 de dezembro de 2023, foram
registrados 699,9 milhões de casos e 6,91 milhões de óbitos no mundo. No Brasil, são
38,1 milhões de casos e mais de 708 mil óbitos no mesmo período.

    Neste contexto, temos como principal problemática a obtenção de candidatos para uma
pesquisa que visa a avaliação de novos testes da covid-19 de um centro clínico,
mantendo os gestores atualizados em tempo real do progresso da obtenção de
candidatos aos testes, com indicadores relacionados à gestão. Os candidatos entram em
um processo de triagem, podendo ocorrer desdobramentos que os permitem seguir com
o agendamento da testagem ou não. É importante que os candidatos aptos tenham como
identificar os locais disponíveis em seu território para realização do estudo clínico para o
novo teste de detecção da covid-19: LAIS-010.

    Diante disso, o projeto tem como objetivo propor uma solução para agendamento online
para triagem de pessoas candidatas a um novo tipo de teste para detecção da covid-19 e
suas variantes, por meio de uma página interna com dados dos perfis das pessoas que
se candidataram por faixa etária, por município e por antecedentes da doença.

### Link - base

https://lais.huol.ufrn.br/wp-content/uploads/2023/12/Edital_028.2023-OrientaA%C2%A7A%C2%B5es-para-a-Fase-2.pdf

### Arquitetura

* Linguagem: Python
* Framework: Django

### 📋 Pré-requisitos

Para instalação do software é necessário:
* Python 3.10.8
* Django 5.0.1

### 🔧 Instalação

1. Clone o repositório:
```
git clone https://github.com/arthurm170110/ProjetorevEla.git
```

2. Crie um ambiente virtual:
```
python -m venv venv
```

3. Ative o ambiente virtual:
    3.1 Para Windows:
    ```
    venv/Scripts/activate
    ```
    3.2 Para Mac e Linux:
    ```
    source venv/bin/activate
    ```

4. Instale as dependências:
```
pip install -r requirements.txt
```

5. Execute as migrações:
```
python manage.py makemigrations
```
```
python manage.py migrate
```

6. Execute o servidor:
```
python manage.py runserver
```