"""
Control/Read TMate2
"""
import hid
from bitstruct import *
from time import sleep

format = ('p8'
            + 'b1' * 7 + 'p1'                   # 1
            + 'b1' * 8                          # 2
            + 'b1' * 8                          # 3
            + 'p3' + 'b1' * 5                   # 4
            + 'p3' + 'b1' * 5                   # 5
            + 'p3' + 'b1' * 5                   # 6
            + 'p3' + 'b1' * 5                   # 8
            + 'p3' + 'b1' * 5                   # 9
            + 'p2' + 'b1' * 6                   # 10
            + 'p2' + 'b1' * 6                   # 11
            + 'p2' + 'b1' * 6                   # 12
            + 'p3' + 'b1' * 5                   # 13
            + 'p3' + 'b1' * 5                   # 14
            + 'p3' + 'b1' * 5                   # 15
            + 'p3' + 'b1' * 5                   # 15
            + 'p2' + 'b1' * 6                   # 16
            + 'p2' + 'b1' + 'p1' + 'b1' * 4     # 17
            + 'p4' + 'b1' * 4                   # 17
            + 'p2' + 'b1' + 'p1' + 'b1' * 4     # 18
            + 'p2' + 'b1' * 6                   # 19
            + 'p2' + 'b1' * 6                   # 19
            + 'b1' * 8                          # 20
            + 'b1' * 4 + 'p1' + 'b1' * 3        # 21           
            + 'b1' * 4 + 'p3' + 'b1'            # 22               
            + 'b1' * 3 + 'p5'                   # 23
            + 'b1' * 4 + 'p3' + 'b1'            # 24
            + 'b1' * 3 + 'p5'                   # 25
            + 'b1' * 4 + 'p3' + 'b1'            # 26
            + 'b1' * 4 + 'p3' + 'b1'            # 27
            + 'b1' * 4 + 'p4'                   # 28
            + 'b1' * 4 + 'p2' + 'b1' * 2        # 29    
            + 'b1' * 4 + 'p1' + 'b1' * 3        # 30
            + 'p6' + 'b1' * 2                   # 31
            + 'u8' * 11)                        # 32 .. 35

names = ['e1', 'nr', 'vfo', 's', 'tx', 'rx', 'lp',                                                  # 1
            'vol', 'nb', 'a', 'smeter_1', 'smeter_bar3', 'smeter_bar2', 'smeter_bar1', 'att',       # 2
            'rfg', 'an', 'b', 'smeter_3', 'smeter_5', 'smeter_7', 's_meter_9', 'smeter_line',       # 3
            'sql', 'main_9d', 'main_9e', 'main_9g', 'main_9f',                                      # 4
            'drv', 'underline_9', 'main_9c', 'main_9b', 'main_9a',                                  # 5
            'nr2', 'main_8d', 'main_8e', 'main_8g', 'main_8f',                                      # 6
            'nb2', 'underline_8', 'main_8c', 'main_8b', 'main_8a',                                  # 7
            'an2', 'main_7d', 'main_7e', 'main_7g', 'main_7f',                                      # 8
            'smeter_10', 'e2', 'underline_7', 'main_7c', 'main_7b', 'main_7a',                      # 9
            'smeter_plus20', 'dot1', 'main_6d', 'main_6e', 'main_6g', 'main_6f',                    # 10
            'smeter_20', 'high', 'underline_6', 'main_6c', 'main_6b', 'main_6a',                    # 11
            'low', 'main_5d', 'main_5e', 'main_5g', 'main_5f',                                      # 12
            'shift', 'underline_5', 'main_5c', 'main_5b', 'main_5a',                                # 13
            'rit', 'main_4d', 'main_4e', 'main_4g', 'main_4f',                                      # 14
            'xit', 'underline_4', 'main_4c', 'main_4b', 'main_4a',                                  # 15
            'smeter_plus40', 'dot2', 'main_3d', 'main_3e', 'main_3g', 'main_3f',                    # 16
            'smeter_40', 'underline_3', 'main_3c', 'main_3b', 'main_3a',                            # 17
            'main_2d', 'main_2e', 'main_2g', 'main_2f',                                             # 18
            'smeter_plus60', 'underline_2', 'main_2c', 'main_2b', 'main_2a',                        # 19
            'smeter_60', 'err', 'main_1d', 'main_1e', 'main_1g', 'main_1f',                         # 20
            'w', 'w_fm', 'underline_1', 'main_1c', 'main_1b', 'main_1a',                            # 21
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


def main_number(value, data):
    def digit(position, value, data):
        for c in 'abcdefg':
            data['main_%d%c' % (position, c)] = c in digit7_layout[value]

    for i in range(1,10):
        number = value % 10
        value = value // 10
        if number == 0 and value == 0:
            number = -1
        digit(i, number, data)


def smeter_number(value, data):

    def digit(position, value, data):
        for c in 'abcdefg':
            data['smeter_%d%c' % (position, c)] = c in digit7_layout[value]    

    data['smeter_db_minus'] = value < 0
    value = abs(value)
    for i in range(1,4):
        number = value % 10
        value = value // 10
        if number == 0 and value == 0:
            number = -1
        digit(i, number, data)


def smeter_bars(value, data):
    for i in range(1,16):
        data['smeter_bar%d' %i] = value >= i

def test():
    i = hid.Device(0x1721, 0x0614)
    i1 = hid.Device(0x1721, 0x0614)
 
    rd = dict(zip(names, (False,) * (len(names))))
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

    smeter_number(120, rd)
    smeter_bars(10, rd)

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

    read_fmt = '>' + 's16' * 4
    old_d = list(unpack(read_fmt, i1.read(9), 8))

    STEPS = 100
    ctr = STEPS
    while 1:        
        d = unpack(read_fmt, i1.read(9))
        if (d[0] != old_d[0]):
            main_value += (old_d[0] - d[0])
            old_d[0] = d[0]
            if main_value < 0:
                main_value = 0
            if main_value > 30_000_000:
                main_value = 30_000_000
            main_number(main_value, rd)
            pack_into_dict(format, names, data, 0, rd)
            b = bytes(data)

        if (d[1] != old_d[1]):
            print ("e1 enc: %d" % (d[1] - old_d[1]))
            old_d[1] = d[1]
        if (d[2] != old_d[2]):
            print ("e2 enc: %d" % (d[2] - old_d[2]))
            old_d[2] = d[2]
        if (d[3] != old_d[3]):
            break
        ctr -= 1
        if ctr == 0:
            ctr = STEPS
            i.write(b)
        sleep(0.001)
        
                   


if __name__ == '__main__':
    test()