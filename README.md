Настройки config.py:

| Переменная         | Описание             |
| :-------------:    |:--------------------:|
| PATH_TO_EXCEL_FILE | путь к файлу для чтения |
| PATH_TO_SAVE       | путь к файлу для сохранения |
| STOPWORDS          | стопслова            |

Пример переменных в config.py:
```
    PATH_TO_EXCEL_FILE = 'excel/Toloka.xlsx'

    PATH_TO_SAVE = 'excel/result.xlsx'

    STOPWORDS = ['адрес', 'район', 'метро', 'ул', 'требуется', 'ищу', 'рассмотрю']
```

Запуск (*nix):
1. git clone https://github.com/a-fenk/toloka_reviews_validator.git
2. cd toloka_reviews_validator
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirements.txt
6. python run.py