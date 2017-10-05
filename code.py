import numpy as np
from PIL import Image

def load8x8(pngPath):
    img = Image.open(pngPath)
    rows, cols = img.size[1] / 8, img.size[0] / 8
    assert(rows * cols == 256)
    arr = np.array(img.getdata(),np.uint8).reshape(img.size[1], img.size[0], 3)
    arr = (arr[:,:,0].reshape(img.size[1], img.size[0]) > 0).reshape(rows,8,cols,8)
    symbols = np.array([arr[i / cols,:,i % cols,:] for i in range(256)])
    return symbols


symbols = load8x8('codepage-437.png')
print 'hex = ['
i = 0
for c in range(256):
    for y in range(8):
        print '    #', ''.join(['*' if symbols[c,y,x] else ' ' for x in range(8)])
    print "    [%s]," % ", ".join(['0x%02X' % sum([(128 >> x) * symbols[c,y,x] for x in range(8)]) for y in range(8)])
print ']'
print
print 'byte = ['
i = 0
for c in range(256):
    print '    ['
    for y in range(8):
        print '        [%s],' % ','.join(['1' if symbols[c,y,x] else '0' for x in range(8)]),
        print '    #', ''.join(['*' if symbols[c,y,x] else ' ' for x in range(8)])
    print '    ],',
print ']'

