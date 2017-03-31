BIRTH = "birth"
DEATH = "death"
MARRIAGE = "marriage"

ALL = frozenset((BIRTH, DEATH, MARRIAGE))

FROM_FILE_IDENTIFIER = {
    'B': BIRTH,
    'M': MARRIAGE,
    'D': DEATH
}
