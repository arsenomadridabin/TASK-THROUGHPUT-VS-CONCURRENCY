#!/usr/bin/env python3
# countasync.py

import asyncio
import socket
import time
import math
import optparse
import os
import hashlib

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5050    # The port used by the server


async def send_data(s,random_file,folder_name):
	f = open('./{}/{}'.format(folder_name,random_file),'rb')
	data = f.read()
	data_size = len(data)
	data_in_mb = data_size/math.pow(10,6)
	md5_of_data = hashlib.md5(data).hexdigest()

	"""Send md5 of data along with data for integrity check"""
	data = data.decode() + "md5-begins:{}:md5-ends".format(md5_of_data)
	s.sendall(data.encode())
	r_data = s.recv(202400)

async def get_data(concurrency,folder_name,no_of_files):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		send_time = time.time()
		list_files = os.listdir(os.getcwd()+"/"+folder_name)
		no_of_slots = int(no_of_files/concurrency) + 1 if int(no_of_files/concurrency) != float(no_of_files/concurrency) else int(no_of_files/concurrency)
		for i in range(no_of_slots):
			files_this_iteration = list_files[concurrency*i: (concurrency*i + concurrency)]
			await asyncio.gather(*[send_data(s,x,folder_name) for x in files_this_iteration])


if __name__ == "__main__":
	import time
	s = time.perf_counter()

	parser = optparse.OptionParser("Usage: python3 concurrent_client.py -n <Concurrency Number> -f  <folder nam> -s <no of files>")
	parser.add_option('-n', dest='concurrency', type='int', help="specify concurrency number")
	parser.add_option('-f', dest='folder_name', type='str', help="specify folder name")
	parser.add_option('-s', dest='no_of_files', type='int', help="specify no of files in a folder")
	(options, args) = parser.parse_args()
	concurrency = options.concurrency
	folder_name = options.folder_name
	no_of_files = options.no_of_files

	asyncio.run(get_data(concurrency,folder_name,no_of_files))
	elapsed = time.perf_counter() - s
	print(f"{__file__} Data Transfered in {elapsed:0.2f} seconds.")
