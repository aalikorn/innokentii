## Скопируйте репозиторий из Github и перейдите в новую папку 

```
git clone https://github.com/wSFhHIrfqG/InnokentiyBot.git
cd InnokentiyBot
```

## Установите и активируйте виртуальное окружение

```
python -m venv venv
venv/bin/activate
```


## Установите зависимости
```
pip install -r requirements.txt
```

## Скопируйте .env и измените переменные
```
cp .env.example .env
```

## Добавьте telegram id в SUPER_ADMINS слитно, через запятую

## Выполните команду

```
python main.py
```

## Добавьте вопросы через админ панель в боте