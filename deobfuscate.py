#!/usr/local/bin/python3
import re
import sys

def deobfusate_char(match):
	try:
		char = match.group(1)
		if char[0] == "x":
			if len(char) == 2:
				char = "x0{}".format(char[1])
			res = bytes(bytearray.fromhex(char[1:])).decode("utf-8")
		else:
			res = chr(int(char, 8))
		if res is "\n" or res is "\t" or res is "\r":
			res = ""
		return res+match.group(2)
	except UnicodeDecodeError:
		print(char)
		return char+match.group(2)

def main(file):
	try:
		with open(file, "r") as f:
			data = f.read()
		for i in range(10000):
			data = re.sub(r'\\([a-z0-9]+?)(\\|\"|\{)', deobfusate_char, data, count=1)
		with open(file, "w") as f:
			f.write(data)
	except Exception as e:
		print("Error: {}".format(e))


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Usage: {} <filename>".format(sys.argv[0]))
		exit()

	main(sys.argv[1])