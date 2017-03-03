JAN = 'jan'
FEB = 'feb'
MAR = 'mar'
APR = 'apr'
MAY = 'may'
JUN = 'jun'
JUL = 'jul'
AUG = 'aug'
SEP = 'sep'
OCT = 'oct'
NOV = 'nov'
DEC = 'dec'

TO_VALID = {
    'ja': JAN,
    'fe': FEB,
    'ma': MAR,  # no May
    'ap': APR,
    'ju': JUN,  # no July
    'au': AUG,
    'se': SEP,
    'oc': OCT,
    'no': NOV,
    'de': DEC
}

ALL = [
    JAN,
    FEB,
    MAR,
    APR,
    MAY,
    JUN,
    JUL,
    AUG,
    SEP,
    OCT,
    NOV,
    DEC
]