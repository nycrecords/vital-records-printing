import os
import json
import xml.etree.ElementTree as ET
import psycopg2.extras
from app.constants import certificate_types, months

CONN = psycopg2.connect(database="vital_records_printing",
                        user="vital_records_printing_db",
                        host="10.0.0.2",
                        port="5432")
CUR = CONN.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

CHUNKSIZE = 500


def _get_value(element, key):
    """
    Returns text from a node in the given element found with
    the given key or None if the node is not found or if the
    text is "-".
    """
    try:
        value = element[1].find(key).text.strip()
        value = value if value != "-" else None
    except Exception:
        value = None
    return value


# TODO: verify if we sould not be storing these results
def _data_is_valid(certificate_number, xml_node):
    is_valid = True
    if certificate_number is None:
        print("Certificate Number not found.")
        is_valid = False
    # write other checks if needed and change 'is_valid' accordingly
    # ...
    if not is_valid:
        print(json.dumps(
            {str(child): child.text for child in xml_node.getchildren()},
            indent=2))
    return is_valid


def _normalize_data(certificate_number, month, county):
    if month not in months.ALL:
        month = months.TO_VALID.get(month)
    return (
        certificate_number.replace(' ', ''),  # certificate numbers should have no whitespace
        month.lower() if month else None,
        county.lower()
    )


def xml_to_db(filename, row_node_key, certificate_type):
    """
    Store certificate data from an XML file.

    :param filename: name of xml file
    :param row_node_key: key of node containing field data
    :param certificate_type: one of app.constants.certificate_types
    """
    try:
        for i, elem in enumerate(ET.iterparse(filename)):
            if row_node_key in str(elem[1]):
                surname = _get_value(elem, 'Surname')
                given_name = _get_value(elem, 'GivenName')
                month = _get_value(elem, 'Month')
                day = _get_value(elem, 'Day')
                year = _get_value(elem, 'Year')
                certnbr = _get_value(elem, 'CertNbr')
                county = _get_value(elem, 'County')
                soundex = _get_value(elem, 'Soundex')

                if not _data_is_valid(certnbr, elem[1]):
                    continue

                certnbr, month, county = _normalize_data(certnbr, month, county)

                query = ("INSERT INTO certificate ("
                         "type, "
                         "last_name, "
                         "first_name, "
                         "month, "
                         "day, "
                         "year, "
                         "number, "
                         "county, "
                         "soundex,"
                         "filename) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                CUR.execute(query, (
                    certificate_type,
                    surname,
                    given_name,
                    month,
                    day,
                    year,
                    certnbr,
                    county,
                    soundex,
                    row_node_key  # TODO: transfer certificate files
                ))
                if i % CHUNKSIZE == 0:
                    CONN.commit()
        CONN.commit()
    except ET.ParseError:
        pass  # XML file was malformed


if __name__ == "__main__":
    files_to_type = {
        "Grooms 1866-1900.xml": certificate_types.MARRIAGE,
        "Brides 1866-1900.xml": certificate_types.MARRIAGE,
        "NYC Births 1901-1907.xml": certificate_types.BIRTH,
        "1868-1890 Deaths Manhattan.xml": certificate_types.DEATH  # TODO: check this
    }
    for file_, type_ in files_to_type.items():
        if file_ == "1868-1890 Deaths Manhattan.xml":
            # special case (might have to do with file name beginning with an integer)
            key = "_x0031_868-1890 Deaths Manhattan.xml"
        else:
            key = file_
        xml_to_db(
            os.path.join('XML', file_),
            key.replace(' ', '_x0020_').rstrip('.xml'),
            type_)
