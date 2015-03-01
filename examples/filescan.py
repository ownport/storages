#!/usr/bin/env python
#
#   scan files
#

import os
import sys
import hashlib

from storages.metadata import Metadata

class FileScanner(object):
    
    def __init__(self, metadata_path):

        if not metadata_path:
            raise RuntimeError('Metadata path is not defined')

        self._storage = Metadata(metadata_path)
        self._block_size = 2 ** 20

    def scan(self, path):

        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                print filepath
                filehash = self.hash(filepath, hashlib.sha1())

                filehash, fileattrs = self._storage.get(filehash)
                if fileattrs:
                    if filepath not in [v for k,v in fileattrs if k == 'filepath']:
                        self._storage.put(filehash, [(u'filepath', filepath)])
                else:
                    self._storage.put(filehash, 
                                        [('filepath', filepath), ('filesize', os.path.getsize(filepath))]
                    )


    def hash(self, filepath, hashfunc):

        with open(filepath, 'rb') as f:
            while True:
                data = f.read(self._block_size)
                if not data:
                    break
                hashfunc.update(data)
        return hashfunc.hexdigest()

if __name__ == '__main__':
    
    import optparse

    parser = optparse.OptionParser()
    parser.add_option('-m', '--metadata', type=str, help='path for files metadata storage (sqlite)')
    parser.add_option('-p', '--path', type=str, help='path for scanning files')
    (options, args) = parser.parse_args()

    if not options.metadata:
        print >> sys.stderr, 'Error! The path to metadata storage is not defined, please use `--metadata` parameter'
        sys.exit(1)

    if not options.path:
        print >> sys.stderr, 'Error! The path is not defined, please use `--path` parameter'
        sys.exit(1)

    scanner = FileScanner(metadata_path=options.metadata)
    try:
        scanner.scan(options.path)
    except KeyboardInterrupt:
        print "Interrupted by user"


