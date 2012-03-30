import os


SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2


class FileChunkIO(file):
    """
    A class that allows you reading only a chunk of a file.
    """
    def __init__(self, name, mode='r', closefd=True, offset=0, bytes=None,
        *args, **kwargs):
        """
        Open a file chunk. The mode can only be 'r' for reading. Offset
        is the amount of bytes that the chunks starts after the real file's
        first byte. Bytes defines the amount of bytes the chunk has, which you
        can set to None to include the last byte of the real file.
        """
        if not mode.startswith('r'):
            raise ValueError("Mode string must begin with 'r'")
        self.offset = offset
        self.bytes = bytes
        if bytes is None:
            self.bytes = os.stat(name).st_size - self.offset
        super(FileChunkIO, self).__init__(name, mode, closefd, *args, **kwargs)
        self.seek(0)

    def seek(self, offset, whence=SEEK_SET):
        """
        Move to a new chunk position.
        """
        if whence == SEEK_SET:
            super(FileChunkIO, self).seek(self.offset + offset)
        elif whence == SEEK_CUR:
            self.seek(self.tell() + offset)
        elif whence == SEEK_END:
            self.seek(self.bytes + offset)

    def tell(self):
        """
        Current file position.
        """
        return super(FileChunkIO, self).tell() - self.offset

    def read(self, n=-1):
        """
        Read and return at most n bytes.
        """
        if n >= 0:
            max_n = self.bytes - self.tell()
            n = min([n, max_n])
            return super(FileChunkIO, self).read(n)
        else:
            return self.readall()

    def readall(self):
        """
        Read all data from the chunk.
        """
        return self.read(self.bytes - self.tell())

    def readinto(self, b):
        """
        Same as RawIOBase.readinto().
        """
        raise NotImplemented, "This method has not been implemented. do not use!"

    def readline(self, limit=-1):
        r"""Read and return a line from the stream.

        If limit is specified, at most limit bytes will be read.

        The line terminator is always b'\n' for binary files; for text
        files, the newlines argument to open can be used to select the line
        terminator(s) recognized.
        """
        # For backwards compatibility, a (slowish) readline().
        if hasattr(self, "peek"):
            def nreadahead():
                readahead = self.peek(1)
                if not readahead:
                    return 1
                n = (readahead.find("\n") + 1) or len(readahead)
                if limit >= 0:
                    n = min(n, limit)
                return n
        else:
            def nreadahead():
                return 1
        if limit is None:
            limit = -1
        elif not isinstance(limit, (int, long)):
            raise TypeError("limit must be an integer")
        res = ""
        #res = bytearray()
        while limit < 0 or len(res) < limit:
            b = self.read(nreadahead())
            if not b:
                break
            res += b
            if res.endswith("\n"):
                break
        return str(res)

    def next(self):
        line = self.readline()
        if not line:
            raise StopIteration
        return line

    def readlines(self, hint=None):
        """Return a list of lines from the stream.

        hint can be specified to control the number of lines read: no more
        lines will be read if the total size (in bytes/characters) of all
        lines so far exceeds hint.
        """
        if hint is not None and not isinstance(hint, (int, long)):
            raise TypeError("integer or None expected")
        if hint is None or hint <= 0:
            return list(self)
        n = 0
        lines = []
        for line in self:
            lines.append(line)
            n += len(line)
            if n >= hint:
                break
        return lines

