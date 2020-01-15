#!/usr/bin/env python3.7
"""Xiaomi MIUI Downloads Devices Info Scraper"""

import json
from bs4 import BeautifulSoup
from requests import get


def china_devices():
    """
    Extract devices json from MIUI downloads page
    :param url: MIUI downloads page
    """
    response = get("http://www.miui.com/download.html")
    page = BeautifulSoup(response.content, 'html.parser')
    data = page.findAll("script")
    data = [i.text for i in data if "var phones" in i.text][0].split('=')[1].split(';')[0]
    info = json.loads(data)
    sorted_info = sorted(info, key=lambda k: k['pid'], reverse=True)
    with open('china.json', 'w') as output:
        json.dump(sorted_info, output, indent=1, ensure_ascii=False)


def global_devices():
    """
    fetch MIUI downloads devices
    """
    headers = {
        'pragma': 'no-cache',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'cache-control': 'no-cache',
        'authority': 'c.mi.com',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://c.mi.com/oc/miuidownload/',
    }

    url = 'http://c.mi.com/oc/rom/getphonelist'
    data = get(url, headers=headers).json()['data']['phone_data']['phone_list']
    with open('c_mi.json', 'w') as output:
        json.dump(data, output, indent=1, ensure_ascii=False)


def china_fastboot():
    """fetch MIUI china fastboot rom devices"""
    page = BeautifulSoup(get("https://www.miui.com/shuaji-393.html").content, 'html.parser')
    links = [f"{i['href'].split('=')[1].split('&')[0].strip()} - {i['href'].split('=')[2].split('&')[0]}"
             for i in page.findAll('a') if "fullromdownload" in str(i)]
    with open("chinese_fastboot.txt", 'w') as output:
        output.writelines(i + '\n' for i in sorted(links))


def global_fastboot():
    """fetch MIUI global fastboot rom devices"""
    data = get("https://c.mi.com/oc/rom/getlinepackagelist").json()["data"]
    links = [f"{i['package_url'].split('=')[1].split('&')[0].strip()} - {i['package_url'].split('=')[2].split('&')[0]}"
             for i in data]
    with open("global_fastboot.txt", 'w') as output:
        output.writelines(i + '\n' for i in sorted(links))


def main():
    """
    Scrap Xiaomi devices downloads info from official site and generate JSON files
    """
    china_devices()
    global_devices()
    china_fastboot()
    global_fastboot()


if __name__ == '__main__':
    main()