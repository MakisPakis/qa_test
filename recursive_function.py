import json


def find_companies(data, result=None):
    if result is None:
        result = []

    if isinstance(data, dict):
        if 'title' in data and 'id' in data:
            result.append((data['title'], data['id']))
        for value in data.values():
            find_companies(value, result)
    elif isinstance(data, list):
        for item in data:
            find_companies(item, result)

    return result


# Чтение данных из JSON-файла
with open('new_test_hw.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Поиск всех названий компании и их id
companies = find_companies(data)

# Вывод результатов
for company in companies:
    print(company)