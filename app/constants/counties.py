KINGS = 'kings'
QUEENS = 'queens'
BRONX = 'bronx'
MANHATTAN = 'manhattan'
RICHMOND = 'richmond'  # staten island

ALL = frozenset((KINGS, QUEENS, BRONX, MANHATTAN, RICHMOND))

FROM_FILE_IDENTIFIER = {
    'K': KINGS,
    'Q': QUEENS,
    'B': BRONX,
    'M': MANHATTAN,
    'R': RICHMOND
    # TODO: 'S': RICHMOND ?
}
