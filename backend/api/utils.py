from shapely import wkb


def dump_geo(geom):
    """
    builds the geojson geometry for web response.
    :param geom: POINT geometry
    :return: geojson geometry, else None
    """
    if geom is not None:
        p = wkb.loads(bytes(geom.data))
        return {'type': 'Point',
                'coordinates': [p.x, p.y]}
    return None


def dump_results(results):
    return [{
        'type': 'Feature',
        'properties': {
            'id': r.id,
            'name': r.name,
            'admin1': r.admin1,
            'admin2': r.admin2,
            'iso2': r.country_code,
            'featureClass': r.feature_class,
            'featureCode': r.feature_code,
            'population': r.population,
            'elevation': r.elevation,
            'gtopo30': r.gtopo30,
            'timezone': r.timezone,
            'moddate': r.moddate,
        },
        'geometry': dump_geo(r.the_geom),
    } for r in results]
