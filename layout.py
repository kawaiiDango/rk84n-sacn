from enum import Enum
import operator

COLS = 16
ROWS = 6

Keys = Enum(
    "Keys",
    [
        "esc",
        "f1",
        "f2",
        "f3",
        "f4",
        "f5",
        "f6",
        "f7",
        "f8",
        "f9",
        "f10",
        "f11",
        "f12",
        "printscr",
        "pause",
        "delete",

        "tilde",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "zero",
        "minus",
        "equal",
        "backspace",
        "home",

        "tab",
        "q",
        "w",
        "e",
        "r",
        "t",
        "y",
        "u",
        "i",
        "o",
        "p",
        "bracket_left",
        "bracket_right",
        "backslash",
        "end",

        "capslock",
        "a",
        "s",
        "d",
        "f",
        "g",
        "h",
        "j",
        "k",
        "l",
        "semicolon",
        "quote",
        "enter",
        "pageup",

        "shift_left",
        "z",
        "x",
        "c",
        "v",
        "b",
        "n",
        "m",
        "comma",
        "period",
        "slash",
        "shift_right",
        "up",
        "pagedown",

        "ctrl_left",
        "win_left",
        "alt_left",
        "space",
        "alt_right",
        "fn",
        "ctrl_right",
        "left",
        "down",
        "right",

        "unused",
    ]
)


keys_matrix = [
    [Keys.esc, Keys.f1, Keys.f2, Keys.f3, Keys.f4, Keys.f5, Keys.f6, Keys.f7, Keys.f8,
        Keys.f9, Keys.f10, Keys.f11, Keys.f12, Keys.printscr, Keys.pause, Keys.delete],
    [Keys.tilde, Keys.one, Keys.two, Keys.three, Keys.four, Keys.five, Keys.six, Keys.seven, Keys.eight,
        Keys.nine, Keys.zero, Keys.minus, Keys.equal, Keys.backspace, Keys.backspace, Keys.home],
    [Keys.tab, Keys.q, Keys.w, Keys.e, Keys.r, Keys.t, Keys.y, Keys.u, Keys.i, Keys.o, Keys.p,
        Keys.bracket_left, Keys.bracket_right, Keys.backslash, Keys.backslash, Keys.end],
    [Keys.capslock, Keys.capslock, Keys.a, Keys.s, Keys.d, Keys.f, Keys.g, Keys.h, Keys.j,
        Keys.k, Keys.l, Keys.semicolon, Keys.quote, Keys.enter, Keys.enter, Keys.pageup],
    [Keys.shift_left, Keys.shift_left, Keys.z, Keys.x, Keys.c, Keys.v, Keys.b, Keys.n, Keys.m,
        Keys.comma, Keys.period, Keys.slash, Keys.shift_right, Keys.shift_right, Keys.up, Keys.pagedown],
    [Keys.ctrl_left, Keys.win_left, Keys.alt_left, Keys.space, Keys.space, Keys.space, Keys.space, Keys.space,
        Keys.space, Keys.space, Keys.alt_right, Keys.fn, Keys.ctrl_right, Keys.left, Keys.down, Keys.right],
]  # 16 x 6

sequence = [
    Keys.esc,
    Keys.tilde,
    Keys.tab,
    Keys.capslock,
    Keys.shift_left,
    Keys.ctrl_left,
    Keys.f1,
    Keys.one,
    Keys.q,
    Keys.a,
    Keys.z,
    Keys.win_left,
    Keys.f2,
    Keys.two,
    Keys.w,
    Keys.s,
    Keys.x,
    Keys.alt_left,
    Keys.f3,
    Keys.three,
    Keys.e,
    Keys.d,
    Keys.c,
    Keys.unused,
    Keys.f4,
    Keys.four,
    Keys.r,
    Keys.f,
    Keys.v,
    Keys.unused,
    Keys.f5,
    Keys.five,
    Keys.t,
    Keys.g,
    Keys.b,
    Keys.space,
    Keys.f6,
    Keys.six,
    Keys.y,
    Keys.h,
    Keys.n,
    Keys.unused,
    Keys.f7,
    Keys.seven,
    Keys.u,
    Keys.j,
    Keys.m,
    Keys.unused,
    Keys.f8,
    Keys.eight,
    Keys.i,
    Keys.k,
    Keys.comma,
    Keys.alt_right,
    Keys.f9,
    Keys.nine,
    Keys.o,
    Keys.l,
    Keys.period,
    Keys.fn,
    Keys.f10,
    Keys.zero,
    Keys.p,
    Keys.semicolon,
    Keys.slash,
    Keys.ctrl_right,
    Keys.f11,
    Keys.minus,
    Keys.bracket_left,
    Keys.quote,
    Keys.shift_right,
    Keys.unused,
    Keys.f12,
    Keys.equal,
    Keys.bracket_right,
    Keys.unused,
    Keys.unused,
    Keys.unused,
    Keys.printscr,
    Keys.backspace,
    Keys.backslash,
    Keys.enter,
    Keys.unused,
    Keys.left,
    Keys.pause,
    Keys.unused,
    Keys.unused,
    Keys.unused,
    Keys.up,
    Keys.down,
    Keys.delete,
    Keys.home,
    Keys.end,
    Keys.pageup,
    Keys.pagedown,
    Keys.right,
]


def colors_list_to_keys_dict(colors_list: list[tuple[int]]):
    colors = {}
    count = 0
    total_rgb = (0, 0, 0)
    prev_key = Keys.unused

    for i, color in enumerate(colors_list):
        key = keys_matrix[i // COLS][i % COLS]
        if key == prev_key:
            # take avg of colors for multi span keys
            count += 1
            total_rgb = tuple(map(operator.add, total_rgb, color))
            colors[key] = tuple(c//count for c in total_rgb)
        else:
            count = 1
            total_rgb = color
            colors[key] = color

        prev_key = key

    return colors


def colors_dict_to_usb_packets(colors: dict[Keys, tuple[int]]) -> list[bytes]:
    buffer = bytearray(65*7)

    buffer[0] = 0x0a
    buffer[1] = 0x07
    buffer[2] = 0x01

    buffer[3] = 0x06
    buffer[4] = 0x00

    # save per key lighting
    # buffer[0] = 0x0a
    # buffer[1] = 0x07
    # buffer[2] = 0x01

    # buffer[3] = 0x03
    # buffer[4] = 0x7e
    # buffer[5] = 0x01

    buffer[65*1] = 0x0a
    buffer[65*1+1] = 0x07
    buffer[65*1+2] = 0x02

    buffer[65*2] = 0x0a
    buffer[65*2+1] = 0x07
    buffer[65*2+2] = 0x03

    buffer[65*3] = 0x0a
    buffer[65*3+1] = 0x07
    buffer[65*3+2] = 0x04

    buffer[65*4] = 0x0a
    buffer[65*4+1] = 0x07
    buffer[65*4+2] = 0x05

    buffer[65*5] = 0x0a
    buffer[65*5+1] = 0x07
    buffer[65*5+2] = 0x06

    buffer[65*6] = 0x0a
    buffer[65*6+1] = 0x07
    buffer[65*6+2] = 0x07

    idx = 5
    for key in sequence:
        color = colors.get(key, (0, 0, 0))

        for c in color:
            while buffer[idx] != 0:
                idx += 1

            buffer[idx] = c
            idx += 1

    return [bytes(buffer[i:i+65]) for i in range(0, 65*7, 65)]
