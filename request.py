'''
  This script will hit Kubernetes API server and watch for events. 
  This is baiscally a streaming API , where are the data is being redirected to POD stdout.
  The Pod service account should have access to KUBE API. 
  If not then create a RBAC for in the Kubernetes Cluster.
'''
import requests 
import json 
import logging
import json
import sys
import ast

'''
  Logging structuer that Docker pasrser understands.
'''
logging.basicConfig(format='%(asctime)s   %(process)d %(processName)s] %(message)s', level=logging.INFO)

token_directory="/var/run/secrets/kubernetes.io/serviceaccount/token"
with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as f:
        token=f.read()
        #print token
ca_cert="/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
kube_api_server="https://kubernetes.default.svc"
kube_api_port="443"


#headers = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tNnZoNDciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjdhNjVmNTVjLTk3ODctMTFlOS1hZDhiLTAwMGQzYTc2OGU4OSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.3JwUYsUklJijQVP7qpaR01LvxYhEN-kPZlBEWnCWAJPpgBja7gHv31dV3z3cowghYAPM9jcW3DGoeWEzna3LzQHkCSQsA1SVnTwNQcmaFyDh_4eJsT3jcFhhCI0nDmPdUp8abbZrwZeBlx-waJ2TpTjIvbcCMSFXIV_22jKeEKk7YOL7lain2mbLvodCdESGdZjn4Y128reHx3XlhdvXslwZRFCONTtwOGfbedQzntyibukwEgxsElKDxDKL5CyAS2o8AJVJwzWWeqEhd52QsTIhlCjw3dJBXxxKtzV0-fKdLMDmB4csee3IgGNdHkSP8Vf89n9xD858yn1SjOC-mg", "Accept": "application/json"}
bearer_token="Bearer {}".format(token)
headers={"Authorization": bearer_token, "Accept": "application/json"}

while True:
  try:
    response = requests.get('https://kubernetes.default.svc/api/v1/watch/events', verify=ca_cert, headers=headers, stream=True)
    for line in response.iter_lines():
      if "forbidden" in line:
         logging.error('Permission denied for Pod Service Account to access KUBE API!')
         #sys.exit(1)
      if line is not None:
         #logging.info(line)
         raw_data=ast.literal_eval(json.dumps(line))
         print json.dumps(json.loads(raw_data.strip("\n")))
      if line is None:
         logging.error('Looks like No response from API. Trying again')
      if line == "":
         logging.warning('No current event')
  except Exception  as e:
    logging.critical(e.message)
    break
