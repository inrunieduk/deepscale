import io
import logging

import numpy as np
import skimage.color
import skimage.io
import skimage.transform

from flask import abort
from maxfw.model import MAXModelWrapper
from config import DEFAULT_MODEL_PATH, MODEL_META_DATA as model_meta
from core.srgan_controller import SRGAN_controller

logger = logging.getLogger()


class ModelWrapper(MAXModelWrapper):
    MODEL_META_DATA = model_meta

    def __init__(self, path=DEFAULT_MODEL_PATH):
        logger.info('Carregando modelo em: {}...'.format(path))

        # Inicializa o controller
        self.SRGAN = SRGAN_controller(checkpoint=DEFAULT_MODEL_PATH)

        logger.info('Modelo carregado')

    def _read_image(self, image_data):
        '''Lê a imagem de um Bytestream.'''
        image = skimage.io.imread(io.BytesIO(image_data), plugin='imageio')
        return image

    def _pre_process(self, image):
        '''
        Pré-processamento de imagem.

        1. Verifica dimensões da imagem
        2. Redimensiona se ultrapassar o tamanho permitido pelo modelo
        3. Normaliza a imagem
        4. Padroniza a imagem
        '''
        # Padronização da imagem
        image = image.astype('uint8')

        # Conversão para RGB
        if image.ndim != 3:
            image = skimage.color.gray2rgb(image)
        # Remoção de canal alpha
        if image.shape[-1] == 4:
            image = image[..., :3]

        # Redimensiona a iamgem
        logger.info(f'dimensão: {image.shape[0]}x{image.shape[1]}')

        # a. encontra fator de escala
        factor = np.ceil(max(image.shape[0], image.shape[1]) / 500)

        # b. redimensiona
        if factor > 1:  # se ao menos uma imagem é maior que 500px
            if factor > 4:
                message = "A imagem é muito grande (>2000px)."
                logger.error(message)
                abort(400, message)

            image = skimage.transform.resize(image,
                                             (np.floor(image.shape[0] / factor), np.floor(image.shape[1] / factor)),
                                             anti_aliasing=True)
            logger.info(f'imagem redimensionada: {image.shape[0]}x{image.shape[1]}')

        # Normalização
        image = image / np.max(image)

        # Converte a imagem em um array numpy com dtype float32
        # (1, H, W, C)
        image = np.array([image]).astype(np.float32)

        return image

    def _predict(self, image):
        '''Chama o modelo'''
        return self.SRGAN.upscale(image)

    def write_image(self, image):
        '''Retorna a imagem gerada como output'''
        logger.info(f'dimensão da imagem de output: {image.shape[0]}x{image.shape[1]}')
        stream = io.BytesIO()
        skimage.io.imsave(stream, image)
        stream.seek(0)
        return stream

    def _post_process(self, result):
        '''Pós-processamento'''
        return result
