from .models import Recognise
from celery import Celery

app = Celery()


@app.task(name='test')
def recognise_scheduled():
    import channels.layers
    from asgiref.sync import async_to_sync

    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)('detectors', {'type': 'send_recognise'})

    # from random import randrange
    #
    # Recognise.objects.create(counter_cars=randrange(0, 10))
    # diff = Recognise.objects.all().count() - 10
    #
    # if diff > 0:
    #     Recognise.objects.filter(pk__in=Recognise.objects.all().order_by('created').values_list('pk')[:diff]).delete()


@app.task(name='get-frame-from-youtube-stream')
def get_frame(*args):
    import streamlink
    import numpy as np
    import subprocess as sp
    from PIL import Image

    streams = streamlink.streams(args[0])

    FFMPEG_BIN = "ffmpeg"
    pipe = sp.Popen([FFMPEG_BIN, "-i", streams['720p'].url,
                     "-loglevel", "quiet",  # no text output
                     "-an",  # disable audio
                     "-f", "image2pipe",
                     "-pix_fmt", "bgr24",
                     "-vcodec", "rawvideo", "-"],
                    stdin=sp.PIPE, stdout=sp.PIPE)

    raw_image = pipe.stdout.read(960 * 720 * 3)  # read 432*240*3 bytes (= 1 frame)
    image = np.fromstring(raw_image, dtype='uint8').reshape((720, 960, 3))

    result = Image.fromarray((image).astype(np.uint8))
    result.save('frontend/static/images/pre_in.png')

    pipe.kill()
    pipe.terminate()


@app.task(name='detect-objects')
def detector(*args):
    from .detector import Detector
    import channels.layers
    from asgiref.sync import async_to_sync

    get_frame(*args)
    det = Detector()
    num_detections = det.detect()

    Recognise.objects.create(counter_cars=num_detections)
    diff = Recognise.objects.all().count() - 10

    if diff > 0:
        Recognise.objects.filter(pk__in=Recognise.objects.all().order_by('created').values_list('pk')[:diff]).delete()

    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)('detectors', {'type': 'send_recognise'})
