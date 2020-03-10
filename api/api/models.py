from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import and_
from api import db
from api.utils import dump_geo, dump_results


def execute_geoname_query(queries):
    """
    executes Geonames query
    """
    return db.session.query(Geoname.geonameid.label('id'),
                            Geoname.name.label('name'),
                            Admin1Code.name.label('admin1'),
                            Admin2Code.name.label('admin2'),
                            Geoname.country_code,
                            Geoname.feature_class,
                            Geoname.feature_code,
                            Geoname.population,
                            Geoname.elevation,
                            Geoname.gtopo30,
                            Geoname.timezone,
                            Geoname.moddate,
                            Geoname.the_geom) \
        .outerjoin(Admin1Code,
                   and_(Geoname.admin1 == Admin1Code.admin1,
                        Geoname.country_code == Admin1Code.country_code)) \
        .outerjoin(Admin2Code, and_(Geoname.admin2 == Admin2Code.admin2,
                                    Admin1Code.admin1 == Admin2Code.admin1)) \
        .filter(*queries) \
        .group_by(Geoname.geonameid,
                  Geoname.name,
                  Admin1Code.name,
                  Admin2Code.name,
                  Geoname.country_code,
                  Geoname.feature_class,
                  Geoname.feature_code,
                  Geoname.population,
                  Geoname.elevation,
                  Geoname.gtopo30,
                  Geoname.timezone,
                  Geoname.moddate,
                  Geoname.the_geom).all()


class Admin1Code(db.Model):
    """ names in English for admin divisions """
    __tablename__ = 'admin1code'
    __table_args__ = (
        db.PrimaryKeyConstraint('code'),
        db.Index('idx_admin1codes_country', 'country_code'),
        db.Index('idx_admin1codes_admin1', 'admin1'),
        db.Index('idx_admin1codes_name', 'name'),
    )
    code = db.Column(db.String(23))
    name = db.Column(db.String(200))
    name_ascii = db.Column(db.String(200))
    geonameid = db.Column(db.Integer)
    country_code = db.Column(db.String(2))
    admin1 = db.Column(db.String(20))

    def __repr__(self):
        return '<Admin1Code %r>' % self.name


class Admin2Code(db.Model):
    """ names for administrative subdivision  """
    __tablename__ = 'admin2code'
    __table_args__ = (
        db.PrimaryKeyConstraint('code'),
        db.Index('idx_admin2codes_admin1', 'admin1'),
        db.Index('idx_admin2codes_admin2', 'admin2'),
        db.Index('idx_admin2codes_name', 'name'),
    )
    code = db.Column(db.String(104))
    country_code = db.Column(db.String(2))
    admin1 = db.Column(db.String(20))
    admin2 = db.Column(db.String(80))
    name = db.Column(db.String(200))
    name_ascii = db.Column(db.String(200))
    geonameid = db.Column(db.Integer)

    def __repr__(self):
        return '<Admin2Code %r>' % self.name


class Geoname(db.Model):
    __tablename__ = 'geoname'
    __table_args__ = (
        db.PrimaryKeyConstraint('geonameid'),
        db.Index('idx_geoname_country', 'country_code'),
        db.Index('idx_geoname_name', 'name'),
        db.Index('idx_geoname_admin1', 'admin1'),
        db.Index('idx_geoname_admin2', 'admin2'),
        db.Index('idx_geoname_fcode', 'feature_code'),
        db.Index('idx_geoname_fclass', 'feature_class'),

        db.Index('idx_geoname_pop', 'population'),
        db.Index('idx_geoname_elev', 'elevation'),
        db.Index('idx_geoname_gtopo', 'gtopo30'),
        db.Index('idx_geoname_tzone', 'timezone'),
        db.Index('idx_geoname_mod', 'moddate'),
        db.Index('idx_geoname_geom', 'the_geom', postgresql_using='gist')
    )
    geonameid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    asciiname = db.Column(db.String(200))
    alternatenames = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    feature_class = db.Column(db.String(1))
    feature_code = db.Column(db.String(10))
    country_code = db.Column(db.String(2))
    cc2 = db.Column(db.String(200))
    admin1 = db.Column(db.String(20))
    admin2 = db.Column(db.String(80))
    admin3 = db.Column(db.String(20))
    admin4 = db.Column(db.String(20))
    population = db.Column(db.BigInteger)
    elevation = db.Column(db.Integer)
    gtopo30 = db.Column(db.Integer)
    timezone = db.Column(db.String(40))
    moddate = db.Column(db.Date)
    the_geom = db.Column(Geometry('POINT', 4326, spatial_index=False))

    def __repr__(self):
        return '<Geoname {}>'.format(self.name)

    @staticmethod
    def geocode(iso2=None, name=None, admin1=None, admin2=None, feature_code=None, feature_class=None):
        """
        Geocodes a place or city.
        :param iso2: 2 digit country code
        :param name: a geoname. This field is required.
        :param admin1: First level administrative code. Ex., a state in the US. This field is optional.
        :param admin2: Second level administrative code. Ex., a county in the US. This field is optional.
        :param feature_code: Geoname Feature Code
        :param feature_class: Geoname Feature Class
        :return: a list of geojson results
        """
        queries = []
        if name:
            queries.append(Geoname.name.ilike('%{}%'.format(name)))
        if iso2:
            queries.append(Geoname.country_code == iso2.upper())
        if admin1:
            queries.append(Admin1Code.name.ilike('%{}%'.format(admin1)))
        if admin2:
            queries.append(Admin2Code.name.ilike('%{}%'.format(admin2)))
        if feature_code:
            queries.append(Geoname.feature_code == feature_code.upper())
        if feature_class:
            queries.append(Geoname.feature_class == feature_class.upper())
        return dump_results(execute_geoname_query(queries))

    @staticmethod
    def reverse_geocode(lat=None, lon=None, accuracy=None, feature_code=None, feature_class=None):
        """
        Returns a city or place based on latitude and longitude input.
        :param lat: latitude
        :param lon: longitude
        :param accuracy: how far to search outside given coordinates
        :param feature_code: Geoname Feature Code
        :param feature_class: Geoname Feature Class
        :return: list of geojson results
        """
        if lon and lat:
            queries = []
            point = WKTElement('POINT({0} {1})'.format(lon, lat), srid=4326).ST_Buffer(accuracy)
            queries.append(Geoname.the_geom.ST_Intersects(point))
            if feature_code:
                queries.append(Geoname.feature_code == feature_code.upper())
            if feature_class:
                queries.append(Geoname.feature_class == feature_class.upper())
            return dump_results(execute_geoname_query(queries))
        return None
