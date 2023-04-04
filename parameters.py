class Parameters():
    def __init__(self, REMAIN, THICKNESS, POSITIVE_ERROR, NEGATIVE_ERROR, LEFT_FUR, RIGHT_FUR, LEFT_CUT, RIGHT_CUT, LEFT_STOCK, RIGHT_STOCK, MIN_LENGTH, length_difference, mode, scheme_name):
        self.REMAIN_MIN_WIDTH = REMAIN
        #SIDE_BAR_WIDTH=[47,57]#边条列表
        self.THICKNESS = THICKNESS
        self.POSITIVE_ERROR_PERCENT = POSITIVE_ERROR
        self.NEGATIVE_ERROR_PERCENT = NEGATIVE_ERROR
        self.LEFT_FUR = LEFT_FUR
        self.RIGHT_FUR = RIGHT_FUR
        self.LEFT_CUT = LEFT_CUT
        self.RIGHT_CUT = RIGHT_CUT
        self.LEFT_STOCK = LEFT_STOCK
        self.RIGHT_STOCK = RIGHT_STOCK
        self.MIN_LENGTH = MIN_LENGTH
        # self.MAXNUM1 = MAXNUM1
        # self.MAXNUM2 = MAXNUM2
        # self.MAXNUM3 = MAXNUM3
        # self.MAXTIMES = MAXTIMES
        self.length_difference = length_difference
        self.mode = mode
        self.scheme_name = scheme_name