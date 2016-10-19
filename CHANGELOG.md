# 0.3.0 - Address filtering
- For "allow" configuration rules, Sherpa can now specify which addresses to allow. If not specified, all addresses, or "0.0.0.0/0", is implied. See [NGINX allow](http://nginx.org/en/docs/http/ngx_http_access_module.html#allow) for accepted values.

# 0.2.0 - Smarter Sherpa
- Introducing ACLs. Sherpa can now allow or deny access to specific remote api endpoints.
- `--allow` or `--deny` mode specifies implicit allow or deny access to resources
