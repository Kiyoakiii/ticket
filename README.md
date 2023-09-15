# 🚂🎟Train ticket monitoring in Russia

Этот телеграм-бот позволяет пользователю экономить своё время на мониторинге билетов на поезд.

## 🤔💡Идея создания

Поскольку мой родной дом находится в туристическом городе в тысяче километров от места учебы, а самолеты туда не летают, приходится покупать билет на поезд за пол года. Но это бессмысленно так как планы меняются. И хотелось бы купить билет за неделю или день до отправления.

Была выявлена лазейка. Билет можно сдать (онлайн) вплоть до дня отправления без потери денег. Люди сдают свои билеты и они сразу появляются на сайте. Я решил воспользоваться этой фичей и написал телеграмм-бота который проверяет наличие билетов за вас. Бот просто пришлет уведомление и ссылку, где вы сможете купить себе билет. Главное успеть!!!

Этот бот уже помог многим людям уехать за день два до отправления. 

## 🔍📝Основные функции

- Выбор места отправления и прибытия
- Выбор даты поездки
- Выбор времени поездки
- Выбор типа места (нижнее, верхнее или любое)
- Отмена операции с помощью команды `/cancel`

## 🔧👥Использование

1. Запустите бота с помощью команды `/start`.
2. Следуйте инструкциям бота, чтобы выбрать место отправления, место прибытия, дату и время поездки, а также тип места.
3. Если вы хотите отменить операцию, используйте команду `/cancel`.

## Требования

Для работы бота необходимо установить следующие библиотеки:

- aiogram
- asyncio
- selenium + WebDriver

## Конфигурация

Перед запуском бота необходимо указать токен API в файле `config.py`.

```python
BOT_API_TOKEN = 'YOUR_API_TOKEN_HERE'
```

