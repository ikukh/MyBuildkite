from pip import main
import requests
import time
from datetime import datetime
import os

buildkite_token = os.environ['BKT']
print (os.environ['BKT'])

print(os.environ[MYENV])


class Buildkite_runner:

    def __init__(self):
        self.data = None

    def create_build(self):
        timestamp = datetime.now()
        url = 'https://api.buildkite.com/v2/organizations/ikukh-org/pipelines/test/builds'
        header = { 'Authorization': 'Bearer %s'%(buildkite_token)}
        body = {"commit": "FETCH_HEAD", "branch": "master", "message": "Started via API, attemps %s"%timestamp}

        # Make a request and create new build 
        request = requests.post(url, headers=header, json=body)

        self.data = request.json()
        print(type(self.data))
 

    def pipeline_details(self):
        self.jobs = self.data['jobs']
        self.build_id = self.data['id']
        self.build_number = self.data['number']
        self.pipeline_id = (self.data['pipeline']['id'])

        # Print build details
        print('Buildkite Pipeline ID:', self.pipeline_id)
        print('Buildkite Build ID: ', self.build_id)
        print('Buildkite Build Number: ', self.build_number)
        print('Buildkite Executed jobs:')
        # Print jobs details
        for items in self.jobs:
            try:
                print('Job ID:', items['id'], items['state'])
            except:
                pass

        # Wait while job is running
        time.sleep(20)


    # Make one more call to receive current job states
    def state_check(self):
        url = "https://api.buildkite.com/v2/organizations/ikukh-org/pipelines/test//builds/%s"%self.build_number
        header = { 'Authorization': 'Bearer %s'%(buildkite_token)}
        response = requests.get(url, headers=header)
        data2 = response.json()
        jobs2 = data2['jobs']

        for items2 in jobs2:
            try:
                a = items2['id']
                b = items2['state']
                print('Job ID:', a, 'State:', b)
            except:
                pass
        return b == 'passed'
        
        
    # Make a request to Jenkins server and start job there
    def start_jenkins_job(self):
        url = 'http://admin:117e5cd4b9eda880bdb88b0571dd36f47d@localhost:8080/job/TestJob/buildWithParameters?token=123token'
        print('Starting Jenkins job ...')
        request = requests.post(url)
        header = request.headers
        build_number_line = header['Location']
        build_number = (build_number_line.partition("item/")[2])
        print('Jenkins Build triggered! JENKINS Build number is:', (build_number[:-1]))
        

    # Check if we can proceed and start Jenkins Job
    def decision_to_procced(self):
        if self.state_check():
            self.start_jenkins_job()
        else:
            print('OH NO, SOMETHING WENT WRONG!')
    



if __name__ == '__main__':
    buildkite_runner = Buildkite_runner()
    buildkite_runner.create_build()
    buildkite_runner.pipeline_details()
    buildkite_runner.state_check()
    buildkite_runner.decision_to_procced()
