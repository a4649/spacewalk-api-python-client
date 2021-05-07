# Spacewalk (RedHat Satellite) API Python client

Spacewalk version 2.10 - https://spacewalkproject.github.io/documentation.html

### How To

```
import spacewalk

key = spacewalk.login()

target = spacewalk.get_systems(key, "web")

spacewalk.run_cmd(key, 'Update apache in web servers', target, 'root', 'root', '!#/bin/bash\n yum update -y httpd;systemctl restart httpd') 
```
