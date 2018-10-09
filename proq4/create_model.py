from __future__ import division
import os
import collections

import numpy as np
import keras

proq4 = collections.namedtuple('ProQ4', ['model', 'renormalisation'])


def _get_proq4(version=1):
    # FIXME
    """Get the ProQ4 architecture.

    Version:
        0: No weights
        1: first model
        -1: latest
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    model = ''

    # Pick the right model
    if version == -1:
        version = 1

    if version == 0:
        model_path = None
    elif version == 1:
        model_path = 'models/pq4_v1.h5'
    else:
        raise (ValueError('Unkown version number {}'.format(version)))

    if model_path:
        model.load_weights(os.path.join(base_path, model_path), by_name=True)
    return model


def get_proq4(version=1):
    """Get the ProQ4 architecture.

    Version:
        0: No weights
        1: first model
        -1: latest
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    model_path = 'models/pq4_v1.h5'
    model = keras.models.load_model(os.path.join(base_path, model_path))

    def renorm(classes):
        options = {'hi': 0.8790753677665549, 'low': 0.08856313291052981, 'offset': -0.008493915223623744,
                   'error_hi': 1.5523259116908388, 'error_low': 1.5513558612873304, 'error_offset': 1.5378064091796733}

        predicted = np.sum(classes * np.linspace(options['low'], options['hi'], num=classes.shape[1])[None, :], axis=1)
        return predicted

    return proq4(model, renorm)


if __name__ == '__main__':
    m = get_proq4(1).model
    m.summary()
    print(m.input_shape)
    print([m for m in m.input_layers])
