from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
from django.utils.safestring import SafeString
import json
import random
import requests
import ast


conn = sqlite3.connect("C:/Users/Егор/Desktop/ПРИ-321/дгту/database/db.db", check_same_thread=False)
cursor = conn.cursor()

def get_place(request):
    responsed_data = []
    train = request.GET.get("train")
    van = request.GET.get("van")

    cursor.execute(f"SELECT name, price, count, img FROM products WHERE train='{train}' AND van='{van}'")
    products = cursor.fetchall()
    for i in products:
        if not i is None:
            responsed_data.append({
                "name": i[0],
                "price": i[1],
                "count": i[2],
                "img": i[3],
            })
    data = {'data': responsed_data}

    context = {'datas': SafeString(data)}

    return render(request, "api/index.html", context=context)

def create_link(request):
    if request.method == "GET":
        train = request.GET.get("train")
        van = request.GET.get("van")
        place = request.GET.get("place")
        products = ast.literal_eval(request.GET.get("products"))
        prices = 0
        for key, item in products.items():
            cursor.execute(f"SELECT price FROM products WHERE name='{key}'")
            price = cursor.fetchone()[0]
            prices += int(price)*int(item)
        user_id = cursor.execute(f"SELECT id FROM tickets WHERE train='{train}' AND van='{van}' AND place='{place}'")
        token = '5656192477:AAF72rp7q0gqT9mlYONs96MMXh8tz5HY0V4'
        while True:
            number_order = random.randint(10000000, 99999999)
            cursor.execute(f"SELECT * FROM orders WHERE number_order={number_order}")
            order = cursor.fetchone()
            if order is None:
                break

        description = f'Поезд: {train}     Вагон: {van}     Место: {place}\nЗаказ: '

        for key, item in products.items():
            description += f'{key}: {item}     '

        data = {
            'title': f'Заказ: №{number_order}', 
            'description': description,
            'payload': 'buy_stake_package',
            # 'provider_token': '401643678:TEST:b759c1d2-2a5a-4808-8410-c0207f6d3022',
            'provider_token': '381764678:TEST:69429',
            # 'provider_token': '1744374395:TEST:947772bf737f3361f0b7',
            'currency': 'rub',
            'prices': json.dumps([{
                'label': f'Заказ: №{number_order}',
                'amount': prices*100,
            }]),
        }

        link = requests.get(f'https://api.telegram.org/bot{token}/createInvoiceLink?', data=data)
        link = json.loads(link.text)['result']

        cursor.execute(f"INSERT INTO orders VALUES ({user_id}, {number_order}, '{products}', {prices}, 0, 0)")
        conn.commit()

        return HttpResponse(json.dumps({'data': f'{link}'}), content_type="application/json")