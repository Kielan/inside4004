from hdl import *

'''
;shifter	ROM1 bit0	    ROM1 bit1	ROM1 bit2	    ROM1 bit3
;----------------------------------------------------------------------------------------------------------------------------------
;bit0		CM (81)		    RM (82)		M- (83)		    M+ (84)
;bit1		SQRT (85)	    % (86)		M=- (87)	    M=+ (88)
;bit2		diamond (89)	/ (8a)		* (8b)		    = (8c)
;bit3		- (8d)		    + (8e)		diamond2 (8f)	000 (90)
;bit4		9 (91)		    6 (92)		3 (93)		    . (94)
;bit5		8 (95)		    5 (96)		2 (97)		    00 (98)
;bit6		7 (99)		    4 (9a)		1 (9b)		    0 (9c)
;bit7		Sign (9d)	    EX (9e)		CE (9f)		    C (a0)
;bit8		dp0		        dp1		    dp2		        dp3	(digit point switch, value 0,1,2,3,4,5,6,8 can be switched)
;bit9		sw1		        (unused)	(unused)	    sw2	(rounding switch, value 0,1,8 can be switched)
;----------------------------------------------------------------------------------------------------------------------------------
'''
_lookup = [
    ["CM",  "RM", "M-",     "M+"],
    ["SQ",  "%",  "M=-",    "M=+"],
    ["<>",  "/",  "*",      "="],
    ["-",   "+",  "#",      "000"],
    ["9",   "6",  "3",      "."],
    ["8",   "5",  "2",      "00"],
    ["7",   "4",  "1",      "0"],
    ["S",   "EX", "CE",     "C"]
]
for c in _lookup:
    c.reverse()


class keyboard(sensor):
    def __init__(self, name="keyboard"):
        self._input = bus(n=10)
        sensor.__init__(self, name, self._input)
        self._output = bus()
        self._buffer = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
            [0, 0, 0, 0], [0, 0, 0, 0]] 

    def input(self):
        return self._input

    def output(self):
        return self._output

    def always(self):
        for i in range(10):
            if self._input.wire(i).v() == 0:
                for j in range(4):
                    self._output.wire(3-j).v(self._buffer[i][j])
                    self._buffer[i][j] = 0


    def readKey(self):
        global _lookup
        k = input("Press a button on the keyboard: ")
        k = k.strip()
        if k != "":
            for c in range(8):
                for r in range(4):
                    s = _lookup[c][r]
                    if k == s:
                        print("  Key press '{}' recorded.".format(k))
                        self._buffer[c][r] = 1
                        return
            print("  Unknown key '{}'!".format(k))