# Projeto Shipay

Para as questões 2, 3, 4, 5 foi desenvolvido uma aplicação em python que possui uma API e realiza consultas no banco para retornar informações de Usuario, Obrigações e Permissões.

## Sobre o Projeto
### Explicação da arquitetura optada

O projeto foi desenvolido utilizando os princípios de Arquitetura Limpa e Arquitetura Hexagonal, onde separamos os nossos domínios, regras de negócio, casos de uso, e aplicação web em pastas seraradas. E também foi utilizado o máximo de proveitamento do conceito de POO, pois foi criado Classes Principais, e Classes Abstratas para facilitar a implementação de futuras tecnologias, como por exemplo, o repositório para salvar as informações do núcleo da aplicação foi feito em memória, e a aplicação web feita em flask apenas implementa a classe de repositório para poder salvar em um banco de dados.

A pasta "core" é responsável por separar todas as regras de negócio e de aplicação, onde cada pasta interna (user, claim, role) representa um núcleo separado, onde declaramos nosso domínio com as entidades principais, e também geramos nossos caso de uso da aplicação (cadastrar, listar, atualizar e deletar). Perceba que criado um CRUD sem a necessidade de um serviço web, pois como é apresentado na Arquitetura Hexagonal, a aplicação web chega para agregar no isstema e não para ter dentro das regras de negócio.

Portanto, a pasta "api" representa toda a aplicação web gerada, com os endpoints para cada caso de uso criado no núcleo da nossa aplicação. Que por sua vez, também foi dividida em pastas de acordo com cada domainpara seguir os conceitos de Arquitetura Hexagonal.

## Como rodar esse projeto

```bash
# clone este repositorio
git clone https://github.com/Igorcand/shipay

# Entre na pasta
cd shipay

# Rode os serviços
docker-compose up --build

```

## Testes
Esse projeto foi desenvolvido utilizando o conceito de TDD (Test Driven Desing) possuindo vários testes, dentre eles unitários, integração.

Nos testes unitários, sua intenção é testar a menor unidade do sistema, o código. E para isso é bem importante que teste a maior parte de problemas técnicos de implementação possíveis, buscando mitigar ao máximo a possibilidade de um erro de codificação

Testes de integração, nessa camada, você deve buscar executar testes que garantam a integridade com outros componentes como tabelas, arquivos e filas

### Como rodar os testes

```bash
# Com os containeres rodando, rode o comando
docker exec -it shipay_app bash

# Rode os testes
pytest

```

## API

Para melhor visualização das rotas, acesse o endpoint http://127.0.0.1:8000/apidocs para visualizar o swagger

![api](https://github.com/Igorcand/shipay/blob/master/assets/swagger.png)

# QUESTÕES # 

## 1 - Construa uma consulta SQL que retorne o nome, e-mail, a descrição do papel e as descrições das permissões/claims que um usuário possui. ##

Para realizarmos esse tipo de consulta precisamos realizar alguns joins para formar tabelas com todas as informações necessárias para a query. O primeiro join foi utilizado com o comando INNER JOIN, pois como o campo role_id é uma chave estrangeira da tabela role, temos a certeza que para cada registro de user temos um registro de role correspondente, então o INNER JOIN retorna apenas os registros que possuem correspondência em ambas as tabelas. Após isso, fazemos mais dois joins utilizando o comando LEFT JOIN, pois as permissões (claims) são itens não obrigatórios, logo o comando utilizado nos retorna todos os registros a esquerda, ou seja, todos os usuários aparecerão mesmo os que não tem permissões.

```
    SELECT 
        u.name AS user_name,
        u.email AS user_email,
        r.description AS role_description,
        c.description AS claim_description
    FROM 
        users u
    INNER JOIN 
        roles r ON u.role_id = r.id
    LEFT JOIN 
        user_claims uc ON u.id = uc.user_id
    LEFT JOIN 
        claims c ON uc.claim_id = c.id
    ORDER BY 
        u.name, c.description;

```

## 2 -  Utilizando a mesma estrutura do banco de dados da questão anterior, rescreva a consulta anterior utilizando um ORM (Object Relational Mapping) de sua preferência utilizando a query language padrão do ORM adotado(SQL Alchemy)

Para a realização dessa query, utilizando os conceitos de Arquitetura Hexagonal adotado para o projeto, foi utilizado querys en algumas tabelas para realizar o maperamento entre os objetos de User do core da aplicação e User do model. Logo abaixo tem uma pré visualização da query realizada para capturar os dados do usuário e criar o objeto User da aplicação. Pra melhor visualização acesse o arquivo src/api/user/repository.py

``` bash

def get_by_id(self, id: UUID) -> User | None:
        user_model = self.session.query(UserModel).filter_by(id=id).first()
        if user_model:
            # Filtra claims ativas associadas ao usuário
            claim_ids = {
                claim.claim_id
                for claim in (
                    self.session.query(UserClaim)
                    .join(Claim, Claim.id == UserClaim.claim_id)
                    .filter(UserClaim.user_id == id, Claim.active == True)
                    .all()
                )
            }
            return User(
                id=user_model.id,
                name=user_model.name,
                email=user_model.email,
                role_id=user_model.role_id,
                password=user_model.password,
                claim_ids=claim_ids,
            )
        return None

```

Para transformar esse objeto User no retorno esperado, foi feito o manuseio das informações no Use Case GetUser. Para melhor visualização acesse o arquivo src/src/user/application/use_cases/get_user.py

```bash

    def execute(self, input: Input):
        user = self.repository.get_by_id(input.id)
        if user is None:
            raise UserNotFound(f"User with {input.id} not found")
        
        role = self.role_repository.get_by_id(user.role_id)

        claims = self.claim_repository.list() 
        claims_descriptions = {claim.id: claim.description for claim in claims}

        return self.Output(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    role=role.description,
                    claims={claims_descriptions.get(claim_id) for claim_id in user.claim_ids }
            )

```

## 3 - Utilizando a mesma estrutura do banco de dados fornecida anteriormente, e a linguagem que desejar, construa uma API REST que irá listar o papel de um usuário pelo “Id” (role_id).
No end-point /users/<id> com o método HTTP GET, podemos visualizar as informações do usuário. Internamente, existe uma classe do domínio que se chama User, e nela existe o campo role_id que armazena um UUID relacionado a algum registro da tabela Role. E é feito a mudança para a descrição da role nos usecases de user.

![q3](https://github.com/Igorcand/shipay/blob/master/assets/get_user_route.png)

## 4 - Utilizando a mesma estrutura do banco de dados fornecida anteriormente, e a linguagem que desejar, construa uma API REST que irá criar um usuário. Os campos obrigatórios serão nome, e-mail e papel do usuário. A senha será um campo opcional, caso o usuário não informe uma senha o serviço da API deverá gerar essa senha automaticamente.
No end-point /users/ com o método HTTP POST, podemos criar um registro de usuário. Como descrito no enunciado, os campos obrigatório são nome, email e role, caso não informe algum desses dados, o erro será retornado para o usuário com o status code 400, bad request.

![q3](https://github.com/Igorcand/shipay/blob/master/assets/post_user_route.png)

O campo senha é opcional e está sendo criado no use case CreateUser. Para melhor visualização acesse o arquivo src/core/user/application/use_cases/create_user.py

```bash
    if not input.password:
        caracteres = string.ascii_letters + string.digits + string.punctuation
        input.password =  ''.join(random.choice(caracteres) for _ in range(12))

```

Para a alteração da senha do usuário é necessário realizar uma requisição para o end-point /users/<id> no método HTTP PATCH para salvar a senha enviada pelo usuário.

## 5 - Crie uma documentação que explique como executar seu projeto em ambiente local e também como deverá ser realizado o ‘deploy’ em ambiente produtivo.
O projeto utiliza sistema de containers Docker e docker-compose para facilitar a configuração e execução local, basta seguir o passo a passo a seguir.

```bash
# clone este repositorio
git clone https://github.com/Igorcand/shipay

# Entre na pasta
cd shipay

# Rode os serviços
docker-compose up --build

```

Para realizar o deploy da aplicação, foi configurado um pipeline no GitHub Action para poder fazer o deploy de forma automática. os steps configurados foram: Configuração do ambiente Docker, Build da imagem Docker, Execução dos tests, Envio da imgame Docker para o DockerHub, e Deploy para a AWS.
Para visualizar com maior detalhamento acesse o arquivo: /.github/workflows/deploy.yaml

## 6 - De acordo com o log capturado, o que pode estar originando a falha?

A falha ocorre porque a variável WALLET_X_TOKEN_MAX_AGE não está definida no ambiente de homologação. No projeto, o arquivo core.settings é responsável por configurar as variáveis de ambiente, carregando os valores definidos no arquivo .env. Isso permite que as variáveis do .env fiquem acessíveis em todo o projeto.

Como cada ambiente (desenvolvimento, homologação, produção, etc.) pode ter seu próprio arquivo .env com valores específicos, o problema está no fato de que o arquivo .env do ambiente de homologação não possui a variável WALLET_X_TOKEN_MAX_AGE configurada. Por isso, o sistema não consegue acessar esse valor, resultando no erro reportado.


## 7 - Ajude-nos fazendo o Code Review do código de um robô/rotina que exporta os dados da tabela “users” de tempos em tempos. O código foi disponibilizado no mesmo repositório do git hub dentro da pasta “bot”. ##

#### Credenciais no Código

A URL de conexão com o banco de dados contém o nome de usuário, senha e host diretamente no código. É uma boa prática utilizar variáveis de ambiente para armazenar essas informações.

```bash
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'default_value')
```

#### Validação do arquivo de config
O arquivo /tmp/bot/settings/config.ini é lido sem validação de existência. Caso ele não exista, o script falhará.

```bash
if not os.path.exists(config_file):
    app.logger.error(f"Config file not found: {config_file}")
    sys.exit(1)
```

#### Uso do task1 como Função
task1(db) está sendo chamado diretamente, ao invés de ser passado como função. Isso faz com que a tarefa seja executada imediatamente ao invés de ser agendada.


```bash
task1_instance = scheduler.add_job(task1, 'interval', id='task1_job', minutes=var1, args=[db])
```


#### Segurança no Log de Dados Sensíveis
O código imprime no console e no log os valores da coluna password da tabela users. 

```bash
print('Password: ****')
worksheet.write('D{0}'.format(index), '****')
```

#### Colocar cabeçalhos na primeira linha do Excel:
Melhorar a legibilidade ao adicionar cabeçalhos

```bash
headers = ['Id', 'Name', 'Email', 'Password', 'Role Id', 'Created At', 'Updated At']
for col_num, header in enumerate(headers):
    worksheet.write(0, col_num, header)
```

#### Tratamento de Exceções

Caso haja falha no método db.session.execute() irá quebrar o código.

```bash
try:
    orders = db.session.execute('SELECT * FROM users;')
except Exception as e:
    app.logger.error(f"Database query failed: {e}")
    return
```

A rotina principal e a tarefa não possuem tratamento de exceções. Caso haja erro, a rotina poderá falhar sem deixar muitas evidências.

```bash
def task1(db):
    try:
        # Lógica atual da exportação...
        print('job executed!')
    except Exception as e:
        logging.error(f"Task failed: {e}")

```

####  Mensagens de Log
Adicionar níveis e mensagens de log mais informativas, substituir os print() por app.logger.info() ou app.logger.error() para garantir consistência no log


## 8 - Qual ou quais Padrões de Projeto/Design Patterns você utilizaria para normalizar serviços de terceiros (tornar múltiplas interfaces de diferentes fornecedores uniforme), por exemplo serviços de disparos de e-mails, ou então disparos de SMS.

#### Adapter

O Design Pattern Adapter é ideal para traduzir a interface de um serviço de terceiros para uma interface esperada pelo sistema. Ele atua como um intermediário que adapta a interface de um fornecedor para que o sistema principal possa utilizá-la de maneira uniforme.

Para disparos de e-mails ou SMS, onde cada fornecedor possui APIs diferentes, podemos criar adaptadores que convertem os métodos específicos de cada fornecedor para um formato padronizado.

#### Strategy

O padrão Strategy permite encapsular diferentes algoritmos ou comportamentos dentro de classes distintas, selecionáveis em tempo de execução. Nesse caso, cada fornecedor seria uma estratégia que implementa a interface comum.

Para SMS ou e-mails, podemos implementar estratégias como uma estratégia padrão para cada fornecedor.

