
import itertools
#from skimage.measure import compare_ssim, compare_mse
import cv2 
import base64
import azure.batch.batch_service_client as batch
import azure.batch.batch_auth as batchauth
import azure.batch.models as batchmodels
import sys

creds = batchauth.SharedKeyCredentials('searchtesting', 'F9TaLHOShNOskte7D/FUYcjvmLyv0tHWZmisokT73t8d6GNNNezhK/G//8mpX/Yb4ibqA7GL5r1AryDQoYW9dA==')
#config = batch.BatchServiceClientConfiguration(creds, base_url = 'https://searchtesting.centralus.batch.azure.com')
client = batch.BatchServiceClient(creds,batch_url='https://searchtesting.centralus.batch.azure.com')


min_circles = 20
max_circles = 45
ssim_test = .992
job_id = 'run1'

params = {
    'hough_blurLevel': range(7,15,2),
    'hough_minDist': range(20,100,5),
    'hough_param2': range(90,120,2),
    'hough_param1': range(30,80,2),
    'hough_maxRadius': range(10,30),
    'hough_minRadius':range(5,15)
}


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 




f = open(r"C:\Users\joscholt\Downloads\testfile.txt",'r')
source_image_bytes = f.read()


retval, buffer = cv2.imencode('.jpg', cv2.imread(r"C:\Users\joscholt\Documents\image_processing_test\baseline.jpg"))
test_image_bytes = base64.b64encode(buffer)


job = batch.models.JobAddParameter(
    id=job_id,
    pool_info=batch.models.PoolInformation(pool_id="paramTune"))
client.job.add(job)


keys = list(params)
prd = itertools.product(*map(params.get, keys))
total = len(list(prd))
count = 0

print("")
print("Total Tests: {}".format(total))
print("")
tasks = []
for values in itertools.product(*map(params.get, keys)):
    progress(count,total, "")
    count+=1
    command = "/env3/bin/python3 /app/paramtest.py params {} min_circles {} max_circles {} ssim_test {} source_image_bytes {} test_image_bytes {} destination {}".format( 
    dict(zip(keys, values)), min_circles,max_circles,ssim_test,'','','tune')
    print(dict(zip(keys, values)))
    tasks.append(batch.models.TaskAddParameter( 
        id='Task{}'.format(count), 
        command_line=command
    ))
    break

#env = batch.models.EnvironmentSetting('AZ_BATCH_TASK_WORKING_DIR','/app')


client.task.add_collection(job_id, tasks)
           


print('DONE..')
