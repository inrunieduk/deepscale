# modo debug do Flask
DEBUG = True

# configurações Flask-restx
RESTX_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'none'

# metadados da API
API_TITLE = 'Deepscale'
API_DESC = 'Aumento de resolução de imagem. Modelo treinado usando o dataset OpenImagesV4.'
API_VERSION = '1.0'
CORS_ENABLE = True

# modelo padrão
MODEL_NAME = 'SRGAN'
DEFAULT_MODEL_PATH = 'assets/SRGAN/model'

MODEL_META_DATA = {
    'id': 'SRGAN-tensorflow',
    'name': 'Super-Resolution Generative Adversarial Network (SRGAN)',
    'description': 'SRGAN trained on the OpenImagesV4 dataset.',
    'type': 'Image-To-Image Translation Or Transformation',
    'source': 'https://github.com/brade31919/SRGAN-tensorflow',
    'license': 'MIT'
}
