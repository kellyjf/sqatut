#!/usr/bin/python3
from argparse import ArgumentParser as ap
import signal

import requests

if __name__ == "__main__":
	signal.signal(signal.SIGINT,signal.SIG_DFL)
	parser=ap()
	parser.add_argument("--list","-l", action="store_true", help="List Database")
	args=parser.parse_args()




