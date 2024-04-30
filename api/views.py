from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.chrome.options import Options
import time
import re
import telegram
import asyncio
from asgiref.sync import sync_to_async
from django.http import JsonResponse
import threading
import aiogram

from .serializers import TaskRequestSerializer
from .constans import url, cookies, bot
from .models import Product


def page_open(driver, url):
    driver.delete_all_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(
            ES.presence_of_all_elements_located((By.ID, 'ozonTagManagerApp')))
    finally:
        return driver.page_source


def send_telegram_message(products):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_send_telegram_message(products))
    loop.close()


async def async_send_telegram_message(products):
    await bot.send_message(722541015, f'Задача на парсинг товаров с сайта Ozon завершена. Сохранено: {len(products)} товаров')

@api_view(['POST'])
def run_parse(request):
    serializer = TaskRequestSerializer(data=request.data)
    if serializer.is_valid():
        chrome_options = Options()
        chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        source_text = page_open(driver, url)
        soup = BeautifulSoup(source_text, 'html.parser')
        products = []
        for product in soup.find_all('div', class_='y2i y3i tile-root'):
            if len(products) == serializer.validated_data.get('products_count'):
                threading.Thread(target=send_telegram_message, args=(products,)).start()
                driver.quit()
                return Response(products)
            product_info = {}
            product_info['name'] = product.find('span', class_='tsBody500Medium').text.strip()
            product_info['price'] = re.sub(r'[^\d]+', '', product.find('span', class_='c302-a1 tsHeadline500Medium c302-c0').text.strip())
            product_info['image'] = product.find('img', class_='zi2 b900-a').get('src')
            product_info['discount'] = product.find('span', class_='tsBodyControl400Small c302-a2 c302-a7 c302-b1').text.strip()
            products.append(product_info)
            Product.objects.create(name=product_info['name'], price=product_info['price'],
                                   image=product_info['image'], discount=product_info['discount'])
        threading.Thread(target=send_telegram_message, args=(products,)).start()
        driver.quit()
        return Response(products)
    driver.quit()
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

