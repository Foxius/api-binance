# api-binance

[![GitHub issues](https://img.shields.io/github/issues/foxius/api-binance?style=plastic)](https://github.com/foxius/api-binance/issues) [![GitHub stars](https://img.shields.io/github/stars/foxius/api-binance)](https://github.com/foxius/api-binance/stargazers) [![GitHub forks](https://img.shields.io/github/forks/foxius/api-binance)](https://github.com/foxius/api-binance/network)


Данный репозиторий содержит код для создания бота, который работает с Binance API и обрабатывает информацию о позициях и маржинальных требованиях на Binance Futures. Бот также использует Google Sheets API для сохранения данных и Telegram API для отправки уведомлений.

## Запуск

Для запуска бота выполните команду:

```
python3 api.py
```

Перед запуском необходимо настроить файл `config.py`, предоставив следующие данные:

```python
# Binance API
api_key = "ваш_api_key"
api_secret = "ваш_api_secret"

# Telegram
RECIPIENT_ID = ваш_id_получателя
bot_token = "ваш_токен"

# Другие настройки
symbols = {'ETHUSDT', 'BTCUSDT', 'BNBUSDT'} # список торговых пар
ratiolimit = 0.0 # лимит для отслеживания Margin Ratio
sheet_id = 'идентификатор_гугл_таблицы' # ID Google Sheets таблицы
```

## Функционал

Бот выполняет следующие действия:

- Получает информацию о позициях и маржинальных требованиях с Binance Futures.
- Обновляет данные в Google Sheets таблице для дальнейшего анализа.
- Отправляет уведомления через Telegram, если Margin Ratio превышает установленный лимит.

## Зависимости

Для корректной работы бота необходимо установить следующие зависимости:

- Python 3
- Библиотеки: requests, gspread, telebot, schedule

Установка библиотек:

```
pip install requests gspread telebot schedule
```

## Поддержка и контакты

По всем вопросам и предложениям можно связаться с автором репозитория:

- Автор: [foxius](https://github.com/foxius)

## Отказ от ответственности

Использование данного бота может повлечь финансовые риски. Автор не несет ответственности за возможные убытки или ущерб, связанные с использованием этого кода.

**Используйте бота на свой страх и риск.**
