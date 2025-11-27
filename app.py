from flask import Flask
from logger.logger import Logger
from schemas.schemaVPNMayo import RegistroSchemaVPNMayo
from schemas.schemaTel import RegistroSchemaTel
from schemas.schemaRFC import RegistroSchemaRFC
from schemas.schemaInter import RegistroSchemaInter
from schemas.schemaDNS import RegistroSchemaDNS
from schemas.schemaABC import RegistroSchemaABC
from schemas.schemaFolio import BusquedaPorFolio
from schemas.schemaActualizarCampo import ActualizacionCampo
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
form_schemaDNS=RegistroSchemaDNS()
form_schemaABC=RegistroSchemaABC()
form_schemaFolio = BusquedaPorFolio()
form_schemaCampo = ActualizacionCampo()

# Model
db_conn = BDModel()
db_conn.connect_to_database()

# Service
service = Service(db_conn)

# Routes
routes = FileGeneratorRoute(service, form_schemaVPNMayo, form_schemaTel, form_schemaRFC, form_schemaInter, form_schemaDNS,form_schemaABC,form_schemaFolio, form_schemaCampo)

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