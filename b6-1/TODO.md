# B6-1 TODO — 미완료 사항 및 향후 진행 방법 [거의 완료 — Billing 확인만 남음]

## 왜 미완료인가

이 과제는 실제 AWS 계정에서 VPC/EC2/Security Group/IAM을 직접 생성·조작해야 하는 핸즈온
과제입니다. 이 환경에는 AWS 자격증명(`aws sts get-caller-identity` 실패, `~/.aws` 없음
확인 완료)이 없고, 가짜 스크린샷이나 가짜 실행 결과를 만드는 것은 부정확한 제출이 되므로
만들지 않았습니다. 그래서 **가이드·템플릿·설명자료까지만 준비**했고, 실제 리소스 생성과
검증은 사용자가 AWS 콘솔에서 직접 진행해야 합니다.

---

## 미완료 항목 (진행 순서대로)

### 1. AWS 계정 준비
- [x] 루트 계정이 아닌 **IAM 사용자**로 로그인 (평가 질문 6장 대비) — `b6-1-lab-user` 생성 완료 (`docs/screenshots/IAM-사용자생성화면.png`)
- [x] `가이드.md` 1장의 IAM 최소 권한 정책 JSON을 그대로 적용 (EC2/VPC 범위만, `AdministratorAccess` 미부여) — `b6_AWS_connect` 정책 생성 및 연결 완료

### 2. 네트워크 구성
- [x] VPC 생성 (`10.0.0.0/16`) — `b6-1-vpc` (vpc-0c545f75c5e99316e) 생성 완료 (`docs/screenshots/VPC-생성.png`)
- [x] Public Subnet 생성 (`10.0.1.0/24`, 퍼블릭 IPv4 자동 할당 활성화) — `b6-1-public-subnet` (subnet-07bfad6ae86d9d462) 생성 완료 (`docs/screenshots/public-subnet-생성.png`)
- [x] Internet Gateway 생성 후 VPC에 Attach — `b6-1-igw` (igw-0e32f9c97e6045945), `b6-1-vpc`에 Attached 완료 (`docs/screenshots/internet-gateway.png`)
- [x] Public Subnet의 Route Table에 `0.0.0.0/0 → IGW` 경로 추가 — `b6-1-public-rt` (rtb-0569535b0d4ad7ed4), 라우팅+서브넷 연결 완료 (`docs/screenshots/route-table.png`)

### 3. EC2 + 웹 서버
- [x] EC2 인스턴스 1대를 Public Subnet에 생성 — `i-033dab99aa8ef4810`, Amazon Linux 2023(al2023-ami-2023.12.20260710.0), t3.micro, 퍼블릭 IP `13.125.33.210`, 키페어 `b6-1-key`, SSH 접속 후 `dnf install nginx`로 수동 설치
- [x] SSH 접속 확인 — 사용자명 `ec2-user` (Amazon Linux는 `ubuntu`가 아님, 트러블슈팅 기록됨)
- [x] `curl -i http://localhost` → `200` 확인
- [x] `curl -i https://example.com` → 아웃바운드 통신 확인 (200 OK, cloudflare 응답 확인)

### 4. Security Group
- [x] 인바운드 80/TCP ← `0.0.0.0/0` — `b6-1-web-sg` (sg-0879a9a06d512313a) 생성 완료
- [x] 인바운드 22/TCP ← 본인 공인 IP `/32`만 (전체 허용 금지) — `212.102.51.72/32`
- [x] 전체 포트(`0-65535`) 허용 규칙이 없는지 재확인 — 확인 완료 (`docs/screenshots/security-group.png`)

### 5. 외부 접속 검증 (택 1) — 스크린샷 필수
- [x] (A) 브라우저로 `http://13.125.33.210` 접속 스크린샷 — "Welcome to nginx!" 확인 (`docs/screenshots/외부접속검증.png`)
- [x] (B, 보조) `curl -i http://13.125.33.210/health` → `200`/`OK` SSH 내부에서 확인 완료
- [x] `docs/screenshots/` 폴더 만들어 저장

### 6. 문서 완성 (템플릿 → 실제 내용으로 교체)
- [ ] `README.md`의 `<...>` 전부 교체 (퍼블릭 IP, 선택한 검증 방식, 스크린샷 경로, 네트워크/보안 요약 표)
- [x] `docs/troubleshooting.md`의 사건 #1을 **실제로 겪은 문제**로 채우기 — 실제 3건 기록 완료 (① default SG 오연결 ② SSH 사용자명 오류 ③ nginx 문서 루트 경로 차이)
- [ ] `docs/architecture.png`는 이미 생성되어 있음 — 실제 구성과 일치하는지 눈으로 재확인만 하면 됨

### 7. 리소스 정리 (실습 완전히 끝난 뒤에만)
- [x] `docs/cleanup-checklist.md`를 순서대로 실행하며 `[x]` 체크 (EC2 → EBS → EIP → IGW → Subnet/RouteTable/SG → VPC) — 전체 완료
- [ ] 1~2일 뒤 Billing Dashboard에서 과금 0 수렴 확인 — **2026-07-17~18경 확인 필요**

### 8. 최종 자가 검수
- [x] `제출전_자가검수_체크리스트.md`의 9개 섹션을 위 1~7번을 마친 뒤 순서대로 체크 — 완료
      (Billing Dashboard 확인만 2026-07-17~18경 남음, 9번 보너스는 진행 안 함)

### 9. (선택) 보너스 — 스킵
- [x] 보너스 1: HTTPS 적용 — 스킵 (진행 안 함)
- [x] 보너스 2: Docker 컨테이너 배포 — 스킵 (진행 안 함)

---

## 이미 준비되어 있어 다시 만들 필요 없는 것

- `가이드.md` — 10단계 실습 가이드, IAM 정책 JSON, SG 규칙 표, 트러블슈팅 참고표 포함
- `평가질문_설명자료.md` — 평가 질문 5개 항목 답변 자료 (실습 후 본인 경험으로 검토·보완 권장)
- `docs/architecture.png` — 다이어그램 완성본
- `README.md`, `docs/troubleshooting.md`, `docs/cleanup-checklist.md` — 구조가 잡힌 템플릿 (내용만 채우면 됨)

---

## 완료 후 이 파일에서 할 일

위 체크리스트를 모두 마치면 이 `TODO.md` 파일은 삭제하거나, 상단에 "완료" 표시만 남기고
보관하세요.
