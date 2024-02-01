from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread
import asyncio
import json
import time
import os

url = 'https://steamcommunity.com/login/home/?goto='


class Selen:
    @classmethod
    async def check_accunt(cls, login: str, password: str) -> bool:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, cls.selen_going, login, password)
        return result

    @classmethod
    def update_thread(cls):
        while True:
            try:
                with open('files/account.txt', 'r', encoding='utf-8') as file:
                    users = file.read().replace('\r', '').split('\n')

            except:
                time.sleep(43200)
                continue

            for user in users:
                if user != '':
                    login, password = user.split(':')
                    cls.selen_going(login, password)

            time.sleep(43200)

    @staticmethod
    def selen_going(*args) -> bool:
        driver = webdriver.Chrome()

        login = args[0]
        password = args[1]
        try:
            driver.get(url)
            # Write login
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[1]/input'))
            )
            element.send_keys(login)
            # Write password
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[2]/input'))
            )
            element.send_keys(password)
            # Click button
            # /html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[4]/button

            driver.find_element(
                By.XPATH, '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[4]/button').click()
            # Check accaunt
            time.sleep(10)
            try:
                element = driver.find_element(
                    By.XPATH, '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[5]')
                return False
            except:
                cookies = driver.get_cookies()
                with open(f'cookies/cookies-{login}', 'w') as file:
                    json.dump(cookies, file)
                return True

        except Exception as ex:
            print(ex)

        finally:
            driver.close()
            driver.quit()


Thread(target=Selen.update_thread, daemon=True).start()


if __name__ == "__main__":
    asyncio.run(Selen.check_accunt('sadasd', 'saasdasd'))
