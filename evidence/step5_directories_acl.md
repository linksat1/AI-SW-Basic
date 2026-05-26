# 5단계: 디렉토리 구조 및 권한 설정 증거

## ls -la /home/agent-admin/agent-app/
```
drwxr-x---  agent-admin  agent-core   .
drwxr-x---  agent-admin  agent-core   ..
drwxrwx---+ agent-admin  agent-core   api_keys
drwxr-xr-x  agent-admin  agent-admin  bin
drwxrwsr-x+ agent-admin  agent-common upload_files
-rwxr-xr-x  agent-admin  agent-admin  agent-app-linux-x86
```

## getfacl upload_files
```
# owner: agent-admin  # group: agent-common  # flags: -s-
user::rwx
group::rwx
group:agent-common:rwx
mask::rwx
other::r-x
default:user::rwx
default:group::rwx
default:group:agent-common:rwx
```

## getfacl api_keys
```
# owner: agent-admin  # group: agent-core
user::rwx
group::r-x
group:agent-core:rwx
mask::rwx
other::---
default:user::rwx
default:group::r-x
default:group:agent-core:rwx
default:other::---
```

## getfacl /var/log/agent-app
```
# owner: agent-admin  # group: agent-core
user::rwx
group::rwx
group:agent-core:rwx
mask::rwx
other::---
default:user::rwx
default:group::rwx
default:group:agent-core:rwx
default:other::---
```

## 검증 결과
| 디렉토리 | 그룹 | 권한 | ACL | 결과 |
|---------|------|------|-----|------|
| upload_files | agent-common | 2775(rwxrwsr-x) | agent-common:rwx | ✅ |
| api_keys | agent-core | 770(rwxrwx---) | agent-core:rwx | ✅ |
| /var/log/agent-app | agent-core | 770(rwxrwx---) | agent-core:rwx | ✅ |
