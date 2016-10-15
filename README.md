# Sherpa
Enable Docker's remote API via reverse-proxy

The current recommendation to enable Docker's remote API is to [change the daemon configuration and then restart](https://docs.docker.com/engine/admin/#/configuring-docker). With Sherpa, you simply need to run the container and you'll have access to the docker.sock via TCP.

# ACL Configuration
Sherpa has two access modes, `--allow` and `--deny`(default). In `allow` mode, access to the Docker API is implicitly allowed. Meaning, you must explicitly define endpoints and HTTP methods that are forbidden. In `--deny` mode, the default mode, the reverse is true: access to the API is implicitly forbidden. Paths must be explicitly defined.

Paths can be configured using the `$CONFIG` environment variable with a json blob passed in and/or by mounting config files to `/etc/config`. This blob has the following schema:
```json
[
    { 
        "Path" : "STRING",
        "Access": "allow|deny",
        "Methods": ["STRING"]
    }
]
```
- "Path": The URI path to configure
- "Access": The access mode. Accepts "allow" or "deny"
- "Methods": The HTTP Methods to allow. *Note*: If access is "deny", this is ignored.

Admins can also restrict access to Sherpa by using a combination of volume mounting permissions and IP binding.

## Examples
Multiple ACLs can be defined to create a strictly contained remote API. Here are a few examples:

### Full access
```bash
docker run -d \
-v /var/run/docker.sock:/tmp/docker.sock \
-p 4550:4550 \
djenriquez/sherpa --allow
```

### Access to /containers/json GET only
```bash
docker run -d \
-e CONFIG='[
    { 
        "Path" : "/containers/json",
        "Access": "allow",
        "Methods": ["GET"]
    }
]' \
-v /var/run/docker.sock:/tmp/docker.sock \
-p 4550:4550 \
djenriquez/sherpa
```

### Access to everything but kill
```bash
docker run -d \
--name sherpa \
-e CONFIG='[
    { 
        "Path" : "/containers/*/kill",
        "Access": "deny"
    }
]' \
-v /var/run/docker.sock:/tmp/docker.sock \
-p 4550:4550 \
djenriquez/sherpa --allow
```

### Mount example config files /w env Config
```bash
docker run -d \
--name sherpa \
-e CONFIG='[
    { 
        "Path" : "/containers/json",
        "Access": "deny"
    }
]' \
-v `pwd`/examples:/etc/sherpa \
-v /var/run/docker.sock:/tmp/docker.sock \
-p 4550:4550 \
djenriquez/sherpa --allow
```