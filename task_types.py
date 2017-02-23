class CacheServer:
    def __init__(self, id, size, endpoints_count):
        self.id = id
        self.size = size
        self.endpoints = [None for _ in range(endpoints_count)]


class Endpoint:
    def __init__(self, id, caches_count):
        self.id = id
        self.caches = [None for _ in range(caches_count)]
        self.requests = []
        self.videos = []


def get_parameter_dict(params_line):
    numbers = map(int, params_line.split(' '))
    return {
        'videos_count': numbers[0],
        'endpoints_count': numbers[1],
        'request_descriptions_count': numbers[2],
        'caches_count': numbers[3],
        'cache_size': numbers[4]
    }


def get_created_caches(param_dict):
    result = []
    for i in range(param_dict['caches_count'] + 1):
        cache = CacheServer(
            id=i,
            size=param_dict['cache_size'],
            endpoints_count=param_dict['endpoints_count']
        )
        result.append(cache)
    return result


def get_parsed_items(path):
    result = {}
    with open(path) as config:
        param_dict = get_parameter_dict(config.readline())
        result['videos'] = map(int, config.readline().split(' '))
        result['endpoints'] = [None] * param_dict['endpoints_count']
        result['cache_servers'] = get_created_caches(param_dict)
        datacenter = result['cache_servers'][-1]
        datacenter.id=-1
        datacenter.size=float('infinity')
        for i in range(param_dict['endpoints_count']):
            latency, caches_links_count = map(int, config.readline().split(' '))
            endpoint = Endpoint(id=i, caches_count=param_dict['caches_count'])
            datacenter.endpoints[i] = endpoint
            for j in range(caches_links_count):
                cache_id, cache_latency = map(int, config.readline().split(' '))
                endpoint.caches[cache_id] = cache_latency
                result['cache_servers'][cache_id].endpoints[i] = endpoint
            endpoint.caches[-1] = latency
            endpoint.videos = result['videos']
            result['endpoints'][i] = endpoint
        for _ in range(param_dict['request_descriptions_count']):
            video, endpoint_id, requests_count = map(int, config.readline().split(' '))
            result['endpoints'][endpoint_id].requests.append({
                'video': video,
                'requests_count': requests_count
            })
    return result


# def write_output_to_file(cache_servers, path):
#     filtered_caches = [(i, cache) for i, cache in enumerate(cache_servers) if cache[0].fill]
#     with open(path, 'w') as output_file:
#         output_file.write(str(len(filtered_caches)) + '\n')
#         for i in range(len)


if __name__ == '__main__':
    items = get_parsed_items('kittens.in')
    print(items['videos'], items['endpoints'], items['cache_servers'])