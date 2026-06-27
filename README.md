# Eventos SaaS v6

Melhorias desta versão:
- configuração por evento do modo do QR Code do crachá;
- três opções: salvar contato, check-in, ou contato + check-in;
- uso do mesmo QR Code para as duas finalidades no modo combinado, pensando em etiqueta pequena;
- tela inicial de check-in para validar QR lido por scanner;
- indicação visual do modo atual do QR em branding, painel e etiqueta.

## Modos do QR Code

- `Salvar contato`: gera vCard com nome, telefone, e-mail, empresa e cargo.
- `Check-in`: gera payload técnico de check-in para leitura operacional.
- `Contato + check-in`: combina os dois conteúdos no mesmo QR Code. É a opção mais compacta para etiquetas pequenas, mas o comportamento pode variar conforme o leitor do QR.

## Atualização

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Recomendação prática

Para eventos onde o principal é operação de entrada, use `Check-in`.
Para networking/comercial, use `Salvar contato`.
Para uso misto e etiqueta pequena, teste `Contato + check-in` com os celulares e leitores que sua equipe realmente usará no evento.


## Correção incluída na v6.1

Foi corrigido explicitamente o erro de sintaxe em `core/views.py` na função `registration_vcard`, substituindo a string multilinha quebrada por montagem segura com lista de linhas e `\n`.


## Ajustes da v6.2

- botão para voltar ao painel da organização nas telas do evento;
- botão de logout no painel da organização;
- participante já cadastrado agora pode se inscrever em outro evento sem erro, reutilizando o cadastro;
- QR Code do modo combinado volta a priorizar vCard limpo para preservar salvamento de contato.


## Ajustes da v6.3

- logout funcional por POST com tela `registration/logged_out.html`;
- `core/views.py` refeito para eliminar strings quebradas recorrentes;
- garantia do campo `qr_mode` no model `Event`;
- hotpage pública exibindo local, início e fim do evento;
- e-mail e páginas públicas usando datas formatadas;
- modo combinado do QR segue priorizando vCard limpo para salvar contato.


## Ajustes da v6.4

- primeira integração prática do template do Google Stitch na hotpage pública;
- hero escuro com banner dinâmico, quick info bar, cards, blocos de destaque e CTA final;
- conteúdo ligado às variáveis reais do evento no Django;
- pronto para próxima rodada com inscrição pública e painel administrativo no mesmo padrão visual.


## Ajustes da v6.5

- integração do template de inscrição pública inspirado no Stitch;
- correção preventiva em `core/views.py` para evitar quebra por joins de string;
- reforço do campo `qr_mode` no model `Event`;
- formulário público alinhado ao novo padrão visual da hotpage.


## Ajustes da v6.6

- nova rodada visual com painel da organização no padrão enviado;
- nova lista de participantes no padrão enviado;
- ajuste textual no `views.py` para o trecho `text_body = "\n".join([` indicado pelo usuário;
- mantida a linha `qr_mode` no model `Event`.


## Ajustes da v6.7

- correção do dashboard principal para usar apenas rotas existentes em `badge_project/urls.py`;
- remoção de links para páginas não implementadas que causavam redirecionamento/erro;
- criação do template `core/event_participants.html` como alias visual da nova lista de participantes.


## Ajustes da v6.8

- correção estrutural do `core/base.html` para usar `{% block content %}` em vez de `{{ content|safe }}`;
- links Início, Painel e Sair agora usam `{% url %}` corretamente;
- login ajustado para postar em `{% url 'login' %}` e respeitar `next`;
- `LOGOUT_REDIRECT_URL = '/'` adicionado nas settings.


## Ajustes da v6.9

- correção definitiva do erro `Unknown field(s) (qr_mode) specified for Event`;
- campo `qr_mode` adicionado novamente ao model `Event`;
- migration `core/migrations/0002_event_qr_mode.py` incluída;
- após atualizar os arquivos, executar `python manage.py makemigrations` somente se necessário e depois `python manage.py migrate`.


## Ajustes da v6.10

- removida migration duplicada `0002_event_qr_mode.py`;
- mantido o campo `qr_mode` no `core/models.py`;
- a linha de migração correta segue a cadeia já existente do projeto, evitando `multiple leaf nodes`.


## Ajustes da v6.11

- removida a navegação superior quando o usuário está autenticado;
- botão sair da barra lateral do dashboard e participantes agora envia POST para `logout`;
- template `event_participants.html` corrigido para usar apenas rotas existentes (`event_participants`, `event_checkin`, `event_branding`, `event_detail`, `export_event_csv`, `export_event_xlsx`, `registration_admin`, `print_badge`);
- layouts internos dashboard e participantes alinhados ao visual novo.


## Ajustes da v6.12

- login atualizado para o padrão visual novo;
- dashboard reformulado com topbar, seletor de evento, notificações e iniciais do usuário, além de cards e sessões por evento;
- menu lateral do dashboard com espaçamento ajustado e sem botão `Visão do evento`;
- check-in refeito em layout mobile-first;
- branding refeito no layout novo com preview lateral inspirado no arquivo anexado.
