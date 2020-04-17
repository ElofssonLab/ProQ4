# ProQ4:
Protein Quality Estimation.

https://arxiv.org/abs/1804.06281

## Installation instructions:

    pip3 install numpy Cython &&
    pip3 install .

You will also need a deep learning backend compatible with Keras. We recommend Tensorflow:

    pip3 install -U tensorflow


You will also need dssp to be installed and in the path (as well as
the Bio.PDB module from biopython

## Usage instructions

Inside Python:

    import proq4

    model = proq4.get_proq4()
    ali = proq4.process_a3m('path/to/alignment.a3m')
    # Also available: process_aln and process_fasta
    
    pred_1 = proq4.predict(model, ali, 'path/to/pdb1')
    pred_2 = proq4.predict(model, ali, 'path/to/pdb2')

## Example
example file to run and predict values for lddt is in casp-run.py

This command should work

python3 proq4/casp-run.py -msa PL-pro.fasta.a3m -pdb C1904TS003_1.pdb -out C1904TS003_1.QA
(the results is save in proq4.qa for comparison=