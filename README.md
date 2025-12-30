# Aplicação Django (simples)

Instruções rápidas para configurar e executar o projeto localmente (Windows).

## Pré-requisitos

- Python 3.10+ instalado
- Node.js (opcional, para desenvolvimento do Tailwind se estiver usando o `tailwind` app)

## Passos (rápido)

1. Abra um terminal na pasta que contém o arquivo `manage.py` (ex: `app` dentro deste repositório).

2. Crie e ative um ambiente virtual:

```powershell
python -m venv venv
venv\Scripts\activate
```

3. Instale dependências (se existir `requirements.txt`):

```powershell
pip install -r requirements.txt
# ou, caso não haja requirements, instale Django e django-tailwind manualmente
pip install django django-tailwind
```

4. Aplique migrações e crie um superuser:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

5. Build do Tailwind (gerar `styles.css`) — em desenvolvimento use o watch, em produção faça o build:

```powershell
# modo desenvolvimento (recompila automaticamente)
python manage.py tailwind start

# ou apenas gerar o CSS final uma vez
python manage.py tailwind build
```

6. Rode o servidor local:

```powershell
python manage.py runserver
# Acesse http://127.0.0.1:8000/
```

## Observações

- Templates importantes:
  - `core/templates/core/index.html` — página inicial
  - `core/templates/registration/login.html` — tela de login
  - `templates/includes/header.html` e `templates/includes/footer.html` — header/footer globais

- O CSS gerado pelo Tailwind fica em `theme/static/css/dist/styles.css` e os templates referenciam `{% static 'css/dist/styles.css' %}`.
- Para ambiente de produção rode `python manage.py collectstatic` e sirva os arquivos estáticos com seu servidor.

## Dúvidas / próximos passos

- Posso adicionar um `requirements.txt` com versões fixas, tornar as seções estáticas em modelos dinâmicos (models + admin), ou converter templates para herdar de um `base.html`. Quer que eu faça algum desses?
