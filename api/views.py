import re
import threading

from bs4 import BeautifulSoup
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.support.wait import WebDriverWait

from .constans import cookies, url
from .models import Product
from .serializers import ProductSerializer, TaskRequestSerializer
from .telegram import send_telegram_message


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


@swagger_auto_schema(
    method='post',
    request_body=TaskRequestSerializer,
    responses={
        200: openapi.Response(
            description="Пример успешного ответа",
            examples={
                "application/json": {
                    "products": [
                        {
                            "name": "Продукт 1",
                            "price": "100",
                            "image": "https://example.com/image1.jpg",
                            "discount": "10%"
                        },
                        {
                            "name": "Продукт 2",
                            "price": "200",
                            "image": "https://example.com/image2.jpg",
                            "discount": "15%"
                        }
                    ]
                }
            }
        )
    }
)
@api_view(['POST'])
def run_parse(request):
    """
    Этот эндпоинт предназначен для запуска парсинга товаров.
    """
    serializer = TaskRequestSerializer(data=request.data)
    if serializer.is_valid():
        chrome_options = Options()
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
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


@swagger_auto_schema(
    method='get',
    responses={200: openapi.Response(description="Список продуктов", schema=ProductSerializer(many=True))}
)
@api_view(['GET'])
def get_product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={200: openapi.Response(description="Детали продукта", schema=ProductSerializer())}
)
@api_view(['GET'])
def get_product_by_id(request, product_id):
    product = Product.objects.get(pk=product_id)
    serializer = ProductSerializer(product)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
