# 1단계: VM 접속 및 파일 준비 증거

## 1-1. OrbStack VM 접속

### 접속 명령
```bash
orb shell b1-lab
```

### VM 정보
```
Static hostname: b1-lab
Operating System: Ubuntu 22.04.5 LTS
Architecture: x86-64
Kernel: Linux b1-lab 6.17.8-orbstack-00308-g8f9c941121b1 x86_64
```

---

## 1-2. OS 버전 및 기본 환경 확인

### lsb_release -a
```
Distributor ID: Ubuntu
Description:    Ubuntu 22.04.5 LTS
Release:        22.04
Codename:       jammy
```

### whoami / sudo whoami
```
whoami   → cspag5955
sudo whoami → root
```

**결과:**
- ✅ Ubuntu 22.04 LTS 확인
- ✅ sudo 권한 확인

---

## 1-3. 필수 패키지 설치 확인

```bash
sudo apt update
sudo apt install -y acl ufw net-tools
```

### dpkg 설치 확인
```
acl       2.3.1-1
net-tools 1.60+git20181103.0eebece-1ubuntu5.4
ufw       0.36.1-4ubuntu0.1
```

**결과:**
- ✅ acl (세밀한 권한 설정)
- ✅ ufw (방화벽)
- ✅ net-tools (네트워크 확인)

---

## 1-4. 앱 파일 VM으로 복사

### 복사 명령 (macOS에서)
```bash
orb push b1-lab \
  /Users/cspag5955/cspag/AI-SW-Basic/agent-app/agent-app-linux-x86 \
  /tmp/agent-app-linux-x86
```

### 배치 후 확인
```bash
sudo ls -lh /home/agent-admin/agent-app/agent-app-linux-x86
```

```
-rwxr-xr-x 1 agent-admin agent-admin 6.2M May 20 11:11 agent-app-linux-x86
```

> **참고 - CPU 아키텍처별 바이너리 선택:**
> ```
> agent-app-linux-x86     → x86_64 (Intel/AMD) ← 사용 파일
> agent-app-linux-arm64   → ARM64 (Apple M1/M2)
> ```
> 현재 VM: x86-64 → `agent-app-linux-x86` 사용

**결과:**
- ✅ x86_64 바이너리 배치 완료 (6.2MB)
- ✅ 실행 권한(+x) 확인
