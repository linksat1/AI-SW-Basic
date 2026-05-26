# 4단계: 계정 및 그룹 생성 증거

## 그룹 목록 (/etc/group)
```
agent-common:x:1000:agent-admin,agent-dev,agent-test
agent-core:x:1001:agent-admin,agent-dev
agent-admin:x:1002:
agent-dev:x:1003:
agent-test:x:1004:
```

## id 명령어 확인 결과
```
uid=1000(agent-admin) gid=1002(agent-admin) groups=1002(agent-admin),27(sudo),1000(agent-common),1001(agent-core)
uid=1001(agent-dev)   gid=1003(agent-dev)   groups=1003(agent-dev),1000(agent-common),1001(agent-core)
uid=1002(agent-test)  gid=1004(agent-test)  groups=1004(agent-test),1000(agent-common)
```

## 검증 결과
| 항목 | 기대 | 실제 | 결과 |
|------|------|------|------|
| agent-admin | common, core, sudo | common, core, sudo | ✅ |
| agent-dev | common, core | common, core | ✅ |
| agent-test | common 만 | common 만 | ✅ |
| agent-common 멤버 | admin,dev,test | admin,dev,test | ✅ |
| agent-core 멤버 | admin,dev | admin,dev | ✅ |
