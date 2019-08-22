from plugin_collection import Plugin
from keras.models import Model
from keras.models import load_model
import json

class Keras(Plugin):

    def __init__(self):
        super().__init__()
        self.description = 'Keras Frontend Plugin'
        self.identifier = 'keras'

    def transform_to_intermediate_format(self, input):

        model = load_model(input)
        model_json = json.loads(model.to_json())

        count=0
        last_batch_input_shape=None
        last_units=0

        for layer in model_json['config']['layers']:
            weights = model.layers[count].get_weights()[0]
            biases = model.layers[count].get_weights()[1]
            layer['kernel_values'] = weights.tolist()
            layer['bias_values'] = biases.tolist()

            if (last_batch_input_shape!=None):
                new_batch_input_shape = last_batch_input_shape
                new_batch_input_shape[1]= last_units
                layer['config']['batch_input_shape'] = new_batch_input_shape
            count+=1
            last_units = layer['config']['units']
            last_batch_input_shape = layer['config']['batch_input_shape']

        return model_json