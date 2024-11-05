import csv
import numpy as nmp
import matplotlib.pyplot as plt
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By

from typing import Any


def task_1() -> None:
    data: nmp.ndarray = nmp.random.normal(loc=0, scale=1, size=1000)

    plt.hist(data, bins=20)
    plt.xlabel('Значения')
    plt.ylabel('Частота')
    plt.title('Гистограмма нормального распределения')
    plt.show()


def task_2() -> None:
    x_random_array: nmp.ndarray = nmp.random.rand(5)
    y_random_array: nmp.ndarray = nmp.random.rand(5)

    plt.scatter(x_random_array, y_random_array)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Диаграмма рассеивания')

    plt.show()


def is_number(value: Any) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def parse_site() -> list[int]:

    divan_price: list[int] = []
    driver: webdriver = webdriver.Chrome()

    driver.get("https://www.divan.ru/ekaterinburg/category/divany-i-kresla")

    div_set: list[webdriver.remote] = driver.find_elements(By.CLASS_NAME, 'lsooF')

    for one_div in div_set:
        get_meta: webdriver.remote = one_div.find_element(By.CSS_SELECTOR, 'meta[itemprop=\'price\']')
        price: str = get_meta.get_attribute('content')

        if is_number(price):
            divan_price.append(int(price))

    driver.quit()

    if len(divan_price) > 0:
        print('Список цен удачно создан')
        return divan_price
    else:
        print('Создание списка цен не удалось (не найдены соответствующие элементы)')
        return [0]


def csv_saver(data: list[int]) -> None:
    if data[0] == 0:
        print('Программа завершает работу')
        exit()

    csv_path: Path = Path('csv_data/price.csv')

    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_write:
        writer: csv.writer = csv.writer(csv_write)
        for one_item in data:
            writer.writerow([one_item])
    print('Файл price.csv успешно сохранен!')


def csv_loader() -> list[int]:
    csv_path: Path = Path('csv_data/price.csv')

    with open(csv_path, 'r', newline='', encoding='utf-8') as csv_read:
        reader: csv.reader = csv.reader(csv_read)
        next(reader)
        data: list[csv.reader] = list(reader)
        print('Файл price.csv успешно загружен!')

    return data


def task_3() -> None:
    csv_path: Path = Path('csv_data/price.csv')
    new_data: list[int] = []

    if csv_path.is_file():
        print('Файл price.csv находится в папке csv_data')
        print('Список цен на диваны будет загружен из этого файла')

        new_data: list[csv.reader] = csv_loader()
        new_data: list[int] = [int(one_item[0]) for one_item in new_data if is_number(one_item[0])]

    else:
        print('Cейчас создается список с ценами на диваны, подождите...')

        new_data: list[int] = parse_site()
        csv_saver(new_data)

    # Подготовка данных для построения гистограммы
    graph_data: nmp.ndarray = nmp.array(new_data)

    plt.hist(graph_data, bins=20)
    plt.xlabel('Цена')
    plt.ylabel('Частота')
    plt.title('Гистограмма цен на диваны')
    plt.show()


if __name__ == "__main__":
    task_1()
    task_2()
    task_3()