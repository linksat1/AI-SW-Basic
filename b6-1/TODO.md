# B6-1 TODO — 미완료 사항 및 향후 진행 방법

## 왜 미완료인가

이 과제는 실제 AWS 계정에서 VPC/EC2/Security Group/IAM을 직접 생성·조작해야 하는 핸즈온
과제입니다. 이 환경에는 AWS 자격증명(`aws sts get-caller-identity` 실패, `~/.aws` 없음
확인 완료)이 없고, 가짜 스크린샷이나 가짜 실행 결과를 만드는 것은 부정확한 제출이 되므로
만들지 않았습니다. 그래서 **가이드·템플릿·설명자료까지만 준비**했고, 실제 리소스 생성과
검증은 사용자가 AWS 콘솔에서 직접 진행해야 합니다.

---

## 미완료 항목 (진행 순서대로)

### 1. AWS 계정 준비
- [ ] 루트 계정이 아닌 **IAM 사용자**로 로그인 (평가 질문 6장 대비)
- [ ] `가이드.md` 1장의 IAM 최소 권한 정책 JSON을 그대로 적용 (EC2/VPC 범위만, `AdministratorAccess` 미부여)

### 2. 네트워크 구성
- [ ] VPC 생성 (`10.0.0.0/16`)
- [ ] Public Subnet 생성 (`10.0.1.0/24`, 퍼블릭 IPv4 자동 할당 활성화)
- [ ] Internet Gateway 생성 후 VPC에 Attach
- [ ] Public Subnet의 Route Table에 `0.0.0.0/0 → IGW` 경로 추가

### 3. EC2 + 웹 서버
- [ ] EC2 인스턴스 1대를 Public Subnet에 생성 (`가이드.md`의 user-data 스크립트로 nginx 자동 설치, 또는 SSH 접속 후 수동 설치)
- [ ] SSH 접속 확인
- [ ] `curl -i http://localhost` → `200` 확인
- [ ] `curl -i https://example.com` → 아웃바운드 통신 확인

### 4. Security Group
- [ ] 인바운드 80/TCP ← `0.0.0.0/0`
- [ ] 인바운드 22/TCP ← 본인 공인 IP `/32`만 (전체 허용 금지)
- [ ] 전체 포트(`0-65535`) 허용 규칙이 없는지 재확인

### 5. 외부 접속 검증 (택 1) — 스크린샷 필수
- [ ] (A) 브라우저로 `http://<퍼블릭IP>` 접속 스크린샷, 또는
- [ ] (B) `curl -i http://<퍼블릭IP>/health` → `200`/`OK` 스크린샷
- [ ] `docs/screenshots/` 폴더 만들어 저장

### 6. 문서 완성 (템플릿 → 실제 내용으로 교체)
- [ ] `README.md`의 `<...>` 전부 교체 (퍼블릭 IP, 선택한 검증 방식, 스크린샷 경로, 네트워크/보안 요약 표)
- [ ] `docs/troubleshooting.md`의 사건 #1을 **실제로 겪은 문제**로 채우기 (겪지 않았다면 `가이드.md` 7장 참고해 하나를 의도적으로 재현)
- [ ] `docs/architecture.png`는 이미 생성되어 있음 — 실제 구성과 일치하는지 눈으로 재확인만 하면 됨

### 7. 리소스 정리 (실습 완전히 끝난 뒤에만)
- [ ] `docs/cleanup-checklist.md`를 순서대로 실행하며 `[x]` 체크 (EC2 → EBS → EIP → IGW → Subnet/RouteTable/SG → VPC)
- [ ] 1~2일 뒤 Billing Dashboard에서 과금 0 수렴 확인

### 8. 최종 자가 검수
- [ ] `제출전_자가검수_체크리스트.md`의 9개 섹션을 위 1~7번을 마친 뒤 순서대로 체크

### 9. (선택) 보너스
- [ ] 보너스 1: HTTPS 적용 (도메인 + Let's Encrypt) 후 README.md에 기재
- [ ] 보너스 2: Docker 컨테이너 배포 후 README.md에 기재

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
