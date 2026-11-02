# SmartStock

Система умного складского учёта. Бэкенд на Django и Django REST Framework, авторизация через JWT, интерфейс на трёх языках: английском, русском и казахском.

## Требования

- Python 3.12+
- GNU gettext (нужен для компиляции переводов; на macOS: `brew install gettext`)
- PostgreSQL (только для prod; локально используется SQLite)

## Запуск локально

```bash
# 1. Виртуальное окружение и зависимости
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Переменные окружения
cp settings/.env.example settings/.env
# заполните settings/.env (см. ниже)

# 3. База данных и переводы
python manage.py migrate
python manage.py compilemessages --ignore=venv

# 4. Администратор и запуск
python manage.py createsuperuser
python manage.py runserver
```

После запуска доступны:

- админка: `http://127.0.0.1:8000/<SMARTSTOCK_ADMIN_SITE_URL>`
- Swagger: http://127.0.0.1:8000/api/docs/swagger/
- ReDoc: http://127.0.0.1:8000/api/docs/redoc/

## Переменные окружения

Файл `settings/.env`:

| Переменная | Описание |
|---|---|
| `SMARTSTOCK_ENV_ID` | `local` или `prod` — какой файл настроек из `settings/env/` использовать |
| `SMARTSTOCK_SECRET_KEY` | секретный ключ Django |
| `SMARTSTOCK_ADMIN_SITE_URL` | путь к админке, например `admin/` (со слэшем в конце) |
| `SMARTSTOCK_DB_*` | параметры PostgreSQL (только для `prod`) |
| `SMARTSTOCK_ALLOWED_HOSTS` | домены через запятую (только для `prod`) |
| `SMARTSTOCK_CSRF_TRUSTED_ORIGINS` | адреса с протоколом через запятую, например `https://example.com` (только для `prod`) |

Для `local` переменные `SMARTSTOCK_DB_*`, `SMARTSTOCK_ALLOWED_HOSTS` и `SMARTSTOCK_CSRF_TRUSTED_ORIGINS` можно оставить пустыми.

Сгенерировать секретный ключ:

```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

## Переводы

Скомпилированные файлы `.mo` не хранятся в репозитории, поэтому после клонирования и при каждом деплое нужно выполнить `compilemessages`.

Чтобы добавить новые строки в перевод:

```bash
python manage.py makemessages -l ru -l kk --ignore=venv
# заполните msgstr в locale/<язык>/LC_MESSAGES/django.po
python manage.py compilemessages --ignore=venv
```

Язык ответа API выбирается по заголовку `Accept-Language` (`en`, `ru`, `kk`).

## Структура проекта

```
apps/
  abstracts/   общая абстрактная модель (created_at, updated_at)
  users/       кастомная модель пользователя (вход по email)
settings/
  conf.py      переменные окружения, DRF, JWT, OpenAPI
  base.py      общие настройки Django
  env/         local.py и prod.py
locale/        переводы на ru и kk
```

## Лицензия

MIT — см. [LICENSE](LICENSE).
