# 포트폴리오 교본 - 시작 가이드

## 폴더 구조

```
portfolio/
├── index.html        ← 메인 HTML 파일 (여기서 시작!)
├── css/
│   └── style.css     ← 스타일 (레이아웃, 색상, 반응형)
├── js/
│   └── main.js       ← 동작 로직 (이벤트, API, 폼 검사)
├── images/
│   └── profile.jpg   ← 프로필 이미지 (직접 추가)
└── README.md         ← 이 파일
```

## 시작하는 순서

1. `index.html`을 VS Code로 열기
2. Live Server 확장 설치 후 "Go Live" 클릭
3. 브라우저에서 `http://127.0.0.1:5500` 확인

## 내 정보로 수정할 곳

| 파일 | 찾을 내용 | 바꿀 내용 |
|------|-----------|-----------|
| `index.html` | `홍길동` | 본인 이름 |
| `index.html` | `hong@example.com` | 본인 이메일 |
| `index.html` | `yourusername` | 본인 GitHub 아이디 |
| `js/main.js` | `const GITHUB_USERNAME = 'yourusername'` | 본인 GitHub 아이디 |
| `images/` | profile.jpg 없음 | 본인 사진 파일 추가 |

## GitHub Pages 배포 방법

1. GitHub에 새 저장소 생성
2. 이 폴더 파일들을 전부 push
3. 저장소 Settings → Pages → Branch: main, 폴더: / (root) → Save
4. 1~2분 후 `https://yourusername.github.io/저장소이름` 접속 확인

## 사용 기술

- HTML5 (시맨틱 마크업)
- CSS3 (Flexbox, Grid, CSS 변수, 미디어 쿼리)
- JavaScript ES6+ (async/await, Intersection Observer, localStorage)
- GitHub API

## 브레이크포인트 기준값

- 모바일 → 태블릿: **768px**
- 태블릿 → 데스크톱: **1024px**

## 스크롤 기준값

- 헤더 배경 변경: **60px**
- 스크롤 탑 버튼 표시: **300px**
- Intersection Observer threshold: **0.2**
