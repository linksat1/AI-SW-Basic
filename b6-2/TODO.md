# B6-2 TODO — 미완료 사항 및 향후 진행 방법

## 왜 미완료인가

CLI 도구 자체(git 연동, safe-mode, 프롬프트 구성, 검증 로직, CLI 옵션, 예외 처리)는 이
환경에서 실제로 실행해 전부 검증했습니다(`제출/results/` 10개 캡처, `최종검수결과.md`
참고). 다만 이 환경에는 **실제 Anthropic API 키**와 **사용자의 GitHub 계정**이 없어, 이
두 가지에 의존하는 마지막 단계만 사용자가 직접 진행해야 합니다.

---

## 미완료 항목 (진행 순서대로)

### 1. 실제 API 키로 응답 품질 확인
- [ ] https://console.anthropic.com 에서 API 키 발급
- [ ] `export AI_API_KEY="sk-ant-..."` 설정
- [ ] 저장소에 임의로 파일을 하나 수정한 뒤 `git add .` → `python main.py commit` 실행
- [ ] 실제로 생성된 커밋 메시지가 변경 내용과 맞는지, 72자 이내인지 육안 확인
- [ ] `python main.py pr --base <기준브랜치>` 도 동일하게 실행해 PR 초안 품질 확인
- [ ] `--safe-mode`를 켠 채로도 한 번 실행해, 실제 Claude 응답이 마스킹된 diff만으로도
      충분히 괜찮은 메시지를 만드는지 확인 (마스킹 때문에 품질이 심하게 떨어지면
      `ai_gitgen/safe_mode.py`의 마스킹 패턴/줄 수 제한을 조정)

### 2. GitHub 저장소 생성 및 push
- [ ] GitHub에서 새 저장소 생성 (이 프로젝트 전체 `AI-SW-basic`를 이미 쓰고 있다면 그대로 push해도 됨)
- [ ] `가이드.md` 7장의 명령어 그대로 실행:
  ```bash
  cd b6-2
  git init            # AI-SW-basic 전체를 이미 쓰는 중이면 생략
  git add .
  git commit -m "feat: AI 기반 git commit/PR 생성기 초기 구현"
  git remote add origin https://github.com/<사용자명>/<저장소명>.git
  git push -u origin main
  ```
- [ ] `README.md`의 `## GitHub 저장소` 섹션에 있는 `<여기에 실제로 push한 GitHub 저장소 URL을 기재하세요>` 플레이스홀더를 실제 URL로 교체

### 3. 문서 최종 점검
- [ ] `README.md` 출력 예시가 "mock 응답 기반"이라고 명시된 부분을, 실제 키로 받은 진짜
      출력 예시로 교체 (선택 — 원한다면 mock 예시를 그대로 남겨둬도 되지만, 실제 응답으로
      바꾸면 더 신뢰도 높은 제출물이 됨)
- [ ] `최종검수결과.md`의 "1-1. 동작하는 CLI 도구" 표에서 "⚠️ 코드는 완비, 실제 네트워크
      호출은 미검증" 행을 실제 실행 후 "✅"로 갱신

### 4. (선택) 보너스 과제
- [ ] 보너스 1: 이전 미션에서 만든 실제 저장소에 이 도구를 적용해, 실제 커밋/PR을 생성해보기
- [ ] 보너스 2: 프로젝트별 커밋/PR 컨벤션(Conventional Commits 등)을 설정 파일로 분리해
      `prompt_builder.py`가 그 설정을 읽도록 확장
- [ ] 보너스 3: safe-mode 마스킹 패턴을 더 정교하게 확장하거나, 전송 전 사용자 확인
      (diff 미리보기 → 승인) 단계를 `cli.py`에 추가

---

## 이미 준비되어 있어 다시 만들 필요 없는 것

- `main.py` + `ai_gitgen/` 패키지 전체 — 실제 실행으로 검증된 동작하는 코드
- `가이드.md` — 설치/실행/설계 이유 설명
- `평가질문_설명자료.md` — 과제 목표 5개 항목 답변
- `제출/results/*.txt` (10개) — git 연동/safe-mode/검증/예외 처리 실행 캡처
- `README.md` — install/env-setup/usage/output/safety-cost 항목 전부 작성 완료 (GitHub URL만 채우면 됨)

---

## 완료 후 이 파일에서 할 일

위 항목을 모두 마치면 이 `TODO.md` 파일은 삭제하거나, 상단에 "완료" 표시만 남기고
보관하세요.
