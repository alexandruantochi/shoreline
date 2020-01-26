# Sequential
A sequential 64 bit id generator that can save the sequence to disk

## Implementation

There are numerous examples of how to implement twitter snowflake or variations of this id generator so I decided to do a sequential one that saves the state to disk every given number of requests.

One advantage would be that the system does not need to have access UNIX time and having a counter that measures system uptime in milliseconds is enough for the requests throttling to work, if we want that feature (e.g. an array of microcontrollers not connected to the internet). Because of this, the current state needs to be saved in case of a restart. 

In theory, Twitter snowflake can produce 4096 unique ids every 1 millisecond and then rollback (with a counter of 12bits). Sequential can theoretically produce MAX_INT / 1024.

## Extra features

* request throttling (number of requests / time)
* works without having access to UNIX Epoch / internet as long as there is a system uptime clock available

## Usage

Sequential has a few config options:

```JSON
config = {
    'starting_id': -1,
    'id_file_path': './id.dat',
    'max_requests': 100000,
    'max_requests_period': 1000,
    'save_state': 300000
}
```

`id_file_path`: location where the state will be saved

`max_requests`: number of maximum requests per `max_requests_period`

`max_requests_period` : timeframe in milliseconds in which `max_requests` can happen; the period counter resets if `max_requests` have happened in more than the period

`save_state` : number of requests after which the state is saved; this takes into account the worst case scenario when the system fails just before the state is saved, thus at the next restart, the node will start serving the last state + `save_state` count

## Testing

Unit tests that check if request throttling works, state is saved etc. 

