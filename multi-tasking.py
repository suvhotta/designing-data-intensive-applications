import socket, threading, sys, requests, time, dis

messages = []

squares = []
# print(sys.getcheckinterval())
print(sys.getswitchinterval())
def socket_connect(i):
    # This is an example of cooperative multi-tasking
    s = socket.socket()
    messages.append(f'Thread-{i}: connecting')
    s.connect(('python.org', 80))
    # Python thread drops the GIL at this spot when it is trying to do a network operation
    messages.append(f'Thread-{i}: connected')
import time
def calculate_squares(i):
    messages.append(f'Thread-{i}: calculating')
    for j in range(5):
        j*j
    messages.append(f'Thread-{i}: calculated')
#
#
threads = []

for i in range(3):
    t = threading.Thread(target=calculate_squares, args=(i+1,))
    threads.append(t)
    t.start()
#
#
for t in threads:
    t.join()
#
#
print('\n'.join(messages))
# print(squares)
# sys.setswitchinterval(0.000001)
# def run(thread_name):
#     # This execution will be taking beyond 5ms, hence the threads will be toggling for the GIL due to the preemptive multi-tasking.
#     for i in range(5000):
#         for j in range(5000):
#             pass
#         messages.append(f'Thread: {thread_name}')
#
# threads = []
#
#
# for i in range(2):
#     t = threading.Thread(target=run, args=(i,))
#     threads.append(t)
#     t.start()
#
# for t in threads:
#     t.join()
#
# print('\n'.join(messages))

# Checking thread safety




n = 0
# sys.setswitchinterval(0.000000000001)
def foo():
    global n
    n += 1

threads = []

for i in range(1000):
    t = threading.Thread(target=foo)
    threads.append(t)


for t in threads:
    t.start()

for t in threads:
    t.join()

print(n)
#
# websites_list = [
#     'https://www.youtube.com/',
#     'https://www.google.com/',
#     'https://boto3.amazonaws.com/',
#     'https://go.dev/learn/',
#     'https://aws.amazon.com/',
#     'https://jsonlint.com/',
#     'https://techbeacon.com/',
#     'https://stackoverflow.com/',
#     'https://www.quora.com/',
#     'https://www.hotstar.com/',
#     'https://www.youtube.com/watch?v=Dw_oH5oiUSE',
#     'https://music.youtube.com/watch?v=QptW1xR5jmM&list=PLjVdRxRYBaFvdeNVSf5L6SaT111rTN7YY',
#     'https://music.youtube.com/library/playlists',
#     'https://aws.amazon.com/premiumsupport/knowledge-center/',
#     'https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/sqs_lambda?tab=code'
#     'https://console.aws.amazon.com/events/home?region=us-east-1#/eventbus/default/rules/test-scheduled-event-rule'
# ]
#
# fetched_url_data = {}
#
#
# def worker():
#     for _ in websites_list:
#         url = websites_list.pop()
#         # except IndexError:
#         #     break
#
#         result = requests.get(url)
#         print(f'Fetched URL: {url}')
#         fetched_url_data[url] = result
#
#
# start = time.time()
# threads = []
# for _ in range(10):
#     t = threading.Thread(target=worker)
#     t.start()
#     threads.append(t)
#
# for t in threads:
#     t.join()
#
# print(f'Total time: {time.time()-start}')
# def increment(a):
#     a+=1
# print(dis.dis(increment))

