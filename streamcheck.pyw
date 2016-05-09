#!python2

import argparse
import logging
from subprocess import Popen
import json
from livestreamer import streams as livestreamer_stream
from stream_lib import Streams
from configparser import SafeConfigParser, ParsingError
from shutil import copy
import webbrowser
from movewindows import WindowsPosition
import time


# Reading and loading configs
try:
    conf = SafeConfigParser()
    conf.read('E:\code\stream-check\config.ini')
    STREAM_LIST_PATH = conf.get('stream_dict', 'path')
    STREAM_BACKUP_PATH = conf.get('stream_dict', 'backup')
    TEXT_PATH = conf.get('massiveadd', 'path')
    LOG_PATH = conf.get('log', 'path')
    FORMATTER = '%(asctime)-15s | %(levelname)-8s \n %(message)-8s'
    logging.basicConfig(
        filename=LOG_PATH, level=logging.INFO, format=FORMATTER)
    logging.getLogger("requests").setLevel(logging.WARNING)
    browser = webbrowser.get('windows-default')
except ParsingError as e:
    print("Couldn't parse because {}".format(e))


def open_dict():
    with open(STREAM_LIST_PATH) as f:
        logging.info('Opening dictionary')
        read_dict = json.load(f)
        stream_dict = Streams(read_dict)
    return stream_dict


def add_streams(url, game):
    stream_dict = open_dict()
    stream_dict.addStream(game.upper(), str(url))
    try:
        copy(STREAM_LIST_PATH, STREAM_BACKUP_PATH)
        logging.info('Backing up stream list at {}'.format(STREAM_BACKUP_PATH))
    except Exception as e:
        logging.error('Backup failed: {}'.format(e))
    with open(STREAM_LIST_PATH, 'w') as f:
        json.dump(stream_dict.streams, f)
        logging.info('Added url: {} \n category: {}'.format(url, game))


def check_stream(url):
    try:
        if livestreamer_stream(url):
            return True
        else:
            return False
    except Exception as e:
        if args.verbose:
            logging.error('Couldnt open: {} ({})'.format(url, e))
        else:
            logging.error('Couldnt open: {}'.format(url))


def check_vod(url):
    if '?t=' in url:
        return True
    try:
        int(str(url).split('/')[-1])
    except ValueError:
        return False
    return True


def open_livestreamer(stream_urls, quality, verbose, chat, monitor):
    for stream_url in stream_urls:
        if check_stream(stream_url):
            if chat:
                webbrowser.open_new_tab(
                    '{}/{}'.format(str(stream_url), 'chat'))
            if check_vod(stream_url):
                Popen(
                    'livestreamer {} {} -Q --player-passthrough=hls'.format(str(stream_url), quality), shell=verbose)
            else:
                Popen(
                    'livestreamer {} {} -Q '.format(str(stream_url), quality), shell=verbose)

            logging.info('Opening: {} \n Quality: {} \n verbose: {}'.format(
                stream_url, quality, verbose))

            time.sleep(16)
            windows = WindowsPosition()
            windows.move(monitor)


def massive_add(text):
    with open(text, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            if line == line.upper():
                game = line
            else:
                url = line.split()
                add_streams(''.join(url[1::3]), game)


def main(game=None, quality='source', verbose=True, chat=False, monitor='monitor2'):
    streams = open_dict()
    if game == None:
        for stream in streams:
            open_livestreamer(stream, quality, verbose, chat, monitor)
    else:
        for game_category in game:
            open_livestreamer(
                streams[game_category.upper()], quality, verbose, chat, monitor)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Game streams to open')
    parser.add_argument(
        '--single', '-s', help='opens a single stream. Use "-s URL -a CATEGORY" to add stream to dictionary', action="store")
    parser.add_argument(
        '--multi', '-m', help="open multiple streams", nargs='*', action="store")
    parser.add_argument(
        '--add', '-a', help="add stream to the list. Use '-a URL GAME'", action="store")
    parser.add_argument(
        '-v', '--verbose', help="Makes cmd windows appear", action="store_true")
    parser.add_argument(
        '-c', '--chat', help="Opens twitch chat if available", action="store_true")
    parser.add_argument(
        '--quality', '-q', help='Chooses the quality to open streams, default = source', default='source')
    parser.add_argument(
        '--monitor', '-mn', help='Chooses the monitor to open, default = monitor2, n (see movewindows.py)', default='monitor2', action="store")
    args = parser.parse_args()
    verbose = False if args.verbose else True
    chat = True if args.chat else False
    if args.single:
        open_livestreamer(
            [args.single], args.quality, verbose, chat, args.monitor)
        if args.add:
            add_streams(args.single, args.add)
    elif args.multi:
        main(args.multi, args.quality, verbose, chat, args.monitor)
    elif args.add:
        add_streams(args.add[0], args.add[1])
    else:
        main()
