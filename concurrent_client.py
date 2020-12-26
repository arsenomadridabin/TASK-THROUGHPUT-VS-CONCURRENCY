#!/usr/bin/env python3
# countasync.py

import asyncio
import socket
import time
import math
import optparse
import os

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5051    # The port used by the server


async def send_data(s,random_file):
	f = open('./10/{}'.format(random_file),'rb')
	data = f.read()
	data_size = len(data)
	data_in_mb = data_size/math.pow(10,6)
	s.sendall(data)
	r_data = s.recv(202400)

async def get_data(concurrency):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		send_time = time.time()
		list_files = os.listdir(os.getcwd()+"/10")
		no_of_slots = int(100/concurrency) + 1 if int(100/concurrency) != float(100/concurrency) else int(100/concurrency)
		for i in range(no_of_slots):
			files_this_iteration = list_files[concurrency*i: (concurrency*i + concurrency)]
			await asyncio.gather(*[send_data(s,x) for x in files_this_iteration])
			print(i)


if __name__ == "__main__":
	import time
	s = time.perf_counter()

	parser = optparse.OptionParser("Usage: python3 concurrent_client.py -n <Concurrency Number>")
	parser.add_option('-n', dest='concurrency', type='int', help="specify concurrency number")
	(options, args) = parser.parse_args()
	concurrency = options.concurrency

	asyncio.run(get_data(concurrency))
	elapsed = time.perf_counter() - s
	print(f"{__file__} Data Transfered in {elapsed:0.2f} seconds.")
