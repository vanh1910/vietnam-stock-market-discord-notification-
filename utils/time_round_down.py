import pandas as pd
import bisect 

def _milestone(ts: pd.Timestamp, day: int, hour:int, minute: int) -> pd.Timestamp:
    ts = ts.normalize()
    return ts + pd.Timedelta(days=day, hours=hour,minutes=minute)


def _time_round_down_by_minutes(ts: pd.Timestamp) -> pd.Timestamp:
    open_time = _milestone(ts,0,9,30)
    close_time = _milestone(ts,0,14,45)
    freeze_time = _milestone(ts,0,14,30)
    break_time = _milestone(ts,0,11,0)
    second_time = _milestone(ts,0,13,0)

    if ts < open_time:
        ts = close_time() - pd.Timedelta(days=1)
    elif ts > close_time:
        ts = close_time
    elif ts < close_time and ts > freeze_time:
        ts = freeze_time
    elif ts < second_time and ts > break_time:
        ts = break_time
    
    return ts

def _time_round_down_by_hours(ts: pd.Timestamp) -> pd.Timestamp:   
    avail_hour = [
        _milestone(ts,0,9,0),
        _milestone(ts,0,10,0),
        _milestone(ts,0,11,0),
        _milestone(ts,0,13,0),
        _milestone(ts,0,14,0),
    ] 
    ts = avail_hour[bisect.bisect_right(avail_hour,ts)-1]
    return ts


def time_round_down(ts: pd.Timestamp, resolution: str) -> pd.Timestamp:
    """
        Return the lastest available timestamp
        Args:
            ts (pandas.Timestamp) The timestamp needed to round down
            resolution (str): Time interval
    """ 
    if resolution == "1":
        ts = _time_round_down_by_minutes(ts)
    if (resolution == "60"):
        ts = _time_round_down_by_hours(ts)

if __name__ == "__main__":
    # print(_milestone(pd.Timestamp.now(), 0,10,0))
    print(_time_round_down_by_hours(pd.Timestamp.now()))