import concurrent.futures
import requests
import json
import time


def timer(func):
    def wrapper():
        start = time.perf_counter()
        func()
        finish = time.perf_counter()
        print(f'\nProgram executed in {round(finish - start, 2)} seconds.')

    return wrapper


def get_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error with {url}')
        return None


def process_links(links):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        tasks = [executor.submit(get_json, url) for url in links]
        for task in concurrent.futures.as_completed(tasks):
            result = task.result()
            if result is not None:
                results.append(result)
    return results


def sort(lst):
    sorting = True
    current_id = 1

    while sorting:
        for product in range(0, len(lst) - (current_id - 1)):
            if current_id == lst[product]['id']:
                current_element = lst[product]
                lst.remove(current_element)
                lst.append(current_element)
                current_id += 1
            if current_id == len(lst) + 1:
                sorting = False


@timer
def main():
    links = [f"https://dummyjson.com/products/{i}" for i in range(1, 101)]

    links = [links[i:i + 20] for i in range(0, len(links), 20)]

    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_links, link) for link in links]

        results = []
        for future in concurrent.futures.as_completed(futures):
            results.extend(future.result())

    sort(results)

    with open("products.json", "w", encoding='utf-8') as json_file:
        json.dump(results, json_file, indent=2)

    print("Data saved successfully!")


if __name__ == "__main__":
    main()
