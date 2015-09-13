from amodem import main
from amodem import common
from amodem import sampling
from amodem import config
import utils

import numpy as np
import os
from io import BytesIO

import pytest
import logging

def get_bigger_string(size):
    acc = ""
    for x in range(0,size):
        acc += "s"
    return acc

def run(size, chan=None, df=0, success=True, cfg=None):

    if cfg is None:
        cfg = config.slowest()
        
    tx_data=get_bigger_string(10000)
    tx_audio = BytesIO()
    main.send(config=cfg, src=BytesIO(tx_data), dst=tx_audio, gain=0.5)
    with open('rx_data.wav','w') as f:
        f.write(tx_audio.getvalue())
        f.flush()
    dst = BytesIO()
    sampling.resample(src=tx_audio, dst=dst, df=50.0)
    

"""
    data = tx_audio.getvalue()
    data = common.loads(data)
    if chan is not None:
        data = chan(data)
    if df:
        sampler = sampling.Sampler(data, sampling.Interpolator())
        sampler.freq += df
        data = sampler.take(len(data))

    data = common.dumps(data)
    rx_audio = BytesIO(data)
    dump = BytesIO()

    try:
            result = main.recv(config=cfg, src=rx_audio, dst=rx_data, dump_audio=dump, pylab=None)
    finally:
        rx_audio.close()

    
    rx_data = rx_data.getvalue()

    assert data.startswith(dump.getvalue())

    assert result == success
    if success:
        assert rx_data == tx_data
        """

run(54321)
