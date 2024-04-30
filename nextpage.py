import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
import re
import telegram
import asyncio

cookies = [{'name': 'ADDRESSBOOKBAR_WEB_CLARIFICATION',
            'value': '1714214079',
            'domain': '.ozon.kz'},
           {'name': '__Secure-ab-group',
            'value': '29',
            'domain': '.ozon.kz'},
           {'name': '__Secure-access-token',
            'value': '4.0.HT14ErzRQoKFXNBfeTzGfw.29.AfbGW3diDc30Mged-YjRfjUEZBAG1FNBTj60kNEFZWKRETnxaerInT6TU9i774kPRA..20240428140531.IqB3QmZXhBjYPrt4hAqo9FbmVJBkK3WP0fJIG0YMzZQ',
            'domain': '.ozon.kz'},
           {'name': '__Secure-ext_xcid',
            'value': '3843485e183b7e084f95b147f01de478',
            'domain': '.ozon.kz'},
           {'name': '__Secure-refresh-token',
            'value': '4.0.HT14ErzRQoKFXNBfeTzGfw.29.AfbGW3diDc30Mged-YjRfjUEZBAG1FNBTj60kNEFZWKRETnxaerInT6TU9i774kPRA..20240428140531.LRKV_t9LSuQQRm4CFW4fOl5yiD13-XN4I6AxBJtQnIE',
            'domain': '.ozon.kz'},
           {'name': '__Secure-user-id',
            'value': '0',
            'domain': '.ozon.kz'},
           {'name': 'abt_data',
            'value': '33c44054e8eb42143336d44d36fbcb37:7c19f284f34768a25725d7275f07aee38637ceb1ebd835b02e909c6fb02d401a6c74fbc915bfddf8ccf681e36d0789ec1308839ee98cc1f60c38d58c2d5ce49a67dd08578164740c169465869bf0f0f6e9b3498ce2f848b1113a582d436a3b207f0b17082704e85bff4e8b8a458eac9efbf76ec4dd31680a2ebf64fed6eba701d9f7281c9f9c683d8c0bffe7134ac184a1aad1356124e3998fa499a89031e4745cb9aaf9d48dbdfdfad23352d727151f6707013bb6996442abadf50b814666156cb24fe142340fde9e09913dd77bbb5fe3926c0873df7ca8de7df0d3ba78decf',
            'domain': '.ozon.kz'},
           {'name': 'rfuid',
            'value': 'NjkyNDcyNDUyLDEyNC4wNDM0NzUyNzUxNjA3NCwxMzkzNjg1NDU1LC0xLC0xMDIzNDk2ODc3LFczc2libUZ0WlNJNklsQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMWxJRkJFUmlCV2FXVjNaWElpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgwc2V5SnVZVzFsSWpvaVEyaHliMjFwZFcwZ1VFUkdJRlpwWlhkbGNpSXNJbVJsYzJOeWFYQjBhVzl1SWpvaVVHOXlkR0ZpYkdVZ1JHOWpkVzFsYm5RZ1JtOXliV0YwSWl3aWJXbHRaVlI1Y0dWeklqcGJleUowZVhCbElqb2lZWEJ3YkdsallYUnBiMjR2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZTeDdJblI1Y0dVaU9pSjBaWGgwTDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMWRmU3g3SW01aGJXVWlPaUpOYVdOeWIzTnZablFnUldSblpTQlFSRVlnVm1sbGQyVnlJaXdpWkdWelkzSnBjSFJwYjI0aU9pSlFiM0owWVdKc1pTQkViMk4xYldWdWRDQkdiM0p0WVhRaUxDSnRhVzFsVkhsd1pYTWlPbHQ3SW5SNWNHVWlPaUpoY0hCc2FXTmhkR2x2Ymk5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlMSHNpZEhsd1pTSTZJblJsZUhRdmNHUm1JaXdpYzNWbVptbDRaWE1pT2lKd1pHWWlmVjE5TEhzaWJtRnRaU0k2SWxkbFlrdHBkQ0JpZFdsc2RDMXBiaUJRUkVZaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMWQsV3lKeWRTMVNWU0pkLDAsMSwwLDI0LDIzNzQxNTkzMCw4LDIyNzEyNjUyMCwwLDEsMCwtNDkxMjc1NTIzLFIyOXZaMnhsSUVsdVl5NGdUbVYwYzJOaGNHVWdSMlZqYTI4Z1YybHVNeklnTlM0d0lDaFhhVzVrYjNkeklFNVVJREV3TGpBN0lGZHBialkwT3lCNE5qUXBJRUZ3Y0d4bFYyVmlTMmwwTHpVek55NHpOaUFvUzBoVVRVd3NJR3hwYTJVZ1IyVmphMjhwSUVOb2NtOXRaUzh4TWpRdU1DNHdMakFnVTJGbVlYSnBMelV6Tnk0ek5pQXlNREF6TURFd055Qk5iM3BwYkd4aCxleUpqYUhKdmJXVWlPbnNpWVhCd0lqcDdJbWx6U1c1emRHRnNiR1ZrSWpwbVlXeHpaU3dpU1c1emRHRnNiRk4wWVhSbElqcDdJa1JKVTBGQ1RFVkVJam9pWkdsellXSnNaV1FpTENKSlRsTlVRVXhNUlVRaU9pSnBibk4wWVd4c1pXUWlMQ0pPVDFSZlNVNVRWRUZNVEVWRUlqb2libTkwWDJsdWMzUmhiR3hsWkNKOUxDSlNkVzV1YVc1blUzUmhkR1VpT25zaVEwRk9UazlVWDFKVlRpSTZJbU5oYm01dmRGOXlkVzRpTENKU1JVRkVXVjlVVDE5U1ZVNGlPaUp5WldGa2VWOTBiMTl5ZFc0aUxDSlNWVTVPU1U1SElqb2ljblZ1Ym1sdVp5SjlmWDE5LDY1LDEwMTczNDIwOCwxLDEsLTEsMTY5OTk1NDg4NywxNjk5OTU0ODg3LDMzNjAwNzkzMywxMg==',
            'domain': '.ozon.kz'},
           {'name': 'xcid',
            'value': '727199f0645486daf0dc8bfdafebfc64',
            'domain': '.ozon.kz'}]
bot = telegram.Bot(token='6469093913:AAEFSzzL-rAYGpBE01LL6BxO0Z576fxWCuM')
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

url = 'https://ozon.kz/seller/proffi-1/products/?miniapp=seller_1'
async def main(count):
        try:
            chrome_options = Options()
            chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)

        # Открываем страницу и парсим товары
            products = []
            for page in range(1,3):
                source_text = page_open(driver, f'{url}&page={page}')
                soup = BeautifulSoup(source_text, 'html.parser')
                for product in soup.find_all('div', class_='y2i y3i tile-root'):
                    if len(products) == count:
                        await bot.send_message(722541015, f'Задача на парсинг товаров с сайта Ozon завершена. Сохранено: {len(products)} товаров')
                        return products
                    product_info = {}
                    product_info['name'] = product.find('span', class_='tsBody500Medium').text.strip()
                    product_info['price'] = re.sub(r'[^\d]+', '', product.find('span', class_='c302-a1 tsHeadline500Medium c302-c0').text.strip())
                    product_info['image'] = product.find('img', class_='zi2 b900-a').get('src')
                    product_info['discount'] = product.find('span', class_='tsBodyControl400Small c302-a2 c302-a7 c302-b1').text.strip()
                    products.append(product_info)

                await bot.send_message(722541015, f'Задача на парсинг товаров с сайта Ozon завершена. Сохранено: {len(products)} товаров')
                return products

        except Exception as e:
            print("Ошибка:", e)
 
        driver.quit()
        return products


            
    
    
print(asyncio.run(main(71)))

