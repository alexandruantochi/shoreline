import time
import os

requests_since_start = 0
max_request_counter = 0
max_request_timer = 0
save_state_counter = 0
save_state_flag = False

config = {
    'starting_id': -1,
    'id_file_path': './id.dat',
    'max_requests': 100000,
    'max_requests_period': 1000,
    'save_state': 300000
}


def request_limit_hit():
    """checks if the maximum number of requests is hit in the last max_request_period"""
    global max_request_counter, max_request_timer
    max_request_counter += 1
    if max_request_counter > config['max_requests']:
        if timestamp() - max_request_timer < config['max_requests_period']:
            return True
        else:
            max_request_counter = 0
            max_request_timer = timestamp()
    return False


def get_id():
    global requests_since_start, save_state_counter, config
    save_state_counter += 1

    if request_limit_hit():
        return -1

    requests_since_start += 1

    if save_state_counter > config['save_state']:
        save_state_counter = 0
        save_state(requests_since_start + config['starting_id'])

    return requests_since_start + config['starting_id']


def node_id():
    """chose a random number for this"""
    return 130


def save_state(state):
    """saves the current number of requests on disk"""
    with open(config['id_file_path'], 'w') as f:
        f.write(str(state))


def init_node():
    """
    runs every time the node starts
    """
    global requests_since_start, config, max_request_timer
    config['starting_id'] = compute_starting_id()
    # if the file is already there, that means the system is restarting
    # we need to presume the system failed right before the id was written on disk
    if os.path.exists(config['id_file_path']):
        with open(config['id_file_path'], 'r') as f:
            try:
                requests_since_start = int(f.readline()) + config['save_state']
            except ValueError:
                print("Can't access requests file, pull data from backup (not implemented)")
    else:
        requests_since_start = 0
        save_state(requests_since_start)
    max_request_timer = timestamp()


def timestamp():
    """return time in millis since epoch"""
    return round(time.time() * 1000)


def compute_starting_id():
    """
    returns the id from which the particular node will start serving
    i.e each node will have their own 9007199254740991 ids which will
    last for ~2800 years with 100k requests per second
    """
    return 9223372036854775807 // 1024 * node_id()
