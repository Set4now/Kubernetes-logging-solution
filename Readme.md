# Kubernetes-logging-solution
This is logging solution for kubernetes ( fluentbit to splunk)

This will deploy fluent bit as a daemon set which is an opensource logging agent for kubernetes and send logs ( events) as well
to splunk. 

Please check the configMap.

This project is mainly focussed on how to push kubernetes events as logs to splunk.
Since k8 events don't have any log files. 
So the idea is to create an app which will hit the kubernrtes API server and send the json output to stdout.

1. Create a service account
```
kubectl create -f k8-event-service-account.yaml 
```
2. Create cluster Role and Role Binding
```
kubectl create -f k8-event-cluster-role.yaml -f k8-event-rolebinding.yaml
```
3. Create a Fluent bit configmap and Daemonset

```
kubectl create -f fluent-bit-config.yaml -f fluent-bit-daemonset.yaml

```
4.Now deploy our add as a pod or deployment.
```


Docker hub image id:-    sumandevops/k8events:v3

kubectl run --generator=run-pod/v1 splunkeventlogger --image sumandevops/k8events:v3 

kubectl logs -f splunkeventlogger

```
Now go to splunk and see your logs
