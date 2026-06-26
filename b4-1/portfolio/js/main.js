/**
 * main.js - 포트폴리오 메인 JavaScript 파일
 *
 * 파일 실행 순서:
 * HTML에서 <script defer>로 연결되어 있으므로
 * HTML 파싱이 완료된 후 자동으로 실행된다.
 *
 * 구성:
 * 1. DOM 요소 선택
 * 2. 다크 모드
 * 3. 햄버거 메뉴
 * 4. 스크롤 이벤트
 * 5. 스크롤 애니메이션 (Intersection Observer)
 * 6. GitHub API 연동
 * 7. 폼 유효성 검사
 * 8. 타이핑 효과 (보너스)
 */

"use strict";
/*
  "use strict" : 엄격 모드 선언.
  자바스크립트를 더 엄격하게 검사해 실수를 에러로 잡아준다.
  - 선언하지 않은 변수 사용 금지
  - 예약어를 변수명으로 사용 금지
  등의 규칙이 적용된다.
  파일 맨 위에 문자열로 선언한다.
*/


/* =====================================================
   1. DOM 요소 선택

   HTML이 완전히 로드된 후 실행되므로
   여기서 선택하면 모든 요소를 찾을 수 있다.
   ===================================================== */

/*
  document.getElementById('id') : id로 요소를 하나 선택.
  가장 빠른 선택 방법.

  document.querySelector('CSS선택자') : CSS 선택자로 요소를 하나 선택.
  - '#id'    : id로 선택 (getElementById와 동일)
  - '.class' : 클래스로 선택
  - 'div'    : 태그로 선택
  - '[data-filter]' : 속성으로 선택
  매칭되는 첫 번째 요소를 반환한다.

  document.querySelectorAll('CSS선택자') : 조건에 맞는 모든 요소를 선택.
  NodeList(배열과 유사)를 반환한다.
*/

const header = document.getElementById('header');
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const scrollTopBtn = document.getElementById('scroll-top');
const projectsGrid = document.getElementById('projects-grid');
const projectsLoading = document.getElementById('projects-loading');
const projectsError = document.getElementById('projects-error');
const projectsEmpty = document.getElementById('projects-empty');
const retryBtn = document.getElementById('retry-btn');
const contactForm = document.getElementById('contact-form');
const formSuccess = document.getElementById('form-success');
const filterBtns = document.querySelectorAll('.filter-btn');
/*
  const vs let:
  - const : 재할당 불가능한 상수. 변수 선언 후 값을 바꿀 수 없다.
            객체/배열의 내부 값은 변경 가능. (참조만 고정)
  - let   : 재할당 가능한 변수. 나중에 값을 바꿀 일이 있으면 let 사용.
  - var   : 구식 방법. 사용하지 말 것. (스코프 문제 있음)

  원칙: 기본적으로 const를 쓰고, 재할당이 필요할 때만 let으로 변경.
*/


/* =====================================================
   2. 다크 모드

   상태 관리 패턴:
   [토글 버튼 클릭] → [isDark 상태 변경] → [화면 업데이트]
   ===================================================== */

/*
  localStorage : 브라우저에 데이터를 영구 저장하는 공간.
  새로고침이나 브라우저를 닫아도 데이터가 유지된다.

  주요 메서드:
  - localStorage.setItem('키', '값')   : 저장
  - localStorage.getItem('키')         : 읽기 (없으면 null 반환)
  - localStorage.removeItem('키')      : 삭제
  - localStorage.clear()               : 전체 삭제

  단, 문자열만 저장 가능하다. 객체는 JSON.stringify()로 변환 필요.
*/

// 저장된 테마를 읽어온다. 없으면 null 반환.
const savedTheme = localStorage.getItem('theme');

// 앱이 처음 시작될 때 저장된 테마를 적용한다.
if (savedTheme === 'dark') {
  document.body.setAttribute('data-theme', 'dark');
  themeIcon.className = 'fa-solid fa-sun'; /* 달 → 해 아이콘으로 변경 */
}

// 다크 모드 토글 버튼에 클릭 이벤트 연결
themeToggle.addEventListener('click', () => {
  /*
    addEventListener(이벤트유형, 콜백함수) :
    이벤트가 발생했을 때 실행할 함수를 등록한다.

    이벤트 유형: 'click', 'submit', 'scroll', 'input', 'change', 'keydown' 등

    콜백함수 표기법:
    1. 화살표 함수 : () => { ... }    ← 현대적인 방법 (권장)
    2. 일반 함수   : function() { ... }

    HTML 속성(onclick="...")을 사용하면 안 된다!
    → addEventListener로 분리하는 것이 올바른 방법.
  */

  // 현재 테마 확인
  const currentTheme = document.body.getAttribute('data-theme');
  /*
    getAttribute('속성명') : HTML 요소의 속성값을 가져온다.
    setAttribute('속성명', '값') : 속성을 설정한다.
    removeAttribute('속성명') : 속성을 제거한다.
  */

  if (currentTheme === 'dark') {
    // 다크 → 라이트
    document.body.removeAttribute('data-theme');
    themeIcon.className = 'fa-solid fa-moon';
    localStorage.setItem('theme', 'light');
  } else {
    // 라이트 → 다크
    document.body.setAttribute('data-theme', 'dark');
    themeIcon.className = 'fa-solid fa-sun';
    localStorage.setItem('theme', 'dark');
  }
});


/* =====================================================
   3. 햄버거 메뉴 (모바일)

   상태 관리 패턴:
   [햄버거 클릭] → [isOpen 상태 변경] → [메뉴 표시/숨김]
   ===================================================== */

hamburger.addEventListener('click', () => {
  /*
    classList : 요소의 클래스 목록을 조작하는 객체.
    - classList.add('클래스명')    : 클래스 추가
    - classList.remove('클래스명') : 클래스 제거
    - classList.toggle('클래스명') : 있으면 제거, 없으면 추가 (토글)
    - classList.contains('클래스명') : 클래스가 있는지 확인 (true/false 반환)
  */
  hamburger.classList.toggle('active');
  navMenu.classList.toggle('active');

  // 접근성: 메뉴 열림/닫힘 상태를 스크린리더에 알린다.
  const isOpen = navMenu.classList.contains('active');
  hamburger.setAttribute('aria-label', isOpen ? '메뉴 닫기' : '메뉴 열기');
  /*
    삼항 연산자 : 조건 ? 참일때값 : 거짓일때값
    if/else의 단축 표현이다.
    isOpen ? '메뉴 닫기' : '메뉴 열기'
    = isOpen이 true면 '메뉴 닫기', false면 '메뉴 열기'
  */
});

// 메뉴 링크 클릭 시 메뉴를 닫는다.
navMenu.addEventListener('click', (event) => {
  /*
    event : 이벤트 발생 시 자동으로 전달되는 이벤트 객체.
    event.target : 실제로 클릭된 요소.
    event.currentTarget : 이벤트 리스너가 달린 요소 (navMenu).
  */
  if (event.target.classList.contains('nav__link')) {
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
  }
});


/* =====================================================
   4. 스크롤 이벤트

   스크롤 위치에 따라 헤더 스타일, 스크롤 탑 버튼 표시.
   ===================================================== */

/*
  window.addEventListener('scroll', ...) :
  사용자가 스크롤할 때마다 이 함수가 실행된다.

  window.scrollY : 현재 세로 스크롤 위치 (픽셀 단위).
  0 = 맨 위, 증가할수록 아래로 스크롤된 상태.
*/
window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;

  // 헤더 배경 변경 (60px 이상 스크롤 시)
  if (scrollY >= 60) {
    header.classList.add('scrolled');
  } else {
    header.classList.remove('scrolled');
  }

  // 스크롤 탑 버튼 표시 (300px 이상 스크롤 시)
  if (scrollY >= 300) {
    scrollTopBtn.classList.remove('hidden');
  } else {
    scrollTopBtn.classList.add('hidden');
  }

  // 섹션 등장 애니메이션
  revealOnScroll();
});

// 스크롤 탑 버튼 클릭 → 맨 위로 이동
scrollTopBtn.addEventListener('click', () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
    /*
      window.scrollTo({ top: 0, behavior: 'smooth' }) :
      페이지 맨 위(top: 0)로 부드럽게(smooth) 스크롤.
      behavior: 'instant'으로 하면 즉시 이동.
    */
  });
});


/* =====================================================
   5. 스크롤 애니메이션 (Intersection Observer)

   요소가 화면에 들어올 때 페이드인+슬라이드업 효과.
   ===================================================== */

/*
  Intersection Observer API :
  요소가 뷰포트(화면)와 교차하는지(보이는지) 감지하는 API.
  스크롤 이벤트보다 성능이 훨씬 좋다.

  사용법:
  1. IntersectionObserver 생성 (콜백 함수 + 옵션 설정)
  2. 감시할 요소를 observer.observe(요소)로 등록
  3. 요소가 화면에 들어오면 콜백이 실행됨

  entries : 감시 중인 요소들의 상태 정보 배열.
  entry.isIntersecting : 요소가 현재 화면에 보이는지 여부 (true/false).
*/
/*
  스크롤 애니메이션 함수.
  스크롤할 때마다 animate-on-scroll 요소들의 위치를 확인하고
  화면 안에 들어온 요소에 visible 클래스를 추가한다.

  getBoundingClientRect() : 요소의 위치를 뷰포트 기준으로 반환한다.
  - rect.top : 요소 상단이 화면 상단으로부터 몇 px 아래에 있는지
  - window.innerHeight : 현재 브라우저 창의 높이(px)
  rect.top < window.innerHeight - 100 이면
  요소가 화면 하단에서 100px 위 지점까지 올라온 것 → 보이기 시작!
*/
function revealOnScroll() {
  const elements = document.querySelectorAll('.animate-on-scroll:not(.visible)');
  elements.forEach((el) => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight - 100) {
      el.classList.add('visible');
    }
  });
}

// 섹션들에 animate-on-scroll 클래스를 동적으로 추가
// Hero는 페이지 로드 시 바로 보이는 영역이므로 제외한다
document.querySelectorAll('.section').forEach((section) => {
  if (!section.classList.contains('hero')) {
    section.classList.add('animate-on-scroll');
  }
});

// 페이지 로드 직후 한 번 실행 (화면에 이미 보이는 요소 처리)
revealOnScroll();


/* =====================================================
   6. GitHub API 연동

   비동기 처리 패턴:
   [함수 호출] → [로딩 상태] → [API 요청]
   → 성공: [성공 상태 + 카드 렌더링]
   → 실패: [에러 상태 + 재시도 버튼]
   ===================================================== */

/*
  === 비동기(Asynchronous)란? ===

  동기(Synchronous) : 한 작업이 끝나야 다음 작업 시작. 순서 보장.
  비동기(Asynchronous) : 기다리는 동안 다른 작업 진행. 끝나면 콜백.

  API 요청처럼 시간이 걸리는 작업을 기다리는 동안
  다른 코드가 계속 실행된다.

  === async/await ===

  async : 함수 앞에 붙이면 비동기 함수가 된다.
          항상 Promise를 반환한다.

  await : async 함수 안에서만 사용 가능.
          Promise가 완료될 때까지 기다린다.
          동기 코드처럼 읽기 쉽게 만들어준다.

  === try/catch ===

  try   : 실행할 코드 (에러 발생 가능)
  catch : try에서 에러가 발생하면 실행되는 코드
  finally : 에러 여부와 상관없이 항상 실행 (선택)
*/

// GitHub 사용자명 설정 (본인 아이디로 변경!)
const GITHUB_USERNAME = 'linksat1';

// 현재 저장된 전체 프로젝트 데이터 (필터링에 사용)
let allRepos = [];
/*
  let으로 선언한 이유 : 나중에 API 응답 데이터로 재할당해야 하기 때문.
  const로 선언하면 재할당 불가.
*/

// 현재 선택된 필터
let currentFilter = 'all';


/*
  fetch() : HTTP 요청을 보내고 응답을 받는 Web API.
  Promise를 반환한다.

  GitHub API URL 형식:
  https://api.github.com/users/{사용자명}/repos
  → 사용자의 공개 저장소 목록을 JSON으로 반환.

  주의: 인증 없이는 시간당 60회 요청 제한(Rate Limit)이 있다.
*/

async function loadProjects() {
  // 상태 초기화: 에러/빈상태 숨기고, 로딩 표시
  showLoadingState();

  // 로딩 상태를 최소 1초 보여주기 위해 대기
  // (API가 너무 빠르면 로딩 상태가 눈에 띄지 않기 때문)
  await new Promise((resolve) => setTimeout(resolve, 1000));

  try {
    /*
      fetch(url) : URL로 GET 요청을 보낸다.
      await : 응답이 올 때까지 기다린다.
      response : 응답 객체 (아직 JSON이 아님!)
    */
    const response = await fetch(
      `https://api.github.com/users/${GITHUB_USERNAME}/repos?sort=updated&per_page=12`
      /*
        템플릿 리터럴(Template Literal) : 백틱(`)으로 감싸는 문자열.
        ${변수} 로 변수를 문자열 안에 삽입할 수 있다.
        여러 줄 문자열도 가능하다.

        쿼리 파라미터:
        ?sort=updated  : 최근 업데이트 순 정렬
        &per_page=12   : 최대 12개만 가져오기
      */
    );

    if (!response.ok) {
      /*
        response.ok : HTTP 상태 코드가 200~299이면 true, 그 외엔 false.
        403 : Rate Limit 초과
        404 : 사용자를 찾을 수 없음
        !response.ok : 정상 응답이 아니면 에러를 발생시킨다.
      */
      throw new Error(`HTTP 오류: ${response.status}`);
      /*
        throw new Error('메시지') : 직접 에러를 발생시킨다.
        이 에러는 catch 블록에서 처리된다.
      */
    }

    /*
      response.json() : 응답 본문을 JSON으로 파싱한다.
      이것도 비동기이므로 await 필요.
      결과는 JavaScript 객체(배열)가 된다.
    */
    const repos = await response.json();

    // 응답 데이터를 전역 변수에 저장 (필터링에 사용)
    allRepos = repos;

    if (repos.length === 0) {
      showEmptyState();
      return;
      /*
        return : 함수를 즉시 종료한다.
        이후 코드를 실행하지 않는다.
      */
    }

    renderProjects(repos);

  } catch (error) {
    /*
      catch(error) : try 블록에서 에러가 발생하면 실행.
      error : 발생한 에러 객체. error.message로 메시지 확인 가능.
    */
    console.error('프로젝트 로드 실패:', error);
    /*
      console.error() : 브라우저 개발자 도구 콘솔에 에러 메시지 출력.
      (F12 → Console 탭에서 확인)
      console.log() : 일반 로그
      console.warn() : 경고
    */
    showErrorState();
  }
}

// 재시도 버튼 클릭 이벤트
retryBtn.addEventListener('click', loadProjects);


/*
  프로젝트 카드를 화면에 렌더링하는 함수.

  매개변수(Parameter): repos (배열)
  repos : GitHub API에서 받은 저장소 데이터 배열.
*/
function renderProjects(repos) {
  // 로딩/에러/빈상태 요소들을 숨긴다.
  hideAllStates();

  /*
    Array.map() : 배열의 각 항목을 변환해 새 배열을 반환하는 메서드.

    repos.map((repo) => { return '...' })
    = repos 배열의 각 repo를 HTML 문자열로 변환한 새 배열 반환.

    Array.join('') : 배열의 모든 항목을 하나의 문자열로 합친다.
    join('') → 구분자 없이 합치기 (각 카드 사이에 아무것도 없음).
    join(', ') → 쉼표+공백으로 구분.
  */
  const cardsHTML = repos.map((repo) => {
    /*
      구조분해 할당(Destructuring Assignment) :
      객체의 속성을 변수로 꺼내는 문법.

      const { name, description, ... } = repo;
      = repo.name, repo.description 을 각각 name, description 변수로.
    */
    const {
      name,
      description,
      html_url,     /* GitHub 저장소 주소 */
      language,     /* 주 사용 언어 */
      stargazers_count,  /* 별표 수 */
      forks_count,       /* 포크 수 */
    } = repo;

    return `
      <article class="project-card animate-on-scroll" data-language="${language || ''}">
        <h3 class="project-card__title">
          <a href="${html_url}" target="_blank" rel="noopener noreferrer">
            ${name}
          </a>
        </h3>
        <p class="project-card__desc">
          ${description || '설명이 없습니다.'}
        </p>
        <div class="project-card__footer">
          <span class="project-card__lang">
            ${language ? `<i class="fa-solid fa-circle" style="color: ${getLangColor(language)}"></i> ${language}` : '언어 없음'}
          </span>
          <span class="project-card__stars">
            ⭐ ${stargazers_count}
            🍴 ${forks_count}
          </span>
        </div>
      </article>
    `;
    /*
      || (논리 OR 연산자) :
      왼쪽이 falsy(null, undefined, '', 0, false)이면 오른쪽 값을 사용.
      description || '설명이 없습니다.'
      = description이 있으면 description, 없으면 '설명이 없습니다.'
    */
  }).join('');

  /*
    innerHTML : 요소의 HTML 내용을 설정하거나 읽는다.
    cardsHTML 문자열이 실제 HTML 요소로 파싱되어 삽입된다.

    vs textContent : textContent는 텍스트만 삽입 (HTML 태그 무시).
    보안상 사용자 입력을 삽입할 때는 textContent를 사용하고
    신뢰할 수 있는 템플릿 문자열에는 innerHTML을 사용한다.
  */
  projectsGrid.innerHTML = cardsHTML;

  // 새로 생성된 카드에 스크롤 애니메이션 적용
  // 새로 생성된 카드에도 스크롤 애니메이션 적용
  revealOnScroll();
}

// 언어별 색상 반환 함수
function getLangColor(language) {
  const colors = {
    JavaScript: '#f7df1e',
    TypeScript: '#3178c6',
    Python: '#3776ab',
    HTML: '#e34f26',
    CSS: '#264de4',
    Java: '#b07219',
    'C++': '#f34b7d',
  };
  /*
    객체(Object) : 키-값 쌍의 집합.
    colors['JavaScript'] 또는 colors.JavaScript 로 접근.
    대괄호 표기법은 변수를 키로 사용할 때 유용하다.
  */
  return colors[language] || '#6b7280';
  /* 정의되지 않은 언어는 회색 반환 */
}


/*
  === 필터링 기능 (보너스 과제) ===

  Array.filter() : 조건에 맞는 항목만 남긴 새 배열을 반환.
  원본 배열은 변경되지 않는다.
*/
filterBtns.forEach((btn) => {
  btn.addEventListener('click', () => {
    // 모든 버튼에서 active 클래스 제거
    filterBtns.forEach((b) => b.classList.remove('active'));
    // 클릭한 버튼에 active 클래스 추가
    btn.classList.add('active');

    // data-filter 속성값 읽기
    currentFilter = btn.dataset.filter;
    /*
      dataset : data-* 속성에 접근하는 방법.
      data-filter="all" → element.dataset.filter === 'all'
      data-language="JavaScript" → element.dataset.language === 'JavaScript'
      kebab-case는 camelCase로 자동 변환된다.
      data-my-value → dataset.myValue
    */

    // 필터 적용
    if (currentFilter === 'all') {
      renderProjects(allRepos);
    } else {
      /*
        Array.filter() : 조건을 만족하는 항목만 남긴다.
        repo.language === currentFilter : 선택한 언어와 일치하는 저장소만.
      */
      const filtered = allRepos.filter(
        (repo) => repo.language === currentFilter
      );
      renderProjects(filtered);
    }
  });
});


/* 상태 관리 헬퍼 함수들 */
function showLoadingState() {
  projectsLoading.classList.remove('hidden');
  projectsError.classList.add('hidden');
  projectsEmpty.classList.add('hidden');
}

function showErrorState() {
  projectsLoading.classList.add('hidden');
  projectsError.classList.remove('hidden');
  projectsEmpty.classList.add('hidden');
}

function showEmptyState() {
  projectsLoading.classList.add('hidden');
  projectsError.classList.add('hidden');
  projectsEmpty.classList.remove('hidden');
}

function hideAllStates() {
  projectsLoading.classList.add('hidden');
  projectsError.classList.add('hidden');
  projectsEmpty.classList.add('hidden');
}


/* =====================================================
   7. 폼 유효성 검사

   상태 관리 패턴:
   [폼 제출] → [각 필드 검사] → 실패: [에러 표시]
                                → 성공: [성공 메시지]
   ===================================================== */

/*
  유효성 검사 함수
  매개변수: value (검사할 값), type (검사 유형)
  반환값: 에러 메시지 문자열 (유효하면 빈 문자열 '')
*/
function validateField(value, type) {
  const trimmed = value.trim();
  /*
    String.trim() : 문자열 앞뒤의 공백을 제거한다.
    '  박주선  '.trim() → '박주선'
    공백만 입력한 경우를 빈 값으로 처리하기 위해 사용.
  */

  if (trimmed === '') {
    return '필수 항목입니다.';
  }

  if (type === 'email') {
    /*
      정규표현식(Regular Expression, RegEx) :
      문자열 패턴을 표현하는 방법.
      /패턴/플래그 형식으로 작성한다.

      이메일 패턴: 문자@문자.문자 형식 검사.
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      - ^     : 문자열 시작
      - [^\s@]+ : 공백(\s)과 @가 아닌 문자 1개 이상
      - @     : @ 문자
      - \.    : . 문자 (일반 점, . 은 RegEx에서 '모든 문자'를 의미하므로 이스케이프)
      - $     : 문자열 끝

      RegEx.test(문자열) : 패턴과 일치하면 true, 아니면 false.
    */
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(trimmed)) {
      return '유효한 이메일 주소를 입력하세요.';
    }
  }

  if (type === 'message' && trimmed.length < 10) {
    /*
      String.length : 문자열의 길이(글자 수).
      'hello'.length → 5
    */
    return '메시지를 10자 이상 입력하세요.';
  }

  return ''; /* 유효함 → 에러 없음 */
}

/*
  에러 표시/초기화 헬퍼 함수.
  input : 입력 요소, errorEl : 에러 메시지 요소, message : 에러 내용
*/
function showError(input, errorEl, message) {
  input.classList.add('error');      /* 빨간 테두리 */
  errorEl.textContent = message;
  /*
    textContent : 요소의 텍스트 내용을 설정한다.
    innerHTML과 달리 HTML 태그를 텍스트 그대로 출력한다. (XSS 방지)
    사용자 입력을 화면에 표시할 때는 항상 textContent를 사용한다.
  */
}

function clearError(input, errorEl) {
  input.classList.remove('error');
  errorEl.textContent = '';
}

// 폼 제출 이벤트 처리
contactForm.addEventListener('submit', (event) => {
  /*
    event.preventDefault() :
    폼의 기본 동작(페이지 새로고침 + 서버 전송)을 막는다.
    우리가 JS로 직접 처리하기 위해 반드시 호출해야 한다.
  */
  event.preventDefault();

  // 각 입력 요소와 에러 요소 선택
  const nameInput = document.getElementById('name');
  const emailInput = document.getElementById('email');
  const messageInput = document.getElementById('message');
  const nameError = document.getElementById('name-error');
  const emailError = document.getElementById('email-error');
  const messageError = document.getElementById('message-error');

  // 유효성 검사 실행
  const nameMsg = validateField(nameInput.value, 'name');
  const emailMsg = validateField(emailInput.value, 'email');
  const messageMsg = validateField(messageInput.value, 'message');
  /*
    .value : input, textarea 요소의 현재 입력값을 문자열로 가져온다.
  */

  // 에러 표시
  if (nameMsg) showError(nameInput, nameError, nameMsg);
  else clearError(nameInput, nameError);

  if (emailMsg) showError(emailInput, emailError, emailMsg);
  else clearError(emailInput, emailError);

  if (messageMsg) showError(messageInput, messageError, messageMsg);
  else clearError(messageInput, messageError);

  // 모든 검사 통과 시 성공 처리
  if (!nameMsg && !emailMsg && !messageMsg) {
    /*
      !'' === true  : 빈 문자열은 falsy이므로 !''는 true.
      !nameMsg : 에러 메시지가 없으면(빈 문자열이면) true.
    */
    contactForm.classList.add('hidden');    /* 폼 숨기기 */
    formSuccess.classList.remove('hidden'); /* 성공 메시지 표시 */

    // 3초 후 폼을 다시 표시한다.
    setTimeout(() => {
      /*
        setTimeout(함수, 밀리초) :
        지정한 시간(밀리초, 1000ms = 1초) 후에 함수를 실행한다.
        비동기 함수이므로 다른 코드 실행을 막지 않는다.
      */
      contactForm.reset();
      /*
        form.reset() : 폼의 모든 입력값을 초기화한다.
        (빈 값으로 리셋)
      */
      contactForm.classList.remove('hidden');
      formSuccess.classList.add('hidden');
    }, 3000);
  }
});

// 실시간 유효성 검사 (입력 중 에러 메시지 즉시 업데이트)
['name', 'email', 'message'].forEach((fieldId) => {
  /*
    배열.forEach((항목) => { ... }) :
    배열의 각 항목에 대해 함수를 실행한다.
  */
  const input = document.getElementById(fieldId);
  const errorEl = document.getElementById(`${fieldId}-error`);

  input.addEventListener('input', () => {
    /*
      'input' 이벤트 : 사용자가 입력할 때마다 발생.
      'change' 이벤트와 달리 글자를 입력할 때마다 실시간으로 발생한다.
    */
    if (input.classList.contains('error')) {
      /* 에러 상태일 때만 실시간 검사 (처음 입력 시에는 검사 안 함) */
      const type = fieldId === 'email' ? 'email' : fieldId;
      const msg = validateField(input.value, type);
      if (msg) showError(input, errorEl, msg);
      else clearError(input, errorEl);
    }
  });
});


/* =====================================================
   8. 타이핑 효과 (보너스 과제)

   Hero 섹션에서 이름이 한 글자씩 타이핑되는 효과.
   ===================================================== */

const typingEl = document.getElementById('typing-text');
const texts = ['박주선', 'Web Developer', '열정적인 개발자'];
/*
  texts : 순서대로 타이핑할 문자열 배열.
  이 순서대로 반복되며 출력된다.
*/

let textIndex = 0;   /* 현재 표시 중인 텍스트의 배열 인덱스 */
let charIndex = 0;   /* 현재 표시 중인 글자 위치 */
let isDeleting = false; /* 삭제 중인지 여부 */

function typeEffect() {
  const currentText = texts[textIndex];
  /*
    배열[인덱스] : 배열에서 특정 위치의 값을 가져온다.
    texts[0] = '박주선', texts[1] = 'Web Developer', ...
    인덱스는 0부터 시작한다.
  */

  if (isDeleting) {
    /* 삭제 중: 글자를 한 개씩 줄인다 */
    charIndex--;
    /* charIndex-- : charIndex = charIndex - 1 의 단축 표현 */
  } else {
    /* 입력 중: 글자를 한 개씩 늘린다 */
    charIndex++;
  }

  /*
    String.slice(start, end) : 문자열의 일부를 잘라낸다.
    'hello'.slice(0, 3) → 'hel'  (0번째부터 3번째 직전까지)
    'hello'.slice(0, charIndex) → charIndex가 늘어날수록 더 많이 표시
  */
  typingEl.textContent = currentText.slice(0, charIndex);

  let speed = isDeleting ? 80 : 150;
  /*
    삭제할 때(80ms)가 입력할 때(150ms)보다 빠르다.
    자연스러운 타이핑 효과를 위해 속도를 다르게 설정.
  */

  if (!isDeleting && charIndex === currentText.length) {
    /* 타이핑 완료: 1.5초 대기 후 삭제 시작 */
    speed = 1500;
    isDeleting = true;
  } else if (isDeleting && charIndex === 0) {
    /* 삭제 완료: 다음 텍스트로 이동 */
    isDeleting = false;
    textIndex = (textIndex + 1) % texts.length;
    /*
      % (나머지 연산자, Modulo) :
      (textIndex + 1) % texts.length
      = 0, 1, 2, 0, 1, 2, 0, ... 순환
      texts.length = 3이면:
      0+1=1, 1%3=1 → 1번 텍스트
      1+1=2, 2%3=2 → 2번 텍스트
      2+1=3, 3%3=0 → 다시 0번 텍스트 (순환!)
    */
  }

  setTimeout(typeEffect, speed);
  /*
    재귀 호출 : 함수 안에서 자기 자신을 다시 호출하는 패턴.
    setTimeout으로 지연 호출하여 무한 루프 없이 반복 효과를 구현한다.
  */
}


/* =====================================================
   앱 초기화 (모든 설정이 완료된 후 실행)
   ===================================================== */

function init() {
  loadProjects();  /* GitHub 프로젝트 로드 */
  typeEffect();    /* 타이핑 효과 시작 */
}

/*
  앱을 시작한다.
  defer 속성으로 HTML이 다 로드된 후 실행되므로
  DOMContentLoaded 이벤트를 별도로 기다릴 필요가 없다.
*/
init();
