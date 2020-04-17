#!/usr/bin/env python
'''
Toy example to get transmembrane currents from axon
'''
import os
from os.path import join
import numpy as np
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
import neuron
import LFPy

outfolder = "results"
# os.makedirs(outfolder, exist_ok=True)
os.makedirs(outfolder)


def return_cell():

    neuron.load_mechanisms("HallermannEtAl2012")
    # Define cell parameters
    cell_parameters = {          # various cell parameters,
        'morphology' : 'unmyelinated_axon_Hallermann.hoc', # Mainen&Sejnowski, 1996
        'v_init' : -80.,    # initial crossmembrane potential
        'passive' : False,   # switch off passive mechs
        'nsegs_method' : 'lambda_f',
        'lambda_f' : 1000.,
        'dt' : 2.**-7,   # [ms] dt's should be in powers of 2
        'tstart' : -200.,    # start time of simulation, recorders start at t=0
        'tstop' : 2.,   # stop simulation at 2 ms.
    }

    cell = LFPy.Cell(**cell_parameters)
    cell.set_pos(x=-np.max(cell.xmid) / 2, z=2.5)

    #  To induce a spike:
    synapseParameters = {
        'idx' : 0,               # insert synapse on index "0", the soma
        # 'idx' : cell.get_closest_idx(x=-35,y=0,z=2.5)
        'e' : 0.,                # reversal potential of synapse
        'syntype' : 'Exp2Syn',   # conductance based double-exponential synapse
        'tau1' : 0.1,            # Time constant, decay
        'tau2' : 0.1,            # Time constant, decay
        'weight' : 0.004,         # Synaptic weight
        'record_current' : False, # Will enable synapse current recording
    }

    # attach synapse with parameters and input time
    synapse = LFPy.Synapse(cell, **synapseParameters)
    synapse.set_spike_times(np.array([0.1]))

    cell.simulate(rec_vmem=True, rec_imem=True)
    return cell

cell = return_cell()

source_pos = np.array([cell.xmid, cell.ymid, cell.zmid]).T
np.save(join(outfolder, "source_pos.npy"), source_pos)
np.save(join(outfolder, "axon_imem.npy"), cell.imem)
np.save(join(outfolder, "axon_tvec.npy"), cell.tvec)

max_vmem_t_idx = np.argmax(np.abs(cell.vmem[-1] - cell.vmem[0, 0]))
max_imem_t_idx = np.argmax(np.abs(cell.imem[-1] - cell.imem[0, 0]))

fig = plt.figure(figsize=[9, 9])
fig.subplots_adjust(wspace=0.5, hspace=0.5)

ax1 = fig.add_subplot(221, xlabel="Time (ms)", ylabel="Membrane potential (mV)")
ax2 = fig.add_subplot(222, xlabel="Time (ms)", ylabel="Transmembrane Current (nA)")
ax3 = fig.add_subplot(212, xlabel="x ($\mu$m)",
                      ylabel="Membrane current at t={:1.2f}".format(cell.tvec[max_vmem_t_idx]))
ax1.axvline(cell.tvec[max_imem_t_idx], ls=":", c='gray')
ax2.axvline(cell.tvec[max_imem_t_idx], ls=":", c='gray')
[ax1.plot(cell.tvec, cell.vmem[idx, :]) for idx in range(cell.totnsegs)]
[ax2.plot(cell.tvec, cell.imem[idx, :]) for idx in range(cell.totnsegs)]

clrs = lambda t_idx: plt.cm.Reds(t_idx *350/ len(cell.tvec))
for t_idx in np.arange(len(cell.tvec)):
    ax3.plot(cell.xmid, cell.imem[:, t_idx], c=clrs(t_idx))

ax3.plot(cell.xmid, cell.imem[:, max_imem_t_idx], lw=2, c='k')
ax3.axhline(0, c='gray', ls='--')

plt.savefig("axon_simulation.png")
