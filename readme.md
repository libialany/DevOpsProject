### Troubleshooting conectivity

```
k exec -it deploy/app  -n demo2 -- nc -zv db 5432 
Connection to db (10.96.228.71) 5432 port [tcp/postgresql] succeeded!
```

### simulate the mistake

change labels 

#### 1. get pods by label

```
k get pods -l app=db
```

#### 2. get endpoints

```
k get endpoints db
```

#### Compare

```
kubectl get service db -n demo2 -o jsonpath='{.spec.selector}'
echo
kubectl get pods  -n demo2  --show-labels
```

#### more feaure

kubernetes networking policies
