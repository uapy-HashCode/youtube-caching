from task_types import items

items = items()
videos = items['videos']
end_points = items['endpoints']
cache_servers = items['cache_servers']

def process_video(video_weights_per_cache, request, end_point, cache_id):

    video_id = request['video']
    number_of_request = request['requests_count']
    l_d = end_point.caches[-1]
    size = videos[video_id]
    l_c = end_point.caches[cache_id]
    saved_time = number_of_request*(l_d-l_c)
    #if video in bug
    if video_id in video_weights_per_cache.keys():
        video_weights_per_cache[video_id][0]+=saved_time
    else:
        video_weights_per_cache[video_id] = [saved_time, size, end_point.id]
    return

configuration = []
# Run by each cache
for cache in cache_servers:

    video_weights_per_cache = {}
    # Run by each end_point
    for end_point in cache.endpoints:
        # Run by each video for end_point
        if end_point is not None:
            for request in end_point.requests:
            # calculate weight
                process_video(video_weights_per_cache, request = request, end_point=end_point, cache_id=cache.id)

    print(video_weights_per_cache)
    # sort videos
    v = sorted(video_weights_per_cache,key = lambda x: x.values()[0])

    # process cache server
    cache_config = {'cache_id': cache.id, 'number_of_videos': 0, 'videos': []}
    packed = 0
    for i in v:
        video_weight = i.values()[0][0]
        if video_weight + packed < cache.weight:
            cache_config['number_of_videos'] += 1
            video_id = i.keys()[0]
            cache_config['videos'].append({'video_id': video_id, 'weight': video_weight})
            packed += video_weight
        else:
            pass
    configuration.append({'cache_id': cache.id, 'config': cache_config})