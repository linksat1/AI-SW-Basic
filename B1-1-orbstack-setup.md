# OrbStack으로 Ubuntu 22.04 LTS 실습 환경 만들기

> **이 문서는?**
> macOS에 설치된 OrbStack을 사용하여 B1-1 미션 실습용 Ubuntu 22.04 LTS 환경을 구축하는 방법을 단계별로 안내합니다.
> 이 작업을 완료하면 [B1-1-selfstudy.md](B1-1-selfstudy.md) 교본을 그대로 따라할 수 있는 환경이 준비됩니다.

---

## OrbStack이란?

OrbStack은 macOS에서 Docker 컨테이너와 Linux VM을 빠르게 실행할 수 있는 경량 툴입니다.
Docker Desktop보다 훨씬 빠르고 가볍게 동작하며, Linux 머신(VM)을 네이티브에 가까운 성능으로 실행할 수 있습니다.

이 미션에서는 OrbStack의 **Linux Machine** 기능을 사용합니다.
Docker 컨테이너보다 완전한 리눅스 환경(systemd, 방화벽, SSH 등)을 제공하기 때문에 서버 운영 실습에 적합합니다.

---

## 방법 선택: Linux Machine vs Docker 컨테이너

| 항목 | Linux Machine (권장) | Docker 컨테이너 |
|------|---------------------|----------------|
| systemd | ✅ 지원 | ❌ 기본 미지원 |
| SSH 서비스 | ✅ 자동 실행 | 별도 설정 필요 |
| UFW 방화벽 | ✅ 정상 동작 | 제한적 |
| 실습 난이도 | 낮음 (실서버에 가까움) | 높음 |

> **이 교본은 Linux Machine 방식으로 진행합니다.**

---

## 1단계: OrbStack 설치 확인

```bash
# 터미널에서 orb 명령어가 있는지 확인
orb version
```

**정상 출력 예시:**
```
OrbStack version 1.x.x ...
```

설치가 안 되어 있다면 [https://orbstack.dev](https://orbstack.dev) 에서 다운로드하세요.

---

## 2단계: Ubuntu 22.04 Linux Machine 생성

### 2.1 GUI로 생성 (쉬운 방법)

1. macOS 상단 메뉴바에서 OrbStack 아이콘 클릭
2. **"New Machine"** 선택
3. 다음과 같이 설정:
   - **Distribution:** Ubuntu
   - **Version:** 22.04 (jammy)
   - **Name:** `b1-lab` (원하는 이름)
4. **"Create"** 버튼 클릭
5. 이미지 다운로드 및 부팅이 자동으로 진행됩니다 (1~3분 소요)

### 2.2 터미널 명령어로 생성 (빠른 방법)

```bash
# Ubuntu 22.04 머신 생성 (이름: b1-lab)
orb create ubuntu:22.04 b1-lab
```

**출력 예시:**
```
Creating machine 'b1-lab' with Ubuntu 22.04...
Pulling image...
Starting machine...
Machine 'b1-lab' is ready!
```

---

## 3단계: Ubuntu 머신에 접속

### 3.1 기본 접속

```bash
# b1-lab 머신에 셸로 접속
orb shell b1-lab
```

또는 더 짧게:

```bash
# 기본 머신이 b1-lab 하나라면 이것도 됩니다
orb shell
```

접속 성공 시 프롬프트가 아래처럼 바뀝니다:

```
ubuntu@b1-lab:~$
```

### 3.2 SSH로 접속 (선택)

OrbStack Linux Machine은 SSH 접속도 지원합니다.

```bash
# SSH 접속 (OrbStack이 자동으로 키 설정해줌)
ssh b1-lab@orb
```

---

## 4단계: Ubuntu 머신 기본 설정

### 4.1 OS 버전 확인

```bash
cat /etc/os-release
```

**출력:**
```
NAME="Ubuntu"
VERSION="22.04.x LTS (Jammy Jellyfish)"
...
```

### 4.2 현재 사용자 확인

```bash
whoami
# 출력: ubuntu (OrbStack 기본 계정)

# sudo 권한 확인
sudo whoami
# 출력: root
```

### 4.3 패키지 업데이트

```bash
sudo apt update && sudo apt upgrade -y
```

> 처음 실행 시 약 2~5분 소요됩니다.

### 4.4 필수 패키지 설치

```bash
sudo apt install -y \
  acl \
  ufw \
  net-tools \
  python3 \
  python3-pip \
  unzip \
  nano \
  curl
```

---

## 5단계: 실습 파일 머신에 넣기

### 5.1 macOS에서 머신으로 파일 복사

OrbStack Linux Machine은 macOS와 자동으로 볼륨을 공유하므로 파일 복사가 매우 쉽습니다.

```bash
# macOS 터미널에서 (orb shell 밖에서 실행)
# agent-app.zip 파일을 머신의 /tmp 로 복사
orb push b1-lab /path/to/agent-app.zip /tmp/agent-app.zip
```

또는 `scp` 사용:

```bash
scp -o ProxyJump=b1-lab@orb /path/to/agent-app.zip ubuntu@b1-lab:/tmp/
```

> **Tip:** macOS 파인더에서 파일을 드래그하여 OrbStack 머신 경로에 직접 넣을 수도 있습니다.
> OrbStack GUI → 해당 머신 → Files 탭에서 드래그 앤 드롭 가능합니다.

### 5.2 머신 내에서 파일 확인

```bash
# b1-lab 머신 안에서
ls /tmp/agent-app.zip
```

---

## 6단계: SSH 서비스 확인

B1-1 미션에서 SSH 포트를 변경하는 작업이 있습니다.
OrbStack Linux Machine은 기본적으로 SSH 데몬이 실행 중입니다.

```bash
# SSH 서비스 상태 확인
sudo systemctl status ssh

# SSH가 실행 중이 아니라면 시작
sudo systemctl start ssh
sudo systemctl enable ssh
```

**정상 출력:**
```
● ssh.service - OpenBSD Secure Shell server
   Loaded: loaded (/lib/systemd/system/ssh.service; enabled; ...)
   Active: active (running) since ...
```

---

## 7단계: UFW(방화벽) 사전 확인

```bash
# UFW 설치 확인
sudo ufw status
# 출력: Status: inactive (처음에는 비활성 상태가 정상)
```

> **주의:** OrbStack Linux Machine에서 UFW를 활성화해도 macOS 호스트와의 통신에는 영향이 없습니다.
> 실습 시 `ufw enable` 전에 반드시 SSH 포트(20022)를 허용해야 합니다.

---

## 8단계: 머신 관리 명령어 요약

```bash
# 머신 목록 확인
orb list

# 머신 시작
orb start b1-lab

# 머신 중지
orb stop b1-lab

# 머신 접속
orb shell b1-lab

# 머신 삭제 (주의: 데이터 전체 삭제)
orb delete b1-lab

# 머신 상태 확인
orb info b1-lab
```

---

## 9단계: VS Code에서 머신에 연결 (선택)

VS Code에서 OrbStack 머신에 직접 연결하면 파일 편집이 훨씬 편합니다.

1. VS Code에서 **Remote - SSH** 확장 설치
2. `Ctrl + Shift + P` → `Remote-SSH: Connect to Host...` 선택
3. 호스트 입력: `b1-lab@orb`
4. 연결 후 `/home/agent-admin/agent-app` 폴더를 열어서 편집

---

## 환경 준비 완료 체크리스트

```bash
# 머신 접속 후 아래 명령어로 모든 항목 확인

# ✅ Ubuntu 22.04 확인
lsb_release -a

# ✅ sudo 권한 확인
sudo echo "sudo OK"

# ✅ Python3 확인
python3 --version

# ✅ 필수 도구 확인
which acl ufw nano unzip curl

# ✅ systemd 동작 확인 (Linux Machine에서는 정상 동작)
systemctl --version

# ✅ SSH 서비스 확인
sudo systemctl is-active ssh
```

모든 항목이 확인되면 [B1-1-selfstudy.md](B1-1-selfstudy.md) 교본의 **1단계 시작 전 준비**부터 진행하세요!

---

## 자주 묻는 질문 (FAQ)

### Q. orb shell 접속 시 어떤 계정으로 들어가나요?
기본적으로 `ubuntu` 계정으로 접속됩니다. sudo 권한이 있으므로 관리자 작업이 가능합니다.

### Q. 머신을 재시작하면 설정이 유지되나요?
네. OrbStack Linux Machine은 VM과 같이 디스크 이미지로 데이터를 유지합니다.
`orb stop` → `orb start` 후에도 모든 설정과 파일이 그대로입니다.

### Q. macOS와 파일을 공유하는 쉬운 방법은?
```bash
# macOS의 홈 디렉토리는 머신 안에서 /mac/Users/사용자명 으로 마운트됩니다
ls /mac/Users/$(whoami)/

# 예: macOS 바탕화면의 파일을 머신으로 복사
cp /mac/Users/$(whoami)/Desktop/agent-app.zip /tmp/
```

### Q. 머신의 포트를 macOS에서 접근하려면?
OrbStack은 머신의 포트를 자동으로 macOS에 노출시킵니다.
머신 내에서 15034 포트로 앱이 실행되면, macOS 브라우저에서 `http://localhost:15034` 로 접근 가능합니다.

### Q. SSH 포트를 20022로 바꾸면 `orb shell`이 안 되나요?
`orb shell`은 SSH와 별개의 방법으로 접속하므로 영향 없습니다.
SSH 포트 변경 후에도 `orb shell b1-lab` 명령은 정상 동작합니다.

---

> **다음 단계:** 이 환경 구성이 완료되면 [B1-1-selfstudy.md](B1-1-selfstudy.md) 교본을 따라 미션을 진행하세요.
