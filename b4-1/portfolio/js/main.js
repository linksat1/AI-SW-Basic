"use strict";

/* =====================================================
   0. EmailJS 설정
   https://www.emailjs.com 가입 후 Email Services / Email Templates /
   Account > General 메뉴에서 아래 세 값을 발급받아 채워 넣는다.
   ===================================================== */
const EMAILJS_PUBLIC_KEY  = 'BFd7UNNYIBtiSa4ik';
const EMAILJS_SERVICE_ID  = 'service_6op40ej';
const EMAILJS_TEMPLATE_ID = 'template_qcs9wac';

if (typeof emailjs !== 'undefined') {
  emailjs.init({ publicKey: EMAILJS_PUBLIC_KEY });
}


/* =====================================================
   1. DOM 요소 선택
   ===================================================== */
const header      = document.getElementById('header');
const hamburger   = document.getElementById('hamburger');
const navMenu     = document.getElementById('nav-menu');
const themeToggle = document.getElementById('theme-toggle');
const themeIcon   = document.getElementById('theme-icon');
const scrollTopBtn = document.getElementById('scroll-top');
const projectsGrid = document.getElementById('projects-grid');
const contactForm  = document.getElementById('contact-form');
const formSuccess  = document.getElementById('form-success');
const filterBtns   = document.querySelectorAll('.filter-btn');
const root = document.documentElement;


/* =====================================================
   2. 다크 모드
   ===================================================== */
function getSavedTheme() {
  try {
    return localStorage.getItem('theme');
  } catch (err) {
    return null;
  }
}

function saveTheme(theme) {
  try {
    localStorage.setItem('theme', theme);
  } catch (err) {
    console.warn('테마 설정을 저장할 수 없습니다.', err);
  }
}

function applyTheme(isDark) {
  if (isDark) {
    root.setAttribute('data-theme', 'dark');
    themeIcon.className = 'fa-solid fa-sun';
  } else {
    root.setAttribute('data-theme', 'light');
    themeIcon.className = 'fa-solid fa-moon';
  }
  themeToggle.setAttribute('aria-pressed', String(isDark));
}

// 저장된 테마 불러오기
applyTheme(getSavedTheme() === 'dark');

// 토글 버튼 클릭
themeToggle.addEventListener('click', () => {
  const isDark = root.getAttribute('data-theme') === 'dark';
  applyTheme(!isDark);
  saveTheme(!isDark ? 'dark' : 'light');
});


/* =====================================================
   3. 햄버거 메뉴 (모바일)
   ===================================================== */
hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('active');
  navMenu.classList.toggle('active');
  const isOpen = navMenu.classList.contains('active');
  hamburger.setAttribute('aria-label', isOpen ? '메뉴 닫기' : '메뉴 열기');
});

navMenu.addEventListener('click', (e) => {
  if (e.target.classList.contains('nav__link')) {
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
  }
});


/* =====================================================
   4. 스크롤 이벤트
   ===================================================== */
window.addEventListener('scroll', () => {
  const y = window.scrollY;
  header.classList.toggle('scrolled', y >= 60);
  scrollTopBtn.classList.toggle('hidden', y < 300);
});

scrollTopBtn.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});


/* =====================================================
   5. 스크롤 애니메이션 (Intersection Observer)
   ===================================================== */
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target); // 한 번만 실행
      }
    });
  },
  { threshold: 0.2 }
);

function observeSections() {
  document.querySelectorAll('.section:not(.hero)').forEach((el) => {
    el.classList.add('animate-on-scroll');
    observer.observe(el);
  });
}


/* =====================================================
   6. GitHub API 연동
   ===================================================== */
const GITHUB_USERNAME = 'linksat1';
const REPOS_CACHE_KEY = `github-repos-${GITHUB_USERNAME}`;
const REPOS_CACHE_TIME = 10 * 60 * 1000;
const MIN_LOADING_TIME = 500;
let allRepos = [];
let currentFilter = 'all';

function setGridContent(html) {
  projectsGrid.innerHTML = html;
}

function showLoading() {
  setGridContent(`
    <div class="projects__loading">
      <div class="spinner"></div>
      <p>프로젝트를 불러오는 중...</p>
    </div>`);
}

function showError(status) {
  const message = status === 403
    ? 'GitHub API 요청 제한에 걸렸습니다. 잠시 후 다시 시도해주세요.'
    : '프로젝트를 불러올 수 없습니다.';

  setGridContent(`
    <div class="projects__error">
      <p>${message}</p>
      <button class="btn btn--primary" id="retry-btn">
        <i class="fa-solid fa-rotate-right"></i> 다시 시도
      </button>
    </div>`);
  document.getElementById('retry-btn').addEventListener('click', loadProjects);
}

function showEmpty() {
  setGridContent(`<div class="projects__empty"><p>표시할 프로젝트가 없습니다.</p></div>`);
}

function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  }[char]));
}

function getLangClass(lang) {
  const classes = {
    JavaScript: 'javascript', TypeScript: 'typescript', Python: 'python',
    HTML: 'html', CSS: 'css', Java: 'java', 'C++': 'cpp',
  };
  return classes[lang] || 'default';
}

function getCachedRepos() {
  try {
    // 선택 과제: sessionStorage 캐싱으로 같은 탭에서 GitHub API 요청을 줄임
    const cached = JSON.parse(sessionStorage.getItem(REPOS_CACHE_KEY));
    if (!cached || Date.now() - cached.savedAt > REPOS_CACHE_TIME) return null;
    return cached.repos;
  } catch (err) {
    return null;
  }
}

function cacheRepos(repos) {
  try {
    sessionStorage.setItem(REPOS_CACHE_KEY, JSON.stringify({
      savedAt: Date.now(),
      repos,
    }));
  } catch (err) {
    console.warn('프로젝트 캐시를 저장할 수 없습니다.', err);
  }
}

function wait(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

// 선택 과제: 프로젝트 언어별 필터링(filter() 사용)
function getFilteredRepos() {
  if (currentFilter === 'all') return allRepos;
  return allRepos.filter((repo) => repo.language === currentFilter);
}

function renderFilteredProjects() {
  renderProjects(getFilteredRepos());
}

function renderProjects(repos) {
  if (repos.length === 0) { showEmpty(); return; }

  setGridContent(
    repos.map(({ name, description, html_url, language, stargazers_count, forks_count }) => `
      <article class="project-card animate-on-scroll" data-language="${escapeHTML(language || '')}">
        <h3 class="project-card__title">
          <a href="${escapeHTML(html_url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(name)}</a>
        </h3>
        <p class="project-card__desc">${escapeHTML(description || '설명이 없습니다.')}</p>
        <div class="project-card__footer">
          <span class="project-card__lang">
            ${language
              ? `<i class="fa-solid fa-circle project-card__lang-dot project-card__lang-dot--${getLangClass(language)}"></i> ${escapeHTML(language)}`
              : '언어 없음'}
          </span>
          <span class="project-card__stars">⭐ ${escapeHTML(stargazers_count)} 🍴 ${escapeHTML(forks_count)}</span>
        </div>
      </article>`).join('')
  );

  // 새로 생성된 카드에 스크롤 애니메이션 적용
  document.querySelectorAll('.project-card.animate-on-scroll').forEach((card) => {
    observer.observe(card);
  });
}

async function loadProjects() {
  showLoading();
  await wait(MIN_LOADING_TIME);

  const cachedRepos = getCachedRepos();
  if (cachedRepos) {
    allRepos = cachedRepos;
    renderFilteredProjects();
    return;
  }

  try {
    const res = await fetch(
      `https://api.github.com/users/${GITHUB_USERNAME}/repos?sort=updated&per_page=12`
    );
    if (!res.ok) {
      const error = new Error(`HTTP ${res.status}`);
      error.status = res.status;
      throw error;
    }
    allRepos = await res.json();
    cacheRepos(allRepos);
    renderFilteredProjects();
  } catch (err) {
    console.warn('프로젝트 로드 실패:', err);
    showError(err.status);
  }
}

// 필터 버튼
filterBtns.forEach((btn) => {
  btn.addEventListener('click', () => {
    filterBtns.forEach((b) => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    renderFilteredProjects();
  });
});


/* =====================================================
   7. 폼 유효성 검사
   ===================================================== */
function validateField(value, type) {
  if (value.trim() === '') return '필수 항목입니다.';
  if (type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim()))
    return '유효한 이메일 주소를 입력하세요.';
  if (type === 'message' && value.trim().length < 10)
    return '메시지를 10자 이상 입력하세요.';
  return '';
}

function showFieldError(input, errorEl, msg) {
  input.classList.add('error');
  errorEl.textContent = msg;
}

function clearFieldError(input, errorEl) {
  input.classList.remove('error');
  errorEl.textContent = '';
}

contactForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const fields = [
    { id: 'name',    type: 'name' },
    { id: 'email',   type: 'email' },
    { id: 'message', type: 'message' },
  ];
  let valid = true;
  fields.forEach(({ id, type }) => {
    const input   = document.getElementById(id);
    const errorEl = document.getElementById(`${id}-error`);
    const msg     = validateField(input.value, type);
    if (msg) { showFieldError(input, errorEl, msg); valid = false; }
    else      { clearFieldError(input, errorEl); }
  });

  if (!valid) return;

  const submitBtn = contactForm.querySelector('button[type="submit"]');
  submitBtn.disabled = true;

  emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, {
    name:    document.getElementById('name').value,
    email:   document.getElementById('email').value,
    message: document.getElementById('message').value,
  })
    .then(() => {
      contactForm.classList.add('hidden');
      formSuccess.classList.remove('hidden');
      setTimeout(() => {
        contactForm.reset();
        contactForm.classList.remove('hidden');
        formSuccess.classList.add('hidden');
      }, 3000);
    })
    .catch((err) => {
      console.error('메일 전송 실패:', err);
      alert('메일 전송에 실패했습니다. 잠시 후 다시 시도해주세요.');
    })
    .finally(() => {
      submitBtn.disabled = false;
    });
});

['name', 'email', 'message'].forEach((id) => {
  const input   = document.getElementById(id);
  const errorEl = document.getElementById(`${id}-error`);
  input.addEventListener('input', () => {
    if (input.classList.contains('error')) {
      const msg = validateField(input.value, id);
      msg ? showFieldError(input, errorEl, msg) : clearFieldError(input, errorEl);
    }
  });
});


/* =====================================================
   8. 타이핑 + 문구 전환 효과 (보너스)
   Hero 섹션 문구를 3초 간격으로 번갈아 깜박이며 표시
   ===================================================== */
function startTyping() {
  const el = document.getElementById('typing-text');
  const phrases = ['저는 박주선입니다', '우주상황인식(SSA) 프로그램을 소개합니다'];
  let index = 0;

  const showPhrase = (text) => {
    el.textContent = text;
  };

  showPhrase(phrases[index]);

  setInterval(() => {
    /*
      hero__name--blink 클래스를 붙이면 CSS 전환으로 살짝 사라졌다가(깜박임),
      투명해진 순간(300ms 후) 다음 문구로 교체하고 다시 나타나게 한다.
    */
    el.classList.add('hero__name--blink');
    setTimeout(() => {
      index = (index + 1) % phrases.length;
      showPhrase(phrases[index]);
      el.classList.remove('hero__name--blink');
    }, 300);
  }, 3000);
}


/* =====================================================
   앱 초기화
   ===================================================== */
observeSections();
loadProjects();
startTyping();
