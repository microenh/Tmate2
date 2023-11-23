typedef struct _display_bitfield {
    unsigned int :8,

    unsigned int e1: 1,
    unsigned int nr: 1,
    unsigned int vfo: 1,
    unsigned int s: 1,
    unsigned int tx: 1,
    unsigned int rx: 1,
    unsigned int lp: 1,
    unsigned int: 1,

    unsigned int vol: 1,
    unsigned int nb: 1,
    unsigned int a: 1,
    unsigned int smeter_1: 1,
    unsigned int smeter_bar_3: 1,
    unsigned int smeter_bar_2: 1,
    unsigned int smeter_bar_1: 1,
    unsigned int att: 1,

    unsigned int rfg: 1,
    unsigned int an: 1,
    unsigned int b: 1,
    unsigned int smeter_3: 1,
    unsigned int smeter_5: 1,
    unsigned int smeter_7: 1,
    unsigned int smeter_9: 1,
    unsigned int smeter_line: 1,

    unsigned int: 3,
    unsigned int sql: 1,
    unsigned int main_9l: 4,

    unsigned int: 3,
    unsigned int drv: 1,
    unsigned int underline_9: 1,
    unsigned int main_9r: 3,

    // continue



} DISPLAY_BITFIELD