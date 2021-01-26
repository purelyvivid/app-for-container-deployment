This is a Test APP for Container Deployment.
This APP allows uploading Content Image and Style Image, then do Style Transfer.
Container Image as been uploaded to https://hub.docker.com/r/purelyvivid/captcha-demo.

```
docker run -d --name captcha-demo-api -p <your port>:5000 purelyvivid/captcha-demo:v0
```

```
export ENDPOINT_URL=localhost:<your port>/api/v1.0/predictions 
```

```
curl -F 'binData=@./<your image location>' ${ENDPOINT_URL}
```
> {"jsonData":{"prediction":"<Result>"},"meta":{}}


