from youtubesearchpython import VideosSearch, Video, ChannelsSearch


def video_search(video_name: str, limit: int or str) -> list:
    videosSearch = VideosSearch(video_name, limit=int(limit))
    result = videosSearch.result()['result']

    return result


def video_info(uri: str) -> dict:
    videoInfo = Video.getInfo(uri)

    return videoInfo


def channel_info(name: str) -> dict:
    channelInfo = ChannelsSearch(name, limit = 1)

    return channelInfo.result()['result']
