from configparser import ConfigParser, NoOptionError
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load the db.ini file
parser = ConfigParser()
parser.read(Path(__file__).parent.resolve().joinpath('../config.ini'))

# Read DB info
db_url = None
if parser.has_section('db'):
    try:
        db_url = parser.get('db', 'sqlite')
    except NoOptionError:
        raise Exception('db URL not found in db section of config.ini file.')
else:
    raise Exception('Section db not found in config.ini file.')

engine = create_engine(db_url, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
