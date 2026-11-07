# Sistema de Denúncia · Colégio Esperança 🛡️

Aplicação de apoio contra cyberbullying. Estudantes podem consultar
orientações, apoiar um colega e enviar um relato à escola. A coordenação pode
acompanhar os relatos e responder.

O projeto usa Python, Django, SQLite, JavaScript, Tailwind CSS, daisyUI e
Jazzmin. As instruções abaixo são para executar o projeto localmente durante o
desenvolvimento.

## 1. O que instalar antes de começar

Instale o **Python** (versão compatível com Django 6.1) e, se for clonar o
projeto pela internet, o **Git**. Durante a instalação do Python no Windows,
marque a opção para adicioná-lo ao PATH, se ela aparecer.

Abra um terminal e verifique se o Python está instalado:

### Windows — PowerShell

```powershell
py --version
```

### macOS ou Linux

```bash
python3 --version
```

O terminal deve mostrar a versão do Python. Se disser que o comando não foi
encontrado, instale o Python ou corrija o PATH antes de continuar.

O Git é necessário somente para baixar o código usando `git clone`. Se a pasta
do projeto já foi recebida por outro meio, pule a verificação e a etapa de
clonagem.

Para verificar se o Git está disponível:

```bash
git --version
```

## 2. Baixar o projeto e abrir a pasta correta

Há duas opções:

### Opção A — o projeto já está no computador

Abra o terminal e use `cd` para entrar na pasta do projeto. Entre na pasta que
contém o arquivo `manage.py` e a pasta `config`.

Exemplo no Windows (troque o caminho pelo local em que salvou o projeto):

```powershell
cd C:\caminho\para\Bem-Estar_Jovem
```

Exemplo no macOS ou Linux:

```bash
cd /caminho/para/Bem-Estar_Jovem
```

Confira se está na pasta certa:

```bash
python manage.py --help
```

No Windows, se `python` não for reconhecido, tente:

```powershell
py manage.py --help
```

Se aparecer a lista de comandos do Django, você está no diretório correto. Se
aparecer um erro dizendo que `manage.py` não foi encontrado, use `cd` para
entrar na pasta certa antes de continuar.

### Opção B — clonar com Git

Peça o endereço Git do repositório à pessoa que compartilhou o projeto. No
comando abaixo, substitua `<URL_DO_REPOSITORIO>` pelo endereço recebido,
removendo os sinais `<` e `>`.

```bash
git clone <URL_DO_REPOSITORIO>
```

Entre na pasta criada pelo Git (o nome costuma ser o nome do repositório):

```bash
cd Bem-Estar_Jovem
```

Confirme que `manage.py` está nessa pasta:

```bash
python manage.py --help
```

No Windows, se necessário, use `py` no lugar de `python`:

```powershell
py manage.py --help
```

## 3. Criar um ambiente virtual

Um ambiente virtual mantém as bibliotecas deste projeto separadas das de outros
projetos Python. Execute o comando correspondente ao seu sistema **na pasta
que contém `manage.py`**.

### Windows — PowerShell

```powershell
py -m venv .venv
```

Esse comando cria a pasta `.venv` com um ambiente Python isolado.

### macOS ou Linux

```bash
python3 -m venv .venv
```

Esse comando também cria a pasta `.venv`.

## 4. Ativar o ambiente virtual

Ative o ambiente no terminal em que vai instalar as dependências e executar o
servidor.

### Windows — PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Quando estiver ativo, o terminal normalmente mostrará `(.venv)` no início da
linha de comando.

Se o PowerShell bloquear a execução do script de ativação, não é necessário
alterar a política de segurança do computador. Abra o **Prompt de Comando
(cmd.exe)**, entre novamente na pasta do projeto e execute:

```bat
.\.venv\Scripts\activate.bat
```

### macOS ou Linux

```bash
source .venv/bin/activate
```

Para sair do ambiente virtual mais tarde, execute `deactivate`. Será necessário
ativá-lo novamente sempre que abrir um terminal novo para trabalhar no projeto.

## 5. Instalar as dependências do projeto

Com o ambiente virtual ativo, execute:

```bash
python -m pip install -r requirements.txt
```

O comando lê `requirements.txt` e instala as bibliotecas necessárias, incluindo
Django e Jazzmin. Aguarde até que o processo termine sem erros antes de seguir.

## 6. Criar o banco de dados local

Ainda na pasta que contém `manage.py` e com o ambiente virtual ativo, execute:

```bash
python manage.py migrate
```

Esse comando aplica as migrações do Django e cria o banco de dados SQLite
(`db.sqlite3`) neste computador. Cada pessoa que executar o projeto terá seu
próprio banco local.

## 7. Iniciar o site

Execute:

```bash
python manage.py runserver
```

O servidor fica em execução nesse terminal. Mantenha-o aberto enquanto usa o
site e acesse <http://127.0.0.1:8000/> no navegador. Para encerrar o servidor,
volte ao terminal e pressione `Ctrl+C`.

Se a porta 8000 já estiver ocupada, inicie o servidor em outra porta:

```bash
python manage.py runserver 8001
```

Nesse caso, acesse <http://127.0.0.1:8001/>.

## 8. Entrar na área da coordenação

Para experimentar o site com relatos fictícios, abra **outro terminal** na
pasta do projeto, ative o ambiente virtual nesse terminal e execute:

```bash
python manage.py demo
```

O comando cria uma conta de demonstração e relatos fictícios. No final, imprime
um protocolo para testar a consulta de relatos. Acesse
<http://127.0.0.1:8000/coordenacao/> e use:

- **Usuário:** `coordenacao`
- **Senha:** `coord1234`

> **Atenção:** o comando `demo` apaga os relatos que já existem no banco local
> antes de criar os exemplos. Use-o somente em um banco de demonstração, nunca
> se houver dados que deseja manter. A senha fixa é somente para demonstração;
> não a utilize em produção.

### Criar um usuário da coordenação pelo admin do Django

Para criar uma conta de coordenação sem usar os dados fictícios, primeiro
precisa existir uma conta administradora do Django. Se ainda não criou uma,
faça isso no terminal, com o ambiente virtual ativado:

```bash
python manage.py createsuperuser
```

Responda às perguntas para definir o usuário, o e-mail e a senha do
administrador. Com o servidor iniciado, abra <http://127.0.0.1:8000/admin/> e
entre com essa conta.

No admin do Django:

1. Abra **Usuários** e clique em **Adicionar usuário**.
2. Informe o nome de usuário e a senha.
3. Marque **Acesso à equipe** (`is_staff`) no formulário e salve. Esse campo é
   necessário para entrar na tela da coordenação.
4. Acesse <http://127.0.0.1:8000/coordenacao/> e entre com o usuário e a senha
   que acabou de criar.

Se o usuário já existir, abra o cadastro dele em **Usuários**, marque
**Acesso à equipe** e salve.

Não é necessário marcar **Superusuário** para a conta da coordenação. Essa
opção concede permissões administrativas amplas; mantenha-a desmarcada, a
menos que a pessoa também precise administrar todo o sistema.

O superusuário criado com `createsuperuser` pode entrar no admin e na tela da
coordenação. Use-o para gerenciar usuários, e não como conta diária da equipe,
quando possível.

## 9. Executar os testes

Com o ambiente virtual ativo, execute:

```bash
python manage.py test
```

O Django executa os testes do projeto e mostra no terminal se passaram ou se
algum deles falhou.

## Problemas comuns

### `python` ou `py` não é reconhecido

Confirme que o Python foi instalado. No Windows, tente `py`; no macOS ou Linux,
tente `python3`. Se acabou de instalar, feche e abra o terminal para atualizar
o PATH.

### `No module named django`

Ative o ambiente virtual e instale as dependências:

```bash
python -m pip install -r requirements.txt
```

### `can't open file 'manage.py'`

O terminal está na pasta errada. Use `cd` para entrar na pasta do projeto que
contém `manage.py`.

### Não consigo acessar o site

Confira se `runserver` continua rodando no terminal e se está usando o mesmo
endereço e porta informados pelo Django. Se iniciou com a porta 8001, por
exemplo, acesse <http://127.0.0.1:8001/>.

## Páginas do projeto

| Para quem | Endereço | O que faz |
|---|---|---|
| Estudantes | `/guia/` | Orientações e passos para buscar ajuda |
| Colegas | `/colega/` | Como apoiar e frases para iniciar uma conversa |
| Qualquer aluno | `/relatar/` | Envio de relato anônimo ou identificado, com anexo opcional |
| Qualquer aluno | `/acompanhar/` | Consulta do status e da resposta pelo protocolo |
| Coordenação | `/coordenacao/` | Triagem, filtros e resposta aos relatos |
| Administrador | `/admin/` | Administração do Django com Jazzmin |

## Privacidade e uso

- Alunos podem enviar relatos sem criar uma conta.
- Em relatos anônimos, nome e contato são descartados no servidor.
- O protocolo é consultado por envio de formulário, sem ser colocado na URL.
- Os anexos ficam fora das pastas públicas e só a coordenação autenticada pode
  baixá-los.
- O sistema oferece orientação e encaminhamento; não substitui profissionais.
- Os relatos criados pelo comando `demo` são fictícios.

`runserver` e as configurações atuais são para desenvolvimento local, não para
publicar o sistema em produção.
