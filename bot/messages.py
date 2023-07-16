import code

def reg() -> str:
    return f'Вас приветствует бот мониторинга жд билетов. Выбирайте направление. Откуда: \n' 

def to() -> str:
    return f'Прибытие в город:'

def time(time_travel) -> str:
    return  f'Выберите время отправления:\n{time_travel}'

def time_none(date) -> str:
    return  f'На указанную дату: {date} рейсов нет. Пожалуйста, выберите другую'

def date() -> str:
    return  f'Выберите дату отправления:' 

def time_departure(place_of_arrival, departure_place, arrival_date, time) -> str:
    return  f'Отлично! Теперь я сообщу вам, когда появится билет {code.cities.get(departure_place)} - {code.cities.get(place_of_arrival)} на {arrival_date}: {time}' 

def ticket_is_ready(time_travel, ticket) -> str:
    return f'Билет на вашу поездку готов!\n{time_travel}\n{ticket}'

def ticket_is_ready(time_travel, ticket) -> str:
    return f'Билет на вашу поездку готов!\n{time_travel}\n{ticket}'

def cancel() -> str:
    return f'Поиск остановлен'


