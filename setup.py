import os
import sys

def kill():
	os.system("ps aux | grep ython | grep forward | awk '{print $2}' | xargs kill -9")
	os.system("ps aux | grep ython | grep reply | awk '{print $2}' | xargs kill -9")

def setup():
	kill()
	if 'kill' in str(sys.argv):
		return 
	addtional_arg = ' '.join(sys.argv[1:])
	os.system('touch nohup.out')
	os.system('nohup python3 -u forward.py &' % addtional_arg)
	os.system('nohup python3 -u reply.py &' % addtional_arg)
	os.system('tail -F nohup.out')

if __name__ == '__main__':
	setup()