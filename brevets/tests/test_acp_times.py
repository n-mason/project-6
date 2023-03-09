"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

from acp_times import open_time, close_time
import arrow
import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


def test_brevet1():
    start_time = arrow.get("2023-02-18 08:00", "YYYY-MM-DD HH:mm")
    dist = 200
    checkpoints = {
                    0: (start_time, start_time.shift(hours=1)),
                    50: (start_time.shift(hours=1, minutes=28), start_time.shift(hours=3, minutes=30)),
                    150: (start_time.shift(hours=4, minutes=25), start_time.shift(hours=10)),
                    200: (start_time.shift(hours=5, minutes=53), start_time.shift(hours=13, minutes=30)),
                    }

    for km, time_tuple in checkpoints.items():
        checkpoint_open, checkpoint_close = time_tuple
        
        assert open_time(km, dist, start_time) == checkpoint_open
        assert close_time(km, dist, start_time) == checkpoint_close


def test_brevet2():
    start_time = arrow.get("2023-04-04 13:00", "YYYY-MM-DD HH:mm")
    dist = 300
    checkpoints = {
                    0: (start_time, start_time.shift(hours=1)),
                    60: (start_time.shift(hours=1, minutes=46), start_time.shift(hours=4)),
                    120: (start_time.shift(hours=3, minutes=32), start_time.shift(hours=8)),
                    180: (start_time.shift(hours=5, minutes=18), start_time.shift(hours=12)),
                    240: (start_time.shift(hours=7, minutes=8), start_time.shift(hours=16)),
                    300: (start_time.shift(hours=9), start_time.shift(hours=20)),
                    }

    for km, time_tuple in checkpoints.items():
        checkpoint_open, checkpoint_close = time_tuple
        
        assert open_time(km, dist, start_time) == checkpoint_open
        assert close_time(km, dist, start_time) == checkpoint_close

def test_brevet3():
    start_time = arrow.get("2023-08-14 09:00", "YYYY-MM-DD HH:mm")
    dist = 400
    checkpoints = {
                    0: (start_time, start_time.shift(hours=1)),
                    100: (start_time.shift(hours=2, minutes=56), start_time.shift(hours=6, minutes=40)),
                    200: (start_time.shift(hours=5, minutes=53), start_time.shift(hours=13, minutes=20)),
                    300: (start_time.shift(hours=9), start_time.shift(hours=20)),
                    400: (start_time.shift(hours=12, minutes=8), start_time.shift(hours=27)),
                    }

    for km, time_tuple in checkpoints.items():
        checkpoint_open, checkpoint_close = time_tuple
        
        assert open_time(km, dist, start_time) == checkpoint_open
        assert close_time(km, dist, start_time) == checkpoint_close

def test_brevet4():
    start_time = arrow.get("2023-04-04 00:00", "YYYY-MM-DD HH:mm")
    dist = 600
    checkpoints = {
                    0: (start_time, start_time.shift(hours=1)),
                    150: (start_time.shift(hours=4, minutes=25), start_time.shift(hours=10)),
                    350: (start_time.shift(hours=10, minutes=34), start_time.shift(hours=23, minutes=20)),
                    450: (start_time.shift(hours=13, minutes=48), start_time.shift(hours=30)),
                    600: (start_time.shift(hours=18, minutes=48), start_time.shift(hours=40)),
                    }

    for km, time_tuple in checkpoints.items():
        checkpoint_open, checkpoint_close = time_tuple
        
        assert open_time(km, dist, start_time) == checkpoint_open
        assert close_time(km, dist, start_time) == checkpoint_close

def test_brevet5():
    start_time = arrow.get("2022-02-22 00:00", "YYYY-MM-DD HH:mm")
    dist = 1000
    checkpoints = {
                    0: (start_time, start_time.shift(hours=1)),
                    200: (start_time.shift(hours=5, minutes=53), start_time.shift(hours=13, minutes=20)),
                    400: (start_time.shift(hours=12, minutes=8), start_time.shift(hours=26, minutes=40)),
                    600: (start_time.shift(hours=18, minutes=48), start_time.shift(hours=40)),
                    800: (start_time.shift(hours=25, minutes=57), start_time.shift(hours=57, minutes=30)),
                    1000: (start_time.shift(hours=33, minutes=5), start_time.shift(hours=75)),
                    }

    for km, time_tuple in checkpoints.items():
        checkpoint_open, checkpoint_close = time_tuple
        
        assert open_time(km, dist, start_time) == checkpoint_open
        assert close_time(km, dist, start_time) == checkpoint_close


""" Some print statements for debugging tests
print("---- run opt,clt--------")
print(open_time(km, dist, start_time))
print(close_time(km, dist, start_time))
print("--------chpointop, chpointclose-------")
print(checkpoint_open)
print(checkpoint_close)
print("------------------------")
"""
