times = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
time_index = 0
total_count = 0

def getFPS(time):
    global times
    global time_index
    global total_count

    times[time_index] = time
    total_count = total_count + 1
    time_index = time_index + 1
    if (total_count > 30):
        total_count = 30
    if (time_index >= 30):
        time_index = 0

    total_time = 0.0
    for i in range(0,total_count):
        total_time = total_time + times[i]

    avg_time = total_time/total_count

    ret_fps = 1/avg_time
    ret_fps = int(ret_fps*10)/10

    return ret_fps
