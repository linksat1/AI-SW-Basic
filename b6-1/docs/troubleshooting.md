# B6-1 트러블슈팅 보고서

실습 중 실제로 겪은 문제 3건을 아래에 기록합니다.

---

## 사건 #1 — EC2 인스턴스에 `default` 보안 그룹이 붙어 외부 접속이 거부됨

| 항목 | 내용 |
|---|---|
| 발생 일시 | 2026-07-15 23:40경 |
| 증상(문제 상황) | EC2 인스턴스 시작 완료 후 `http://<퍼블릭IP>/health`로 브라우저 접속 시 "사이트에 연결할 수 없음 / 연결이 재설정되었습니다(ERR_CONNECTION_RESET)"가 발생. 브라우저 스킴을 `http://`로 명시해도 동일하게 재현됨 |
| 원인 가설 | Security Group 인바운드 규칙(HTTP 80←0.0.0.0/0)이 실제로는 인스턴스에 적용되지 않았을 것이다. 인스턴스 생성 마법사에서 방화벽(보안 그룹) 선택 단계를 놓쳤을 가능성 |
| 검증 방법 | EC2 콘솔 → 인스턴스 → 해당 인스턴스 → "보안" 탭에서 실제 연결된 보안 그룹 확인 |
| 조치 내용 | 확인 결과 `b6-1-web-sg`가 아니라 **`default` 보안 그룹**(인바운드가 같은 SG 내부 트래픽만 허용)이 연결되어 있었음. 인스턴스 선택 → 작업 → 보안 → 보안 그룹 변경에서 `default`를 제거하고 `b6-1-web-sg`로 교체 |
| 결과 | 보안 그룹 교체 후 "보안" 탭에 HTTP(0.0.0.0/0)·SSH(212.102.51.72/32) 인바운드 규칙이 정상 표시됨. 다만 이 시점엔 아직 SSH 접근 문제(사건 #2)가 남아 있어 외부 접속 자체는 이어서 추가 조치 필요했음 |
| 재발 방지 | EC2 인스턴스 시작 시 "방화벽(보안 그룹)" 단계에서 "기존 보안 그룹 선택"이 실제로 선택되어 있는지(기본값 `default`로 남아있지 않은지) 시작 직전에 반드시 육안 재확인한다 |

**근거**: 대화 로그 — 인스턴스 "보안" 탭 캡처에서 `sg-0f0fdc2af6add2d0d (default)` 확인 → 교체 후 `sg-0879a9a06d512313a (b6-1-web-sg)`로 변경된 배너(`eni-...에 대한 보안 그룹이 변경됨`) 확인 (별도 스크린샷 파일로는 저장하지 않고 콘솔 화면으로 실시간 확인)

---

## 사건 #2 — SSH 접속 시 `Permission denied (publickey)` 발생 (사용자명 오류)

| 항목 | 내용 |
|---|---|
| 발생 일시 | 2026-07-16 00:05경 |
| 증상(문제 상황) | `ssh -i <키페어이름>.pem ubuntu@<퍼블릭IP>` 실행 시 `Permission denied (publickey,gssapi-keyex,gssapi-with-mic)` 오류로 접속 거부됨. 키 페어 이름은 인스턴스에 등록된 것과 동일했음 |
| 원인 가설 | (1) `.pem` 키 파일 자체가 잘못됐거나, (2) 접속 사용자명이 실제 AMI와 맞지 않을 것이다. Ubuntu는 `ubuntu`, Amazon Linux는 `ec2-user`를 쓰는데 AMI 종류를 재확인하지 않고 가이드의 Ubuntu 예시(`ubuntu@`)를 그대로 사용함 |
| 검증 방법 | EC2 콘솔 → 인스턴스 세부 정보에서 AMI ID/이름 확인 → `ami-08c64967154312fa5`, `al2023-ami-2023.12.20260710.0-kernel-6.18-x86_64`로 **Amazon Linux 2023**임을 확인 |
| 조치 내용 | 접속 명령의 사용자명을 `ubuntu`에서 **`ec2-user`**로 변경 |
| 결과 | `ssh -i "$env:USERPROFILE\.ssh\<키페어이름>.pem" ec2-user@<퍼블릭IP>`로 정상 접속 성공 |
| 재발 방지 | EC2 인스턴스 생성 직후 AMI 종류(Ubuntu/Amazon Linux)를 먼저 확인하고, 그에 맞는 접속 사용자명·패키지 관리자(`apt-get`/`dnf`)를 사용한다. 가이드 문서의 명령을 AMI 종류 확인 없이 그대로 복사하지 않는다 |

**근거 스크린샷/로그**: 대화 로그의 SSH 세션 출력 (`Permission denied` 메시지 → AMI 확인 → `ec2-user`로 재시도 성공 로그), `docs/screenshots/외부접속검증.png`(최종 정상 접속 결과와 연결됨)

---

## 사건 #3 — `/health` 요청 시 `404 Not Found` (Amazon Linux 문서 루트 경로 차이)

| 항목 | 내용 |
|---|---|
| 발생 일시 | 2026-07-16 00:20경 |
| 증상(문제 상황) | SSH로 인스턴스에 접속해 `echo "OK" | sudo tee /var/www/html/health` 실행 후 `curl -i http://localhost/health` 호출 시 `HTTP/1.1 404 Not Found`(nginx 기본 404 페이지) 응답 |
| 원인 가설 | nginx는 정상 실행 중(`curl -i http://localhost` 루트 경로는 200 OK 확인됨)이므로, 문서 루트 경로 자체가 `/var/www/html`이 아닐 것이다 — 이는 Ubuntu/Debian 계열 nginx 패키지의 기본 경로이고, Amazon Linux는 다를 수 있음 |
| 검증 방법 | 404 응답 본문에 포함된 안내 문구(`This is the default 404 error page for nginx... located /usr/share/nginx/html/404.html`)를 확인 |
| 조치 내용 | `/var/www/html/health` 대신 실제 문서 루트인 **`/usr/share/nginx/html/health`**에 파일 생성: `echo "OK" | sudo tee /usr/share/nginx/html/health` |
| 결과 | `curl -i http://localhost/health` → `HTTP/1.1 200 OK`, 본문 `OK` 확인. 이후 외부 브라우저 접속(`/health`)도 정상 응답(다운로드 프롬프트는 확장자 없는 파일이라 `Content-Type: application/octet-stream`으로 응답되어 나타난 것으로, 오류가 아님을 확인) |
| 재발 방지 | nginx 설치 후에는 배포판별 기본 문서 루트가 다를 수 있음을 감안해, 파일을 배치하기 전에 `nginx -T` 또는 `/etc/nginx/nginx.conf`의 `root` 지시어를 먼저 확인한다. Ubuntu=`/var/www/html`, Amazon Linux=`/usr/share/nginx/html` |

**근거 스크린샷/로그**: 대화 로그의 SSH 세션 출력 (404 응답 전문 → 경로 수정 → 200 OK 재확인), `docs/screenshots/외부접속검증.png`

---

## 사건 #4 — 사용자 데이터 스크립트 들여쓰기로 인한 `Exec format error` (nginx 미설치)

| 항목 | 내용 |
|---|---|
| 발생 일시 | 2026-07-17 재실습 중 |
| 증상(문제 상황) | EC2 시작 시 사용자 데이터에 nginx 설치 스크립트를 넣었는데, 인스턴스가 `실행 중`으로 뜬 뒤에도 `/usr/share/nginx/html`이 존재하지 않고 `nginx.service`도 찾을 수 없었음 |
| 원인 가설 | 가이드 문서(`AWS자료올리기.md`)의 코드 블록을 마크다운 펜스(` ```bash `/` ``` `) 포함해서 그대로 복사·붙여넣기 했고, 목록 들여쓰기 때문에 각 줄 앞에 공백 2칸이 붙은 채 입력됨 |
| 검증 방법 | `sudo cat /var/lib/cloud/instance/scripts/part-001`로 실제 저장된 스크립트 확인 → 첫 줄이 `  #!/bin/bash`(공백 2칸 포함)였음. `sudo grep -A20 scripts-user /var/log/cloud-init.log`에서 `Exec format error: Missing #! in script?` 확인 |
| 조치 내용 | 이미 실행 중인 인스턴스라 재생성 대신 SSH로 직접 `sudo dnf install -y nginx && sudo systemctl enable --now nginx` 실행 |
| 결과 | nginx 정상 설치·기동, 이후 포트폴리오 배포 및 `curl -i http://<퍼블릭IP>` → 200 OK 확인 |
| 재발 방지 | EC2 사용자 데이터 칸에는 마크다운 코드펜스(` ``` `)를 제외한 **순수 셸 스크립트만, 줄 앞 들여쓰기 없이** 붙여넣는다. 붙여넣은 후 " ` ```bash `"나 선행 공백이 남아있지 않은지 육안으로 재확인한다 |

---

## 사건 #5 — 이전 세션에서 남은 EC2 인스턴스가 새 인스턴스와 함께 이중 실행됨

| 항목 | 내용 |
|---|---|
| 발생 일시 | 2026-07-17 재실습 중 |
| 증상(문제 상황) | 새 인스턴스를 시작했더니, 인스턴스 목록에 이름이 이미 붙어 있고 상태 검사까지 통과한 `b6-1-web-server`(`i-03b104633925a5395`)가 함께 떠 있었음. 재실습 진행 기록(`AWS자료올리기.md`)에는 "EC2 미실행"으로 적혀 있었는데 실제로는 남아있던 것 |
| 원인 가설 | 이전(공용 PC) 세션 어느 시점에 EC2를 생성해뒀으나 진행 기록에는 반영되지 않았고, 종료도 되지 않은 채 계속 과금 중이었을 것 |
| 검증 방법 | EC2 콘솔 인스턴스 목록에서 두 인스턴스의 이름·생성 시각·퍼블릭 IP 비교 |
| 조치 내용 | 기존 `b6-1-web-server` 인스턴스를 선택해 종료(Terminate) — 해당 인스턴스는 오늘 다운로드한 키 페어로는 접속 불가능한 상태였고 별도 데이터도 없어 삭제해도 무방하다고 판단 |
| 결과 | 새로 만든 인스턴스 하나만 남아 t3.micro 이중 과금 위험 제거 |
| 재발 방지 | 새 인스턴스를 시작하기 전에 인스턴스 목록을 먼저 확인해, 진행 기록에 없는 리소스가 남아있지 않은지 점검한다 |

---

## 사건 #6 — 로컬 환경에 `rsync` 미설치로 배포 스크립트 실패

| 항목 | 내용 |
|---|---|
| 발생 일시 | 2026-07-17 재실습 중 |
| 증상(문제 상황) | `b6-1/scripts/deploy-portfolio.sh` 실행 시 `rsync: command not found`로 즉시 종료 |
| 원인 가설 | 이 PC의 Git Bash 환경에는 `rsync`가 기본 포함되어 있지 않음 (별도 설치 필요) |
| 검증 방법 | `which rsync`(없음) vs `which scp ssh`(있음) 비교 |
| 조치 내용 | 스크립트를 그대로 쓰는 대신, 동일한 절차(파일 업로드 → nginx 문서 루트로 배치 → 재시작)를 `scp -r`과 `ssh` 명령으로 수동 수행 |
| 결과 | 포트폴리오 파일이 `/usr/share/nginx/html/`에 정상 배치되고 외부 접속 확인됨 |
| 재발 방지 | 이 PC에서 스크립트를 다시 쓰려면 `rsync`를 먼저 설치(예: Git for Windows에 rsync 패키지 추가)하거나, 스크립트를 `scp` 기반으로 수정해둔다 |

---

## 참고 — 자주 발생하는 문제 유형 (겪었을 때 대조용, 예시로만 사용할 것)

| 증상 | 확인해볼 것 |
|---|---|
| 브라우저/curl에서 응답 없음(타임아웃) | SG 인바운드 80/TCP/0.0.0.0/0 존재 여부, Route Table의 0.0.0.0/0→IGW 존재 여부, IGW가 VPC에 Attach 됐는지 |
| Connection refused / Connection reset | 인스턴스 내부 `systemctl status nginx`로 실행 여부 확인, 인스턴스에 붙은 보안 그룹이 의도한 것인지(사건 #1 참고) |
| SSH 접속 timeout | SG 인바운드 22/TCP의 소스 IP가 현재 본인 공인 IP와 일치하는지(`curl -s https://checkip.amazonaws.com`로 재확인 — IP는 네트워크 환경에 따라 바뀔 수 있음) |
| SSH Permission denied (publickey) | `.pem` 권한, 사용자명(Ubuntu=`ubuntu`, Amazon Linux=`ec2-user`) — 사건 #2 참고 |
| /health가 404 | User data 스크립트 실행 여부, 배포판별 문서 루트 경로(Ubuntu=`/var/www/html`, Amazon Linux=`/usr/share/nginx/html`) — 사건 #3 참고 |
| 인스턴스 내부에서 `curl https://example.com` 실패 | Route Table의 0.0.0.0/0→IGW 누락, 퍼블릭 IP 자동 할당 미설정 |
