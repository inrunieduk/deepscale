from flask import send_file
from core.model import ModelWrapper
from maxfw.core import MAX_API, PredictAPI
from flask_restx import abort
from werkzeug.datastructures import FileStorage

# Parser de input (http://flask-restx.readthedocs.io/en/stable/parsing.html)
input_parser = MAX_API.parser()
input_parser.add_argument('image', type=FileStorage, location='files',
                          required=True,
                          help="Upload de imagem (RGB/HWC).\n"
                               "O tamanho ideal é 500x500 ou menor, "
                               "e os melhores resultados são obtidos com o formato PNG.\n"
                               "Imagens com dimensões acima de 2000x2000 resultarão em erro.")


class ModelPredictAPI(PredictAPI):

    model_wrapper = ModelWrapper()

    @MAX_API.doc('predict')
    @MAX_API.expect(input_parser)
    def post(self):
        """Retorna a predição com base no input"""

        args = input_parser.parse_args()
        try:
            input_data = args['image'].read()
            image = self.model_wrapper._read_image(input_data)
        except ValueError:
            abort(400,
                  "Por favor, envie uma imagem em formato PNG, Tiff ou JPEG")

        output_image = self.model_wrapper.predict(image)
        return send_file(self.model_wrapper.write_image(output_image), mimetype='image/png', attachment_filename='result.png')
