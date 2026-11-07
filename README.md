# Escudo 🛡️

Apoio contra cyberbullying para estudantes: o que fazer agora, como ajudar um colega
e como avisar a escola **sem se identificar**. Django + JS + Bootstrap.

## Rodar

Crie e ative o ambiente virtual, depois instale as dependências:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

No Prompt de Comando, ative com `.\.venv\Scripts\activate.bat`.

Com o ambiente ativo, execute:

```bash
python manage.py migrate
python manage.py demo        # coordenação + relatos FICTÍCIOS (apaga os atuais)
python manage.py runserver
```

- Aluno: http://localhost:8000 (sem login)
- Coordenação: http://localhost:8000/coordenacao/ (`coordenacao` / `coord1234`, só para demo local)
- O comando `demo` imprime um protocolo de exemplo para testar "Acompanhar relato".

## O que tem

| Para quem | Página | O que faz |
|---|---|---|
| Vítima | `/guia/` | 4 passos: acalmar, guardar provas (checklist), bloquear/denunciar por plataforma, com quem falar |
| Colega | `/colega/` | Faça / não faça + frases prontas para copiar e mandar no privado |
| Qualquer aluno | `/relatar/` | Relato anônimo ou identificado, anexo opcional, marcação de risco → protocolo |
| Qualquer aluno | `/acompanhar/` | Status e mensagem da coordenação pelo protocolo |
| Coordenação | `/coordenacao/` | Urgentes primeiro, filtros por status, contagem por tipo e plataforma, resposta ao aluno |

## Decisões de privacidade (para o pitch)

- **Sem login para o aluno**: pedir conta afasta quem tem medo de exposição.
- **Anônimo de verdade**: no relato anônimo, nome e contato são descartados no servidor, mesmo se digitados.
- **Protocolo fora da URL**: aparece uma vez e a consulta é por POST, não fica no histórico do navegador.
- **Provas privadas**: anexos ficam em `provas/`, fora das pastas públicas; só a coordenação logada baixa.
  Imagem íntima: o sistema orienta a **não** anexar.
- **Fatos, não perfis**: a coordenação vê o que aconteceu, onde e quando, nunca um "nível emocional" do aluno.
- **Sair rápido**: botão fixo (ou `Esc` 2x) troca a página sem deixar o Escudo no "voltar".
- **Sem diagnóstico**: o Escudo orienta e encaminha (CVV 188, 190, SaferNet, escola); não substitui profissionais.

Todos os relatos de demonstração são fictícios.
