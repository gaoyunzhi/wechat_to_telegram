import os
import sys
import time

def kill():
	os.system("ps aux | grep ython | grep wc_forward | awk '{print $2}' | xargs kill -9")
	os.system("ps aux | grep ython | grep wc_reply | awk '{print $2}' | xargs kill -9")

def setup():
	kill()
	if 'kill' in str(sys.argv):
		return 
	addtional_arg = ' '.join(sys.argv[1:])
	os.system('touch nohup.out')
	os.system('nohup python3 -u wc_forward.py %s &' % addtional_arg)
	time.sleep(2)
	os.system('nohup python3 -u wc_reply.py %s &' % addtional_arg)
	if 'notail' not in str(sys.argv):
		os.system('tail -F nohup.out')

if __name__ == '__main__':
	setup()