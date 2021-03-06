from maxfw.core import MAXApp
from api import ModelMetadataAPI, ModelPredictAPI
from config import API_TITLE, API_DESC, API_VERSION
import os

os.environ['CORS_ENABLE'] = 'true'

max = MAXApp(API_TITLE, API_DESC, API_VERSION)
max.add_api(ModelMetadataAPI, '/metadata')
max.add_api(ModelPredictAPI, '/predict')
max.run()
