import logging
import math

log = logging.getLogger("opserv.database")
log.setLevel(logging.DEBUG)


def get_split_indices(element_count, limit):
    if element_count <= limit:
        # No need to summarize data if element_count does not exceed the limit
        log.error("Method: get_split_indices; Error: The element_count does not exceed the limit. Actual values were: "
                  "element_count=" + element_count + ", limit=" + limit)
        raise ValueError("The element_count does not exceed the limit. Actual values were: element_count="
                         + element_count + ", limit=" + limit)
    if limit <= 0:
        # Impossible to summarize data into 0 data points
        log.error("Method: get_split_indices; Error: The limit has to be an positive integer greater than 0. "
                  "Actual value was: " + limit)
        raise ValueError("The limit has to be an positive integer greater than 0. Actual value was: " + limit)

    step = element_count / limit

    indices = []
    for i in range(0, limit):
        indices.append((
            math.ceil(i * step),
            math.ceil((i + 1) * step) - 1
        ))

    return indices


def summarize_data(data_list, limit):
    limited_list = []

    time_list = list(map(lambda x: x["timestamp"], data_list))
    value_list = list(map(lambda x: x["value"], data_list))

    indices = get_split_indices(len(data_list), limit)
    for index_tuple in indices:
        start_index = index_tuple[0]
        end_index = index_tuple[1]

        value_list_part = value_list[start_index:end_index + 1]
        time_list_part = time_list[start_index:end_index + 1]

        limited_list.append({
            "min": min(value_list_part),
            "average": sum(value_list_part) / len(value_list_part),
            "max": max(value_list_part),
            "timestamp": sum(time_list_part) / len(time_list_part)
        })

    return limited_list


import time

time1 = time.time()
get_split_indices(1000000, 20)
print(time.time() - time1)

time1 = time.time()
get_split_indices(1000000, 50)
print(time.time() - time1)

time1 = time.time()
get_split_indices(1000000, 100)
print(time.time() - time1)

time1 = time.time()
get_split_indices(1000000, 250)
print(time.time() - time1)

time1 = time.time()
get_split_indices(1000000, 500)
print(time.time() - time1)

time1 = time.time()
get_split_indices(1000000, 1000)
print(time.time() - time1)

time1 = time.time()
get_split_indices(1000000, 2500)
print(time.time() - time1)

time1 = time.time()
get_split_indices(1000000, 999999)
print(time.time() - time1)
