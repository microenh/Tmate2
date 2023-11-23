"""
Control/Read TMate2
"""
import hid
import bitstruct.c as bitstruct
# import bitstruct
from time import sleep

read_format = 'p8' + 'u16' * 3 + 'b1' * 8 + 'p7' + 'b1'
read_names = ['main', 'e2', 'e1', 'e2_b', 'main_b', 'f6', 'f5', 'f4', 'f3', 'f2', 'f1', 'e1_b']

write_format = (
    'p8' + 'b1' * 7 + 'p1'              # 1
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
    + 'u8' * 11                         # 34 .. 35
)

write_names = [
    'e1', 'nr', 'vfo', 's', 'tx', 'rx', 'lp',                                               # 1
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
    'enc_speed1', 'enc_speed2', 'enc_speed3', 'enc_trans12', 'enc_trans23', 'speed_trans'   # 35
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

display_data = bytearray(b'\x00' * 45)
display_dict = dict(zip(write_names, (0,) * (len(write_names))))

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
        display_dict['main_%dl' % i], display_dict['main_%dr' % i] = (0,0) if number == 0 and value == 0  and i > 1 else digit_main_layout[number]

def smeter_number(value):

    def digit(position, value):
        for c in 'abcdefg':
            display_dict['smeter_%d%c' % (position, c)] = c in digit7_layout[value]

    display_dict['smeter_db_minus'] = value < 0
    value = abs(value)
    for i in range(1,4):
        number = value % 10
        value = value // 10
        if number == 0 and value == 0:
            number = -1
        digit(i, number)


def smeter_bars(value):
    for i in range(1,16):
        display_dict['smeter_bar%d' %i] = value >= i


def update_display_dict():
    bitstruct.pack_into_dict(write_format, write_names, display_data, 0, display_dict)

def read_state():
    return bitstruct.unpack_dict(read_format, read_names, i1.read(9))

def byte_swap16(value):
    return ((value & 0xff) << 8) | (value >> 8)

def encoder_delta(which, old, current):
    old_value = old[which]
    current_value = current[which]
    return 0 if current_value == old_value else int(byte_swap16(old_value)) - int(byte_swap16(current_value))


def test():
    display_dict['pre'] = True
    display_dict['pre_1'] = True
    display_dict['pre_2'] = True
    display_dict['att'] = True
    display_dict['att_1'] = True
    display_dict['att_2'] = True
    display_dict['smeter_db_minus'] = True
    display_dict['lock'] = True
    display_dict['usb_led'] = True
    # display_dict['dot1'] = True
    # display_dict['dot2'] = True
    display_dict['smeter_line'] = True
    display_dict['rx'] = True
    display_dict['s'] = True
    display_dict['smeter_1'] = True
    display_dict['smeter_3'] = True
    display_dict['smeter_5'] = True
    display_dict['smeter_7'] = True
    display_dict['smeter_9'] = True
    display_dict['smeter_10'] = True
    display_dict['smeter_plus20'] = True
    display_dict['smeter_20'] = True
    display_dict['smeter_plus40'] = True
    display_dict['smeter_40'] = True
    display_dict['smeter_plus60'] = True
    display_dict['smeter_60'] = True
    display_dict['e1'] = True
    display_dict['e2'] = True
    display_dict['k'] = True
    display_dict['hz'] = True
    display_dict['vfo'] = True
    display_dict['a'] = True
    display_dict['lsb'] = True
    display_dict['dbm'] = True

    main_value = 0
    main_number(main_value)

    smeter_number(120)
    smeter_bars(10)

    display_dict['enc_speed1'] = 1
    display_dict['enc_speed2'] = 1
    display_dict['enc_speed3'] = 1

    display_dict['rgb_red'] = 0xf
    display_dict['rgb_green'] = 0xf
    display_dict['rgb_blue'] = 0xf
    display_dict['refresh'] = 1

    update_display_dict()
    i.write(bytes(display_data))

    old_d = read_state()

    STEPS = 100
    ctr = STEPS
    while 1:
        d = read_state()
        if d != old_d:
            # print (d)
            delta = encoder_delta('main', old_d, d)
            if delta:
                main_value += delta
                if main_value < 0:
                    main_value = 0
                if main_value > 30_000_000:
                    main_value = 30_000_000
                main_number(main_value)
                update_display_dict()

            # if (d[1] != old_d[1]):
            #     print ("e1 enc: %d" % (d[1] - old_d[1]))
            #     old_d[1] = d[1]

            # if (d[2] != old_d[2]):
            #     print ("e2 enc: %d" % (d[2] - old_d[2]))
            #     old_d[2] = d[2]

            # quit = False
            # for f in range(3,12):
            #     if d[f] != old_d[f]:
            #         print ('%d: %r' % (f, d[f]))
            #         old_d[f] = d[f]
            #         if f == 4:
            #             quit = True
            #             break
            # if quit:
            #     break

            old_d = d

        ctr -= 1
        if ctr == 0:
            ctr = STEPS
            i.write(bytes(display_data))
        sleep(0.001)




if __name__ == '__main__':
    test()