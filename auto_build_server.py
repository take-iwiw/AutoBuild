# coding: utf-8
#!/usr/bin/env python
import os
import subprocess
import datetime
from bottle import route, run, request, HTTPResponse, template, static_file, request
import zipfile

temp_dir = './uploaded/'

@route('/run', method='GET')
def entry_run():
	work_dir = 'work_manual_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
	subprocess.Popen('python  auto_build.py ' + work_dir, shell=True)
	return 'Build started'

@route('/upload', method='GET')
def upload():
	return '''
		プロジェクト全体をzip圧縮したファイルを選択してください
		<form action="/upload" method="post" enctype="multipart/form-data">
			<input type="file" name="upload"></br>
			<input type="submit" value="Upload & Build"></br>
		</form>
	'''

@route('/upload', method='POST')
def do_upload():
	global temp_dir
	upload = request.files.get('upload', '')
	if not upload.filename.lower().endswith(('.zip')):
		return 'File extension not allowed!'
	file_name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + upload.filename
	upload.save(temp_dir + file_name)

	with zipfile.ZipFile(temp_dir + file_name) as existing_zip:
		existing_zip.extractall(temp_dir + file_name + '_')
	os.remove(temp_dir + file_name)
	subprocess.Popen('python auto_build.py dummy ' + temp_dir + file_name + '_', shell=True)

	return 'Upload OK. Build started'


def main():
	global temp_dir
	if not os.path.exists(temp_dir):
		os.makedirs(temp_dir)
	print('Server Start')
	run(host='0.0.0.0', port=8080, debug=True, reloader=True)
	# run(host='0.0.0.0', port=8080, debug=False, reloader=False)

if __name__ == '__main__':
	main()


# python auto_build_server.py
# 192.168.1.89:8080/run			# build with the latest code on Git
# 192.168.1.89:8080/upload		# build with the uploaded code
