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
const contactForm  = document.getElementById('contact-form');
const formSuccess  = document.getElementById('form-success');
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
   6. 폼 유효성 검사
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
   7. 타이핑 효과 (보너스)
   Hero 섹션 이름(#typing-text)이 페이지 로드 시 한 글자씩 나타난다.
   핵심 제목(h1)은 정적 문장으로 항상 보이고, 타이핑 효과는
   보조 문구(이름)에만 적용해 JS 미실행 시에도 h1은 문제없이 보인다.
   ===================================================== */
function startTyping() {
  const el = document.getElementById('typing-text');
  const name = '박주선';
  let pos = 0;

  const timer = setInterval(() => {
    pos++;
    el.textContent = name.slice(0, pos);
    if (pos >= name.length) {
      clearInterval(timer);
    }
  }, 200);
}


/* =====================================================
   앱 초기화
   ===================================================== */
observeSections();
startTyping();
