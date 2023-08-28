GENERAL_LTE = {
    1.4: [(5, 0), (6, 0), (1, 0), (1, 5)],
    3: [(4, 0), (15, 0), (1, 0), (1, 14), ],
    5: [(8, 0), (25, 0), (1, 0), (1, 24), ],
    10: [(12, 0), (50, 0), (1, 0), (1, 49), ],
    15: [(16, 0), (75, 0), (1, 0), (1, 74), ],
    20: [(18, 0), (100, 0), (1, 0), (1, 99), ],
}

GENERAL_FR1 = {
    5: {
        15: {'DFTS': [(2, 0), (2, 23), (1, 0), (1, 24), (25, 0), (12, 6), (1, 1), (1, 23)],
             'CP': [(2, 0), (2, 23), (1, 0), (1, 24), (25, 0), (13, 6), (1, 1), (1, 23)],
             },
        30: {'DFTS': [(2, 0), (2, 9), (1, 0), (1, 10), (10, 0), (5, 2), (1, 1), (1, 9)],
             'CP': [(2, 0), (2, 9), (1, 0), (1, 10), (11, 0), (5, 2), (1, 1), (1, 9)],
             },
        60: {'DFTS': [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None),
                      (None, None)],
             'CP': [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None),
                    (None, None)],
             },
    },
    10: {
        15: {'DFTS': [(2, 0), (2, 50), (1, 0), (1, 51), (50, 0), (25, 12), (1, 1), (1, 50)],
             'CP': [(2, 0), (2, 50), (1, 0), (1, 51), (52, 0), (26, 13), (1, 1), (1, 50)],
             },
        30: {'DFTS': [(2, 0), (2, 22), (1, 0), (1, 23), (24, 0), (12, 6), (1, 1), (1, 22)],
             'CP': [(2, 0), (2, 22), (1, 0), (1, 23), (24, 0), (12, 6), (1, 1), (1, 22)],
             },
        60: {'DFTS': [(2, 0), (2, 9), (1, 0), (1, 10), (10, 0), (5, 2), (1, 1), (1, 9)],
             'CP': [(2, 0), (2, 9), (1, 0), (1, 10), (11, 0), (5, 2), (1, 1), (1, 9)],
             },
    },
    15: {
        15: {'DFTS': [(2, 0), (2, 77), (1, 0), (1, 78), (75, 0), (36, 18), (1, 1), (1, 77)],
             'CP': [(2, 0), (2, 77), (1, 0), (1, 78), (79, 0), (39, 19), (1, 1), (1, 77)],
             },
        30: {'DFTS': [(2, 0), (2, 36), (1, 0), (1, 37), (36, 0), (18, 9), (1, 1), (1, 36)],
             'CP': [(2, 0), (2, 36), (1, 0), (1, 37), (38, 0), (19, 9), (1, 1), (1, 36)],
             },
        60: {'DFTS': [(2, 0), (2, 16), (1, 0), (1, 17), (18, 0), (9, 4), (1, 1), (1, 16)],
             'CP': [(2, 0), (2, 16), (1, 0), (1, 17), (18, 0), (9, 4), (1, 1), (1, 16)],
             },
    },
    20: {
        15: {'DFTS': [(2, 0), (2, 104), (1, 0), (1, 105), (100, 0), (50, 25), (1, 1), (1, 104)],
             'CP': [(2, 0), (2, 104), (1, 0), (1, 105), (106, 0), (53, 26), (1, 1), (1, 104)],
             },
        30: {'DFTS': [(2, 0), (2, 49), (1, 0), (1, 50), (50, 0), (25, 12), (1, 1), (1, 49)],
             'CP': [(2, 0), (2, 49), (1, 0), (1, 50), (51, 0), (25, 12), (1, 1), (1, 49)],
             },
        60: {'DFTS': [(2, 0), (2, 22), (1, 0), (1, 23), (24, 0), (10, 26), (1, 1), (1, 22)],
             'CP': [(2, 0), (2, 22), (1, 0), (1, 23), (24, 0), (10, 26), (1, 1), (1, 22)],
             },
    },
    25: {
        15: {'DFTS': [(2, 0), (2, 131), (1, 0), (1, 132), (128, 0), (64, 32), (1, 1), (1, 131)],
             'CP': [(2, 0), (2, 131), (1, 0), (1, 132), (133, 0), (67, 33), (1, 1), (1, 131)],
             },
        30: {'DFTS': [(2, 0), (2, 63), (1, 0), (1, 64), (64, 0), (32, 16), (1, 1), (1, 63)],
             'CP': [(2, 0), (2, 63), (1, 0), (1, 64), (65, 0), (33, 16), (1, 1), (1, 63)],
             },
        60: {'DFTS': [(2, 0), (2, 29), (1, 0), (1, 30), (30, 0), (15, 7), (1, 1), (1, 29)],
             'CP': [(2, 0), (2, 29), (1, 0), (1, 30), (31, 0), (15, 7), (1, 1), (1, 29)],
             },
    },
    30: {
        15: {'DFTS': [(2, 0), (2, 158), (1, 0), (1, 159), (160, 0), (80, 40), (1, 1), (1, 158)],
             'CP': [(2, 0), (2, 158), (1, 0), (1, 159), (160, 0), (80, 40), (1, 1), (1, 158)],
             },
        30: {'DFTS': [(2, 0), (2, 76), (1, 0), (1, 77), (75, 0), (36, 18), (1, 1), (1, 76)],
             'CP': [(2, 0), (2, 76), (1, 0), (1, 77), (78, 0), (39, 19), (1, 1), (1, 76)],
             },
        60: {'DFTS': [(2, 0), (2, 36), (1, 0), (1, 37), (36, 0), (18, 9), (1, 1), (1, 36)],
             'CP': [(2, 0), (2, 36), (1, 0), (1, 37), (38, 0), (19, 9), (1, 1), (1, 36)],
             },
    },
    40: {
        15: {'DFTS': [(2, 0), (2, 214), (1, 0), (1, 215), (216, 0), (108, 54), (1, 1), (1, 214)],
             'CP': [(2, 0), (2, 214), (1, 0), (1, 215), (216, 0), (108, 54), (1, 1), (1, 214)],
             },
        30: {'DFTS': [(2, 0), (2, 104), (1, 0), (1, 105), (100, 0), (50, 25), (1, 1), (1, 104)],
             'CP': [(2, 0), (2, 104), (1, 0), (1, 105), (106, 0), (53, 26), (1, 1), (1, 104)],
             },
        60: {'DFTS': [(2, 0), (2, 49), (1, 0), (1, 50), (50, 0), (25, 12), (1, 1), (1, 49)],
             'CP': [(2, 0), (2, 49), (1, 0), (1, 50), (51, 0), (25, 12), (1, 1), (1, 49)],
             },
    },
    50: {
        15: {'DFTS': [(2, 0), (2, 268), (1, 0), (1, 269), (270, 0), (135, 67), (1, 1), (1, 268)],
             'CP': [(2, 0), (2, 268), (1, 0), (1, 269), (270, 0), (135, 67), (1, 1), (1, 268)],
             },
        30: {'DFTS': [(2, 0), (2, 131), (1, 0), (1, 132), (128, 0), (64, 32), (1, 1), (1, 131)],
             'CP': [(2, 0), (2, 131), (1, 0), (1, 132), (133, 0), (67, 33), (1, 1), (1, 131)],
             },
        60: {'DFTS': [(2, 0), (2, 63), (1, 0), (1, 64), (64, 0), (32, 16), (1, 1), (1, 63)],
             'CP': [(2, 0), (2, 63), (1, 0), (1, 64), (65, 0), (33, 16), (1, 1), (1, 63)],
             },
    },
    60: {
        15: {'DFTS': [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None),
                      (None, None)],
             'CP': [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None),
                    (None, None)],
             },
        30: {'DFTS': [(2, 0), (2, 160), (1, 0), (1, 161), (162, 0), (81, 40), (1, 1), (1, 160)],
             'CP': [(2, 0), (2, 160), (1, 0), (1, 161), (162, 0), (81, 40), (1, 1), (1, 160)],
             },
        60: {'DFTS': [(2, 0), (2, 77), (1, 0), (1, 78), (75, 0), (36, 18), (1, 1), (1, 77)],
             'CP': [(2, 0), (2, 77), (1, 0), (1, 78), (79, 0), (39, 19), (1, 1), (1, 77)],
             },
    },
    70: {
        15: {'DFTS': [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None),
                      (None, None)],
             'CP': [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None),
                    (None, None)],
             },
        30: {'DFTS': [(2, 0), (2, 187), (1, 0), (1, 188), (180, 0), (90, 45), (1, 1), (1, 187)],
             'CP': [(2, 0), (2, 187), (1, 0), (1, 188), (189, 0), (95, 47), (1, 1), (1, 187)],
             },
        60: {'DFTS': [(2, 0), (2, 91), (1, 0), (1, 92), (90, 0), (45, 22), (1, 1), (1, 91)],
             'CP': [(2, 0), (2, 91), (1, 0), (1, 92), (93, 0), (47, 23), (1, 1), (1, 91)],
             },
    },
    80: {
        15: {'DFTS': [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None),
                      (None, None)],
             'CP': [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None),
                    (None, None)],
             },
        30: {'DFTS': [(2, 0), (2, 215), (1, 0), (1, 216), (216, 0), (108, 54), (1, 1), (1, 215)],
             'CP': [(2, 0), (2, 215), (1, 0), (1, 216), (217, 0), (109, 54), (1, 1), (1, 215)],
             },
        60: {'DFTS': [(2, 0), (2, 105), (1, 0), (1, 106), (100, 0), (50, 25), (1, 1), (1, 105)],
             'CP': [(2, 0), (2, 105), (1, 0), (1, 106), (107, 0), (53, 26), (1, 1), (1, 105)],
             },
    },
    90: {
        15: {'DFTS': [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None),
                      (None, None)],
             'CP': [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None),
                    (None, None)],
             },
        30: {'DFTS': [(2, 0), (2, 243), (1, 0), (1, 244), (243, 0), (120, 60), (1, 1), (1, 243)],
             'CP': [(2, 0), (2, 243), (1, 0), (1, 244), (245, 0), (123, 61), (1, 1), (1, 243)],
             },
        60: {'DFTS': [(2, 0), (2, 119), (1, 0), (1, 120), (120, 0), (60, 30), (1, 1), (1, 119)],
             'CP': [(2, 0), (2, 119), (1, 0), (1, 120), (121, 0), (61, 30), (1, 1), (1, 119)],
             },
    },
    100: {
        15: {'DFTS': [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None),
                      (None, None)],
             'CP': [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None),
                    (None, None)],
             },
        30: {'DFTS': [(2, 0), (2, 271), (1, 0), (1, 272), (270, 0), (135, 67), (1, 1), (1, 127)],
             'CP': [(2, 0), (2, 271), (1, 0), (1, 272), (273, 0), (137, 68), (1, 1), (1, 127)],
             },
        60: {'DFTS': [(2, 0), (2, 133), (1, 0), (1, 134), (135, 0), (64, 32), (1, 1), (1, 133)],
             'CP': [(2, 0), (2, 133), (1, 0), (1, 134), (135, 0), (67, 33), (1, 1), (1, 133)],
             },
    },
}  # 138 521-1 V16.7.0 (2021-06)

FCC_LTE = {
    20: [(1, 0,), (1, 49,), (1, 99,), (50, 0,), (50, 24,), (50, 50,), (100, 0,), ],
    15: [(1, 0,), (1, 37,), (1, 74,), (36, 0,), (36, 20,), (36, 39,), (75, 0,), ],
    10: [(1, 0,), (1, 25,), (1, 49,), (25, 0,), (25, 12,), (25, 25,), (50, 0,), ],
    5: [(1, 0,), (1, 12,), (1, 24,), (12, 0,), (12, 7,), (12, 13,), (25, 0,), ],
    3: [(1, 0,), (1, 8,), (1, 14,), (8, 0,), (8, 4,), (8, 7,), (15, 0,), ],
    1.4: [(1, 0,), (1, 3,), (1, 5,), (3, 0,), (3, 1,), (3, 3,), (6, 0,), ],
}

FCC_FR1 = {
    2: {
        20: {
            'BPSK': [(1, 1,), (1, 53,), (1, 104,), (50, 0,), (50, 28,), (50, 56,), (100, 0,), ],
            'QPSK': [(1, 1,), (1, 53,), (1, 104,), (50, 0,), (50, 28,), (50, 56,), (100, 0,), ],
            'Q16': [(1, 1,), ],
            'Q64': [(1, 1,), ],
            'Q256': [(1, 1,), ],
        },
        15: {
            'BPSK': [(1, 1,), ],
        },
        10: {
            'BPSK': [(1, 1,), ],
        },
        5: {
            'BPSK': [(1, 1,), ],
        },
    },
    5: {
        20: {
            'BPSK': [(1, 1,), (1, 53,), (1, 104,), (50, 0,), (50, 28,), (50, 56,), (100, 0,), ],
            'QPSK': [(1, 1,), (1, 53,), (1, 104,), (50, 0,), (50, 28,), (50, 56,), (100, 0,), ],
            'Q16': [(1, 1,), ],
            'Q64': [(1, 1,), ],
            'Q256': [(1, 1,), ],
        },
        15: {
            'BPSK': [(1, 1,), ],
        },
        10: {
            'BPSK': [(1, 1,), ],
        },
        5: {
            'BPSK': [(1, 1,), ],
        },
    },
    7: {
        50: {
            'BPSK': [(1, 1,), (1, 135,), (1, 268,), (135, 0,), (135, 68,), (135, 135,), (270, 0,), ],
            'QPSK': [(1, 1,), (1, 135,), (1, 268,), (135, 0,), (135, 68,), (135, 135,), (270, 0,), ],
            'Q16': [(1, 1,), ],
            'Q64': [(1, 1,), ],
            'Q256': [(1, 1,), ],
        },
        40: {
            'BPSK': [(1, 1,), ],
        },
        30: {
            'BPSK': [(1, 1,), ],
        },
        25: {
            'BPSK': [(1, 1,), ],
        },
        20: {
            'BPSK': [(1, 1,), ],
        },
        15: {
            'BPSK': [(1, 1,), ],
        },
        10: {
            'BPSK': [(1, 1,), ],
        },
        5: {
            'BPSK': [(1, 1,), ],
        },
    },
    12: {
        15: {
            'BPSK': [(1, 1,), (1, 40,), (1, 77,), (36, 0,), (36, 22,), (36, 43,), (75, 0,), ],
            'QPSK': [(1, 1,), (1, 40,), (1, 77,), (36, 0,), (36, 22,), (36, 43,), (75, 0,), ],
            'Q16': [(1, 1,), ],
            'Q64': [(1, 1,), ],
            'Q256': [(1, 1,), ],
        },
        10: {
            'BPSK': [(1, 1,), ],
        },
        5: {
            'BPSK': [(1, 1,), ],
        },
    },
    25: {
        40: {
            'BPSK': [(1, 1,), (1, 108,), (1, 214,), (108, 0,), (108, 54,), (108, 108), (216, 0,), ],
            'QPSK': [(1, 1,), (1, 108,), (1, 214,), (108, 0,), (108, 54,), (108, 108), (216, 0,), ],
            'Q16': [(1, 1,), ],
            'Q64': [(1, 1,), ],
            'Q256': [(1, 1,), ],
        },
        30: {
            'BPSK': [(1, 1,), ],
        },
        25: {
            'BPSK': [(1, 1,), ],
        },
        20: {
            'BPSK': [(1, 1,), ],
        },
        15: {
            'BPSK': [(1, 1,), ],
        },
        10: {
            'BPSK': [(1, 1,), ],
        },
        5: {
            'BPSK': [(1, 1,), ],
        },
    },
    26: {
        20: {
            'BPSK': [(1, 1,), (1, 53), (1, 104), (50, 0), (50, 28), (50, 56), (100, 0)],
            'QPSK': [(1, 1,), (1, 53), (1, 104), (50, 0), (50, 28), (50, 56), (100, 0)],
            'Q16': [(1, 1,), ],
            'Q64': [(1, 1,), ],
            'Q256': [(1, 1,), ],
        },
        15: {
            'BPSK': [(1, 1,), ],
        },
        10: {
            'BPSK': [(1, 1,), ],
        },
        5: {
            'BPSK': [(1, 1,), ],
        },
    },
    30: {
        10: {
            'BPSK': [(1, 1,), (1, 26,), (1, 50,), (25, 0,), (25, 14,), (25, 27,), (50, 0,), ],
            'QPSK': [(1, 1,), (1, 26,), (1, 50,), (25, 0,), (25, 14,), (25, 27,), (50, 0,), ],
            'Q16': [(1, 1,), ],
            'Q64': [(1, 1,), ],
            'Q256': [(1, 1,), ],
        },
        5: {
            'BPSK': [(1, 1,), ],
        },
    },
    66: {
        40: {
            'BPSK': [(1, 1,), (1, 108,), (1, 214,), (108, 0,), (108, 54,), (108, 108), (216, 0,), ],
            'QPSK': [(1, 1,), (1, 108,), (1, 214,), (108, 0,), (108, 54,), (108, 108), (216, 0,), ],
            'Q16': [(1, 1,), ],
            'Q64': [(1, 1,), ],
            'Q256': [(1, 1,), ],
        },
        30: {
            'BPSK': [(1, 1,), ],
        },
        25: {
            'BPSK': [(1, 1,), ],
        },
        20: {
            'BPSK': [(1, 1,), ],
        },
        15: {
            'BPSK': [(1, 1,), ],
        },
        10: {
            'BPSK': [(1, 1,), ],
        },
        5: {
            'BPSK': [(1, 1,), ],
        },
    },
    70: {
        15: {
            'BPSK': [(1, 1,), (1, 40), (1, 77), (36, 0), (36, 22), (36, 43), (75, 0)],
            'QPSK': [(1, 1,), (1, 40), (1, 77), (36, 0), (36, 22), (36, 43), (75, 0)],
            'Q16': [(1, 1,), ],
            'Q64': [(1, 1,), ],
            'Q256': [(1, 1,), ],
        },
        10: {
            'BPSK': [(1, 1,), ],
        },
        5: {
            'BPSK': [(1, 1,), ],
        },
    },
    71: {
        20: {
            'BPSK': [(1, 1,), (1, 53,), (1, 104,), (50, 0,), (50, 28,), (50, 56,), (100, 0,), ],
            'QPSK': [(1, 1,), (1, 53,), (1, 104,), (50, 0,), (50, 28,), (50, 56,), (100, 0,), ],
            'Q16': [(1, 1,), ],
            'Q64': [(1, 1,), ],
            'Q256': [(1, 1,), ],
        },
        15: {
            'BPSK': [(1, 1,), ],
        },
        10: {
            'BPSK': [(1, 1,), ],
        },
        5: {
            'BPSK': [(1, 1,), ],
        },
    },
    38: {
        # 40: {
        #     'BPSK': [(1, 1,), (1, 108,), (1, 214,), (108, 0,), (108, 54,), (108, 108), (216, 0,), ],
        #     'QPSK': [(1, 1,), (1, 108,), (1, 214,), (108, 0,), (108, 54,), (108, 108), (216, 0,), ],
        #     'Q16': [(1, 1,), ],
        #     'Q64': [(1, 1,), ],
        #     'Q256': [(1, 1,), ],
        # },
        # 30: {
        #     'BPSK': [(1, 1,), ],
        # },
        # 25: {
        #     'BPSK': [(1, 1,), ],
        # },
        20: {
            'BPSK': [(1, 1,), (1, 26,), (1, 49,), (25, 0,), (25, 13,), (25, 26), (50, 0,), ],
            'QPSK': [(1, 1,), (1, 26,), (1, 49,), (25, 0,), (25, 13,), (25, 26), (50, 0,), ],
            'Q16': [(1, 1,), ],
            'Q64': [(1, 1,), ],
            'Q256': [(1, 1,), ],
        },
        15: {
            'BPSK': [(1, 1,), ],
        },
        10: {
            'BPSK': [(1, 1,), ],
        },
        5: {
            'BPSK': [(1, 1,), ],
        },
    },
    41: {
        100: {
            'BPSK': [(1, 1,), (1, 137,), (1, 271,), (135, 0,), (135, 69,), (135, 138), (270, 0,), ],
            'QPSK': [(1, 1,), (1, 137,), (1, 271,), (135, 0,), (135, 69,), (135, 138), (270, 0,), ],
            'Q16': [(1, 1,), ],
            'Q64': [(1, 1,), ],
            'Q256': [(1, 1,), ],
        },
        90: {
            'BPSK': [(1, 1,), ],
        },
        80: {
            'BPSK': [(1, 1,), ],
        },
        70: {
            'BPSK': [(1, 1,), ],
        },
        60: {
            'BPSK': [(1, 1,), ],
        },
        50: {
            'BPSK': [(1, 1,), ],
        },
        40: {
            'BPSK': [(1, 1,), ],
        },
        30: {
            'BPSK': [(1, 1,), ],
        },
        20: {
            'BPSK': [(1, 1,), ],
        },
        15: {
            'BPSK': [(1, 1,), ],
        },
        10: {
            'BPSK': [(1, 1,), ],
        },
    },
    48: {
        100: {
            'BPSK': [(1, 1,), (1, 137,), (1, 271,), (135, 0,), (135, 69,), (135, 138), (270, 0,), ],
            'QPSK': [(1, 1,), (1, 137,), (1, 271,), (135, 0,), (135, 69,), (135, 138), (270, 0,), ],
            'Q16': [(1, 1,), ],
            'Q64': [(1, 1,), ],
            'Q256': [(1, 1,), ],
        },
        90: {
            'BPSK': [(1, 1,), ],
        },
        80: {
            'BPSK': [(1, 1,), ],
        },
        70: {
            'BPSK': [(1, 1,), ],
        },
        60: {
            'BPSK': [(1, 1,), ],
        },
        50: {
            'BPSK': [(1, 1,), ],
        },
        40: {
            'BPSK': [(1, 1,), ],
        },
        30: {
            'BPSK': [(1, 1,), ],
        },
        20: {
            'BPSK': [(1, 1,), ],
        },
        15: {
            'BPSK': [(1, 1,), ],
        },
        10: {
            'BPSK': [(1, 1,), ],
        },
        5: {
            'BPSK': [(1, 1,), ],
        },
    },
    77: {
        100: {
            'BPSK': [(1, 1,), (1, 137,), (1, 271,), (135, 0,), (135, 69,), (135, 138), (270, 0,), ],
            'QPSK': [(1, 1,), (1, 137,), (1, 271,), (135, 0,), (135, 69,), (135, 138), (270, 0,), ],
            'Q16': [(1, 1,), ],
            'Q64': [(1, 1,), ],
            'Q256': [(1, 1,), ],
        },
        90: {
            'BPSK': [(1, 1,), ],
        },
        80: {
            'BPSK': [(1, 1,), ],
        },
        70: {
            'BPSK': [(1, 1,), ],
        },
        60: {
            'BPSK': [(1, 1,), ],
        },
        50: {
            'BPSK': [(1, 1,), ],
        },
        40: {
            'BPSK': [(1, 1,), ],
        },
        30: {
            'BPSK': [(1, 1,), ],
        },
        25: {
            'BPSK': [(1, 1,), ],
        },
        20: {
            'BPSK': [(1, 1,), ],
        },
        15: {
            'BPSK': [(1, 1,), ],
        },
        10: {
            'BPSK': [(1, 1,), ],
        },
    },
    78: {
        100: {
            'BPSK': [(1, 1,), (1, 137,), (1, 271,), (135, 0,), (135, 69,), (135, 138), (270, 0,), ],
            'QPSK': [(1, 1,), (1, 137,), (1, 271,), (135, 0,), (135, 69,), (135, 138), (270, 0,), ],
            'Q16': [(1, 1,), ],
            'Q64': [(1, 1,), ],
            'Q256': [(1, 1,), ],
        },
        90: {
            'BPSK': [(1, 1,), ],
        },
        80: {
            'BPSK': [(1, 1,), ],
        },
        70: {
            'BPSK': [(1, 1,), ],
        },
        60: {
            'BPSK': [(1, 1,), ],
        },
        50: {
            'BPSK': [(1, 1,), ],
        },
        40: {
            'BPSK': [(1, 1,), ],
        },
        30: {
            'BPSK': [(1, 1,), ],
        },
        25: {
            'BPSK': [(1, 1,), ],
        },
        20: {
            'BPSK': [(1, 1,), ],
        },
        15: {
            'BPSK': [(1, 1,), ],
        },
        10: {
            'BPSK': [(1, 1,), ],
        },
    },
}  # P22 FCC, band > bandwidth > mcs > rb

CE_FR1 = {
    1: {
        20: {
            'BPSK': [(50, 25,), (100, 0,), (1, 0,), (1, 105,), ],
            'QPSK': [(50, 25,), (100, 0,), (1, 0,), (1, 105,), ],
            'Q16': [(50, 25,), ],
            'Q64': [(50, 25,), ],
            'Q256': [(50, 25,), ],
        },
        15: {
            'BPSK': [(36, 18,), ],
        },
        10: {
            'BPSK': [(25, 12,), ],
        },
        5: {
            'BPSK': [(12, 6,), ],
        },
    },
    3: {
        # 40: {
        #     'BPSK': [(108, 54,), (216, 0,), (1, 0,), (1, 215,), ],
        #     'QPSK': [(108, 54,), (216, 0,), (1, 0,), (1, 215,), ],
        #     'Q16': [(108, 54,), ],
        #     'Q64': [(108, 54,), ],
        #     'Q256': [(108, 54,), ],
        # },
        30: {
            'BPSK': [(80, 40,), ],
            'QPSK': [(80, 40,), (160, 0,), (1, 0,), (1, 159,), ],
            'Q16': [(80, 40,), (160, 0,), (1, 0,), (1, 159,), ],
            'Q64': [(80, 40,), ],
            'Q256': [(80, 40,), ],
        },
        25: {
            'BPSK': [(64, 32,), ],
        },
        20: {
            'BPSK': [(50, 25,), ],
        },
        15: {
            'BPSK': [(36, 18,), ],
        },
        10: {
            'BPSK': [(25, 12,), ],
        },
        5: {
            'BPSK': [(12, 6,), ],
        },
    },
    5: {
        20: {
            'BPSK': [(50, 25,), (100, 0,), (1, 0,), (1, 105,), ],
            'QPSK': [(50, 25,), (100, 0,), (1, 0,), (1, 105,), ],
            'Q16': [(50, 25,), ],
            'Q64': [(50, 25,), ],
            'Q256': [(50, 25,), ],
        },
        15: {
            'BPSK': [(36, 18,), ],
        },
        10: {
            'BPSK': [(25, 12,), ],
        },
        5: {
            'BPSK': [(12, 6,), ],
        },
    },
    7: {
        # 50: {
        #     'BPSK': [(135, 67,), (270, 0,), (1, 0,), (1, 269,), ],
        #     'QPSK': [(135, 67,), (270, 0,), (1, 0,), (1, 269,), ],
        #     'Q16': [(135, 67,), ],
        #     'Q64': [(135, 67,), ],
        #     'Q256': [(135, 67,), ],
        # },
        # 40: {
        #     'BPSK': [(108, 54,), ],
        # },
        # 30: {
        #     'BPSK': [(80, 40,), ],
        # },
        # 25: {
        #     'BPSK': [(64, 32,), ],
        # },
        20: {
            'BPSK': [(50, 25,), (100, 0,), (1, 0), (1,105), ],
            'QPSK': [(50, 25,), (100, 0,), (1, 0), (1,105), ],
            'Q16': [(50, 25,), ],
            'Q64': [(50, 25,), ],
            'Q256': [(50, 25,), ],
        },
        15: {
            'BPSK': [(36, 18,), ],
        },
        10: {
            'BPSK': [(25, 12,), ],
        },
        5: {
            'BPSK': [(12, 6,), ],
        },
    },
    # 8: {
    #     20: {
    #         'BPSK': [(50, 20,), (100, 0,), (1, 0,), (1, 105,), ],
    #         'QPSK': [(50, 20,), (100, 0,), (1, 0,), (1, 105,), ],
    #         'Q16': [(25, 25,), ],
    #         'Q64': [(25, 25,), ],
    #         'Q256': [(25, 25,), ],
    #     },
    #     15: {
    #         'BPSK': [(36, 18,), ],
    #     },
    #     10: {
    #         'BPSK': [(25, 12,), (50, 0,), (1, 0,), (1, 51,), ],
    #         # 'QPSK': [(25, 12,), (50, 0,), (1, 0,), (1, 51,), ],
    #         # 'Q16': [(25, 12,), ],
    #         # 'Q64': [(25, 12,), ],
    #         # 'Q256': [(25, 12,), ],
    #     },
    #     5: {
    #         'BPSK': [(12, 6,), ],
    #     },
    # },
    20: {
        20: {
            'BPSK': [(50, 25,), (100, 0,), (1, 0,), (1, 105,), ],
            'QPSK': [(50, 25,), (100, 0,), (1, 0,), (1, 105,), ],
            'Q16': [(50, 25,), ],
            'Q64': [(50, 25,), ],
            'Q256': [(50, 25,), ],
        },
        15: {
            'BPSK': [(36, 18,), ],
        },
        10: {
            'BPSK': [(25, 12,), ],
        },
        5: {
            'BPSK': [(12, 6,), ],
        },
    },
    28: {
        # 30: {
        #     'BPSK': [(80, 40,), (160, 0,), (1, 0,), (1, 159,), ],
        #     'QPSK': [(80, 40,), (160, 0,), (1, 0,), (1, 159,), ],
        #     'Q16': [(80, 40,), ],
        #     'Q64': [(80, 40,), ],
        #     'Q256': [(80, 40,), ],
        # },
        20: {
            'BPSK': [(50, 25,), ],
            'QPSK': [(50, 25,), (100, 0,), (1, 0,), (1, 105,), ],
            'Q16': [(50, 25,), ],
            'Q64': [(50, 25,), ],
            'Q256': [(50, 25,), ],
        },
        15: {
            'BPSK': [(36, 18,), ],
        },
        10: {
            'BPSK': [(25, 12,), ],
        },
        5: {
            'BPSK': [(12, 6,), ],
        },
    },
    38: {
        20: {
            'BPSK': [(25, 12,), (50, 0,), (1, 0,), (1, 50,), ],
            'QPSK': [(25, 12,), (50, 0,), (1, 0,), (1, 50,), ],
            'Q16': [(25, 12,), ],
            'Q64': [(25, 12,), ],
            'Q256': [(25, 12,), ],
        },
        15: {
            'BPSK': [(18, 9,), ],
        },
        10: {
            'BPSK': [(12, 6,), ],
        },
        # 5: {
        #     'BPSK': [(5, 2,), ],
        # },
    },
    40: {
        80: {
            'BPSK': [(108, 54,), (216, 0,), (1, 0,), (1, 216,), ],
            'QPSK': [(108, 54,), (216, 0,), (1, 0,), (1, 216,), ],
            'Q16': [(108, 54,), ],
            'Q64': [(108, 54,), ],
            'Q256': [(108, 54,), ],
        },
        60: {
            'BPSK': [(81, 40,), ],
        },
        50: {
            'BPSK': [(64, 32,), ],
        },
        40: {
            'BPSK': [(50, 25,), ],
        },
        30: {
            'BPSK': [(36, 18,), ],
        },
        25: {
            'BPSK': [(32, 16,), ],
        },
        20: {
            'BPSK': [(25, 12,), ],
        },
        15: {
            'BPSK': [(18, 9,), ],
        },
        10: {
            'BPSK': [(12, 6,), ],
        },
        # 5: {
        #     'BPSK': [(5, 2,), ],
        # },
    },
    77: {
        100: {
            'BPSK': [(135, 67,), (270, 0,), (1, 0), (1, 272,), ],
            'QPSK': [(135, 67,), (270, 0,), (1, 0), (1, 272,), ],
            'Q16': [(135, 67,), ],
            'Q64': [(135, 67,), ],
            'Q256': [(135, 67,), ],
        },
        90: {
            'BPSK': [(120, 60,), ],
        },
        80: {
            'BPSK': [(108, 54,), ],
        },
        70: {
            'BPSK': [(90, 45,), ],
        },
        60: {
            'BPSK': [(81, 40,), ],
        },
        50: {
            'BPSK': [(64, 32,), ],
        },
        40: {
            'BPSK': [(50, 25,), ],
        },
        30: {
            'BPSK': [(36, 18,), ],
        },
        25: {
            'BPSK': [(32, 16,), ],
        },
        20: {
            'BPSK': [(25, 12,), ],
        },
        15: {
            'BPSK': [(18, 9,), ],
        },
        10: {
            'BPSK': [(12, 6,), ],
        },
    },
    78: {
        100: {
            'BPSK': [(135, 67,), (270, 0,), (1, 0), (1, 272,), ],
            'QPSK': [(135, 67,), (270, 0,), (1, 0), (1, 272,), ],
            'Q16': [(135, 67,), ],
            'Q64': [(135, 67,), ],
            'Q256': [(135, 67,), ],
        },
        90: {
            'BPSK': [(120, 60,), ],
        },
        80: {
            'BPSK': [(108, 54,), ],
        },
        70: {
            'BPSK': [(90, 45,), ],
        },
        60: {
            'BPSK': [(81, 40,), ],
        },
        50: {
            'BPSK': [(64, 32,), ],
        },
        40: {
            'BPSK': [(50, 25,), ],
        },
        30: {
            'BPSK': [(36, 18,), ],
        },
        25: {
            'BPSK': [(32, 16,), ],
        },
        20: {
            'BPSK': [(25, 12,), ],
        },
        15: {
            'BPSK': [(18, 9,), ],
        },
        10: {
            'BPSK': [(12, 6,), ],
        },
    },
}  # P22 CE, band > bandwidth > mcs > rb

ENDC = {
    '3_78': {
        10: {
            20: [
                [(1715, 3430.02), (50, 0), (50, 0)],
                [(1747.5, 3495), (50, 0), (50, 0)],
                [(1780, 3560.01), (50, 0), (50, 0)],
            ]
        },
        5: {
            10: [
                [(1740, 3574.995), (25, 0), (50, 0)],
            ]
        },
    },  # DTAG
    '2_77': {
        20: {
            40: [
                [(1880, 3759.99), (100, 0), (100, 0)],
            ]
        },
        10: {
            100: [
                [(1880, 3849.99), (50, 0), (6, 106)],
            ]
        },
    },  # AT&T/VZW
    '12_78': {
        10: {
            50: [
                [(711, 3555), (50, 0), (128, 0)],
            ]
        },
    },  # CA
    '5_78': {
        10: {
            50: [
                [(844, 3376.02), (50, 0), (128, 0)],
            ]
        }
    },  # CA/AU
    '28_78': {
        10: {
            20: [
                [(723, 3615), (50, 0), (50, 0)],
            ]
        }
    },  # EU/AU/JPN
    '5_77': {
        10: {
            100: [
                [(836.5, 3849.99), (25, 25), (135, 67)],
            ],
        }
    },  # Verizon
    '5_66': {
        5: {
            10: [
                [(832.5, 1715), (25, 0), (6, 0)],
                [(846.5, 1740), (25, 0), (8, 11)],
            ],
        },
        10: {
            20: [
                [(840, 1720), (25, 25), (27, 79)],
            ],
        },
    },  # AT&T/Verizon
    '13_5': {
        10: {
            10: [
                [(782, 829), (18, 15), (20, 10)],
                [(782, 829), (6, 44), (2, 0)],
            ],
        },
    },  # Verizon
    '66_2': {
        10: {
            10: [
                [(1775, 1855), (25, 25), (15, 25)],
            ],
        },
    },  # Verizon
    '66_5': {
        10: {
            5: [
                [(1720, 832.5), (6, 0), (25, 0)],
                [(1740, 846.5), (8, 10), (25, 0)],
            ],
        },
        20: {
            10: [
                [(1720, 840), (25, 75), (25, 25)],
            ],
        },
    },  # Verizon
    '66_77': {
        10: {
            100: [
                [(1745, 3849.99), (50, 0), (6, 245)],
            ],
        },
    },  # Verizon
}  # band_combo > bw_lte > bw_fr1 > [(tx_freq_lte, tx_freq_fr1), (rb_size_lte, rb_start_lte), (rb_start_size_fr1, rb_start_fr1)]

# 20230131_v17.05
ULCA_3GPP_LTE = {
    '25+25': {
        'QPSK': {
            '1RB_N': ((1, 0), (0, 0)),
            'PRB_N': ((8, 0), (0, 0)),
            'FRB_N': ((25, 0), (0, 0)),
            'FRB_FRB': ((25, 0), (25, 0)),
            '1RB0_1RBmax': ((1, 0), (1, 24)),
        },

        'Q16': {
            'PRB_N': ((8, 0), (0, 0)),
            'FRB_N': ((25, 0), (0, 0)),
            'FRB_FRB': ((25, 0), (25, 0)),
        },
    },

    '25+50': {
        'QPSK': {
            '1RB_N': ((1, 0), (0, 0)),
            'PRB_N': ((8, 0), (0, 0)),
            'FRB_N': ((25, 0), (0, 0)),
            'FRB_FRB': ((25, 0), (50, 0)),
            '1RB0_1RBmax': ((1, 0), (1, 49)),
        },

        'Q16': {
            'PRB_N': ((8, 0), (0, 0)),
            'FRB_N': ((25, 0), (0, 0)),
            'FRB_FRB': ((25, 0), (50, 0)),
        },

        'Q64': {
            'PRB_N': ((8, 0), (0, 0)),
            'FRB_N': ((25, 0), (0, 0)),
            'FRB_FRB': ((25, 0), (50, 0)),
        },

        'Q256': {
            'FRB_N': ((25, 0), (0, 0)),
            'FRB_FRB': ((25, 0), (50, 0)),
        },
    },

    '50+25': {
        'QPSK': {
            '1RB_N': ((1, 0), (0, 0)),
            'PRB_N': ((8, 0), (0, 0)),
            'FRB_N': ((25, 0), (0, 0)),
            'FRB_FRB': ((50, 0), (25, 0)),
            '1RB0_1RBmax': ((1, 0), (1, 24)),
        },

        'Q16': {
            'PRB_N': ((8, 0), (0, 0)),
            'FRB_N': ((25, 0), (0, 0)),
            'FRB_FRB': ((50, 0), (25, 0)),
        },

        'Q64': {
            'PRB_N': ((8, 0), (0, 0)),
            'FRB_N': ((50, 0), (0, 0)),
            'FRB_FRB': ((50, 0), (25, 0)),
        },

        'Q256': {
            'FRB_N': ((50, 0), (0, 0)),
            'FRB_FRB': ((50, 0), (25, 0)),
        },
    },

    '50+50': {
        'QPSK': {
            '1RB_N': ((1, 0), (0, 0)),
            'PRB_N': ((12, 0), (0, 0)),
            'FRB_N': ((50, 0), (0, 0)),
            'FRB_FRB': ((50, 0), (50, 0)),
            '1RB0_1RBmax': ((1, 0), (1, 49)),
        },

        'Q16': {
            'PRB_N': ((12, 0), (0, 0)),
            'FRB_N': ((50, 0), (0, 0)),
            'FRB_FRB': ((50, 0), (50, 0)),
        },

        'Q64': {
            'PRB_N': ((12, 0), (0, 0)),
            'FRB_N': ((50, 0), (0, 0)),
            'FRB_FRB': ((50, 0), (50, 0)),
        },

        'Q256': {
            'FRB_N': ((50, 0), (0, 0)),
            'FRB_FRB': ((50, 0), (50, 0)),
        },
    },

    '50+100': {
        'Q64': {
            'PRB_N': ((12, 0), (0, 0)),
            'FRB_N': ((50, 0), (0, 0)),
            'FRB_FRB': ((50, 0), (100, 0)),
        },

        'Q256': {
            'FRB_N': ((50, 0), (0, 0)),
            'FRB_FRB': ((50, 0), (100, 0)),
        },
    },

    '75+25': {
        'QPSK': {
            '1RB_N': ((1, 0), (0, 0)),
            'PRB_N': ((8, 0), (0, 0)),
            'FRB_N': ((25, 0), (0, 0)),
            'FRB_FRB': ((75, 0), (25, 0)),
            '1RB0_1RBmax': ((1, 0), (1, 24)),
        },

        'Q16': {
            'PRB_N': ((8, 0), (0, 0)),
            'FRB_N': ((25, 0), (0, 0)),
            'FRB_FRB': ((75, 0), (25, 0)),
        },
    },

    '75+50': {
        'QPSK': {
            '1RB_N': ((1, 0), (0, 0)),
            'PRB_N': ((12, 0), (0, 0)),
            'FRB_N': ((50, 0), (0, 0)),
            'FRB_FRB': ((75, 0), (25, 0)),
            '1RB0_1RBmax': ((1, 0), (1, 49)),
        },

        'Q16': {
            'PRB_N': ((12, 0), (0, 0)),
            'FRB_N': ((50, 0), (0, 0)),
            'FRB_FRB': ((75, 0), (25, 0)),
        },

        'Q256': {
            'FRB_N': ((75, 0), (0, 0)),
            'FRB_FRB': ((75, 0), (50, 0)),
        },
    },

    '75+75': {
        'QPSK': {
            '1RB_N': ((1, 0), (0, 0)),
            'PRB_N': ((16, 0), (0, 0)),
            'FRB_N': ((75, 0), (0, 0)),
            'FRB_FRB': ((75, 0), (75, 0)),
            '1RB0_1RBmax': ((1, 0), (1, 74)),
        },

        'Q16': {
            'PRB_N': ((16, 0), (0, 0)),
            'FRB_N': ((75, 0), (0, 0)),
            'FRB_FRB': ((75, 0), (75, 0)),
        },

        'Q64': {
            'PRB_N': ((16, 0), (0, 0)),
            'FRB_N': ((75, 0), (0, 0)),
            'FRB_FRB': ((75, 0), (75, 0)),
        },

        'Q256': {
            'FRB_N': ((75, 0), (0, 0)),
            'FRB_FRB': ((75, 0), (75, 0)),
        },
    },

    '100+25': {
        'QPSK': {
            '1RB_N': ((1, 0), (0, 0)),
            'PRB_N': ((8, 0), (0, 0)),
            'FRB_N': ((25, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (25, 0)),
            '1RB0_1RBmax': ((1, 0), (1, 24)),
        },

        'Q16': {
            'PRB_N': ((8, 0), (0, 0)),
            'FRB_N': ((25, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (25, 0)),
        },

        'Q64': {
            'PRB_N': ((8, 0), (0, 0)),
            'FRB_N': ((100, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (25, 0)),
        },

        'Q256': {
            'FRB_N': ((100, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (25, 0)),
        },
    },

    '100+50': {
        'QPSK': {
            '1RB_N': ((1, 0), (0, 0)),
            'PRB_N': ((12, 0), (0, 0)),
            'FRB_N': ((50, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (50, 0)),
            '1RB0_1RBmax': ((1, 0), (1, 49)),
        },

        'Q16': {
            'PRB_N': ((12, 0), (0, 0)),
            'FRB_N': ((50, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (50, 0)),
        },

        'Q64': {
            'PRB_N': ((12, 0), (0, 0)),
            'FRB_N': ((100, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (50, 0)),
        },

        'Q256': {
            'FRB_N': ((100, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (50, 0)),
        },
    },

    '100+75': {
        'QPSK': {
            '1RB_N': ((1, 0), (0, 0)),
            'PRB_N': ((16, 0), (0, 0)),
            'FRB_N': ((75, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (75, 0)),
            '1RB0_1RBmax': ((1, 0), (1, 74)),
        },

        'Q16': {
            'PRB_N': ((16, 0), (0, 0)),
            'FRB_N': ((75, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (75, 0)),
        },

        'Q64': {
            'PRB_N': ((16, 0), (0, 0)),
            'FRB_N': ((100, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (75, 0)),
        },

        'Q256': {
            'FRB_N': ((100, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (75, 0)),
        },
    },

    '100+100': {
        'QPSK': {
            '1RB_N': ((1, 0), (0, 0)),
            'PRB_N': ((18, 0), (0, 0)),
            'FRB_N': ((100, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (100, 0)),
            '1RB0_1RBmax': ((1, 0), (1, 99)),
        },

        'Q16': {
            'PRB_N': ((18, 0), (0, 0)),
            'FRB_N': ((100, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (100, 0)),
        },

        'Q64': {
            'PRB_N': ((18, 0), (0, 0)),
            'FRB_N': ((100, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (100, 0)),
        },

        'Q256': {
            'FRB_N': ((100, 0), (0, 0)),
            'FRB_FRB': ((100, 0), (100, 0)),
        },
    },

}


# CC1_num, CC1_start, CC2_num, CC2 RB_start
def ulca_fcc_lte(cc1_bw, cc2_bw, rb_setting):
    cc1_bw = int(cc1_bw)
    cc2_bw = int(cc2_bw)
    if rb_setting == '1RB0_1RBmax':
        return (1, 0), (1, cc2_bw * 5 - 1)
    elif rb_setting == '1RBmax_1RB0':
        return (1, cc1_bw * 5 - 1), (1, 0)
    elif rb_setting == 'FRB_FRB':
        return (cc1_bw * 5, 0), (cc2_bw * 5, 0)
    else:
        print(f"FCC doesn't have this allocation: {rb_setting}")
        return None


def main():
    # for rb in FCC_FR1[2][10]['BPSK']:
    #     print(rb)
    for _, __ in ULCA_3GPP_LTE['100+100']['QPSK']:
        print(_, __)


if __name__ == '__main__':
    main()
