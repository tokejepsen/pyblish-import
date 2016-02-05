import os

import pyblish.api


class InfiniteCollector(object):

    def process(self, parent):

        items = [str(parent) + ' - a', str(parent) + ' - b',
                 str(parent) + ' - c']
        for item in items:
            pyblish.api.Instance(item, parent)


class HomeDirectoryCollector(object):

    def process(self, parent):

        path = os.path.expanduser('~')
        if 'path' in parent.data:
            path = parent.data['path']

        if os.path.isdir(path):
            for item in os.listdir(path):
                instance = pyblish.api.Instance(item, parent)
                instance.data['path'] = os.path.join(path, item)

plugins = [InfiniteCollector, HomeDirectoryCollector]
