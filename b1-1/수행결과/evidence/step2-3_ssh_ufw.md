# 2~3단계: SSH 보안 + UFW 방화벽 설정 증거

## [2단계] SSH 보안 설정

### sshd_config 설정 확인
```
Port 20022
PermitRootLogin no
```

### SSH 포트 리슨 상태
```
tcp  LISTEN 0  128  0.0.0.0:20022  0.0.0.0:*  users:(("sshd",...))
tcp  LISTEN 0  128  [::]:20022     [::]:*     users:(("sshd",...))
```

**결과:**
- ✅ SSH 포트 20022로 변경 완료
- ✅ Root 원격 로그인 차단(PermitRootLogin no) 완료

---

## [3단계] 방화벽 설정 (UFW)

### UFW 상태
```
Status: active
Default: deny (incoming), allow (outgoing)

To                         Action      From
20022/tcp                  ALLOW IN    Anywhere
15034/tcp                  ALLOW IN    Anywhere
20022/tcp (v6)             ALLOW IN    Anywhere (v6)
15034/tcp (v6)             ALLOW IN    Anywhere (v6)
```

**결과:**
- ✅ UFW 활성화 완료
- ✅ 20022/tcp (SSH) 허용
- ✅ 15034/tcp (App) 허용
- ✅ 기타 인바운드 트래픽 기본 차단(deny incoming)
