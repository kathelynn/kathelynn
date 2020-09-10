import time
timer = lambda: time.process_time()
timespent = []
timespent.append(timer())
for x in range(0, int(1e2)):
    print('You are cute!')
    timespent.append(timer())

deduction = 0
for pos in range(0, len(timespent)):
    timespent[pos] = timespent[pos] - deduction
    deduction = deduction + timespent[pos]

timespent[0] = 0
total = 0
for pos in range(0, len(timespent)):
    total = total + timespent[pos]

final = total / (len(timespent) + 1) * 1e+9
total *= 1e+6
print(str(total) + ' execution time in microseconds \n' + str(final) + ' nanoseconds every instruction')