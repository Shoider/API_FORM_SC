from flask import Flask
from logger.logger import Logger
from schemas.schemaVPNMayo import RegistroSchemaVPNMayo
from schemas.schemaTel import RegistroSchemaTel
from schemas.schemaRFC import RegistroSchemaRFC
from schemas.schemaInter import RegistroSchemaInter
from routes.route import FileGeneratorRoute  
from services.service import Service
from models.model import BDModel

#ESTO se comenta
#from flask_cors import CORS

app = Flask(__name__)

#ESTO se comenta
#CORS(app)

logger = Logger()

# Schema
form_schemaVPNMayo = RegistroSchemaVPNMayo()
form_schemaTel = RegistroSchemaTel()
form_schemaRFC = RegistroSchemaRFC()
form_schemaInter = RegistroSchemaInter()

# Model
db_conn = BDModel()
db_conn.connect_to_database()

# Service
service = Service(db_conn)

# Routes
routes = FileGeneratorRoute(service, form_schemaVPNMayo, form_schemaTel, form_schemaRFC, form_schemaInter)

#Blueprint
app.register_blueprint(routes)

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", debug=False)
        #app.run(host="0.0.0.0", port=5001, debug=False)
        logger.info("Application started")
    finally:
        db_conn.close_connection()
        logger.info("Application closed")
        logger.info("MongoDB connection closed")