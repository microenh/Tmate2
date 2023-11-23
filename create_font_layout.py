"""
Create font layout description for 7 segment displays

On the Tmate 2, the 7 segments are bits in two different (non-contiguous) offsets. In addition, the layouts
for the main digits and the S-Meter digits are different.

Segment ID
          a
        +---+
      f |   | b
     g  +---+
      e |   | c
        +---+
          d

arrangement main display
    first word:  defg
    second word: cba

arrangement s-meter display
    first word:  fge
    second word: abcd

input:
    arrangement = ('defg', 'cba')
    format = {
         0 : 'abcdef',
         1 : 'bc',
        ...
         9 : 'gfabcd',
        'A': 'abcefg',
    }
        
output:
    layout = (
        #  degf    cba
        (0b1101, 0b111),    # 0
        (0b0000, 0b110),    # 1
        (0b1110, 0b011),    # 2
        (0b1010, 0b111),    # 3
        (0b0011, 0b110),    # 4
        (0b1011, 0b101),    # 5
        (0b1111, 0b101),    # 6
        (0b0000, 0b111),    # 7
        (0b1111, 0b111),    # 8
        (0b1011, 0b111),    # 9
    )
"""

#  !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ

format = {
    ' ': '',
    '!': 'b',
    '"': 'bf',
    '#': 'bcef',
    '$': 'afgcd',
    '%': 'fc',
    '&': '',
    "'": 'f',
    '(': 'afed',
    ')': 'abcd',
    '*': 'fgebc',
    '+': 'bgc',
    ',': 'e',
    '-': 'g',
    '.': 'e',
    '/': 'be',
    '0': 'abcdef',
    '1': 'bc',
    '2': 'abged',
    '3': 'abcdg',
    '4': 'bcgf',
    '5': 'afgcd',
    '6': 'afedcg',
    '7': 'abc',
    '8': 'abcdefg',
    '9': 'gfabcd',
    ':': 'e',
    ';': 'e',
    '<': 'afed',
    '=': 'gd',
    '>': 'abcd',
    '?': 'abcge',
    '@': 'gbafed',
    'A': 'abcefg',
    'B': 'fedcg',
    'C': 'ged',
    'D': 'gedcb',
    'E': 'afedg',
    'F': 'afeg',
    'G': 'afedcg',
    'H': 'fegc',
    'I': 'c',
    'J': 'dcb',
    'K': 'fegc',
    'L': 'fed',
    'M': 'egc',
    'N': 'egc',
    'O': 'egcd',
    'P': 'efabg',
    'Q': 'egcd',
    'R': 'fg',
    'S': 'afgcd',
    'T': 'bedg',
    'U': 'edc',
    'V': 'edc',
    'W': 'edc',
    'X': 'bcefg',
    'Y': 'fgbc',
    'Z': 'abged',
}

# arrangement = ('degf', 'cba')
arrangement = ('fge', 'abcd')


def main():
    print ('layout = (')
    print ('    #  %s    %s' % arrangement)
    for k,v in format.items():
        r = []
        for a in arrangement:
            i = '0b'
            for c in a:
                i += '1' if c in v else '0'
            r.append(i)
        print ("    (%s), # %s" % (', '.join(r), k))
    print (")")

if __name__ == '__main__':
    main()
    # for i in range(32, 133):
    #     print (chr(i), end='')
    # print()
