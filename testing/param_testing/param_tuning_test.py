
import itertools
import cv2 
import base64
import azure.batch.batch_service_client as batch
import azure.batch.batch_auth as batchauth
import azure.batch.models as batchmodels
import sys
import json 

with open(r"C:\Users\joscholt\Documents\GitHub\config.json") as f:
    config = json.load(f)


creds = batchauth.SharedKeyCredentials(config["batch_service"],config["batch_connection_str"] )
client = batch.BatchServiceClient(creds,batch_url=config["batch_url"])


min_circles = 20
max_circles = 50
ssim_test = .9933
job_id = 'run8'
max_tests = 50000

params = {
    "hough_dp":range(1,3),
    "hough_blurLevel": range(7,13,2),
    "hough_minDist": range(10,30,5),
    "hough_param2": range(80,120,10),
    "hough_param1": range(10,80,10),
    "hough_maxRadius": range(15,50,5),
    "hough_minRadius":range(10,20,5),
    "hough_dilate_iter":range(2,7,1)
}

keys = list(params)
prd = itertools.product(*map(params.get, keys))
total_tests = len(list(prd))

print("")
print("Total Tests: {}".format(total_tests))
print("")

if total_tests <= max_tests:

    job = batch.models.JobAddParameter(
        id=job_id,
        pool_info=batch.models.PoolInformation(pool_id="paramTune"),
       on_all_tasks_complete =  'terminateJob'
    )

    client.job.add(job)

    count = 0

    task_container_settings = batch.models.TaskContainerSettings(
        image_name='jscholtes/pid_param_tune:latest',
        container_run_options='--workdir /app')


    tasks = []
    for values in itertools.product(*map(params.get, keys)):
    # progress(count,total, "")
        count+=1
        command = "python3 /app/paramtest.py --params '{}' --min_circles {} --max_circles {} --ssim_test {} --source_file_name '{}' --validation_file_name '{}' --destination '{}'".format( 
        json.dumps(dict(zip(keys, values))), min_circles,max_circles,ssim_test,'test.jpg','baseline.jpg','tune' + "/" + job_id)
        #print(command)
        tasks.append(batch.models.TaskAddParameter( 
            id='Task{}'.format(count), 
            command_line=command,
            container_settings=task_container_settings
        ))
       

    #env = batch.models.EnvironmentSetting('AZ_BATCH_TASK_WORKING_DIR','/app')

    client.task.add_collection(job_id, tasks)
           


print('DONE..')
