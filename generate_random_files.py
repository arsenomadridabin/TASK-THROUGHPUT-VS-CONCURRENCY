import os
import math
import uuid
import random
def generate_random_file(size_in_mb,number_of_files):
	if not str(size_in_mb) in os.listdir():
		os.makedirs(str(size_in_mb))
	for count in range(number_of_files):
		size_in_bytes = size_in_mb * 1024 * 1024
		int_size_in_bytes = int(size_in_bytes)
		data = chr(random.randint(0,127))*int_size_in_bytes
		data = data + "end_of_data"
		data = data.encode()
		with open(os.getcwd()+"/"+str(size_in_mb)+"/"+"random{}".format(str(count+1)), "wb") as f:
			f.write(data)
			f.close()


generate_random_file(10,100)