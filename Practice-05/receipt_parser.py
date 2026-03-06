import re
import json

def parse_receipt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return "Файл не найден"

    # 1. Поиск даты и времени (формат 18.04.2019 11:13:58)
    dt_match = re.search(r'(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})', content)
    date = dt_match.group(1) if dt_match else "Не найдена"
    time = dt_match.group(2) if dt_match else "Не найдено"

    # 2. Поиск Итоговой суммы (ищем число после слова ИТОГО:)
    # Находим строку "ИТОГО:", переходим на следующую и берем число
    total_match = re.search(r'ИТОГО:\s*([\d\s,.]+)', content)
    total = total_match.group(1).replace(' ', '').replace(',', '.') if total_match else "0.00"

    # 3. Поиск товаров
    # Логика: число с точкой (номер пункта), потом название товара до следующей строки с ценой
    # Паттерн ищет: "1.", "2." и захватывает текст до строки с умножением "x"
    product_pattern = r'\d+\.\n(.*?)\n\d+,\d+\s+x'
    products = re.findall(product_pattern, content, re.DOTALL)
    # Очистка названий от лишних пробелов и переносов
    products = [p.strip().replace('\n', ' ') for p in products]

    # 4. Способ оплаты
    payment_pattern = r'(Банковская карта|Наличные|Каспи|Card|Cash)'
    pay_match = re.search(payment_pattern, content, re.IGNORECASE)
    payment_method = pay_match.group(0) if pay_match else "Не указан"

    # Формируем структуру
    data = {
        "чек_инфо": {
            "дата": date,
            "время": time,
            "организация": "EUROPHARMA Астана"
        },
        "товары": products,
        "сумма_к_оплате": f"{total} тг",
        "метод_оплаты": payment_method
    }
    return data

# Вывод результата
result = parse_receipt("raw.txt")

print("\n" + "="*50)
print("             ОБРАБОТАННЫЙ ЧЕК")
print("="*50)
print(json.dumps(result, indent=4, ensure_ascii=False))
print("="*50)