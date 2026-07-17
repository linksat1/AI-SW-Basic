# AWS 자료 올리기 — b6-1 재실습 진행 기록

> 작성일: 2026-07-17 · 공용 PC에서 작업하다가 중단, 집(개인 PC)에서 이어가기 위한 기록입니다.
> ✅ = 오늘 실제로 실행 완료 / ⏳ = 아직 실행 안 함 (다음에 할 일)

---

## ✅ 오늘 완료한 작업 (실제 AWS 콘솔에서 생성 확인됨)

로그인: IAM 사용자 `b6-1-lab-user`, 리전 `ap-northeast-2(서울)`

| 리소스 | 이름 | ID | 주요 설정 |
|---|---|---|---|
| VPC | `b6-1-vpc` | `vpc-0fdc2336b6f5f3b7d` | CIDR `10.0.0.0/16`, 상태 Available |
| Subnet | `b6-1-public-subnet` | `subnet-099705bc6971f71a1` | CIDR `10.0.1.0/24`, AZ `ap-northeast-2a`, 퍼블릭 IPv4 자동 할당 **활성화** |
| Internet Gateway | `b6-1-igw` | `igw-08f3ed5b01a417a40` | 상태 `Attached` → `vpc-0fdc2336b6f5f3b7d` |
| Route Table | `b6-1-public-rt` | `rtb-01abd8fa2c4904b5d` | 라우팅: `0.0.0.0/0`→IGW, `10.0.0.0/16`→local / 서브넷 연결: `b6-1-public-subnet` |
| Security Group | `b6-1-web-sg` | `sg-09bd91733c8dd77a7` | VPC `b6-1-vpc` |

**Security Group 인바운드 규칙 (2개)**

| 유형 | 프로토콜 | 포트 | 소스 |
|---|---|---|---|
| HTTP | TCP | 80 | `0.0.0.0/0` |
| SSH | TCP | 22 | `121.135.181.43/32` (오늘 작업한 공용 PC의 공인 IP — ⚠️ 아래 참고) |

아웃바운드: 기본값(모든 트래픽 / `0.0.0.0/0`) 유지

---

## ⏳ 아직 실행하지 않은 작업 (다음에 할 일 — 반드시 개인 PC에서)

### 1. Security Group SSH 인바운드 IP 재확인 (중요)

위 SSH 규칙(`121.135.181.43/32`)은 **오늘 공용 PC의 공인 IP**입니다. 집(개인 PC)에서는
IP가 다를 가능성이 높으므로, 재개 전에 먼저:

```bash
curl -s https://checkip.amazonaws.com
```

로 집 IP를 확인한 뒤, EC2 콘솔 → 보안 그룹 → `b6-1-web-sg` → 인바운드 규칙 편집에서
SSH 소스를 새 IP(`<집IP>/32`)로 **수정**해야 SSH 접속이 가능합니다.

### 2. EC2 인스턴스 생성 (미실행)

EC2 콘솔 → 인스턴스 시작 → 아래 값으로 생성:

- 이름: `b6-1-web-server`
- AMI: **Amazon Linux 2023** (프리 티어)
- 인스턴스 유형: `t3.micro`
- **키 페어: 여기서 새로 생성 — 반드시 개인 PC에서만.** 다운로드된 `.pem` 파일은
  개인 PC 밖으로 절대 옮기지 말 것(이메일 전송, 클라우드 동기화 폴더 저장 금지)
  ```bash
  chmod 400 <다운로드경로>/b6-1-key-v2.pem
  ```
- 네트워크 설정 → 편집:
  - VPC: `b6-1-vpc`
  - 서브넷: `b6-1-public-subnet`
  - 퍼블릭 IP 자동 할당: 활성화
  - 방화벽: 기존 보안 그룹 `b6-1-web-sg` 선택
- 스토리지: 8~10GiB 기본값
- 고급 세부 정보 → 사용자 데이터:
  ```bash
  #!/bin/bash
  dnf install -y nginx
  systemctl enable nginx
  systemctl start nginx
  ```

### 3. 포트폴리오 배포 (미실행)

EC2가 `running` 상태가 되고 퍼블릭 IP가 나오면, 이 저장소의 스크립트로 배포:

```bash
cd /Users/cspag5955/AI-SW-Basic/b6-1/scripts
./deploy-portfolio.sh <EC2_퍼블릭IP> <pem_키_경로>
```

`b4-1/portfolio/` 전체를 업로드하고 nginx 문서 루트를 교체 + 재시작까지 자동으로 처리합니다.
(스크립트 자체는 이미 만들어져 있음 — `b6-1/scripts/deploy-portfolio.sh`)

### 4. 외부 접속 검증 (미실행)

- 브라우저에서 `http://<퍼블릭IP>` 접속 → 포트폴리오 페이지 확인
- 스크린샷 저장: `docs/screenshots/`

### 5. 문서 업데이트 (미실행)

- `README.md` — 새 퍼블릭 IP, 검증 스크린샷 경로로 갱신 (기존 내용은 이전 실습 결과이므로 교체 필요)
- `docs/troubleshooting.md` — 이번 재실습에서 겪은 문제가 있다면 기록 추가
- `docs/cleanup-checklist.md` — 이번 실습도 끝나면 반드시 리소스 정리 후 갱신

---

## 보안 체크리스트 (재개 전 확인)

- [ ] 공용 PC의 AWS 콘솔에서 로그아웃했는가
- [ ] 공용 PC에는 pem 키 파일이 전혀 남아있지 않은가 (오늘은 생성 자체를 안 했으므로 해당 없음)
- [ ] 키 페어 생성은 개인 PC에서만 진행하는가
- [ ] SSH 인바운드 규칙을 개인 PC의 현재 공인 IP로 갱신했는가
