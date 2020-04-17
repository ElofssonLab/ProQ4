import math

import numpy as np
from Bio.PDB import DSSP, PDBParser
import distutils.spawn

p = PDBParser(QUIET=1)

ss_dict = dict(H=0, E=1, B=2, G=3, I=3, S=4, T=4)
ss_dict[' '] = 5
ss_dict['-'] = 5


def parse(pdb, seq_len):
    structure = p.get_structure('', pdb)
    model = structure[0]
    if not distutils.spawn.find_executable("dssp"):
        print ("ERROR dssp not founs")
    try:
        dssp = DSSP(model, pdb, acc_array='Wilke')
    except:
        print ("ERROR DSSP failed")
        return

    six_state = np.zeros((seq_len, 6), dtype=np.float32)
    dihedrals_sc = np.zeros((seq_len, 4), dtype=np.float32)

    rsa = np.zeros((seq_len, 1))
    valid = np.zeros(seq_len, dtype=np.bool_)
    done = set()

    for k in dssp.keys():
        index = k[1][1] - 1
        if index in done:
            if not k[1][-1].strip():
                continue
        if index < 0 or index >= seq_len:
            index = max(done, default=0)
        done.add(index)

        dssp_content = dssp[k]
        ss = dssp_content[2]
        rsa_ = dssp_content[3]
        if rsa_ == 'NA':
            rsa_ = np.nan
        phi = math.radians(dssp_content[4])
        psi = math.radians(dssp_content[5])

        six_state[index, :] = 0.
        six_state[index, ss_dict[ss]] = 1.
        rsa[index, 0] = rsa_
        dihedrals_sc[index, 0] = math.sin(phi)
        dihedrals_sc[index, 1] = math.cos(phi)
        dihedrals_sc[index, 2] = math.sin(psi)
        dihedrals_sc[index, 3] = math.cos(psi)
        valid[index] = True

    # Fix rsa NaNs
    if np.isnan(rsa).any():
        nans = np.isnan(rsa)
        x = lambda z: z.nonzero()[0]
        rsa[nans] = np.interp(x(nans), x(~nans), rsa[~nans])

    assert not np.isnan(rsa).any()

    three_state = np.zeros((six_state.shape[0], 3), dtype=np.float32)
    three_state[:, 0] = six_state[:, 0] + six_state[:, 3]
    three_state[:, 1] = six_state[:, 1] + six_state[:, 2]
    three_state[:, 2] = six_state[:, 4] + six_state[:, 5]

    assert three_state.sum(axis=1).max() == 1., three_state.sum(axis=1)

    assert six_state.sum(axis=1).max() == 1., six_state.sum(axis=1)

    dssp_arr = np.concatenate((three_state, six_state, rsa, dihedrals_sc), axis=1)
    return dssp_arr, valid


