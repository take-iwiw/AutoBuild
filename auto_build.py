# coding: utf-8
#!/usr/bin/env python

import commands
import datetime
import sys

### settings
git_url = 'https://github.com/take-iwiw/AutoBuild.git'
scripts = [
	['scripts/build_pj1.sh', 'Project 1'],
	['scripts/build_pj2.sh', 'Project 2']
]
log_dir = ''		# log text files are saved here ()
code_dir = ''		# source code cloned from GitHub comes here

def get_source_code():
	global code_dir
	work_dir = './work'
	if len(sys.argv) > 1:
		work_dir = sys.argv[1]
	if work_dir[-1].count('/') == 0:
		work_dir += '/'
	code_dir = work_dir + 'code_dir'
	commands.getoutput('git clone ' + git_url + ' ' + code_dir)

def create_log_dir():
	global log_dir
	log_dir = 'log_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
	commands.getoutput('mkdir ' + log_dir)

def treat_result(result_message):
	print(result_message)
	# todo: send slack message

def run_all_build():
	global log_dir
	global code_dir
	result_message = '\n--------\nAuto build result\n' + log_dir + '\n'
	for script in scripts:
		print('running: ' + script[0])
		ret = commands.getoutput('bash ./' + script[0] + ' ' + code_dir)
		# print ret
		f = open(log_dir + '/log_' + script[0].split('/')[-1] + '.txt', 'w')
		f.write(ret)
		f.close()

		if ret.count('[100%] Built'):
			print("  OK")
			result_message += script[1] + ': OK\n'
		else:
			print("  ERROR")
			result_message += script[1] + ': ERROR\n'
			result_message += '--- build log ---\n'
			result_message += ret
			result_message += '\n---------------\n\n'
	treat_result(result_message)

def main():
	global code_dir
	if len(sys.argv) > 2:
		code_dir = sys.argv[2]
	else:
		get_source_code()
	create_log_dir()
	run_all_build()

if __name__ == '__main__':
	main()

# python auto_build.py [work_dir] [code_dir]
# work_dir: git clone用のワーキングディレクトリ。未指定時は'./code_dir'
# code_dir: ソースコードのディレクトリ。未指定時はgit cloneする