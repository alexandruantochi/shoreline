import unittest
import sequential
import os
import math
import time


class TestSequential(unittest.TestCase):
    def test_first_init_file_creation(self):
        sequential.init_node()
        file_path = sequential.config['id_file_path']
        assert os.path.exists(file_path), 'File was not created at init'
        os.remove(file_path)

    def test_first_init_value_is_zero(self):
        sequential.init_node()
        file_path = sequential.config['id_file_path']
        file_value = ''
        with open(file_path, 'r') as f:
            file_value = f.readline()
        os.remove(file_path)
        assert file_value == '0', 'File value not set to 0'

    def test_init_after_restart(self):
        added_value = 1500
        with open(sequential.config['id_file_path'], 'w') as f:
            f.write(str(added_value))
        sequential.init_node()
        os.remove(sequential.config['id_file_path'])
        assert sequential.requests_since_start == added_value + sequential.config[
            'save_state'], 'Init after crash wrong requests number'

    def test_save_state(self):
        file_path = sequential.config['id_file_path']
        state_value = 1500
        file_value = ''
        sequential.save_state(state_value)
        with open(file_path, 'r') as f:
            file_value = f.readline()
        os.remove(file_path)
        assert state_value == int(file_value), 'File value does not match state'

    def test_request_limit_hit(self):
        sequential.max_request_timer = sequential.timestamp()
        i = 0
        # run for less than max_requests_period
        while sequential.timestamp() - sequential.max_request_timer < sequential.config['max_requests_period']:
            if i < sequential.config['max_requests']:
                assert sequential.request_limit_hit() is False
            if i > sequential.config['max_requests']:
                assert sequential.request_limit_hit() is True
            i += 1

    def test_id_in_sequence(self):
        sequential.config['max_requests'] = math.inf
        sequential.init_node()
        start = time.time()
        run_time_seconds = 1
        cnt = 0
        dummy_id = -1
        while time.time() - start < run_time_seconds:
            dummy_id = sequential.get_id()
            cnt += 1
        assert dummy_id == cnt + sequential.compute_starting_id()


class Benchmark(unittest.TestCase):
    def test_max_requests_possible_with_state_save(self):
        sequential.config['max_requests'] = math.inf
        sequential.init_node()
        start = time.time()
        run_time_seconds = 5
        cnt = 0
        dummy_id = -1
        while time.time() - start < run_time_seconds:
            dummy_id = sequential.get_id()
            cnt += 1
        assert dummy_id == cnt + sequential.compute_starting_id()
        print('Module can handle up to ~' + str(cnt // run_time_seconds) + ' requests per second with state saving.')


if __name__ == '__main__':
    unittest.main()
