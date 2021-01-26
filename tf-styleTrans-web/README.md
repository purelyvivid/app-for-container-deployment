This is a Test APP for Container Deployment.
This APP allows uploading Content Image and Style Image, then do Style Transfer.
Container Image as been uploaded to https://hub.docker.com/r/purelyvivid/tf-style-trans-web.


```
docker run -d --name tf-styleTrans -p <your port>:5000 purelyvivid/tf-styleTrans:v0
```

Open `http://localhost:<your port>`