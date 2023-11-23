"""
Control/Read TMate2
"""
import hid
from bitstruct import *
from time import sleep


read_fmt = 'p8' + 's16' * 3 + 'b1' * 8 + 'p7' + 'b1'

format = ('p8'
            + 'b1' * 7 + 'p1'                   # 1
            + 'b1' * 8                          # 2
            + 'b1' * 8                          # 3
            + 'p3' + 'b1' + 'u4'                # 4
            + 'p3' + 'b1' * 2  + 'u3'           # 5
            + 'p3' + 'b1' + 'u4'                # 6
            + 'p3' + 'b1' * 2  + 'u3'           # 7
            + 'p3' + 'b1' + 'u4'                # 8
            + 'p2' + 'b1' * 3 + 'u3'            # 9
            + 'p2' + 'b1' * 2 + 'u4'            # 10
            + 'p2' + 'b1' * 3 + 'u3'            # 11
            + 'p3' + 'b1' + 'u4'                # 12
            + 'p3' + 'b1' * 2  + 'u3'           # 13
            + 'p3' + 'b1' + 'u4'                # 14
            + 'p3' + 'b1' * 2 + 'u3'            # 15
            + 'p2' + 'b1' * 2 + 'u4'            # 16
            + 'p2' + 'b1' + 'p1' + 'b1' + 'u3'  # 17
            + 'p4' + 'u4'                       # 18
            + 'p2' + 'b1' + 'p1' + 'b1' + 'u3'  # 19
            + 'p2' + 'b1' * 2 + 'u4'            # 20
            + 'p2' + 'b1' * 3 + 'u3'            # 21
            + 'b1' * 8                          # 22
            + 'b1' * 4 + 'p1' + 'b1' * 3        # 23           
            + 'b1' * 4 + 'p3' + 'b1'            # 24               
            + 'b1' * 3 + 'p5'                   # 25
            + 'b1' * 4 + 'p3' + 'b1'            # 26
            + 'b1' * 3 + 'p5'                   # 27
            + 'b1' * 4 + 'p3' + 'b1'            # 28
            + 'b1' * 4 + 'p3' + 'b1'            # 29
            + 'b1' * 4 + 'p4'                   # 30
            + 'b1' * 4 + 'p2' + 'b1' * 2        # 31    
            + 'b1' * 4 + 'p1' + 'b1' * 3        # 32
            + 'p6' + 'b1' * 2                   # 33
            + 'u8' * 11)                        # 34 .. 35

names = ['e1', 'nr', 'vfo', 's', 'tx', 'rx', 'lp',                                                  # 1
            'vol', 'nb', 'a', 'smeter_1', 'smeter_bar3', 'smeter_bar2', 'smeter_bar1', 'att',       # 2
            'rfg', 'an', 'b', 'smeter_3', 'smeter_5', 'smeter_7', 's_meter_9', 'smeter_line',       # 3
            'sql', 'main_9l',                                                                       # 4
            'drv', 'underline_9', 'main_9r',                                                        # 5
            'nr2', 'main_8l',                                                                       # 6
            'nb2', 'underline_8', 'main_8r',                                                        # 7
            'an2', 'main_7l',                                                                       # 8
            'smeter_10', 'e2', 'underline_7', 'main_7r',                                            # 9
            'smeter_plus20', 'dot1', 'main_6l',                                                     # 10
            'smeter_20', 'high', 'underline_6', 'main_6r',                                          # 11
            'low', 'main_5l',                                                                       # 12
            'shift', 'underline_5', 'main_5r',                                                      # 13
            'rit', 'main_4l',                                                                       # 14
            'xit', 'underline_4', 'main_4r',                                                        # 15
            'smeter_plus40', 'dot2', 'main_3l',                                                     # 16
            'smeter_40', 'underline_3', 'main_3r',                                                  # 17
            'main_2l',                                                                              # 18
            'smeter_plus60', 'underline_2', 'main_2r',                                              # 19
            'smeter_60', 'err', 'main_1l',                                                          # 20
            'w', 'w_fm', 'underline_1', 'main_1r',                                                  # 21
            'sam', 'usb', 'fm', 'dsb', 'dig_minus', 'dig_plus', 'cw_minus', 'cw_plus',              # 22
            'am', 'lsb', 'cw', 'dbm', 'stereo', 'dig', 'drm',                                       # 23
            'smeter_1a', 'smeter_1b', 'smeter_1c', 'smeter_1d', 'hz',                               # 24
            'smeter_1f', 'smeter_1g', 'smeter_1e',                                                  # 25    
            'smeter_2a', 'smeter_2b', 'smeter_2c', 'smeter_2d', 'k',                                # 26
            'smeter_2f', 'smeter_2g', 'smeter_2e',                                                  # 27
            'smeter_3a', 'smeter_3b', 'smeter_3c', 'smeter_3d', 'mw_w',                             # 28    
            'smeter_3f', 'smeter_3g', 'smeter_3e', 'smeter_db_minus', 'mw_m',                       # 29
            'smeter_bar12', 'smeter_bar13', 'smeter_bar14', 'smeter_bar15',                         # 30
            'smeter_bar11', 'smeter_bar10', 'smeter_bar9', 'smeter_bar9', 'pre_2', 'pre_1',         # 31
            'smeter_bar4', 'smeter_bar5', 'smeter_bar6', 'smeter_bar7', 'att_1', 'pre', 'att_2',    # 32
            'lock', 'usb_led',                                                                      # 33
            'rgb_red', 'rgb_green', 'rgb_blue', 'contrast', 'refresh',                              # 34
            'enc_speed1', 'enc_speed2', 'enc_speed3', 'enc_trans12', 'enc_trans23', 'speed_trans',  # 35
        ] 

digit7_layout = {
    -1: '',
    0: 'abcdef',
    1: 'bc',
    2: 'abged',
    3: 'abcdg',
    4: 'bcgf',
    5: 'afgcd',
    6: 'afedcg',
    7: 'abc',
    8: 'abcdefg',
    9: 'gfabcd'
}

i = hid.Device(0x1721, 0x0614)
i1 = hid.Device(0x1721, 0x0614)

rd = dict(zip(names, (False,) * (len(names))))


digit_main_layout = (
    #  defg    cba
    (0b1101, 0b111),
    (0b0000, 0b110),
    (0b1110, 0b011),
    (0b1010, 0b111),
    (0b0011, 0b110),
    (0b1011, 0b101),
    (0b1111, 0b101),
    (0b0000, 0b111),
    (0b1111, 0b111),
    (0b1011, 0b111),
)

def main_number(value):
    for i in range(1,10):
        number = value % 10
        value = value // 10
        rd['main_%dl' % i], rd['main_%dr' % i] = (0,0) if number == 0 and value == 0 else digit_main_layout[number]

def smeter_number(value):

    def digit(position, value):
        for c in 'abcdefg':
            rd['smeter_%d%c' % (position, c)] = c in digit7_layout[value]    

    rd['smeter_db_minus'] = value < 0
    value = abs(value)
    for i in range(1,4):
        number = value % 10
        value = value // 10
        if number == 0 and value == 0:
            number = -1
        digit(i, number)


def smeter_bars(value):
    for i in range(1,16):
        rd['smeter_bar%d' %i] = value >= i

def test():
    # rd['pre'] = True
    # rd['pre_1'] = True
    # rd['pre_2'] = True
    # rd['att'] = True
    # rd['att_1'] = True
    # rd['att_2'] = True
    # for j in range(0,16):
    #     rd['smeter_bar%d' % j] = True
    # for j in 'g':
    #     for k in range(1,4):
    #         rd['smeter_%d%c' % (k,j)] = True
    #     for k in range(1,10):
    #         rd['main_%d%c' % (k,j)] = True
    # for j in range(1,10):
    #     rd['underline_%d' %j] = True
    rd['smeter_db_minus'] = True
    # # rd['smeter_plus20'] = True
    # # rd['main_4c'] = True
    # # rd['main_4b'] = True
    # # rd['main_4a'] = True
    # # rd['hz'] = True
    rd['lock'] = True
    rd['usb_led'] = True
    # rd['dot1'] = True
    # rd['dot2'] = True
    rd['smeter_line'] = True
    rd['rx'] = True
    rd['s'] = True
    rd['smeter_1'] = True
    rd['smeter_3'] = True
    rd['smeter_5'] = True
    rd['smeter_7'] = True
    rd['smeter_9'] = True
    rd['smeter_10'] = True
    rd['smeter_plus20'] = True
    rd['smeter_20'] = True
    rd['smeter_plus40'] = True
    rd['smeter_40'] = True
    rd['smeter_plus60'] = True
    rd['smeter_60'] = True
    rd['e1'] = True
    rd['e2'] = True
    # rd['k'] = True
    rd['hz'] = True
    rd['vfo'] = True
    rd['a'] = True
    rd['lsb'] = True
    rd['dbm'] = True
 
    # for j in range(1,10):
    #     digit_main(j,j,rd)

    main_value = 0

    smeter_number(120)
    smeter_bars(10)

    # for j in range(1,4):
    #     digit_smeter(j,j-1,rd)

    rd['enc_speed1'] = 1
    rd['enc_speed2'] = 1
    rd['enc_speed3'] = 1

    rd['rgb_red'] = 0xf
    rd['rgb_green'] = 0xf
    rd['rgb_blue'] = 0xf
    rd['refresh'] = 1

    data = bytearray(b'\x00' * 45)    
    pack_into_dict(format, names, data, 0, rd)

    b = bytes(data)

    old_d = list(unpack(read_fmt, i1.read(9)))

    STEPS = 100
    ctr = STEPS
    while 1:        
        d = unpack(read_fmt, i1.read(9))
        # print (d)
        if (d[0] != old_d[0]):
            main_value += (old_d[0] - d[0])
            old_d[0] = d[0]
            if main_value < 0:
                main_value = 0
            if main_value > 30_000_000:
                main_value = 30_000_000
            main_number(main_value)
            pack_into_dict(format, names, data, 0, rd)
            b = bytes(data)

        if (d[1] != old_d[1]):
            print ("e1 enc: %d" % (d[1] - old_d[1]))
            old_d[1] = d[1]
        if (d[2] != old_d[2]):
            print ("e2 enc: %d" % (d[2] - old_d[2]))
            old_d[2] = d[2]
        quit = False
        for f in range(3,12):
            if d[f] != old_d[f]:
                print ('%d: %r' % (f, d[f]))
                old_d[f] = d[f]
                if f == 4:
                    quit = True
                    break
        if quit:
            break
        ctr -= 1
        if ctr == 0:
            ctr = STEPS
            i.write(b)
        sleep(0.001)
        
                   


if __name__ == '__main__':
    test()