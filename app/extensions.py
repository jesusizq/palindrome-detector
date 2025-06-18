from apifairy import APIFairy
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
apifairy = APIFairy()
cors = CORS()
ma = Marshmallow()
cache = Cache()
