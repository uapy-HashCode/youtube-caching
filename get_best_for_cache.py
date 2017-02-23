from functools import reduce
from operator import add
from collections import namedtuple

CacheServerData = namedtuple(
    'CacheServerData',
    ['video_id', 'size', 'efficiency'],
)
EfficiencyData = namedtuple('EfficiencyData', ['node_id', 'value'])


def get_most_optimal_nodes(cache_server_data):
    return [
        sorted(
            sorted([
                    CacheServerData(
                        item.video_id,
                        item.size,
                        reduce(add, [x.value for x in item.efficiency]),
                    ) for item in cache_data
                ],
                key=lambda x: x.size
            ),
            key=lambda x: x.efficiency,
            reverse=True
        ) for cache_data in cache_server_data
    ]


def get_most_optimal_for_cache(optimal_nodes, cache_id):
    return sorted(
        [item for item in optimal_nodes[cache_id]],
        key=lambda x: x.efficiency,
        reverse=True,
    )


def fill_caches(cache_servers):
    optimal_nodes = get_most_optimal_nodes(
        item.efficiency_info for item in cache_servers
    )
    for i, cache_server in enumerate(cache_servers):
        optimal_list = get_most_optimal_nodes(optimal_nodes, i)
        put_size = 0
        cache_server.fill = []
        for item in optimal_list:
            put_size += item.size
            if put_size > cache_server.size:
                break
            cache_server.fill.append(item)
    return cache_servers
