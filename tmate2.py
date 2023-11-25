"""
Control/Read TMate2
"""
import hid
import bitstruct.c as bitstruct
# import bitstruct
from time import sleep

from format import read_format, write_format
from names import read_names, write_names
from layout import digit_main_layout, digit_smeter_layout

i = hid.Device(0x1721, 0x0614)
# i1 = hid.Device(0x1721, 0x0614)

display_data = bytearray(b'\x00' * 45)
display_dict = dict(zip(write_names, (0,) * (len(write_names))))

def main_number(value):
    for i in range(1,10):
        number = value % 10
        value = value // 10
        display_dict['main_%dl' % i], display_dict['main_%dr' % i] = (0,0) if number == 0 and value == 0  and i > 1 else digit_main_layout[number+16]

def main_string(text, rotate):
    for i in range(0,9):
        pos = (i+rotate)
        display_dict['main_%dl' % (9-i)], display_dict['main_%dr' % (9-i)] = (0,0) if pos >= len(text) else digit_main_layout[ord(text[pos]) - 32]

def smeter_string(text, rotate):
    for i in range(0,3):
        pos = (i+rotate)
        display_dict['smeter_%dl' % (3-i)], display_dict['smeter_%dr' % (3-i)] = (0,0) if pos >= len(text) else digit_smeter_layout[ord(text[pos]) - 32]

def smeter_number(value):
    display_dict['smeter_db_minus'] = value < 0
    value = abs(value)
    for i in range(1,4):
        number = value % 10
        value = value // 10
        display_dict['smeter_%dl' % i], display_dict['smeter_%dr' % i] = (0,0) if number == 0 and value == 0  and i > 1 else digit_smeter_layout[number+16]

def smeter_bars(value):
    for i in range(1,16):
        display_dict['smeter_bar%d' %i] = value >= i

def update_display_dict():
    bitstruct.pack_into_dict(write_format, write_names, display_data, 0, display_dict)

def read_state():
    return bitstruct.unpack_dict(read_format, read_names, i.read(9))

def byte_swap16(value):
    return ((value & 0xff) << 8) | (value >> 8)

def encoder_delta(which, old, current):
    old_value = byte_swap16(old[which])
    current_value = byte_swap16(current[which])
    if current_value == old_value:
        return 0
    else:
        old[which] = current[which]
        if (current_value >= old_value):
            delta = current_value - old_value
        else:
            delta = -(old_value - current_value)
        return delta

def test():
    # display_dict['pre'] = True
    # display_dict['pre_1'] = True
    # display_dict['pre_2'] = True
    # display_dict['att'] = True
    # display_dict['att_1'] = True
    # display_dict['att_2'] = True
    # display_dict['smeter_db_minus'] = True
    # display_dict['lock'] = True
    # display_dict['usb_led'] = True
    # display_dict['dot1'] = True
    # display_dict['dot2'] = True
    # display_dict['smeter_line'] = True
    # display_dict['rx'] = True
    # display_dict['s'] = True
    # display_dict['smeter_1'] = True
    # display_dict['smeter_3'] = True
    # display_dict['smeter_5'] = True
    # display_dict['smeter_7'] = True
    # display_dict['smeter_9'] = True
    # display_dict['smeter_10'] = True
    # display_dict['smeter_plus20'] = True
    # display_dict['smeter_20'] = True
    # display_dict['smeter_plus40'] = True
    # display_dict['smeter_40'] = True
    # display_dict['smeter_plus60'] = True
    # display_dict['smeter_60'] = True
    # display_dict['e1'] = True
    # display_dict['e2'] = True
    # display_dict['k'] = True
    display_dict['hz'] = True
    # display_dict['vfo'] = True
    # display_dict['a'] = True
    # display_dict['lsb'] = True
    # display_dict['dbm'] = True
    # display_dict['mw_w'] = True
    # display_dict['mw_m'] = True

    main_value = 0
    main_number(main_value)
    # rotate = 0
    crawl = "0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ " * 2
    # main_string(crawl, rotate)
    # smeter_string(crawl, rotate)

    # smeter_number(-0)
    # smeter_bars(4)

    display_dict['enc_speed1'] = 1
    display_dict['enc_speed2'] = 10
    display_dict['enc_speed3'] = 100

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
            delta = encoder_delta('main', old_d, d)
            if delta:
                main_value -= delta
                if main_value < 0:
                    main_value = 0
                if main_value > 30_000_000:
                    main_value = 30_000_000
                main_number(main_value)
                display_dict['dot2'] = main_value > 1_000
                display_dict['dot1'] = main_value > 1_000_000
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

            # old_d = d

        ctr -= 1
        if ctr == 0:
            ctr = STEPS
            # rotate += 1
            # main_string(crawl, rotate)
            # smeter_string(crawl, rotate)
            # update_display_dict()
            i.write(bytes(display_data))
        if not d['main_b']:
            print("Done.")
            break
        sleep(0.001)


if __name__ == '__main__':
    test()