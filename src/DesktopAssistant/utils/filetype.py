from typing import BinaryIO

from PySide6.QtCore import QMimeDatabase


def fileType(fp: BinaryIO) -> str:
    """Return the MIME type of the file based on its contents

    :param fp: file handle of the file in question
    """
    db = QMimeDatabase()
    mime = db.mimeTypeForData(fp.read())
    return mime.name()


def gifIsAnimated(fpGif: BinaryIO) -> bool:
    """Return true if image is an animated gif

    shamelessly stolen from https://stackoverflow.com/a/57420980/11659424

    :param fpGif: file handle of the file in question
    :returns: True if the image is an animated gif
    """
    def skipColorTable(fp: BinaryIO, packedByte: int):
        """this will fp.seek() completely past the color table"""

        hasGct = (packedByte & 0b10000000) >> 7
        gctSize = packedByte & 0b00000111

        if hasGct:
            fp.read(3 * pow(2, gctSize + 1))  # global color table

    def skipImageData(fp: BinaryIO):
        """skips the image data, which is basically just a series of sub blocks
        plus the lzw minimum code to decompress the file data"""
        fp.read(1)  # lzw minimum code size
        skipSubBlocks(fp)

    def skipSubBlocks(fp: BinaryIO):
        """skips over the sub blocks
        the first byte of the sub block tells you how big that block is, then
        you read those, then read the next byte, which will tell you how big
        the next sub block is, you keep doing this until you get a sub block
        size of zero"""
        numSubBlocks = ord(fp.read(1))
        while numSubBlocks != 0x00:
            fp.read(numSubBlocks)
            numSubBlocks = ord(fp.read(1))

    imageCount = 0
    header = fpGif.read(6)
    if header == b'GIF89a':  # GIF87a doesn't support animation
        logicalScreenDescriptor = fpGif.read(7)
        skipColorTable(fpGif, logicalScreenDescriptor[4])

        b = ord(fpGif.read(1))
        while b != 0x3B:  # 3B is always the last byte in the gif
            if b == 0x21:  # 21 is the extension block byte
                b = ord(fpGif.read(1))
                if b == 0xF9:  # graphic control extension
                    blockSize = ord(fpGif.read(1))
                    fpGif.read(blockSize)
                    b = ord(fpGif.read(1))
                    if b != 0x00:
                        raise ValueError('GCT should end with 0x00')

                elif b == 0xFF:  # application extension
                    blockSize = ord(fpGif.read(1))
                    fpGif.read(blockSize)
                    skipSubBlocks(fpGif)

                elif b == 0x01:  # plain text extension
                    blockSize = ord(fpGif.read(1))
                    fpGif.read(blockSize)
                    skipSubBlocks(fpGif)

                elif b == 0xFE:  # comment extension
                    skipSubBlocks(fpGif)

            elif b == 0x2C:  # image descriptor
                # if we've seen more than one image it's animated
                imageCount += 1
                if imageCount > 1:
                    return True

                # total size is 10 bytes, we already have the first byte so
                # let's grab the other 9 bytes
                imageDescriptor = fpGif.read(9)
                skipColorTable(fpGif, imageDescriptor[-1])
                skipImageData(fpGif)

            b = ord(fpGif.read(1))

    return False


def isAnimated(fp: BinaryIO) -> bool:
    """Determines if a file is animated.

    :param fp: file handle of the file in question
    :returns: True if animated, False if not
    """
    mimeType = fileType(fp)
    if mimeType.startswith('image/'):
        if mimeType == 'image/gif':
            fp.seek(0)
            return gifIsAnimated(fp)
        return False
    return mimeType.startswith('video/')
