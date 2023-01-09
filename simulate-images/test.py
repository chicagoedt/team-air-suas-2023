import pain
import time
import statistics
test = []
for _ in range(100):
    start_time = time.time()
    pain.fnl_valid_img(1)
    curr_test = time.time() - start_time
    print(curr_test)
    test.append(curr_test)

print("mean:",statistics.mean(test))
print("median:",statistics.median(test))
print("mean:",statistics.mean(test))
print("standard_dev",stdev(test))

