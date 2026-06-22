# B1-2 Codex 작업 대화 로그 - 2026-06-22

이 문서는 2026-06-22 KST 기준, Codex와의 대화에서 수행한 B1-2 실습/보고서/발표자료 작업을 평가 및 제출 이력 확인용으로 정리한 로그입니다.

원문 채팅 전체 export가 아니라, 이 대화창에서 합의하고 실행한 요청, 판단, 생성 파일, 검증 결과를 재현 가능한 작업 기록 형태로 요약했습니다.

## 1. 최초 요청

사용자는 `b1-2_codex/beginner-guide.md`를 그대로 실행하고 결과파일을 생성해 달라고 요청했습니다.

처음에는 Plan Mode였기 때문에 `beginner-guide.md`, `scripts/monitor.sh`, `scripts/run_helpers.sh`, `reports/README.md`, `evidence/README.md`를 읽고 실행 계획을 만들었습니다.

계획의 핵심은 다음과 같았습니다.

- OrbStack Ubuntu `b1-lab`에서 원본 `agent-leak-app` 실행
- OOM, CPU Spike, Deadlock 3개 케이스 실행
- `/var/log/agent-app/evidence_*` 로그 수집
- `b1-2_codex/evidence/logs/`로 증거 복사
- `b1-2_codex/reports/oom.md`, `cpu-spike.md`, `deadlock.md` 작성

## 2. 원본 앱 실행 및 결과파일 생성

Default mode 전환 후 사용자가 계획 실행을 요청했습니다.

실행 과정에서 확인한 내용:

- `orb list` 초기 실행 시 OrbStack 머신이 없거나 목록이 비어 있었습니다.
- `orb create -a amd64 ubuntu b1-lab`로 `b1-lab` Ubuntu VM을 생성했습니다.
- 호스트와 VM 모두 `x86_64`/`amd64`였으므로 `agent-leak-app-x86`를 사용했습니다.
- `b1-2/b1-1 setup.sh`로 B1-1 기준 계정/디렉터리/권한을 복구했습니다.
- `/home/agent-admin/agent-app/agent-leak-app`에 원본 바이너리를 배치했습니다.
- `secret.key` 내용이 `agent_api_key_test`인지 확인했습니다.
- 앱 부팅에서 `All Boot Checks Passed!`, `Agent READY`를 확인했습니다.

생성된 핵심 산출물:

- `b1-2_codex/reports/oom.md`
- `b1-2_codex/reports/cpu-spike.md`
- `b1-2_codex/reports/deadlock.md`
- `b1-2_codex/evidence/logs/*.log`

검증:

- 필수 12개 증거 로그 존재 확인
- 리포트에서 참조한 모든 `evidence/logs/*.log` 파일 존재 확인

## 3. 원본 바이너리 동일성 확인

사용자는 VM에서 실행한 `agent-leak-app-x86`가 오늘 다운로드한 zip에서 압축해제한 파일과 같은지 확인해 달라고 요청했습니다.

비교 대상:

- VM: `/home/agent-admin/agent-app/agent-leak-app`
- 로컬: `b1-2/실행파일/agent-leak-app-x86`
- zip 내부: `b1-2/실행파일/agent-app-leak.zip`의 `agent-leak-app-x86`

확인 결과:

```text
SHA-256:
7e0a19cfa80ece6b547a5008273661f0d4d71e526e96b51e0d0f341dd1bb3e40
```

결론:

- VM 실행 파일, 로컬 압축해제 파일, zip 내부 `agent-leak-app-x86`는 같은 파일입니다.
- 크기도 모두 `6,502,016 bytes`였습니다.

## 4. 기존 보고서와 오늘 결과 비교

사용자는 `b1-2_codex/reports/oom.md`와 `b1-2/report-case1-memory-leak.md`가 같은 결과물인지 비교해 달라고 요청했습니다.

비교 결과:

- 두 파일은 해시와 내용이 다릅니다.
- `b1-2_codex/reports/oom.md`는 오늘 원본 `agent-leak-app-x86` 실행 결과입니다.
- `b1-2/report-case1-memory-leak.md`는 2026-06-09에 만든 Python 시뮬레이터 `b1-2/agent-leak-sim.py` 기반 보고서입니다.

중요 차이:

- 오늘 원본 실행: `MEMORY_LIMIT=50`, `Current Heap: 25MB -> 50MB`, `Memory limit exceeded (50MB >= 50MB)`
- 기존 시뮬레이터 보고서: `MEMORY_LIMIT=256`, `[Memory] Increasing... Total: 275 MB`

결론:

- 둘 다 Memory Leak/OOM 계열 설명이지만 같은 실행 결과물은 아닙니다.
- 원본 앱 기준 제출에는 `b1-2_codex/reports/oom.md`가 더 적합합니다.

## 5. 평가 대비 설명 자료 작성

사용자는 교재 발췌 파일 `b1-2/b1-2-mission_교제발췌`와 평가 질문 파일 `b1-2/b1-2질문`을 참고하여, 오늘 실행 결과 기반의 설명 자료를 만들어 달라고 요청했습니다.

생성 파일:

- `b1-2_codex/reports/evaluation-prep.md`

문서 구성:

- 교재 요구사항과 오늘 결과 매핑
- 실행 환경 설명
- OOM 발표용 설명
- CPU Spike 발표용 설명
- Deadlock 발표용 설명
- 평가 예상 질문 답변
- 평가 때 주의할 표현
- 30초 마무리 멘트

핵심 판단:

- OOM은 원본 앱에서 MemoryGuard 자기 종료 재현 성공
- CPU는 `CPU_MAX_OCCUPY`에 따른 cooldown은 확인했지만 Watchdog/SIGTERM 종료는 미재현
- Deadlock은 경고 문구는 있었지만 `Threads: 1`이고 `WAITING/BLOCKED` 로그가 없어 미재현

## 6. PPT 자료 생성

사용자는 `evaluation-prep.md`를 PPT로 만들어 달라고 요청했습니다.

처음 `python-pptx` 모듈을 확인했지만 설치되어 있지 않았습니다.

대응:

- 외부 패키지 설치 없이 표준 라이브러리만 사용해 PPTX OpenXML 구조를 생성하는 스크립트를 작성했습니다.

생성 파일:

- `b1-2_codex/scripts/make_evaluation_ppt.py`
- `b1-2_codex/reports/evaluation-prep.pptx`

검증:

- `file` 명령에서 Microsoft OOXML로 인식
- `unzip -t b1-2_codex/reports/evaluation-prep.pptx` 통과

## 7. Downloads PPT 복사 및 GitHub 푸시

사용자는 Downloads 디렉터리의 PPT 파일을 `b1-2_codex/reports/`로 복사하고 GitHub로 모두 푸시해 달라고 요청했습니다.

확인된 Downloads 파일:

- `/Users/cspag5955/Downloads/b1-2-evaluation-prep.pptx`

복사 대상:

- `b1-2_codex/reports/b1-2-evaluation-prep.pptx`

검증:

- `unzip -t b1-2_codex/reports/b1-2-evaluation-prep.pptx` 통과
- `unzip -t b1-2_codex/reports/evaluation-prep.pptx` 통과

커밋 및 푸시:

```text
Commit: 34d1cd8 Add B1-2 troubleshooting reports and slides
Remote: https://github.com/linksat1/AI-SW-Basic.git
Branch: main
Push: 69e4bb9..34d1cd8 main -> main
```

커밋에 포함한 범위:

- `b1-2_codex/evidence/logs/*`
- `b1-2_codex/reports/*.md`
- `b1-2_codex/reports/*.pptx`
- `b1-2_codex/scripts/make_evaluation_ppt.py`

커밋에서 제외한 범위:

- `RELEASE_INSTRUCTIONS.md`
- `b1-1/실행파일/*`
- `b1-2/실행파일/*`

제외 이유:

- 위 파일들은 이번 보고서/PPT 산출물과 직접 관련 없는 미추적 파일이었고, 특히 zip/바이너리는 큰 실행파일이므로 의도치 않은 업로드를 피했습니다.

## 8. 현재 대화 로그 저장 요청

마지막으로 사용자는 이 대화창의 대화도 저장하고 푸시해 달라고 요청했습니다.

이에 따라 이 파일 `b1-2_codex/reports/conversation-log-2026-06-22.md`를 생성했습니다.

이 파일에는 원문 전체 채팅이 아니라, 수행한 작업과 판단 근거, 생성 파일, 검증 결과, 푸시 기록을 요약했습니다.

## 9. 최종 산출물 목록

현재 B1-2 Codex 산출물의 핵심 파일:

```text
b1-2_codex/reports/oom.md
b1-2_codex/reports/cpu-spike.md
b1-2_codex/reports/deadlock.md
b1-2_codex/reports/evaluation-prep.md
b1-2_codex/reports/evaluation-prep.pptx
b1-2_codex/reports/b1-2-evaluation-prep.pptx
b1-2_codex/reports/conversation-log-2026-06-22.md
b1-2_codex/evidence/logs/
b1-2_codex/scripts/make_evaluation_ppt.py
```

## 10. 평가 설명 핵심 문장

```text
원본 agent-leak-app-x86를 실행해 로그와 OS 명령어 출력으로 세 가지 장애를 분석했습니다.
OOM은 MemoryGuard 자기 종료가 명확히 재현됐습니다.
CPU는 임계치에 따른 cooldown은 확인했지만 Watchdog/SIGTERM 종료는 원본 앱에서 재현되지 않았습니다.
Deadlock은 경고 문구만 있었고 실제 스레드가 1개라 lock 대기 증거가 없어 미재현으로 판단했습니다.
그래서 관찰 사실과 추론을 분리해 GitHub Issue 형식 리포트와 발표자료로 정리했습니다.
```
