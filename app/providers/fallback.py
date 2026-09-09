from app.providers.registry import image_provider, video_provider


def image():
    return image_provider()


def video():
    return video_provider()
