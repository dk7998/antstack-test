Add your AWS access key and secret key in serverless.yml

To run in local:
Create python virtual env and activate it

Run:
```
pip intall -r requirements.txt
npm install
```

To deploy dynamodb and the endpoints:
```
sls deploy
```
After deploying use the urls from the command output to test the endpoints.


To test in offline mode after deployment, can't be used to test without deployment since dynamodb table is required
```
sls offline
```


