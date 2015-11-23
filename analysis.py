"""


"""

import numpy as np
from neo import AnalogSignal, get_io
from elephant.statistics import mean_firing_rate, cv, isi
from elephant.conversion import BinnedSpikeTrain
from elephant.spike_train_correlation import corrcoef
from quantities import ms, dimensionless, Quantity


def instantaneous_firing_rate(segment, begin, end):
    """Computed in bins of 0.1 ms """
    bins = np.arange(begin, end, 0.1)
    hist, _ = np.histogram(segment.spiketrains[0].time_slice(begin, end), bins)
    for st in segment.spiketrains[1:]:
        h, _ = np.histogram(st.time_slice(begin, end), bins)
        hist += h
    return AnalogSignal(hist, sampling_period=0.1*ms, units=dimensionless,
                        channel_index=0, name="Spike count")


def spike_statistics(idx, row):
    print(idx)
    results = {}

    # read spike trains from file
    io = get_io(row["output_file"])
    data_block = io.read()[0]
    spiketrains = data_block.segments[0].spiketrains

    # calculate mean firing rate
    results["spike_counts"] = sum(st.size for st in spiketrains)
    rates = [mean_firing_rate(st) for st in spiketrains]
    results["firing_rate"] = Quantity(rates, units=rates[0].units).rescale("1/s").mean()

    # calculate coefficient of variation of the inter-spike interval
    cvs = [cv(isi(st)) for st in spiketrains if st.size > 1]
    if len(cvs) > 0:
        results["cv_isi"] = sum(cvs)/len(cvs)
    else:
        results["cv_isi"] = 0

    # calculate global cross-correlation
    #cc_matrix = corrcoef(BinnedSpikeTrain(spiketrains, binsize=5*ms))
    #results["cc_min"] = cc_matrix.min()
    #results["cc_max"] = cc_matrix.max()
    #results["cc_mean"] = cc_matrix.mean()

    io.close()
    return results
