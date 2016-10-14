# Sherpa
Enable Docker's remote API via reverse-proxy

The current recommendation to enable Docker's remote API is to [change the daemon configuration and then restart](https://docs.docker.com/engine/admin/#/configuring-docker). With Sherpa, you simply need to run the container and you'll have access to the docker.sock via TCP.

**Warning**: By enabling this remote API, all that have access to this container's endpoint will have access to the Docker host's API. It is recommended to limit access to Sherpa as much as possible and only allow access where necessary. 

By using a combination of volume mounting permissions and IP binding, users can limit access to Sherpa.
### Full access
```bash
docker run -v /var/run/docker.sock:/tmp/docker.sock -dp 4550:4550 djenriquez/sherpa
```

### Read-only
```bash
docker run -v /var/run/docker.sock:/tmp/docker.sock:ro -dp 4550:4550 djenriquez/sherpa
```

### Local access
```bash
docker run -v /var/run/docker.sock:/tmp/docker.sock -dp 127.0.0.1:4550:4550 djenriquez/sherpa
```