# Sistema de Denúncia · Colégio Esperança: escopo do projeto

> Hackathon: **Bem-Estar e Saúde Mental do Jovem** (apoio emocional, combate ao cyberbullying e rotinas saudáveis)

## 1. Problema escolhido

O **cyberbullying** entre estudantes do Ensino Médio: ofensas, exposição de fotos e conversas, ameaças,
discriminação, perfis falsos e exclusão proposital em grupos.

Recorte, a partir da situação-problema do edital:

- **A vítima** se afasta das atividades e não busca ajuda por **vergonha, medo de julgamento e de exposição**.
- **Os colegas** percebem, mas **não sabem como ajudar sem aumentar a exposição**.
- **A escola** quer agir, mas **não fica sabendo** ou recebe a informação tarde e sem provas.
- Na internet, as orientações são **dispersas e contraditórias**.

## 2. Público-alvo

| Perfil | Necessidade |
|---|---|
| Estudante que sofre cyberbullying | Saber o que fazer agora e pedir ajuda sem se expor |
| Estudante que presencia | Ajudar o colega do jeito certo |
| Coordenação / orientação escolar | Receber os relatos organizados, priorizar casos de risco e responder |

## 3. Objetivo

Oferecer um canal **seguro, anônimo e orientador**, que:

1. Diga à vítima **o que fazer agora**: guardar provas, bloquear, denunciar e com quem falar.
2. Transforme quem só assiste em **alguém que apoia**.
3. Leve os casos à escola **com contexto e prioridade**, preservando a identidade de quem relata.
4. **Encaminhe para pessoas e serviços** (escola, CVV 188, 190, SaferNet), nunca substituindo profissionais.

## 4. Escopo do MVP

### Dentro do escopo

**Área do aluno (sem login)**
- Página inicial com três caminhos: *Está acontecendo comigo*, *Vi acontecer com alguém* e *Avisar a escola*.
- **Guia da vítima** em 4 passos:
  1. Acolhimento e o que não fazer.
  2. Checklist de provas.
  3. Bloquear e denunciar, com instruções por plataforma (WhatsApp, Instagram, TikTok, Discord e jogos online).
  4. Rede de apoio.
- **Guia do colega**: o que fazer e o que não fazer, com frases prontas para copiar e mandar no privado.
- **Relato**:
  - Pode ser anônimo ou identificado.
  - Campos: tipo, plataforma, quando, descrição, anexo opcional e marcação de risco.
  - No fim, o aluno recebe um **protocolo** (`ESC-XXXX-XXXX`).
- **Acompanhar relato**: o aluno digita o protocolo e vê o status e a mensagem da coordenação.
- **Sair rápido**: um botão fixo (ou `Esc` duas vezes) troca a página sem deixar o site no histórico.
- Rodapé fixo com os canais de ajuda: CVV 188, 190 e SaferNet.

**Área da coordenação (com login)**
- Painel com os relatos, com **urgentes primeiro** (ameaça ou risco marcado).
- Indicadores: relatos em aberto, urgentes, contagem por tipo e por plataforma.
- Filtro por status: *Recebida → Em análise → Em acompanhamento → Encerrada*.
- Detalhe do relato: atualizar o status, escrever uma mensagem para quem relatou e baixar a prova.
- Orientações de acolhimento na tela do caso.

**Demonstração**
- Comando `python manage.py demo`, que cria o usuário da coordenação e relatos **fictícios**.

### Fora do escopo (limites intencionais)

- ❌ Diagnóstico, triagem clínica, "teste de ansiedade" ou recomendação de tratamento.
- ❌ Monitoramento de redes sociais ou de mensagens dos alunos.
- ❌ Perfil emocional ou "score de risco" de alunos.
- ❌ Chat em tempo real e atendimento psicológico pela plataforma.
- ❌ Coleta de dados reais: toda a demonstração usa dados fictícios.

### Possíveis evoluções (pós-hackathon)

- Várias escolas, cada uma com a sua coordenação.
- Notificação por e-mail para a coordenação quando chegar um relato urgente.
- Conteúdo educativo sobre convivência digital, para uso em sala de aula.
- Relatórios agregados e anônimos por período, para ações preventivas na escola.
- Acessibilidade revisada (leitor de tela, alto contraste) e versão PWA para celular.

## 5. Privacidade, segurança e ética

| Decisão | Por quê |
|---|---|
| Aluno não precisa de login | Pedir conta afasta quem tem medo de se expor |
| Anônimo de verdade: nome e contato são descartados no servidor | Mesmo se o aluno digitar, nada fica guardado |
| Protocolo exibido uma vez e consultado por POST | Não fica na URL nem no histórico do navegador |
| Provas em pasta privada (`provas/`), download só para a coordenação logada | Evita vazamento de prints por link |
| Orientação para **não** anexar imagem íntima | Não redistribuir conteúdo sensível, nem para "provar" |
| Só aceita imagem ou PDF de até 5 MB | Reduz o risco de arquivo malicioso |
| A coordenação vê **fatos** (o quê, onde, quando), não perfis | Respeita a dignidade e evita rótulos |
| Botão "Sair rápido" | Proteção quando alguém se aproxima da tela |
| Encaminhamento para CVV, 190 e SaferNet | A tecnologia não substitui pessoas nem profissionais |

## 6. Tecnologias

| Camada | Tecnologia | Versão | Uso |
|---|---|---|---|
| Linguagem | Python | 3.14 | Back-end |
| Framework web | Django | 6.1.3 | Rotas, views, ORM, formulários, autenticação, CSRF, admin |
| Banco de dados | SQLite | embutido no Python | Persistência dos relatos (trocável por PostgreSQL em produção) |
| Front-end | HTML + Django Templates | — | Páginas renderizadas no servidor |
| Estilo | Tailwind CSS | 4.1.4 (CDN `@tailwindcss/browser`) | Utilitários de layout, espaçamento, responsividade |
| Componentes | daisyUI | 5.0.0 (CDN jsDelivr) | Cards, botões, formulários, steps, stats, tabs, alertas; tema próprio "escudo" com a paleta |
| Ícones | Bootstrap Icons (só a fonte de ícones) | 1.11.3 (CDN jsDelivr) | Ícones da interface |
| Interatividade | JavaScript (vanilla) | ES2020+ | Guia em etapas, instruções por plataforma, copiar frases e protocolo, "Sair rápido", mostrar e ocultar a identificação |
| Versionamento | Git + GitHub | — | `WhyDede09/Bem-Estar_Jovem` |

**Recursos do Django usados:** `ModelForm` com validação, `choices` no model, `LoginView` e `LogoutView`,
`staff_member_required`, `FileSystemStorage` privado, `FileResponse`, sessões, proteção CSRF e um
management command (`demo`).

## 7. Dois links

| Link | Para quem | Layout |
|---|---|---|
| `/` | Alunos (denúncia e orientação) | `aluno.html`, sem nenhum link para a coordenação |
| `/coordenacao/` | Coordenação (login) | `coord.html`, com painel e saída para o login |

Os dois rodam no mesmo servidor Django; o aluno não vê nem é direcionado à área da coordenação.

**Paleta:** marinho `#0a2fb8` / `#071f80`, ciano `#00b8e6` (fundo `#e3f8ff`), laranja `#ff8a00` (detalhe).
Definida uma vez em `base.html` (`--esc-*`) e usada tanto pelo tema daisyUI quanto pelo Tailwind.

## 8. Arquitetura

```
Navegador (Bootstrap + JS)
        │  HTTP
        ▼
Django (config/)
  └── app apoio/
        ├── models.py      → Denuncia
        ├── forms.py       → DenunciaForm (validação de anexo/anonimato), RespostaForm
        ├── views.py       → páginas do aluno + painel da coordenação
        ├── urls.py
        ├── templates/apoio/
        └── management/commands/demo.py
        │
        ├── SQLite (db.sqlite3)
        └── provas/ (anexos privados, fora do static)
```

### Modelo de dados: `Denuncia`

| Campo | Tipo | Observação |
|---|---|---|
| `protocolo` | texto único | `ESC-XXXX-XXXX`, gerado com `secrets` e sem caracteres ambíguos |
| `quem` | escolha | aconteceu comigo / vi com um colega |
| `tipo` | escolha | ofensa, exposição, ameaça, discriminação, perfil falso, exclusão, outro |
| `plataforma` | escolha | WhatsApp, Instagram, TikTok, Discord, jogo online, outra |
| `quando` | texto | opcional |
| `descricao` | texto | até 3000 caracteres |
| `prova` | arquivo | opcional, privado |
| `anonima` | booleano | padrão: sim |
| `nome`, `contato` | texto | ficam vazios se o relato for anônimo |
| `risco` | booleano | "alguém corre risco agora" |
| `status` | escolha | recebida / em análise / em acompanhamento / encerrada |
| `resposta` | texto | mensagem da coordenação para quem relatou |
| `criada`, `atualizada` | data e hora | automáticas |

**Urgente** = `risco` marcado **ou** `tipo = ameaça`.

### Rotas

| Rota | Acesso | Função |
|---|---|---|
| `/` | público | Início |
| `/guia/` | público | Guia da vítima |
| `/colega/` | público | Guia do colega |
| `/relatar/` | público | Formulário de relato |
| `/relatar/enviado/` | público (sessão) | Exibe o protocolo uma única vez |
| `/acompanhar/` | público | Consulta por protocolo |
| `/coordenacao/entrar/` | público | Login da coordenação |
| `/coordenacao/` | coordenação | Painel |
| `/coordenacao/<id>/` | coordenação | Detalhe e resposta |
| `/coordenacao/<id>/prova/` | coordenação | Download da prova |
| `/admin/` | coordenação | Admin do Django |

## 9. Como rodar

```bash
python manage.py migrate
python manage.py demo
python manage.py runserver
```

- Aluno: http://localhost:8000
- Coordenação: http://localhost:8000/coordenacao/ (`coordenacao` / `coord1234`, só para demo local)

## 10. Antes de ir para produção

- `SECRET_KEY` e `DEBUG` em variáveis de ambiente, com `DEBUG = False` e `ALLOWED_HOSTS` configurado.
- Gerar o CSS do Tailwind/daisyUI no build (CLI) em vez do CDN `@tailwindcss/browser`, que é só para desenvolvimento.
- PostgreSQL no lugar do SQLite e armazenamento privado para as provas (por exemplo, um bucket sem acesso público).
- HTTPS obrigatório.
- Política de retenção: apagar relatos encerrados e provas após um período definido com a escola.
- Termo de uso e de privacidade de acordo com a **LGPD** (dados de menores de idade).
