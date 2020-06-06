import os
import coverage
import unittest
from flask.cli import FlaskGroup
from api import create_app, db


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, "data")

COV = coverage.coverage(
    branch=True,
    include='api/*',
    omit=[
        'tests/*',
        'config.py',
        'api/*/__init__.py'
    ]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('test')
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command('cov')
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@cli.command('recreate_db')
def recreate():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('load')
def load_data():
    db.drop_all()
    db.create_all()
    db.session.commit()
    load_admin1_codes()
    load_admin2_codes()
    load_geonames()


def load_admin1_codes(file=None, cnx=None):
    """
    Load admin 1 codes
    :param file: input file for unit testing
    :param cnx: database connection for unit testing
    :return: None
    """
    if not file:
        file = download_and_extract('admin1CodesASCII.txt')
    with open(file, 'r', encoding='utf8') as f:
        conn = db.create_engine(cnx if cnx else app.config['SQLALCHEMY_DATABASE_URI'], {}).raw_connection()
        cursor = conn.cursor()
        cmd = '''    
        COPY admin1code(code, name, name_ascii, geonameid) FROM STDIN WITH delimiter E'\t' null as ''
        '''
        cursor.copy_expert(cmd, f)
        cursor.execute(
            "UPDATE admin1code SET country_code = SPLIT_PART(code, '.', 1);"
            "UPDATE admin1code SET admin1 = SPLIT_PART(code, '.', 2);"
            "")
        conn.commit()
    if not cnx:
        print('populated the admin codes table.')


def load_admin2_codes(file=None, cnx=None):
    """
    Load admin 2 codes
    :param file: input file for unit testing
    :param cnx: database connection for unit testing
    :return: None
    """
    if not file:
        file = download_and_extract('admin2Codes.txt')
    with open(file, 'r', encoding='utf8') as f:
        conn = db.create_engine(cnx if cnx else app.config['SQLALCHEMY_DATABASE_URI'], {}).raw_connection()
        cursor = conn.cursor()
        cmd = '''    
        COPY admin2code(code, name, name_ascii, geonameid) FROM STDIN WITH delimiter E'\t' null as ''
        '''
        cursor.copy_expert(cmd, f)
        cursor.execute(
            "UPDATE admin2code SET country_code = SPLIT_PART(code, '.', 1);"
            "UPDATE admin2code SET admin1 = SPLIT_PART(code, '.', 2);"
            "UPDATE admin2code SET admin2 = SPLIT_PART(code, '.', 3);"
            "")
        conn.commit()
    if not cnx:
        print('populated the admin 2 codes table.')


def load_geonames(file=None, cnx=None):
    """
    Load geonames data
    :param file: input file for unit testing
    :param cnx: database connection for unit testing
    :return: None
    """
    if not file:
        file = download_and_extract(os.getenv('GEONAMES_DATA') + ".zip")
        print("importing geonames data...")
    with open(file, 'rb') as f:
        conn = db.create_engine(cnx if cnx else app.config['SQLALCHEMY_DATABASE_URI'], {}).raw_connection()
        cursor = conn.cursor()
        cmd = '''    
        COPY geoname(geonameid, name, asciiname, alternatenames, latitude, longitude, feature_class, feature_code, 
        country_code, cc2, admin1, admin2, admin3, admin4, population, elevation, gtopo30, timezone, moddate) 
        FROM STDIN WITH delimiter E'\t' null as ''
        '''
        cursor.copy_expert(cmd, f)
        cursor.execute(
            "UPDATE geoname SET the_geom = ST_PointFromText('POINT(' || longitude || ' ' || latitude || ')', 4326);")
        conn.commit()
    if not cnx:
        print('populated the geonames table.')


def download_and_extract(file_name):
    """
    Downloads from geoname dump and returns the local .txt file location
    :param file_name: input filename to download (.txt or .zip)
    :return: full pathname of downloaded/extracted file.
    """
    from tqdm import tqdm
    import requests
    import zipfile
    print('downloading {}...'.format(file_name))
    url = "http://download.geonames.org/export/dump/{}".format(file_name)
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    dest_path = os.path.join(data_path, file_name)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024  # 1 kb
        t = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(dest_path, "wb") as handle:
            for data in tqdm(r.iter_content(block_size)):
                t.update(len(data))
                handle.write(data)
        t.close()
        if total_size != 0 and t.n != total_size:
            raise Exception("Error downloading {}".format(file_name))
        if ".zip" in file_name:
            with zipfile.ZipFile(dest_path, 'r') as zip_ref:
                zip_ref.extractall(data_path)
            dest_path = os.path.join(data_path, file_name.split(".zip")[0] + ".txt")
        return dest_path
    else:
        raise Exception('Error reaching Geonames server. {} {}.'.format(r.status_code, r.reason))


if __name__ == '__main__':
    cli()
