# mini_redis

해시맵 / 이중 연결 리스트 / 최소 힙을 직접 구현해 만든 **CLI 기반 In-Memory
Key-Value 저장소**입니다. `dict`, `set`, `collections`는 사용하지 않았습니다.

## 실행 방법

`b3-1` 폴더(이 폴더의 상위 폴더) **안에서** 실행해야 합니다.

```bash
cd b3-1
python3 -m mini_redis
```

`mini-redis> ` 프롬프트가 뜨면 명령을 입력합니다. `exit` 또는 `quit`으로
종료합니다.

## 폴더 구조

| 파일 | 역할 |
|---|---|
| `__main__.py` | 진입점. `python -m mini_redis`로 실행하면 가장 먼저 호출됨 |
| `cli.py` | REPL 루프, 명령어 파싱, Redis 스타일 출력 포맷팅 |
| `store.py` | Mini Redis 엔진: String/메모리(LRU)/TTL 명령어 처리 |
| `hashmap.py` | 체이닝 방식 해시맵 (직접 설계한 해시 함수 포함) |
| `linked_list.py` | 이중 연결 리스트 (체이닝 + LRU 순서 추적에 재사용) |
| `heap.py` | 배열 기반 최소 힙 (TTL 만료 관리) |

## 지원 명령어

```
SET key value              GET key
DEL key                    EXISTS key
DBSIZE                     KEYS

CONFIG SET maxmemory bytes INFO memory

EXPIRE key seconds         TTL key

exit / quit                (REPL 종료)
```

값에 공백을 포함하려면 큰따옴표로 감쌉니다: `SET user:1 "Alice Kim"`

## 명령 예시

```
mini-redis> CONFIG SET maxmemory 30
OK
mini-redis> SET user:1 "Alice"
OK
mini-redis> SET user:2 "Bob"
OK
mini-redis> SET user:3 "Charlie"
OK
mini-redis> GET user:1
(nil)
mini-redis> INFO memory
used_memory:22
maxmemory:30
evicted_keys:1
mini-redis> KEYS
1. "user:2"
2. "user:3"
mini-redis> EXPIRE user:2 3
(integer) 1
mini-redis> TTL user:2
(integer) 2
```

더 자세한 실행 로그와 각 자료구조 설명은 상위 폴더의 `가이드.md`,
`평가질문_설명자료.md`, `제출/실행결과.md`를 참고하세요.
