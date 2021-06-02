
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
import os
BASE_DIR =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dowload(query: str, page_count: str):
    header = {"Authorization" : "563492ad6f91700001000001a467ba46a6b941a1a25c73094d5532b6"}
    query=query.strip()
    params = {"query":query,"per_page":1}
    url = f"https://api.pexels.com/v1/search"
    i = 1
    while i <= page_count :
        params["page"]=i
        req = requests.get(url,headers=header,params=params)
        _res = req.json().get('total_results')
        if req.status_code == 200 and _res > 1:
            _r = req.json()
            for item in _r.get("photos"):
                _img_url = item.get("src").get("original")
                resp = requests.get(_img_url)
                # print(_img_url)
                image = Image.open(BytesIO(resp.content))
                try:
                    try:
                        media = os.mkdir(os.path.join(BASE_DIR,'request_library','media'))
                        print("Папка Media создана")
                    except:
                        print("Папка Media уже создана")
                    finally:
                        try:
                            media = os.mkdir(os.path.join(BASE_DIR,'request_library','media',query))
                            print(f'папка {query}  создана')
                        except FileExistsError:
                            print(f'папка {query} уже создана')
                        except FileNotFoundError:
                            print("Папка  {query} не найдена")
                except FileNotFoundError:
                    print("Папка не найдена")
                finally:
                    image.save(f"media/{query}/{query}_{i}.{_img_url.split('.')[-1]}")
                print('____________________\nскачано в папку ',os.path.join(BASE_DIR,'request_library','media',query))
        else:
            if  _res and _res < 1 or _res==0:
                print(f"По запросу {query} найдено {_res} результатов")
            elif req.status_code != 200 :
                print("Ошибка сервера ",req.status_code)
        i+=1


def main() -> None:
    query = input("Query: ")
    page_count = int(input("Count page: "))
    dowload(query,page_count)

main()
