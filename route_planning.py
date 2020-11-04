# 高德地图路径规划
import re
import requests
import pandas as pd
from collections import defaultdict
import pickle


key = '24d8c9893c3f6f054de7ab5f51933b60'

# 计算两点之间的距离
def compute_distance(longitude1, latitude1, longitude2, latitude2):
    request_url = 'http://restapi.amap.com/v3/distance?key='+ key +\
                  '&origins='+str(longitude1)+','+str(latitude1)+\
                  '&destination='+str(longitude2)+','+str(latitude2)+'&type=1'
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    data = requests.get(request_url, headers=header, timeout=10)
    data.encoding = 'utf-8'
    data = data.text
    # print(data)
    pattern = 'distance":"(.*?)","duration":"(.*?)"'
    result = re.findall(pattern, data)
    return int(result[0][0])

compute_distance(116.337581,39.993138, 116.339941,39.976228)

# 找到开销最小节点
def find_lowest_cost_node(costs):
    # 初始化数据
    lowest_cost = float('inf')
    lowest_cost_node = None
    # 遍历所有节点
    for node in costs:
        # 找到非processed集合中
        if not node in processed:
            # 如果当前节点开销比已经存在的开销小，则更新该节点为开销最小的节点
            if costs[node] < lowest_cost:
                lowest_cost = costs[node]
                lowest_cost_node = node
    return lowest_cost_node

# 找到最短路径
def find_shortest_path():
    node = end
    shortest_path = [end]
    while parents[node] != start:
        shortest_path.append(parents[node])
        node = parents[node]
    shortest_path.append(start)
    return shortest_path

# 计算图中从start到end的最短距离
def dijkstra():
    # 找到目前开销最小的节点
    node = find_lowest_cost_node(costs)
    print('当前cost最小节点：', node)
    # 找到开销最小的节点就进行路径规划，如果所有节点都放到processed中，就结束
    while node is not None:
        # 获取节点目前的cost
        cost = costs[node]
        # 获取节点的邻居
        neighbors = graph[node]
        # 遍历所有邻居，看看是否通过node节点，比之前cost更少
        for neighbor in neighbors.keys():
            # 计算经过当前节点到达相邻节点的开销，即当前节点cost+当前节点邻居的cost
            new_cost = cost + neighbors[neighbor]
            # 通过node是否可以更新start->neighbor的cost
            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                # 经过node到达neighbors节点cost更少
                parents[neighbor] = node
        # 将当前节点放到processed
        processed.append(node)
        # 找到接下来要处理的节点，并且继续循环
        node = find_lowest_cost_node(costs)
        print('当前cost最小节点:', node)
    # print(parents)
    # 循环完毕说明所有节点都已经处理完
    shortest_path = find_shortest_path()
    shortest_path.reverse()
    print('从{}到{}的最短路径：{}'.format(start, end, shortest_path))

# 数据加载
data = pd.read_csv('./subway.csv')
# 使用graph保存图中的邻接矩阵表（点到邻居之间的距离）
# 创建图中两点之间距离
graph = defaultdict(dict)
for i in range(data.shape[0]):
    site1 = data.loc[i, 'site']
    if i < data.shape[0]-1:
        site2 = data.loc[i+1, 'site']
        # 如果两个站在同一条线路
        if site1 == site2:
            longitude1, latitude1 = data.loc[i, 'longitude'], data.loc[i, 'latitude']
            longitude2, latitude2 = data.loc[i+1, 'longitude'], data.loc[i+1, 'latitude']
            name1, name2 = data.loc[i, 'name'], data.loc[i+1, 'name']
            distance = compute_distance(longitude1, latitude1, longitude2, latitude2)
            graph[name1][name2] = distance
            graph[name2][name1] = distance
            print(name1, name2, distance)

output = open('graph.pkl', 'wb')
pickle.dump(graph, output)

start = '鸡鸣寺站'
end = '南京南站'
# 查看start的邻居节点
# print(graph[start].keys())
# print(graph[start].values())
# 创建节点的开销表，cost是指从start到这个节点的距离
costs = {}
# 存储父节点的Hash表，用于记录路径
parents = {}
parents[end] = None
# 获取该节点相邻节点
for node in graph[start].keys():
    costs[node] = float(graph[start][node])
    parents[node] = start
# print(costs)
costs[end] = float('inf')
# 记录处理过的节点list
processed = []
dijkstra()