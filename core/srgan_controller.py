from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from core.SRGAN.model import generator
from core.SRGAN.ops import deprocessLR, deprocess
import numpy as np
import skimage
import io


class SRGAN_controller:
    '''Essa classe funciona como um controller para os scripts do modelo'''

    def __init__(self, checkpoint, NUM_RESBLOCK=16):
        '''Inicializa o TF'''

        tf.compat.v1.disable_eager_execution()

        # Inicializa o input com dimensões corretas
        self.inputs_raw = tf.compat.v1.placeholder(tf.float32, shape=[1, None, None, 3], name='inputs_raw')

        # Constrói a rede
        with tf.compat.v1.variable_scope('generator'):
            gen_output = generator(self.inputs_raw, 3, reuse=False, is_training=False, num_resblock=NUM_RESBLOCK)

        with tf.name_scope('convert_image'):
            # Desprocessa o output
            inputs = deprocessLR(self.inputs_raw)
            outputs = deprocess(gen_output)

            # Converte para uint8
            converted_inputs = tf.image.convert_image_dtype(inputs, dtype=tf.uint8, saturate=True)
            converted_outputs = tf.image.convert_image_dtype(outputs, dtype=tf.uint8, saturate=True)

        with tf.name_scope('encode_image'):
            self.save_fetch = {
                "inputs": tf.map_fn(tf.image.encode_png, converted_inputs, dtype=tf.string, name='input_pngs'),
                "outputs": tf.map_fn(tf.image.encode_png, converted_outputs, dtype=tf.string, name='output_pngs')
            }

        # Define o peso do inicializador
        var_list = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES, scope='generator')
        weight_initializer = tf.compat.v1.train.Saver(var_list)

        # Define a operação de inicialização
        tf.compat.v1.global_variables_initializer()

        config = tf.compat.v1.ConfigProto()
        config.gpu_options.allow_growth = True

        self.sess = tf.compat.v1.Session(config=config)
        # Carrega o modelo
        weight_initializer.restore(self.sess, checkpoint)

    def upscale(self, INPUT_IMAGE):
        '''Sobe a escala da imagem'''

        # Verifica se INPUT_IMAGE é um np.array
        if INPUT_IMAGE.dtype != np.float32:
            raise TypeError("Tipo inválido: %r" % INPUT_IMAGE.dtype)

        if INPUT_IMAGE.shape[0] != 1 or INPUT_IMAGE.shape[-1] != 3:
            raise ValueError(f"INPUT_IMAGE.shape inválido: {INPUT_IMAGE.shape}")

        # Envia a imagem até o servidor
        results = self.sess.run(self.save_fetch, feed_dict={self.inputs_raw: INPUT_IMAGE})

        # Converte o bytestream em um objeto skimage
        output_image = skimage.io.imread(io.BytesIO(results['outputs'][0]), plugin='imageio')
        return output_image
