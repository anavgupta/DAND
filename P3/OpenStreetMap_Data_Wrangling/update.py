housenumber_mapping = {

    # To have consistency in the housenumbers
    ';': ', ',
    ' ,': ', ',
    ':': ', ',
    ' & ': ', ',
    '&': ', ',
    ' &': ', ',
    ' to': '-',
    ' - ': '-',
    '- ': '-',
    ' -': '-',

    # To correct the housenumbers
    'Unit12': 'Unit 12',
    'Apt': 'Apartment',
    'rear': 'Rear'
}


# To correct the typos in the street names
street_mapping = {
    'Street,': 'Street',
    'St': 'Street',
    'Gardens': 'Garden',
    'gardens': 'Garden',
    'G4ove': 'Grove',
    'drive': 'Drive',
    'Rd': 'Road',
    'road': 'Road',
    'W': 'West',
    'lane': 'Lane',
    'Lanes': 'Lane',
    'ln': 'Lane',
    'Morningside': 'Morningside Drive',
    'CLose': 'Close',
    'Chelmarsh': 'Chelmarsh Close',
    'Wells': 'Well',
    'Avenueue': 'Avenue',
    'Ave': 'Avenue',
    'avenue': 'Avenue',
    'aveune': 'Avenue',
    'park': 'Park',
    'Fields': 'Field',
    'green': 'Green',
    'Laurels': 'Laurel',
    'Beech': 'Beeches'
}

# To update the street name fields that contain postalcode data
postalCode_street = {
    'B15 2AY': 'Great Colmore Street',
    'B76 1DL': 'Sutton Coldfield',
    'B20 3BQ': 'Penshurst Avenue'
}


# To Update the street names that contain the typos in the street mapping object
def update_street(street, street_type):
    if street_type in street_mapping:
        updated = street.replace(street_type, street_mapping[street_type])
        return updated

    elif street in postalCode_street:
        updated = postalCode_street[street]
        return updated
    else:
        return street


# To update the housenumbers
def update_housenumber(housenumber, type):
    for x in housenumber_mapping:
            if housenumber.find(x) != -1:
                updated = housenumber.replace(x, housenumber_mapping[x])
                return updated.title()
    else:
        return housenumber.title()
