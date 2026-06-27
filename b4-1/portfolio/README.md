# 박주선 포트폴리오

순수 HTML, CSS, JavaScript로 만든 반응형 포트폴리오 웹사이트입니다. Hero, About, Skills, Projects, Contact, Footer 섹션을 포함하며 GitHub API로 저장소 목록을 동적으로 불러옵니다.

## 배포 URL

- GitHub Pages: 배포 후 URL 입력 필요

## 주요 기능

- 모바일, 태블릿, 데스크톱 반응형 레이아웃
- 햄버거 메뉴 토글
- 다크 모드 전환 및 localStorage 저장
- 부드러운 앵커 스크롤
- 스크롤 위치에 따른 헤더 스타일 변경
- 스크롤 탑 버튼
- Intersection Observer 기반 스크롤 애니메이션
- GitHub API 저장소 목록 렌더링
- 프로젝트 로딩, 에러, 빈 상태 UI
- 언어별 프로젝트 필터링
- 문의 폼 필수값 및 이메일 형식 검증
- Hero 타이핑 효과

## 사용 기술

- HTML5 시맨틱 마크업
- CSS3 Flexbox, Grid, CSS 변수, 미디어 쿼리
- JavaScript ES6+, DOM 조작, 이벤트 처리, async/await, fetch
- GitHub REST API
- Font Awesome, Google Fonts

## 폴더 구조

```text
portfolio/
├── index.html
├── css/
│   └── style.css
├── js/
│   └── main.js
├── images/
│   ├── profile.png
│   └── profile.jpg
├── convert_png_to_jpg.py
└── README.md
```

## 기준값

- 모바일 메뉴 전환 기준: 768px 미만
- 태블릿 구간: 768px 이상, 1024px 미만
- 데스크톱 구간: 1024px 이상
- 헤더 배경 변경: 스크롤 60px 이상
- 스크롤 탑 버튼 표시: 스크롤 300px 이상
- Intersection Observer threshold: 0.2

## 실행 방법

1. VS Code에서 `portfolio` 폴더를 엽니다.
2. Live Server 확장에서 `index.html`을 실행합니다.
3. 브라우저에서 화면, 다크 모드, 메뉴, 폼, GitHub API 렌더링을 확인합니다.

## 스크린샷

- 데스크톱 화면: 배포 또는 실행 후 이미지 추가 필요
- 모바일 화면: 배포 또는 실행 후 이미지 추가 필요
- 다크 모드 화면: 배포 또는 실행 후 이미지 추가 필요
