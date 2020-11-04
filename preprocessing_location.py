import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# 根据request_url得到soup
def get_page_content(request_url):
    # 得到页面的内容
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(request_url, headers=header, timeout=10)
    content = html.text
    # print(content)
    # 通过content创建BS对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup

# 获取指定城市的地铁路线
request_url = 'https://ditie.mapbar.com/nanjing_line/'
soup = get_page_content(request_url)

df = pd.DataFrame(columns=['name','site'])
subways = soup.find_all('div', class_='station')
for subway in subways:
    route_name = subway.find('strong', class_='bolder')
    # print(route_name)
    routes = subway.find('ul')
    routes = routes.find_all('a')
    for route in routes:
        # print(route.text)
        temp = {'name':route.text, 'site':route_name}
        df = df.append(temp, ignore_index=True)
# print(df)
df['city'] = '南京'
df.to_csv('./subway.csv', index=False)

# 添加经度longitude、纬度latitude
key = '24d8c9893c3f6f054de7ab5f51933b60'
def get_location(keyword, city):
    request_url = 'http://restapi.amap.com/v3/place/text?key='+ key \
                + '&keywords=' + keyword + '&types=&city='+ city \
                +'&children=1&offset=1&page=1&extensions=all'
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    data = requests.get(request_url, headers=header)
    data.encoding='utf-8'
    data = data.text
    # print(data)
    """
    ?表示懒惰模式; 
    .*具有贪婪的性质，首先匹配到不能匹配为止;
    .*?则相反，一个匹配以后，就往下执行后续的正则
    """
    pattern = 'location":"(.*?),(.*?)"'
    # 得到经纬度
    result = re.findall(pattern, data)
    # 如果有多个，取第一个位置
    try:
        return result[0][0], result[0][1]
    except:
        return get_location(keyword.replace('站', ''), city)

# print(get_location('新街口', '南京'))

df['longitude'], df['latitude'] = None, None
for index, row in df.iterrows():
    longitude, latitude = get_location(row['name'], row['city'])
    df.loc[index, 'longitude'] = float(longitude)
    df.loc[index, 'latitude'] = float(latitude)
    print(row['name'], longitude, latitude)
df.to_csv('subway.csv',index=False)