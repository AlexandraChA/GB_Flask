import requests
import time
import threading
from multiprocessing import Process
import asyncio
import aiohttp


urls_photos = ['https://www.2wired2tired.com/wp-content/uploads/2011/08/Funny-Cat-Photo-Medium.jpg',
        'https://i.pinimg.com/736x/79/a3/16/79a3168cf52edca304ff32db46e0f888.jpg',
        'https://m.media-amazon.com/images/I/61DK+ex803L.jpg',
        'https://i.pinimg.com/474x/78/5a/26/785a26f8eecec873591f43abbfcf2823.jpg',
        'https://i.pinimg.com/736x/63/bc/f8/63bcf860614776518c59f251708ad67d.jpg',
        ]

def download_img(url, start_time):
    response = requests.get(url).content
    filename = url.rsplit('/', 1)[-1] +  '.png'
    with open(filename, "wb") as f:
        f.write(response)
    print(f"Image {url.rsplit('/', 1)[-1]} was downloaded in {time.time() - start_time:.2f} seconds")

# threads = []
# start_time = time.time()

# for url in urls_photos:
#     thread = threading.Thread(target=download_img, args=[url, start_time])
#     threads.append(thread)
#     thread.start()
# for thread in threads:
#     thread.join()
# print(f"All images were downloaded in {time.time() - start_time:.2f} seconds")

# processes = []
# start_time_2 = time.time()

# if __name__ == '__main__':
#     for url in urls_photos:
#         process = Process(target=download_img, args=(url,start_time_2, ))
#         processes.append(process)
#         process.start()
#     for process in processes:
#         process.join()
#     print(f"All images were downloaded in {time.time() - start_time_2:.2f} seconds")

async def download_as_img(url, start_time):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            image = await response.content.read()
            filename = url.rsplit('/', 1)[-1] +  '.png'
            with open(filename, "wb") as f:
                f.write(image)
            print(f"Image {url.rsplit('/', 1)[-1]} was downloaded in {time.time() - start_time:.2f} seconds")

async def main():
    tasks = []
    for url in urls_photos:
        task = asyncio.ensure_future(download_as_img(url, start_time_3))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(f"All images were downloaded in {time.time() - start_time_3:.2f} seconds")

start_time_3 = time.time()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
