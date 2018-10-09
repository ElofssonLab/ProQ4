# ProQ4:
Protein Quality Estimation.

https://arxiv.org/abs/1804.06281

## Installation instructions:

    pip3 install numpy Cython &&
    pip3 install .

You will also need a deep learning backend compatible with Keras. We recommend Tensorflow:

    pip3 install -U tensorflow


## Usage instructions

Inside Python:

    import proq4

    model = proq4.get_proq4()
    ali = proq4.process_a3m('path/to/alignment.a3m')
    # Also available: process_aln and process_fasta
    
    pred_1 = proq4.predict(model, ali, 'path/to/pdb1')
    pred_2 = proq4.predict(model, ali, 'path/to/pdb2')

