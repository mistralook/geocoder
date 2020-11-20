## Geocoder v0.01

Автор задачи: Львов Ярослав ФТ-201.

# Запуск:
    python main.py

## Описание:
	В теории тут должен быть геокодер. Пока что есть только парсер.
	
## Состав:
    Основная логика: main.py
    Тесты: tests/
    Необходимые функции: /utils
    База OSM: NORMAL-DB.osm
    Рабочая SQL база: parsed_data.db

## Тесты:
	Присутствуют в tests/
	Coverage: 0

## Подробности:
    Скачивается база OSM по Великобритании.
    Запускается парсер, преобразующий неудобный формат базы в удобный(sql).
    Используется геокодер по полученной после парсера SQL
    ...

