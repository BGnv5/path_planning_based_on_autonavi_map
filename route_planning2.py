import route_planning_api
import pandas as pd

def get_nearest_subway(data, location1):
    distance = float('inf')
    print(location1[0], location1[1])
    nearest = None
    for i in range(data.shape[0]):
        site1 = data.loc[i, 'name']
        longitude, latitude = float(data.loc[i, 'longitude']), float(data.loc[i, 'latitude'])
        temp = (float(location1[0])-longitude) ** 2 + (float(location1[1])-latitude) ** 2
        if temp < distance:
            distance = temp
            nearest = site1
    return nearest

def compute(site1, site2):
    # 计算site1的location
    location1 = route_planning_api.get_location(site1, city)
    # print(location1)
    location2 = route_planning_api.get_location(site2, city)
    # 计算site1最近的地铁站作为start
    data = pd.read_csv('./subway.csv')
    start = get_nearest_subway(data, location1)
    end = get_nearest_subway(data, location2)
    print('{}最近的地铁站{}'.format(site1, start))
    print('{}最近的地铁站{}'.format(site2, end))
    shortest_path = route_planning_api.compute(start, end)
    if site1 != start:
        shortest_path.insert(0, site1)
    if site2 != end:
        shortest_path.append(site2)
    print('从{}=>{}的最优路径为{}'.format(site1, site2, shortest_path))

city = '南京'
compute('南京大学', '南京南站')