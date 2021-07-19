import flask
from flask import request, jsonify
import os
import re
import json
import redis
import time

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)
input_log = 'GOCACHE=off go test -timeout 20m -v${WHAT:+ -run="$WHAT"} ./test/e2e/' + os.linesep + '[ 0]ENTER: /usr/local/src/pkg/apis/machineconfiguration.openshift.io/v1/register.go:28 0' + os.linesep + '[ 0]EXIT:   /usr/local/src/src/github.com/openshift/machine-config-operator/pkg/apis/machineconfiguration.openshift.io/v1/register.go:28 0' + os.linesep + '[ 0]ENTER:  /usr/local/src/github.com/openshift/machine-config-operator/pkg/generated/clientset/versioned/scheme/register.go:19 0' + os.linesep + '[ 0]ENTER:  /usr/local/src/github.com/openshift/machine-config-operator/pkg/apis/machineconfiguration.openshift.io/v1/register.go:32         addKnownTypes' + os.linesep + '[ 0]EXIT:   /usr/local/src/github.com/openshift/machine-config-operator/pkg/apis/machineconfiguration.openshift.io/v1/register.go:32         addKnownTypes' + os.linesep + '[ 0]EXIT:   /usr/local/src/golang/src/github.com/openshift/machine-config-operator/pkg/generated/clientset/versioned/scheme/register.go:19 0' + os.linesep + '=== RUN   TestMCDToken' + os.linesep + '10 [ 1]ENTER:  /usr/local/src/github.com/openshift/machine-config-operator/test/e2e/mcd_test.go:21 TestMCDToken' + os.linesep + '11 [ 0]ENTER:  /usr/local/src/github.com/openshift/machine-config-operator/cmd/common/client_builder.go:34 NewClientBuilder' + os.linesep + '12 [ 0]EXIT:   /usr/local/src/github.com/openshift/machine-config-operator/cmd/common/client_builder.go:34 NewClientBuilder' + os.linesep + '13 [ 0]ENTER:  /usr/local/src/github.com/openshift/machine-config-operator/cmd/common/client_builder.go:22 KubeClientOrDie' + os.linesep + '14 [ 0]EXIT:   /usr/local/src/github.com/openshift/machine-config-operator/cmd/common/client_builder.go:22 KubeClientOrDie' + os.linesep + '15 [ 1]EXIT:   /usr/local/src/github.com/openshift/machine-config-operator/test/e2e/mcd_test.go:21 TestMCDToken' + os.linesep + '16 --- PASS: TestMCDToken (3.86s)'

@app.route('/', methods=['GET'])
def api_all():
    log_elements = []
    for line in input_log.splitlines():
        # ignoring log lines without any entry or exit action
        if (line.find('ENTER') == -1 and line.find('EXIT') == -1):
            continue
        else:
            # element stores the 4 components of each log line
            element = dict()
            operation = re.search('](.+?):', line)
            if operation:
                element['operation'] = operation.group(1)
            if (element['operation'] == 'ENTER'):
                element['operation'] = 'ENTRY'
            filename = re.search(':\s+(.+?):', line)
            if filename:
                element['filename'] = filename.group(1)
            line_no = re.search('.go:(.+?)\s+', line)
            if line_no:
                element['line number'] = line_no.group(1)
            name = line.split(" ")
            element['name'] = name[len(name) - 1].strip()
            if (element['name'].isdigit()):
                element['name'] = 'anonymous'
            log_elements.append(element)
    jsonString = json.dumps(log_elements)
    json_object = json.loads(jsonString)
    return jsonify(json_object)


app.run()
