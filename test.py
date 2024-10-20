import requests
import json
from requests import post, get

'''products = [
    {"id": 1, "name": "Яблоки", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/apples.jpg"},
    {"id": 2, "name": "Бананы", "freshness_duration": 864000000, "category_id": 1, "image": "https://example.com/images/bananas.jpg"},
    {"id": 3, "name": "Клубника", "freshness_duration": 259200000, "category_id": 1, "image": "https://example.com/images/strawberries.jpg"},
    {"id": 4, "name": "Молоко", "freshness_duration": 120960000, "category_id": 2, "image": "https://example.com/images/milk.jpg"},
    {"id": 5, "name": "Хлеб", "freshness_duration": 43200000, "category_id": 3, "image": "https://example.com/images/bread.jpg"},
    {"id": 6, "name": "Яйца", "freshness_duration": 259200000, "category_id": 2, "image": "https://example.com/images/eggs.jpg"},
    {"id": 7, "name": "Куриное филе", "freshness_duration": 43200000, "category_id": 2, "image": "https://example.com/images/chicken_breast.jpg"},
    {"id": 8, "name": "Говядина", "freshness_duration": 259200000, "category_id": 2, "image": "https://example.com/images/beef.jpg"},
    {"id": 9, "name": "Свинина", "freshness_duration": 259200000, "category_id": 2, "image": "https://example.com/images/pork.jpg"},
    {"id": 10, "name": "Сыр", "freshness_duration": 604800000, "category_id": 2, "image": "https://example.com/images/cheese.jpg"},
    {"id": 11, "name": "Огурцы", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/cucumbers.jpg"},
    {"id": 12, "name": "Помидоры", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/tomatoes.jpg"},
    {"id": 13, "name": "Морковь", "freshness_duration": 259200000, "category_id": 1, "image": "https://example.com/images/carrots.jpg"},
    {"id": 14, "name": "Картофель", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/potatoes.jpg"},
    {"id": 15, "name": "Лук", "freshness_duration": 259200000, "category_id": 1, "image": "https://example.com/images/onions.jpg"},
    {"id": 16, "name": "Чеснок", "freshness_duration": 259200000, "category_id": 1, "image": "https://example.com/images/garlic.jpg"},
    {"id": 17, "name": "Перец", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/peppers.jpg"},
    {"id": 18, "name": "Брокколи", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/broccoli.jpg"},
    {"id": 19, "name": "Цукини", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/zucchini.jpg"},
    {"id": 20, "name": "Капуста", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/cabbage.jpg"},
    {"id": 21, "name": "Грибы", "freshness_duration": 259200000, "category_id": 1, "image": "https://example.com/images/mushrooms.jpg"},
    {"id": 22, "name": "Мед", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/honey.jpg"},
    {"id": 23, "name": "Орехи", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/nuts.jpg"},
    {"id": 24, "name": "Овсянка", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/oatmeal.jpg"},
    {"id": 25, "name": "Рис", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/rice.jpg"},
    {"id": 26, "name": "Макароны", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/pasta.jpg"},
    {"id": 27, "name": "Соль", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/salt.jpg"},
    {"id": 28, "name": "Сахар", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/sugar.jpg"},
    {"id": 29, "name": "Кофе", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/coffee.jpg"},
    {"id": 30, "name": "Чай", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/tea.jpg"},
    {"id": 31, "name": "Сок апельсиновый", "freshness_duration": 259200000, "category_id": 5, "image": "https://example.com/images/orange_juice.jpg"},
    {"id": 32, "name": "Сок яблочный", "freshness_duration": 259200000, "category_id": 5, "image": "https://example.com/images/apple_juice.jpg"},
    {"id": 33, "name": "Кетчуп", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/ketchup.jpg"},
    {"id": 34, "name": "Майонез", "freshness_duration": 259200000, "category_id": 4, "image": "https://example.com/images/mayonnaise.jpg"},
    {"id": 35, "name": "Горчица", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/mustard.jpg"},
    {"id": 36, "name": "Соевый соус", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/soy_sauce.jpg"},
    {"id": 37, "name": "Приправы", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/spices.jpg"},
    {"id": 38, "name": "Чипсы", "freshness_duration": 259200000, "category_id": 4, "image": "https://example.com/images/chips.jpg"},
    {"id": 39, "name": "Шоколад", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/chocolate.jpg"},
    {"id": 40, "name": "Конфеты", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/candies.jpg"},
    {"id": 41, "name": "Замороженные овощи", "freshness_duration": 31536000000, "category_id": 1, "image": "https://example.com/images/frozen_vegetables.jpg"},
    {"id": 42, "name": "Замороженные фрукты", "freshness_duration": 31536000000, "category_id": 1, "image": "https://example.com/images/frozen_fruits.jpg"},
    {"id": 43, "name": "Замороженное мясо", "freshness_duration": 31536000000, "category_id": 2, "image": "https://example.com/images/frozen_meat.jpg"},
    {"id": 44, "name": "Замороженная рыба", "freshness_duration": 31536000000, "category_id": 2, "image": "https://example.com/images/frozen_fish.jpg"},
    {"id": 45, "name": "Творог", "freshness_duration": 604800000, "category_id": 2, "image": "https://example.com/images/cottage_cheese.jpg"},
    {"id": 46, "name": "Йогурт", "freshness_duration": 259200000, "category_id": 2, "image": "https://example.com/images/yogurt.jpg"},
    {"id": 47, "name": "Кефир", "freshness_duration": 120960000, "category_id": 2, "image": "https://example.com/images/kefir.jpg"},
    {"id": 48, "name": "Сметана", "freshness_duration": 259200000, "category_id": 2, "image": "https://example.com/images/sour_cream.jpg"},
    {"id": 49, "name": "Пицца", "freshness_duration": 86400000, "category_id": 3, "image": "https://example.com/images/pizza.jpg"},
    {"id": 50, "name": "Сосиски", "freshness_duration": 43200000, "category_id": 2, "image": "https://example.com/images/sausages.jpg"},
    {"id": 51, "name": "Батон", "freshness_duration": 43200000, "category_id": 3, "image": "https://example.com/images/baton.jpg"},
    {"id": 52, "name": "Песочное печенье", "freshness_duration": 259200000, "category_id": 4, "image": "https://example.com/images/cookies.jpg"},
    {"id": 53, "name": "Сухарики", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/croutons.jpg"},
    {"id": 54, "name": "Гречка", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/buckwheat.jpg"},
    {"id": 55, "name": "Кускус", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/couscous.jpg"},
    {"id": 56, "name": "Лаваш", "freshness_duration": 43200000, "category_id": 3, "image": "https://example.com/images/lavash.jpg"},
    {"id": 57, "name": "Блины", "freshness_duration": 86400000, "category_id": 3, "image": "https://example.com/images/pancakes.jpg"},
    {"id": 58, "name": "Торт", "freshness_duration": 259200000, "category_id": 4, "image": "https://example.com/images/cake.jpg"},
    {"id": 59, "name": "Пирожки", "freshness_duration": 86400000, "category_id": 3, "image": "https://example.com/images/pies.jpg"},
    {"id": 60, "name": "Салаты", "freshness_duration": 86400000, "category_id": 1, "image": "https://example.com/images/salads.jpg"},
    {"id": 61, "name": "Квашеная капуста", "freshness_duration": 31536000000, "category_id": 1, "image": "https://example.com/images/sauerkraut.jpg"},
    {"id": 62, "name": "Оливки", "freshness_duration": 31536000000, "category_id": 1, "image": "https://example.com/images/olives.jpg"},
    {"id": 63, "name": "Сухофрукты", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/dried_fruits.jpg"},
    {"id": 64, "name": "Рыба консервированная", "freshness_duration": 31536000000, "category_id": 2, "image": "https://example.com/images/canned_fish.jpg"},
    {"id": 65, "name": "Мясо консервированное", "freshness_duration": 31536000000, "category_id": 2, "image": "https://example.com/images/canned_meat.jpg"},
    {"id": 66, "name": "Супы в пакетах", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/soup.jpg"},
    {"id": 67, "name": "Каша готовая", "freshness_duration": 259200000, "category_id": 4, "image": "https://example.com/images/ready_oatmeal.jpg"},
    {"id": 68, "name": "Энергетики", "freshness_duration": 31536000000, "category_id": 5, "image": "https://example.com/images/energy_drinks.jpg"},
    {"id": 69, "name": "Спортивные напитки", "freshness_duration": 31536000000, "category_id": 5, "image": "https://example.com/images/sports_drinks.jpg"},
    {"id": 70, "name": "Вода бутилированная", "freshness_duration": 31536000000, "category_id": 5, "image": "https://example.com/images/bottled_water.jpg"},
    {"id": 71, "name": "Лимонад", "freshness_duration": 259200000, "category_id": 5, "image": "https://example.com/images/lemonade.jpg"},
    {"id": 72, "name": "Пиво", "freshness_duration": 259200000, "category_id": 5, "image": "https://example.com/images/beer.jpg"},
    {"id": 73, "name": "Вино", "freshness_duration": 31536000000, "category_id": 5, "image": "https://example.com/images/wine.jpg"},
    {"id": 74, "name": "Виски", "freshness_duration": 31536000000, "category_id": 5, "image": "https://example.com/images/whiskey.jpg"},
    {"id": 75, "name": "Коньяк", "freshness_duration": 31536000000, "category_id": 5, "image": "https://example.com/images/brandy.jpg"},
    {"id": 76, "name": "Ром", "freshness_duration": 31536000000, "category_id": 5, "image": "https://example.com/images/rum.jpg"},
    {"id": 77, "name": "Коктейли", "freshness_duration": 86400000, "category_id": 5, "image": "https://example.com/images/cocktails.jpg"},
    {"id": 78, "name": "Молочные коктейли", "freshness_duration": 86400000, "category_id": 5, "image": "https://example.com/images/milkshakes.jpg"},
    {"id": 79, "name": "Томатный сок", "freshness_duration": 259200000, "category_id": 5, "image": "https://example.com/images/tomato_juice.jpg"},
    {"id": 80, "name": "Плодовые соки", "freshness_duration": 259200000, "category_id": 5, "image": "https://example.com/images/fruit_juices.jpg"},
    {"id": 81, "name": "Протеины", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/proteins.jpg"},
    {"id": 82, "name": "Зеленый горошек", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/green_peas.jpg"},
    {"id": 83, "name": "Фасоль", "freshness_duration": 31536000000, "category_id": 4, "image": "https://example.com/images/beans.jpg"},
    {"id": 84, "name": "Греческий йогурт", "freshness_duration": 259200000, "category_id": 2, "image": "https://example.com/images/greek_yogurt.jpg"},
    {"id": 85, "name": "Кокос", "freshness_duration": 259200000, "category_id": 1, "image": "https://example.com/images/coconut.jpg"},
    {"id": 86, "name": "Арбуз", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/watermelon.jpg"},
    {"id": 87, "name": "Дыня", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/melon.jpg"},
    {"id": 88, "name": "Киви", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/kiwi.jpg"},
    {"id": 89, "name": "Манго", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/mango.jpg"},
    {"id": 90, "name": "Груша", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/pear.jpg"},
    {"id": 91, "name": "Личи", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/lychee.jpg"},
    {"id": 92, "name": "Сливы", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/plums.jpg"},
    {"id": 93, "name": "Абрикосы", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/apricots.jpg"},
    {"id": 94, "name": "Крыжовник", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/gooseberries.jpg"},
    {"id": 95, "name": "Вишня", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/cherries.jpg"},
    {"id": 96, "name": "Малина", "freshness_duration": 259200000, "category_id": 1, "image": "https://example.com/images/raspberries.jpg"},
    {"id": 97, "name": "Ежевика", "freshness_duration": 259200000, "category_id": 1, "image": "https://example.com/images/blackberries.jpg"},
    {"id": 98, "name": "Киви", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/kiwi.jpg"},
    {"id": 99, "name": "Лимоны", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/lemons.jpg"},
    {"id": 100, "name": "Апельсины", "freshness_duration": 604800000, "category_id": 1, "image": "https://example.com/images/oranges.jpg"},
]

categories = [
    {"id": 1, "name": "Фрукты и овощи"},
    {"id": 2, "name": "Молочные продукты"},
    {"id": 3, "name": "Хлебобулочные изделия"},
    {"id": 4, "name": "Продукты длительного хранения"},
    {"id": 5, "name": "Напитки"},
]

for i in categories:
    post(f'http://127.0.0.1:5000/api/categories',
         json=i).json()
'''
'''users = [
    {'login': 'vasya',
     'email': '{{sensitive data}}',
     'password': '{{sensitive data}}'},
    {'login': 'josef',
         'email': '{{sensitive data}}',
         'password': '{{sensitive data}}'},
]
for i in users:
    post(f'http://127.0.0.1:5000/api/register',
         json=i).json()'''
'''
cond = [
    {'name': 'Холодильник'},
    {'name': 'Морозольная камера'},
]
for i in cond:
    post(f'http://127.0.0.1:5000/api/conditions',
         json=i).json()
'''

'''measurement = [
    {'name': 'Грамм'},
    {'name': 'Килограмм'},
    {'name': 'Миллилитры'},
    {'name': 'Литры'}
]

for i in measurement:
    post(f'http://127.0.0.1:5000/api/measurements',
         json=i).json()'''


