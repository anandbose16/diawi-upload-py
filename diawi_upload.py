import pycurl
import os
from io import BytesIO
import json
import time

retry_max_count = 10
retry_wait_time = 5

config_file = open('diawi_metadata.json')
config = json.load(config_file)

diawi_token = config['diawi_token']

def diawi_upload_file(file_path):
	response_buffer = BytesIO()
	c = pycurl.Curl()
	c.setopt(c.URL, 'https://upload.diawi.com/')
	c.setopt(c.HTTPPOST, [('token', diawi_token),('file', (c.FORM_FILE, file_path))])
	c.setopt(c.WRITEDATA, response_buffer)
	c.perform()
	c.close()
	response_str = response_buffer.getvalue().decode('iso-8859-1')
	response_json = json.loads(response_str)
	job_id = response_json["job"]
	return str(job_id)
	
def diawi_check_job(job_id, iter_count=0):
	if iter_count == retry_max_count - 1:
		print('- Error: Tried %d times for job %s' % (retry_max_count, job_id))
		return ''
	response_buffer = BytesIO()
	c = pycurl.Curl()
	c.setopt(c.URL, "https://upload.diawi.com/status?token=%s&job=%s" % (diawi_token, job_id))
	c.setopt(c.WRITEDATA, response_buffer)
	c.perform()
	c.close()
	response_str = response_buffer.getvalue().decode('iso-8859-1')
	response_json = json.loads(response_str)
	status = response_json["status"]
	if status == 2000:
		return response_json["link"]
	else:
		print("Upload Error:")
		print(response_str)
		print("Retrying after", retry_wait_time, "seconds", iter_count + 1)
		time.sleep(retry_wait_time)
		return diawi_check_job(job_id, iter_count + 1)
	
def get_apk_files():
	files = list()
	for (dirpath, dirnames, filenames) in os.walk('.'):
		for filename in filenames:
			if filename.endswith('.apk') or filename.endswith('.ipa'):
				files.append(os.path.join(dirpath, filename))
	return files

apk_files = get_apk_files()
job_ids = list()
diawi_links = list()

apk_file_count = len(apk_files)
upload_count = 1
check_count = 1

for apk_file in apk_files:
	print("Uploading %s / %s" % (str(upload_count), str(apk_file_count)), end="\r", flush=True)
	job_id = diawi_upload_file(apk_file)
	job_ids.append(job_id)
	upload_count += 1

print("")

for job_id in job_ids:
	print("Checking %s / %s" % (str(check_count), str(apk_file_count)), end="\r", flush=True)
	diawi_link = diawi_check_job(job_id)
	diawi_links.append(diawi_link)
	check_count += 1
	
print("\nDone")

for i in range(len(apk_files)):
	line = ""
	apk_file = os.path.basename(apk_files[i])
	if 'artifacts' in config:
		artifacts = config['artifacts']
		if apk_file in artifacts:
			line += str(artifacts[apk_file])
		else:
			line += str(apk_file)
	line += " - "
	line += str(diawi_links[i])
	print(line)
	
