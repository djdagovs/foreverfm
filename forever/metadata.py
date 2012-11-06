import colors
import config
import cStringIO
import logging
import traceback
import soundcloud

PIXELS_PER_SECOND = 1

log = logging.getLogger(__name__)


class Metadata(object):
    client = soundcloud.Client(client_id=config.SOUNDCLOUD_CLIENT_KEY)
    __color = None

    def __init__(self, obj):
        if hasattr(obj, 'obj'):
            self.obj = obj.obj
        else:
            self.obj = obj

    def __getattr__(self, name):
        if name in self.obj:
            return self.obj.get(name)
        raise AttributeError

    def fields(self):
        return self.obj

    def keys(self):
        return self.obj.keys()

    @property
    def color(self):
        if not self.__color:
            try:
                if 'artwork_url' in self.obj and self.obj['artwork_url']:
                    art = self.obj['artwork_url']
                else:
                    art = self.obj['user']['avatar_url']
                if not art:
                    raise ValueError()
                fobj = cStringIO.StringIO(self.client.get(art).raw_data)
                self.__color = colors.colorz(fobj, 1)[0]
            except:
                traceback.print_exc()
                log.error("Could not get artwork colour - defaulting to black.")
                self.__color = (0, 0, 0)
        return self.__color
