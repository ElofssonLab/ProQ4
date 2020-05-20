from __future__ import unicode_literals
import collections
import numpy as np

from proq4 import dssp_parser

proq4_result = collections.namedtuple('ProQ4_results', ('lddt', 'raw_classes'))


def predict(proq4, alignment_data, pdb):
    self_info, part_entr, seq = alignment_data
    dssp_results, valid = dssp_parser.parse(pdb, seq.shape[1])

    classes = proq4.model.predict([seq, self_info, part_entr, dssp_results[None, ...]]).squeeze()
    predictions = proq4.renormalisation(classes)
    predictions[~valid] = 0.

    return proq4_result(predictions, classes)

