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
Esse projeto foi desenvolvido utilizando o conceito de TDD (Test Driven Desing) possuindo vários testes, dentre eles unitários, integração e end-to-end. 

Nos testes unitários, sua intenção é testar a menor unidade do sistema, o código. E para isso é bem importante que teste a maior parte de problemas técnicos de implementação possíveis, buscando mitigar ao máximo a possibilidade de um erro de codificação

Testes de integração, nessa camada, você deve buscar executar testes que garantam a integridade com outros componentes como tabelas, arquivos e filas

Já os testes End to End devem buscar testar sua aplicação de ponta a ponta, com um resultado funcional observável. Neste momento a ideia é testar o sistema da forma mais próxima do ambiente produtivo.

### Como rodar os testes

```bash
# Com os containeres rodando, rode o comando
docker exec -it app bash

# Rode os testes
pytest

```

## API

Para melhor visualização das rotas, acesse o endpoint http://127.0.0.1:8000/ para visualizar o swagger

# QUESTÕES # 

## 1 - Construa uma consulta SQL que retorne o nome, e-mail, a descrição do papel e as descrições das permissões/claims que um usuário possui. ##

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

