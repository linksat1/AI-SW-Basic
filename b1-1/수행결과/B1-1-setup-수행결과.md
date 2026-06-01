# B1-1 실습 환경 구축 수행 기록

> **작성일:** 2026-05-23  
> **작성자:** pagchuseon (cspag5955)  
> **저장소:** linksat1/AI-SW-Basic  
> **목적:** OrbStack + Ubuntu 22.04 + VS Code + Claude Code 환경 구축 전 과정 기록

---

## 환경 구성 요약

| 항목 | 내용 |
|------|------|
| 호스트 OS | macOS |
| 가상화 도구 | OrbStack |
| 게스트 OS | Ubuntu 22.04 LTS (Jammy) |
| 머신 이름 | b1-lab |
| 접속 계정 | cspag5955 |
| 에디터 | VS Code (Remote SSH, SSH: orb) |
| AI 도구 | Claude Code v2.1.150 |
| 저장소 | github.com/linksat1/AI-SW-Basic |

---

## 1단계: OrbStack 머신 생성 및 접속

### 실행 명령어

```bash
orb create ubuntu:22.04 b1-lab
ssh b1-lab@orb
```

### 실행 결과 및 트러블슈팅

```
# orb shell 단독 실행 시 오류
-bash: line 1: b1-lab: command not found

# 머신이 이미 존재할 때 오류
[-32098] create 'b1-lab': machine already exists: 'b1-lab'

# 해결: ssh 명령어로 접속 성공
ssh b1-lab@orb
→ cspag5955@b1-lab:~$  ✅
```

> **교훈:** `orb shell b1-lab` 이 안 될 경우 `ssh b1-lab@orb` 로 접속

---

## 2단계: 필수 패키지 설치

### 실행 명령어

```bash
# 오타로 오류 발생
sudo apt install -y acl ufw net-tools python3 pythos3-pip unzip nano curl
# E: Unable to locate package pythos3-pip

# 올바른 명령어
sudo apt install -y acl ufw net-tools python3 python3-pip unzip nano curl
```

### 설치된 주요 패키지

| 패키지 | 버전 |
|--------|------|
| acl | 2.3.1-1 |
| ufw | 0.36.1-4ubuntu0.1 |
| net-tools | 1.60+git20181103 |
| python3 | 3.10.6 |
| python3-pip | 22.0.2 |
| nano | 6.2 |
| curl | 7.81.0 |

> **교훈:** 패키지 이름 오타(`pythos3-pip` → `python3-pip`) 주의

---

## 3단계: Git 설치 및 설정

### 실행 명령어

```bash
# git 미설치 상태에서 설정 시도 → 오류
git config --global user.name pagchuseon
# -bash: git: command not found

# git 설치 후 설정
sudo apt install -y git
git config --global user.name pagchuseon
git config --global user.email pagchuseon@gmail.com
git --version
# git version 2.34.1  ✅
```

> **교훈:** git 설정 전 반드시 git 설치 먼저 필요

---

## 4단계: Node.js 20.x 설치

### 실행 명령어

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node --version
# v20.20.2  ✅
```

### 실행 로그 요약

```
2026-05-23 16:50:49 - Installing pre-requisites
2026-05-23 16:50:57 - Repository configured successfully.
nodejs 20.20.2-1nodesource1 설치 완료
```

---

## 5단계: Claude Code 설치

### 실행 명령어 및 트러블슈팅

```bash
# 권한 오류 발생
npm install -g @anthropic-ai/claude-code
# npm error code EACCES: permission denied
# npm error path /usr/lib/node_modules/@anthropic-ai

# 해결: sudo 로 재실행
sudo npm install -g @anthropic-ai/claude-code
# added 2 packages in 3s  ✅

claude
# Welcome to Claude Code v2.1.150  ✅
```

### Claude Code 실행 화면

```
Welcome to Claude Code v2.1.150
..........................................................
     *                                       █████▓▓░
                                 *         ███▓░     ░░
            ░░░░░░                        ███▓░
    ░░░   ░░░░░░░░░░                      ███▓░
   ░░░░░░░░░░░░░░░░░░░    *                ██▓░░      ▓
                                             ░▓▓███▓▓░
```

> **교훈:** 글로벌 npm 패키지 설치 시 권한 오류는 `sudo` 로 해결

---

## 6단계: GitHub 저장소 Clone

### 실행 명령어 및 트러블슈팅

```bash
# 오류 1: 예시 URL 그대로 사용
git clone https://github.com/pagchuseon/저장소명.git
# fatal: The requested URL returned error: 400

# 오류 2: 잘못된 계정명 (실제 owner는 linksat1)
git clone https://github.com/pagchuseon/AI-SW-Basic.git
# remote: Repository not found.

# 성공: 올바른 저장소 주소
git clone https://github.com/linksat1/AI-SW-Basic.git
# Cloning into 'AI-SW-Basic'... 완료 ✅

cd AI-SW-Basic && ls
# B1-1-mission.md  B1-1-orbstack-setup.md  B1-1-selfstudy.md
# README.md  수행내역서_시스템관제자동화.docx
```

> **교훈:** 저장소 소유자 계정명 정확히 확인 필요 (pagchuseon ≠ linksat1)

---

## 7단계: VS Code Remote SSH 연결

### 설정 방법

1. VS Code → Extensions(`Cmd+Shift+X`) → **Remote - SSH** 설치
2. `Cmd+Shift+P` → `Remote-SSH: Connect to Host`
3. 호스트: `b1-lab@orb` 입력
4. 좌측 하단 **`SSH: orb`** 표시 확인 ✅

---

## 최종 환경 체크리스트

| 항목 | 결과 |
|------|------|
| Ubuntu 22.04 머신 생성 | ✅ |
| SSH 접속 (`ssh b1-lab@orb`) | ✅ |
| 필수 패키지 설치 | ✅ |
| Git 2.34.1 설치 및 설정 | ✅ |
| Node.js v20.20.2 설치 | ✅ |
| Claude Code v2.1.150 설치 | ✅ |
| GitHub 저장소 Clone | ✅ |
| VS Code Remote SSH 연결 | ✅ |

---

## 다음 단계

- [ ] `B1-1-selfstudy.md` 교본 따라 미션 진행
- [ ] 작업 종료 시 `git add . && git commit -m "메시지" && git push` 로 백업

---

> **비고:** 공용 PC 환경이므로 작업 종료 시 반드시 GitHub에 push하여 파일 보존
