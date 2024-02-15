"""
Stream to Sliding Window.

Useful when combined with XY plot/constellation plot.

e.g. [0, 1, 2, 3, 4, ...] with a window size of 3: [0, 1, 2, 1, 2, 3, 2, 3, 4, ...]
"""

import numpy as np
from gnuradio import gr


class blk(gr.basic_block):
    """
    Stream to Sliding Window.

    Useful when combined with XY plot/constellation plot.

    e.g. [0, 1, 2, 3, 4, ...] with a window size of 3: [0, 1, 2, 1, 2, 3, 2, 3, 4, ...]
    """

    def __init__(self, window_size=2, step=1):
        """sliding window"""
        gr.basic_block.__init__(
            self,
            name='Stream to Sliding Window',
            in_sig=[np.float32],
            out_sig=[np.float32],
        )
        self._step = step
        self._window_size = window_size
        self.set_history(window_size + 1)
        self.declare_sample_delay(step)
        self.set_output_multiple(window_size)
        self.set_relative_rate(window_size, step)
        self.set_min_noutput_items(window_size)

    def general_work(self, input_items, output_items):
        """sliding window"""
        in_buf = input_items[0]
        out_buf = output_items[0]
        npos = 0
        spos = 0
        while npos <= len(out_buf) - self._window_size:
            if len(in_buf) - spos < self._window_size:
                break
            out_buf[npos:][:self._window_size] = in_buf[spos:][:self._window_size]
            npos += self._window_size
            spos += self._step
        self.consume_each(spos)
        return npos
