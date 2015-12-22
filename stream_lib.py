class Streams(object):  # Base stream class, you need to load the dictionary


    def __init__(self, stream_dict=None):
        if stream_dict is not None:
            self.streams = stream_dict
        else:
            self.streams = {}

    def addStream(self, game, stream_url):
        try:
            if stream_url not in self.streams[game.upper()]:
                self.streams[game.upper()].append(stream_url)
            else:
                pass
        except:
            self.streams[game.upper()] = [stream_url]

    def getStream(self, stream_url):
        for v in self.streams.values():
            if v == stream_url:
                return v

    def __str__(self):
        return '\n'.join(['Category: {}\nstream: {}'.format(categories,stream) for categories,streams in self.streams.items() for stream in streams])


    def __len__(self):
        return len(self.streams)

    def __iter__(self):
        for game_category, streams in self.streams.items():
            yield streams

    def __getitem__(self, game_category):
        try:
            return self.streams[game_category]
        except KeyError:
            raise KeyError('No game category with this name')

