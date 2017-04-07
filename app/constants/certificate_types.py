BIRTH = "birth"
DEATH = "death"
MARRIAGE = "marriage"

ALL = frozenset((BIRTH, DEATH, MARRIAGE))

FROM_FILE_IDENTIFIER = {
    'B': BIRTH,
    'SB': BIRTH,  # special
    'DB': BIRTH,  # delayed

    'M': MARRIAGE,

    'D': DEATH
}
