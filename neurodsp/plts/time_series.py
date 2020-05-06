"""Plots for time series."""

from itertools import repeat, cycle

import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

from neurodsp.plts.style import style_plot
from neurodsp.plts.utils import check_ax, savefig

###################################################################################################
###################################################################################################

@savefig
@style_plot
def plot_time_series(times, sigs, labels=None, colors=None, ax=None):
    """Plot a time series.

    Parameters
    ----------
    times : 1d array or list of 1d array
        Time definition(s) for the time series to be plotted.
    sigs : 1d array or list of 1d array
        Time series to plot.
    labels : list of str, optional
        Labels for each time series.
    cols : str or list of str
        Colors to use to plot lines.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.

    Examples
    --------
    Create a time series plot:

    >>> from neurodsp.sim import sim_combined
    >>> from neurodsp.utils import create_times
    >>> sig = sim_combined(n_seconds=10, fs=500,
    ...                    components={'sim_synaptic_current': {},
    ...                                'sim_bursty_oscillation' : {'freq': 10}},
    ...                    component_variances=(0.1, 0.9))
    >>> times = create_times(n_seconds=10, fs=500)
    >>> plot_time_series(times, sig)

    """

    ax = check_ax(ax, (15, 3))

    times = repeat(times) if isinstance(times, np.ndarray) else times
    sigs = [sigs] if isinstance(sigs, np.ndarray) else sigs

    if labels is not None:
        labels = [labels] if not isinstance(labels, list) else labels
    else:
        labels = repeat(labels)

    if colors is not None:
        colors = repeat(colors) if not isinstance(colors, list) else cycle(colors)
    else:
        colors = cycle(['k', 'r', 'b', 'g', 'm', 'c'])

    for time, sig, color, label in zip(times, sigs, colors, labels):
        ax.plot(time, sig, color, label=label)

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Voltage (uV)')


@savefig
@style_plot
def plot_instantaneous_measure(times, sigs, measure='phase', ax=None, **plt_kwargs):
    """Plot an instantaneous measure, of phase, amplitude or frequency.

    Parameters
    ----------
    times : 1d array or list of 1d array
        Time definition(s) for the time series to be plotted.
    sigs : 1d array or list of 1d array
        Time series to plot.
    measure : {'phase', 'amplitude', 'frequency'}
        Which kind of measure is being plotted.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    **plt_kwargs
        Keyword arguments to pass into `plot_time_series`.

    Examples
    --------
    Create a instantaneous phase plot:

    >>> from neurodsp.sim import sim_combined
    >>> from neurodsp.utils import create_times
    >>> sig = sim_combined(n_seconds=10, fs=500,
    ...                    components={'sim_synaptic_current': {},
    ...                                'sim_bursty_oscillation' : {'freq': 10}},
    ...                    component_variances=(0.1, 0.9))
    >>> times = create_times(n_seconds, fs=500)
    >>> plot_instantaneous_measure(times, sig, measure='phase')

    """

    if measure not in ['phase', 'amplitude', 'frequency']:
        raise ValueError('Measure not understood.')

    if measure == 'phase':
        plot_time_series(times, sigs, ax=ax, ylabel='Phase (rad)', **plt_kwargs)
        plt.yticks([-np.pi, 0, np.pi], ['-$\pi$', 0, '$\pi$'])
    elif measure == 'amplitude':
        plot_time_series(times, sigs, ax=ax, ylabel='Amplitude', **plt_kwargs)
    elif measure == 'frequency':
        plot_time_series(times, sigs, ax=ax, ylabel='Instantaneous\nFrequency (Hz)', **plt_kwargs)


@savefig
@style_plot
def plot_bursts(times, sig, bursting, ax=None, **plt_kwargs):
    """Plot a time series, with labeled bursts.

    Parameters
    ----------
    times : 1d array
        Time definition for the time series to be plotted.
    sig : 1d array
        Time series to plot.
    bursting : 1d array
        A boolean array which indicates identified bursts.
    ax : matplotlib.Axes, optional
        Figure axes upon which to plot.
    **plt_kwargs
        Keyword arguments to pass into `plot_time_series`.

    Examples
    --------
    Plot bursts:

    >>> from neurodsp.sim import sim_combined
    >>> from neurodsp.utils import create_times
    >>> from neurodsp.burst import detect_bursts_dual_threshold
    >>> sig = sim_combined(n_seconds=10, fs=500,
    ...                    components={'sim_synaptic_current': {},
    ...                                'sim_bursty_oscillation' : {'freq': 10}},
    ...                    component_variances=(0.1, 0.9))
    >>> is_burst = detect_bursts_dual_threshold(sig, fs=500, dual_thresh=(1, 2), f_range=(7, 12))
    >>> times = create_times(n_seconds, fs=500)
    >>> plot_bursts(times, sig, is_burst, labels=['Raw Data', 'Detected Bursts'])

    """

    ax = check_ax(ax, (15, 3))

    bursts = ma.array(sig, mask=np.invert(bursting))
    plot_time_series(times, [sig, bursts], ax=ax, **plt_kwargs)
