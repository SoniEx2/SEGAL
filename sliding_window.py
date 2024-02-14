"""
Stream to Sliding Window.

Useful when combined with XY plot/constellation plot.

e.g. [0, 1, 2, 3, 4, ...] with a window size of 3: [0, 1, 2, 1, 2, 3, 2, 3, 4, ...]
"""

import numpy as np
from gnuradio import gr


class blk(gr.interp_block):
    """
    Stream to Sliding Window.

    Useful when combined with XY plot/constellation plot.

    e.g. [0, 1, 2, 3, 4, ...] with a window size of 3: [0, 1, 2, 1, 2, 3, 2, 3, 4, ...]
    """

    def __init__(self, window_size=2):
        """sliding window"""
        gr.interp_block.__init__(
            self,
            name='Stream to Sliding Window',
            in_sig=[np.float32],
            out_sig=[np.float32],
            interp=window_size
        )
        self._buf = np.empty(0, np.float32)
        self._window_size = window_size

    def work(self, input_items, output_items):
        """sliding window"""
        self._buf = np.append(self._buf, input_items[0])
        npos = 0
        while npos <= len(output_items[0]) - self._window_size:
            if len(self._buf) < self._window_size:
                return npos
            output_items[0][npos:][:self._window_size] = self._buf[:self._window_size]
            npos += self._window_size
            self._buf = np.delete(self._buf, 0)
        return npos
