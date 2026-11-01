// B3-2 추가 과제 발표자료(PPTX) 생성 스크립트.
// 실행: NODE_PATH=<pptxgenjs·react-icons·sharp가 설치된 node_modules> node build_presentation.js <apply_theme.js 경로>
const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");

const { applyTheme } = require(process.argv[2]);
const OUT = path.join(__dirname, "AI코드설명도우미_과제설명.pptx");

const THEME = {
  name: "AI Code Desc",
  headFontFace: "Apple SD Gothic Neo",
  bodyFontFace: "Apple SD Gothic Neo",
  colors: {
    dk1: "16202A", lt1: "FFFFFF", dk2: "3A4A5A", lt2: "EEF4F2",
    accent1: "13A38B", accent2: "F2A93B", accent3: "E0604D",
    accent4: "4F7BD9", accent5: "8696A3", accent6: "0D6E5E",
    hlink: "13A38B", folHlink: "0D6E5E",
  },
};
const HEX = THEME.colors;
const MONO = "Menlo";
const FOOTER = "B3-2 추가 과제 · AI 코드 설명 도우미";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.title = "AI 코드 설명 도우미 과제 설명";
pres.author = "AI-SW-Basic";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

// ---------- 레이아웃 ----------
const footer = (dark) => [
  { text: { text: FOOTER, options: { x: 0.6, y: 6.95, w: 8, h: 0.3, fontSize: 10, color: dark ? C.accent5 : C.accent5, margin: 0 } } },
];
pres.defineSlideMaster({
  title: "TITLE", background: { color: HEX.dk1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.3, w: 11.7, h: 1.5, fontSize: 44, bold: true, align: "left", color: C.background1, valign: "bottom", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", align: "left", x: 0.8, y: 3.95, w: 11.7, h: 0.9, fontSize: 22, color: C.accent1, valign: "top", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "SECTION", background: { color: HEX.dk1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 2.6, y: 2.75, w: 9.9, h: 1.1, fontSize: 40, bold: true, align: "left", color: C.background1, valign: "middle", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", align: "left", x: 2.6, y: 3.9, w: 9.9, h: 0.8, fontSize: 18, color: C.accent5, valign: "top", margin: 0 }, text: "" } },
    ...footer(true),
  ],
  slideNumber: { x: 12.2, y: 6.95, w: 0.6, h: 0.3, fontSize: 10, color: C.accent5, align: "right" },
});
pres.defineSlideMaster({
  title: "CONTENT", background: { color: HEX.lt1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.85, fontSize: 32, bold: true, align: "left", color: C.text1, valign: "middle", margin: 0 }, text: "" } },
    ...footer(false),
  ],
  slideNumber: { x: 12.2, y: 6.95, w: 0.6, h: 0.3, fontSize: 10, color: C.accent5, align: "right" },
});
pres.defineSlideMaster({
  title: "CLOSING", background: { color: HEX.dk1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.85, fontSize: 32, bold: true, align: "left", color: C.background1, valign: "middle", margin: 0 }, text: "" } },
    ...footer(true),
  ],
  slideNumber: { x: 12.2, y: 6.95, w: 0.6, h: 0.3, fontSize: 10, color: C.accent5, align: "right" },
});

// ---------- 공통 도형 ----------
async function iconPng(Icon, hex) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Icon, { size: 256, color: "#" + hex }));
  const buf = await sharp(Buffer.from(svg)).resize(256, 256).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
const ICON_CACHE = {};
async function icon(name, hex = "FFFFFF") {
  const key = name + hex;
  if (!ICON_CACHE[key]) ICON_CACHE[key] = await iconPng(fa[name], hex);
  return ICON_CACHE[key];
}

// 모티프: 색 원 안의 아이콘
async function badge(slide, name, x, y, d, fill, id) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { type: "none" }, objectName: `${id}-circle` });
  const p = d * 0.26;
  slide.addImage({ data: await icon(name), x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p, objectName: `${id}-icon`, altText: name });
}
function card(slide, x, y, w, h, fill, id, shadow = true) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.12, fill: { color: fill }, line: { type: "none" }, objectName: id,
    shadow: shadow ? { type: "outer", color: "16202A", opacity: 0.12, blur: 8, offset: 2, angle: 90 } : undefined,
  });
}
function text(slide, t, o) {
  slide.addText(t, { isTextBox: true, margin: 0, valign: "top", fontSize: 16, color: C.text1, ...o });
}
// 모티프: 터미널 창
function terminal(slide, x, y, w, h, lines, id, fontSize = 12) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1, fill: { color: "0F161D" }, line: { type: "none" }, objectName: id,
    shadow: { type: "outer", color: "16202A", opacity: 0.2, blur: 10, offset: 3, angle: 90 } });
  ["E0604D", "F2A93B", "13A38B"].forEach((c, i) =>
    slide.addShape(pres.shapes.OVAL, { x: x + 0.22 + i * 0.22, y: y + 0.17, w: 0.13, h: 0.13, fill: { color: c }, line: { type: "none" }, objectName: `${id}-dot${i}` }));
  const runs = lines.map((l, i) => {
    const o = typeof l === "string" ? { text: l } : l;
    return { text: o.text, options: { color: o.color || "D6E2E8", bold: !!o.bold, breakLine: i < lines.length - 1 } };
  });
  slide.addText(runs, { isTextBox: true, x: x + 0.25, y: y + 0.45, w: w - 0.5, h: h - 0.6, fontFace: MONO, fontSize, margin: 0, valign: "top", paraSpaceAfter: 2, objectName: `${id}-text` });
}
function content(title, section) {
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: section });
  s.addText(title, { placeholder: "title" });
  return s;
}
function sectionSlide(num, title, sub, section) {
  pres.addSection({ title: section });
  const s = pres.addSlide({ masterName: "SECTION", sectionTitle: section });
  s.addShape(pres.shapes.OVAL, { x: 0.8, y: 2.65, w: 1.4, h: 1.4, fill: { color: HEX.accent1 }, line: { type: "none" }, objectName: "section-num-circle" });
  s.addText(String(num), { isTextBox: true, x: 0.8, y: 2.65, w: 1.4, h: 1.4, fontSize: 48, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, objectName: "section-num" });
  s.addText(title, { placeholder: "title" });
  s.addText(sub, { placeholder: "body" });
  return s;
}

// pptxgenjs는 테마의 동아시아(ea) 글꼴을 비워 두므로 한글 글꼴을 명시한다.
async function setEastAsianFont(file, face) {
  const fs = require("fs");
  const JSZip = require(require.resolve("jszip", { paths: [require.resolve("pptxgenjs")] }));
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const part = "ppt/theme/theme1.xml";
  const xml = await zip.file(part).async("string");
  zip.file(part, xml.replace(/<a:ea typeface=""\/>/g, `<a:ea typeface="${face}"/>`));
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

async function build() {
  // 1. 표지
  pres.addSection({ title: "시작" });
  let s = pres.addSlide({ masterName: "TITLE", sectionTitle: "시작" });
  await badge(s, "FaRobot", 0.8, 1.05, 1.0, HEX.accent1, "cover-badge");
  s.addText("내가 고친 코드, AI가 설명해 줍니다", { placeholder: "title" });
  s.addText("B3-2 추가 과제 · AI 코드 설명 도우미 만들기", { placeholder: "body" });
  text(s, "과제 내용  →  실행 방법  →  결과", { x: 0.8, y: 5.3, w: 8, h: 0.4, fontSize: 16, color: C.accent5, objectName: "cover-path" });
  s.addNotes("오늘은 B3-2 추가 과제인 'AI 코드 설명 도우미'를 소개합니다. 과제가 무엇이었는지, 어떻게 만들고 실행했는지, 결과가 어땠는지 세 부분으로 나눠 설명하겠습니다. 프로그래밍을 처음 접하는 분도 따라올 수 있게 용어부터 풀어서 설명하겠습니다.");

  // 2. 한눈에 보기
  s = content("한 장으로 보는 과제", "시작");
  const overview = [
    ["FaClipboardList", HEX.accent1, "무엇을", "코드를 고친 뒤 '무엇을 왜 바꿨는지' 쓰는 설명문을 AI가 대신 써 주는 터미널 프로그램 만들기"],
    ["FaTerminal", HEX.accent4, "어떻게", "Git에서 바뀐 내용을 모으고, 민감정보를 가린 뒤, Claude AI에 보내 정해진 형식의 설명문을 받기"],
    ["FaCheckCircle", HEX.accent2, "결과", "실제 AI로 설명문 생성 성공, 자동 테스트 27개 통과, 보너스 과제 3개 모두 완료"],
  ];
  for (let i = 0; i < 3; i++) {
    const [ic, col, h, body] = overview[i];
    const x = 0.6 + i * 4.1;
    card(s, x, 1.65, 3.8, 3.5, HEX.lt2, `overview-card-${i}`, false);
    await badge(s, ic, x + 0.35, 2.0, 0.9, col, `overview-${i}`);
    text(s, h, { x: x + 0.35, y: 3.15, w: 3.1, h: 0.55, fontSize: 24, bold: true, objectName: `overview-h-${i}` });
    text(s, body, { x: x + 0.35, y: 3.8, w: 3.1, h: 1.2, fontSize: 16, color: C.text2, objectName: `overview-body-${i}` });
  }
  text(s, "발표 순서", { x: 0.6, y: 5.6, w: 2, h: 0.5, fontSize: 18, bold: true, valign: "middle", objectName: "order-h" });
  ["과제 내용", "실행 방법", "결과"].forEach((t, i) => {
    const x = 2.4 + i * 3.4;
    s.addShape(pres.shapes.OVAL, { x, y: 5.6, w: 0.5, h: 0.5, fill: { color: HEX.accent1 }, line: { type: "none" }, objectName: `order-circle-${i}` });
    text(s, String(i + 1), { x, y: 5.6, w: 0.5, h: 0.5, fontSize: 16, bold: true, color: C.background1, align: "center", valign: "middle", objectName: `order-n-${i}` });
    text(s, t, { x: x + 0.65, y: 5.6, w: 2.2, h: 0.5, fontSize: 18, valign: "middle", objectName: `order-t-${i}` });
    if (i < 2) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 2.65, y: 5.72, w: 0.4, h: 0.26, fill: { color: HEX.accent5 }, line: { type: "none" }, objectName: `order-arrow-${i}` });
  });
  s.addNotes("이 한 장이 발표 전체의 요약입니다. 첫째, 무엇을 만들었나: 코드를 고친 다음 '무엇을, 왜 바꿨는지' 쓰는 설명문을 AI가 대신 써 주는 프로그램입니다. 둘째, 어떻게: Git이라는 도구에서 바뀐 내용을 모으고, 비밀번호 같은 민감정보를 가린 뒤 AI에게 보냅니다. 셋째, 결과: 실제 AI로 설명문을 만드는 데 성공했고, 자동 테스트 27개가 모두 통과했으며, 보너스 과제 3개도 모두 했습니다.");

  // ===== 1장. 과제 내용 =====
  sectionSlide(1, "과제는 무엇이었나", "왜 필요한지, 꼭 알아야 할 개념, 요구사항", "1. 과제 내용");

  // 4. 왜 필요한가
  s = content("왜 이런 도구가 필요할까", "1. 과제 내용");
  card(s, 0.6, 1.6, 5.8, 3.3, HEX.lt2, "why-before", false);
  await badge(s, "FaTired", 0.95, 1.95, 0.8, HEX.accent3, "why-before");
  text(s, "지금까지", { x: 1.95, y: 2.1, w: 4, h: 0.5, fontSize: 22, bold: true, objectName: "why-before-h" });
  text(s, [
    { text: "코드를 고친 뒤 리뷰어에게 보낼 설명을 직접 씁니다", options: { bullet: true, breakLine: true } },
    { text: "바뀐 파일이 많으면 빠뜨리기 쉽습니다", options: { bullet: true, breakLine: true } },
    { text: "사람마다 형식이 달라 읽기 어렵습니다", options: { bullet: true } },
  ], { x: 0.95, y: 3.0, w: 5.1, h: 1.7, color: C.text2, paraSpaceAfter: 10, objectName: "why-before-list" });
  card(s, 6.9, 1.6, 5.8, 3.3, "E3F4F0", "why-after", false);
  await badge(s, "FaMagic", 7.25, 1.95, 0.8, HEX.accent1, "why-after");
  text(s, "이 도구를 쓰면", { x: 8.25, y: 2.1, w: 4, h: 0.5, fontSize: 22, bold: true, objectName: "why-after-h" });
  text(s, [
    { text: "명령 한 줄로 설명 초안이 나옵니다", options: { bullet: true, breakLine: true } },
    { text: "바뀐 내용(diff)을 근거로 쓰니 빠뜨림이 줄어듭니다", options: { bullet: true, breakLine: true } },
    { text: "항상 같은 4칸 형식이라 읽기 쉽습니다", options: { bullet: true } },
  ], { x: 7.25, y: 3.0, w: 5.1, h: 1.7, color: C.text2, paraSpaceAfter: 10, objectName: "why-after-list" });
  card(s, 0.6, 5.25, 12.1, 1.3, "FDF1DE", "why-key", false);
  await badge(s, "FaLightbulb", 0.9, 5.47, 0.85, HEX.accent2, "why-key");
  text(s, [
    { text: "핵심 메시지  ", options: { bold: true, color: C.text1 } },
    { text: "AI에게 무엇을 보여 주느냐가 결과를 결정합니다. 그래서 바뀐 내용(diff), 수정 의도, 원하는 형식을 함께 보냅니다.", options: { color: C.text2 } },
  ], { x: 2.0, y: 5.4, w: 10.4, h: 1.0, fontSize: 17, valign: "middle", objectName: "why-key-text" });
  s.addNotes("개발자는 코드를 고친 뒤 동료에게 '무엇을 왜 바꿨는지' 설명을 써서 보냅니다. 이 과정이 귀찮고, 바뀐 파일이 많으면 빠뜨리기 쉽고, 사람마다 쓰는 형식도 다릅니다. 이 도구를 쓰면 명령 한 줄로 초안이 나오고, 실제로 바뀐 내용을 근거로 쓰기 때문에 빠뜨림이 줄고, 항상 같은 형식으로 나옵니다. 과제의 핵심 메시지는 'AI에게 무엇을 보여주느냐가 결과를 결정한다'는 것입니다.");

  // 5. 개념
  s = content("먼저 알아야 할 개념 4가지", "1. 과제 내용");
  const concepts = [
    ["FaCodeBranch", HEX.accent6, "Git · git status · git diff", "Git은 코드 변경 기록 도구입니다. status는 '어떤 파일이 바뀌었나', diff는 '어떤 줄이 어떻게 바뀌었나'를 보여 줍니다."],
    ["FaCloud", HEX.accent4, "AI API", "프로그램이 인터넷으로 AI에게 질문을 보내고 답을 받는 창구입니다. 이 과제는 Anthropic의 Claude를 씁니다."],
    ["FaKey", HEX.accent2, "API Key와 환경변수", "API Key는 AI 창구의 출입증입니다. 코드에 적으면 유출되므로 컴퓨터의 '환경변수'에만 넣어 둡니다."],
    ["FaCommentDots", HEX.accent1, "프롬프트", "AI에게 보내는 질문지입니다. 바뀐 내용, 수정 의도, 원하는 출력 형식을 함께 적어 보냅니다."],
  ];
  for (let i = 0; i < 4; i++) {
    const [ic, col, h, body] = concepts[i];
    const x = 0.6 + (i % 2) * 6.2, y = 1.55 + Math.floor(i / 2) * 2.6;
    await badge(s, ic, x, y + 0.05, 0.85, col, `concept-${i}`);
    text(s, h, { x: x + 1.1, y, w: 4.8, h: 0.5, fontSize: 20, bold: true, objectName: `concept-h-${i}` });
    text(s, body, { x: x + 1.1, y: y + 0.6, w: 4.8, h: 1.7, fontSize: 15, color: C.text2, objectName: `concept-body-${i}` });
  }
  s.addNotes("네 가지 개념만 알면 나머지가 쉬워집니다. Git은 코드 변경 기록 도구이고, git status는 바뀐 파일 목록, git diff는 바뀐 줄을 보여 줍니다. AI API는 프로그램이 인터넷으로 AI에게 질문하고 답을 받는 창구입니다. API Key는 그 창구의 출입증이라 코드에 적으면 안 되고 환경변수라는 곳에 넣어 둡니다. 프롬프트는 AI에게 보내는 질문지입니다.");

  // 6. 요구사항
  s = content("과제가 요구한 것", "1. 과제 내용");
  const reqs = [
    ["FaCodeBranch", "Git 변경 수집", "status·diff 수집, 변경 없으면 안내 후 종료"],
    ["FaUserEdit", "수정 의도 입력", "옵션(--intent) 또는 대화식 입력"],
    ["FaCloud", "AI API 연동", "Key는 환경변수, 실패 원인 출력, 파라미터 옵션"],
    ["FaFileAlt", "설명문 생성", "제목 1줄 + 4개 섹션 템플릿"],
    ["FaRulerHorizontal", "형식 검증", "제목 72자 이하, 섹션마다 불릿 1개 이상"],
    ["FaShieldAlt", "안전 모드", "민감정보 가리기, 전송량 제한"],
  ];
  for (let i = 0; i < 6; i++) {
    const [ic, h, body] = reqs[i];
    const x = 0.6 + (i % 3) * 4.1, y = 1.55 + Math.floor(i / 3) * 2.2;
    card(s, x, y, 3.8, 1.95, HEX.lt2, `req-card-${i}`, false);
    await badge(s, ic, x + 0.3, y + 0.3, 0.7, HEX.accent1, `req-${i}`);
    text(s, h, { x: x + 1.2, y: y + 0.35, w: 2.4, h: 0.5, fontSize: 18, bold: true, objectName: `req-h-${i}` });
    text(s, body, { x: x + 0.3, y: y + 1.1, w: 3.3, h: 0.75, fontSize: 14, color: C.text2, objectName: `req-body-${i}` });
  }
  text(s, [
    { text: "제출물: ", options: { bold: true, color: C.text1 } },
    { text: "GitHub 저장소 + 사용 가이드(README.md)   ·   보너스: 실제 저장소 적용, 팀 컨벤션, 안전 모드 고도화", options: { color: C.text2 } },
  ], { x: 0.6, y: 6.15, w: 12.1, h: 0.4, fontSize: 15, objectName: "req-submit" });
  s.addNotes("과제 문서의 요구사항을 여섯 묶음으로 정리했습니다. Git 변경 수집, 수정 의도 입력, AI API 연동, 설명문 생성, 형식 검증, 안전 모드입니다. 여기에 GitHub 저장소와 README 사용 가이드를 제출해야 하고, 선택 과제로 보너스 3개가 있습니다.");

  // 7. 결과물 형식
  s = content("AI가 써야 하는 설명문의 모양", "1. 과제 내용");
  terminal(s, 0.6, 1.55, 6.6, 5.0, [
    { text: "--- Description Title ---", color: "8696A3" },
    { text: "feat: 사용자 세션 처리 보완", color: "F2A93B", bold: true },
    "",
    { text: "--- Description Body ---", color: "8696A3" },
    { text: "## Summary", color: "13A38B", bold: true },
    "- 로그인 흐름이 안정적으로 동작합니다.",
    { text: "## What Changed", color: "13A38B", bold: true },
    "- session.py에 예외 처리를 추가했습니다.",
    { text: "## Why It Was Needed", color: "13A38B", bold: true },
    "- 빈 입력에도 세션이 만들어졌습니다.",
    { text: "## How to Verify", color: "13A38B", bold: true },
    "- 빈 문자열로 로그인해 오류를 확인합니다.",
  ], "format-term", 13);
  const fmt = [
    ["제목 1줄", "50자 이내 권장, 최대 72자"],
    ["Summary", "한 줄 요약"],
    ["What Changed", "무엇이 바뀌었나 (파일 1~3개 언급)"],
    ["Why It Was Needed", "왜 바꿔야 했나"],
    ["How to Verify", "리뷰어가 어떻게 확인하나"],
  ];
  fmt.forEach(([h, b], i) => {
    const y = 1.6 + i * 0.98;
    text(s, h, { x: 7.7, y, w: 5, h: 0.42, fontSize: 18, bold: true, color: i === 0 ? C.accent2 : C.accent6, objectName: `fmt-h-${i}` });
    text(s, b, { x: 7.7, y: y + 0.43, w: 5, h: 0.4, fontSize: 15, color: C.text2, objectName: `fmt-b-${i}` });
  });
  s.addNotes("AI가 아무렇게나 쓰면 쓸모가 없기 때문에, 과제는 형식을 정해 두었습니다. 제목은 한 줄이고 50자 이내를 권장하며 72자를 넘으면 안 됩니다. 본문은 Summary, What Changed, Why It Was Needed, How to Verify 네 칸이고, 칸마다 '-'로 시작하는 항목이 하나 이상 있어야 합니다. 이 형식이 지켜졌는지 프로그램이 직접 검사합니다.");

  // ===== 2장. 실행 =====
  sectionSlide(2, "어떻게 만들고 실행했나", "전체 흐름, 프로그램 구조, 실행 방법, 안전장치", "2. 실행 방법");

  // 9. 전체 흐름
  s = content("명령 한 줄 뒤에서 일어나는 6단계", "2. 실행 방법");
  const flow = [
    ["FaCodeBranch", "① 수집", "git status\ngit diff"],
    ["FaUserEdit", "② 의도 입력", "무엇을 왜\n고쳤는지"],
    ["FaShieldAlt", "③ 안전 모드", "비밀값 가리기\n양 줄이기"],
    ["FaCloud", "④ AI 호출", "Claude에게\n질문 보내기"],
    ["FaRulerHorizontal", "⑤ 검증", "형식 검사\n필요 시 재요청"],
    ["FaTerminal", "⑥ 출력", "터미널에\n설명문 표시"],
  ];
  for (let i = 0; i < 6; i++) {
    const [ic, h, b] = flow[i];
    const x = 0.6 + i * 2.05;
    await badge(s, ic, x + 0.45, 2.0, 1.0, i === 3 ? HEX.accent2 : HEX.accent1, `flow-${i}`);
    if (i < 5) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 1.6, y: 2.35, w: 0.35, h: 0.3, fill: { color: HEX.accent5 }, line: { type: "none" }, objectName: `flow-arrow-${i}` });
    text(s, h, { x, y: 3.25, w: 1.9, h: 0.45, fontSize: 18, bold: true, align: "center", objectName: `flow-h-${i}` });
    text(s, b, { x, y: 3.75, w: 1.9, h: 0.8, fontSize: 14, color: C.text2, align: "center", objectName: `flow-b-${i}` });
  }
  terminal(s, 0.6, 4.95, 12.1, 1.6, [
    { text: "$ python3 b3-2_추가/main.py describe --safe-mode --intent \"로그인 예외 처리를 보완했다\"", color: "F2A93B" },
    { text: "[INFO] Git status 수집 완료: 3개 파일 변경 감지   ·   [INFO] AI API 요청 중...   ·   [DONE] 코드 설명 생성 완료", color: "D6E2E8" },
  ], "flow-term", 13);
  s.addNotes("사용자는 describe 명령 한 줄만 입력합니다. 그 뒤에서 여섯 단계가 자동으로 진행됩니다. 1단계 Git에서 바뀐 내용을 모으고, 2단계 사용자가 수정 의도를 입력하고, 3단계 비밀번호 같은 값을 가리고, 4단계 AI에게 보내고, 5단계 받은 답이 형식에 맞는지 검사하고, 6단계 터미널에 보여 줍니다. 각 단계마다 [INFO] 로그가 찍혀서 지금 어디까지 왔는지 알 수 있습니다.");

  // 10. 프로그램 구조
  s = content("프로그램은 역할별로 6개 파일로 나눴습니다", "2. 실행 방법");
  const mods = [
    ["cli.py", "지휘자", "6단계 순서를 조립하고 옵션을 받습니다"],
    ["git_context.py", "수집 담당", "git status·diff를 실행해 변경 내용을 모읍니다"],
    ["safe_mode.py", "보안 담당", "비밀값을 가리고 보낼 양을 줄입니다"],
    ["ai_client.py", "통신 담당", "Claude API를 호출하고 오류를 해석합니다"],
    ["generator.py", "편집 담당", "질문지를 만들고 답을 검사·정리합니다"],
    ["convention.py", "규칙 담당", "팀별 작성 규칙 파일을 읽습니다"],
  ];
  for (let i = 0; i < 6; i++) {
    const [f, role, b] = mods[i];
    const x = 0.6 + (i % 2) * 6.2, y = 1.55 + Math.floor(i / 2) * 1.65;
    card(s, x, y, 5.9, 1.4, i === 0 ? "E3F4F0" : HEX.lt2, `mod-card-${i}`, false);
    text(s, [{ text: f, options: { fontFace: MONO, bold: true, color: C.accent6 } }, { text: `   ${role}`, options: { bold: true, color: C.text1 } }],
      { x: x + 0.3, y: y + 0.2, w: 5.3, h: 0.45, fontSize: 17, objectName: `mod-h-${i}` });
    text(s, b, { x: x + 0.3, y: y + 0.72, w: 5.3, h: 0.5, fontSize: 15, color: C.text2, objectName: `mod-b-${i}` });
  }
  s.addNotes("프로그램을 한 파일에 몰아 쓰지 않고 역할별로 나눴습니다. cli.py가 지휘자 역할로 전체 순서를 조립합니다. git_context.py는 변경 수집, safe_mode.py는 보안, ai_client.py는 AI와의 통신, generator.py는 질문지 작성과 답 검사, convention.py는 팀 규칙 파일 읽기를 맡습니다. 이렇게 나누면 고칠 곳을 찾기 쉽고 하나씩 테스트할 수 있습니다.");

  // 11. 실행 방법
  s = content("직접 실행하는 방법: 3단계", "2. 실행 방법");
  const steps = [
    ["1", "설치", "AI 라이브러리를 설치합니다", "python3 -m pip install -r requirements.txt"],
    ["2", "API Key 설정", "출입증을 환경변수에 넣습니다 (화면에 안 보이게)", "read -s AI_API_KEY && export AI_API_KEY"],
    ["3", "실행", "Git 저장소 맨 위 폴더에서 실행합니다", "python3 b3-2_추가/main.py describe --safe-mode"],
  ];
  steps.forEach(([n, h, b, cmd], i) => {
    const y = 1.55 + i * 1.6;
    s.addShape(pres.shapes.OVAL, { x: 0.6, y: y + 0.1, w: 0.8, h: 0.8, fill: { color: HEX.accent1 }, line: { type: "none" }, objectName: `step-circle-${i}` });
    text(s, n, { x: 0.6, y: y + 0.1, w: 0.8, h: 0.8, fontSize: 26, bold: true, color: C.background1, align: "center", valign: "middle", objectName: `step-n-${i}` });
    text(s, h, { x: 1.7, y: y + 0.05, w: 3.6, h: 0.45, fontSize: 20, bold: true, objectName: `step-h-${i}` });
    text(s, b, { x: 1.7, y: y + 0.55, w: 3.6, h: 0.75, fontSize: 14, color: C.text2, objectName: `step-b-${i}` });
    terminal(s, 5.5, y, 7.2, 1.3, [{ text: "$ " + cmd, color: "F2A93B" }], `step-term-${i}`, 14);
  });
  text(s, [
    { text: "API 없이 연습하기  ", options: { bold: true, color: C.accent6 } },
    { text: "--mock: 가짜 응답으로 흐름만 확인   ·   --dry-run: AI에 보낼 질문지만 미리 보기 (둘 다 비용 0원)", options: { color: C.text2 } },
  ], { x: 0.6, y: 6.35, w: 12.1, h: 0.4, fontSize: 15, objectName: "step-tip" });
  s.addNotes("직접 실행하는 방법은 세 단계입니다. 첫째, requirements.txt로 AI 라이브러리를 설치합니다. 둘째, API Key를 환경변수에 넣습니다. read -s를 쓰면 입력한 키가 화면에 보이지 않습니다. 셋째, Git 저장소의 맨 위 폴더에서 describe 명령을 실행합니다. API Key가 없어도 --mock으로 가짜 응답을 써서 흐름을 확인할 수 있고, --dry-run으로 AI에 보낼 질문지를 미리 볼 수 있습니다.");

  // 12. 파라미터
  s = content("AI 답을 조절하는 손잡이: 파라미터", "2. 실행 방법");
  const params = [
    ["FaMicrochip", HEX.accent4, "--model", "어떤 AI 모델을 쓸지", "기본 claude-opus-5-5"],
    ["FaBrain", HEX.accent1, "--effort", "답하기 전에 얼마나 깊이 생각할지", "기본 low (요약엔 충분)"],
    ["FaRulerVertical", HEX.accent2, "--max-tokens", "답의 최대 길이 (생각한 양 포함)", "기본 16000"],
    ["FaThermometerHalf", HEX.accent3, "--temperature", "답의 무작위성 (높을수록 다양)", "현재 API는 받지 않음"],
  ];
  for (let i = 0; i < 4; i++) {
    const [ic, col, h, b, d] = params[i];
    const x = 0.6 + i * 3.1;
    card(s, x, 1.55, 2.85, 3.9, HEX.lt2, `param-card-${i}`, false);
    await badge(s, ic, x + 0.3, 1.85, 0.8, col, `param-${i}`);
    text(s, h, { x: x + 0.3, y: 2.85, w: 2.4, h: 0.45, fontSize: 18, bold: true, fontFace: MONO, objectName: `param-h-${i}` });
    text(s, b, { x: x + 0.3, y: 3.4, w: 2.35, h: 1.1, fontSize: 15, color: C.text2, objectName: `param-b-${i}` });
    text(s, d, { x: x + 0.3, y: 4.6, w: 2.35, h: 0.6, fontSize: 13, bold: true, color: i === 3 ? C.accent3 : C.accent6, objectName: `param-d-${i}` });
  }
  card(s, 0.6, 5.7, 12.1, 0.95, "FDF1DE", "param-note", false);
  text(s, "알게 된 점: 과제 예시의 temperature는 최신 API에서 지원이 끝났습니다. 그래서 기본은 보내지 않고, 같은 역할을 effort로 대신합니다.",
    { x: 0.9, y: 5.85, w: 11.5, h: 0.7, fontSize: 15, color: C.text1, valign: "middle", objectName: "param-note-text" });
  s.addNotes("파라미터는 AI 답을 조절하는 손잡이입니다. model은 어떤 AI를 쓸지, effort는 답하기 전에 얼마나 깊이 생각할지, max-tokens는 답의 최대 길이입니다. 최신 모델은 생각한 양도 이 길이에 포함되기 때문에 너무 작게 잡으면 답이 잘립니다. 과제 예시에 나온 temperature는 답의 무작위성을 정하는 값인데, 현재 API 버전에서는 더 이상 받지 않습니다. 그래서 기본으로는 보내지 않고 effort로 품질을 조절했습니다. 과제 문서와 실제 API가 다를 때 확인하고 근거를 남긴 사례입니다.");

  // 13. safe-mode
  s = content("안전 모드: 비밀은 가리고, 양은 줄이고", "2. 실행 방법");
  text(s, "끄면 (OFF)", { x: 0.6, y: 1.5, w: 5.9, h: 0.45, fontSize: 18, bold: true, color: C.accent3, objectName: "safe-off-h" });
  terminal(s, 0.6, 2.0, 5.9, 2.1, [
    { text: "+API_KEY = \"sk-ant-api03-abcd...\"", color: "F2A93B" },
    { text: "+ADMIN_EMAIL = \"admin@example.com\"", color: "F2A93B" },
    { text: "+SUPPORT_PHONE = \"010-1234-5678\"", color: "F2A93B" },
  ], "safe-off", 13);
  text(s, "켜면 (ON)", { x: 6.8, y: 1.5, w: 5.9, h: 0.45, fontSize: 18, bold: true, color: C.accent1, objectName: "safe-on-h" });
  terminal(s, 6.8, 2.0, 5.9, 2.1, [
    { text: "+API_KEY = \"[MASKED_ANTHROPIC_KEY]\"", color: "13A38B" },
    { text: "+ADMIN_EMAIL = \"[MASKED_EMAIL]\"", color: "13A38B" },
    { text: "+SUPPORT_PHONE = \"[MASKED_PHONE]\"", color: "13A38B" },
  ], "safe-on", 13);
  const stats = [["10개", "보내는 최대 파일 수"], ["200줄", "보내는 최대 diff 줄 수"], ["7종+", "가리는 패턴 (키·토큰·이메일·전화 등)"]];
  stats.forEach(([n, l], i) => {
    const x = 0.6 + i * 4.1;
    text(s, n, { x, y: 4.5, w: 3.8, h: 1.0, fontSize: 54, bold: true, color: C.accent6, objectName: `safe-stat-${i}` });
    text(s, l, { x, y: 5.55, w: 3.8, h: 0.5, fontSize: 15, color: C.text2, objectName: `safe-stat-l-${i}` });
  });
  text(s, "기준은 --max-files, --max-diff-lines, --mask-pattern 옵션으로 바꿀 수 있습니다. (화면 속 키는 시연용 가짜 값)",
    { x: 0.6, y: 6.2, w: 12.1, h: 0.4, fontSize: 13, color: C.accent5, objectName: "safe-note" });
  s.addNotes("git diff에는 실수로 넣은 API Key나 이메일, 전화번호가 섞여 있을 수 있습니다. 그대로 AI 회사 서버로 보내면 정보가 밖으로 나가게 됩니다. 안전 모드를 켜면 보내기 전에 이런 값을 [MASKED]로 바꿉니다. 또 한 번에 최대 10개 파일, 200줄까지만 보내서 비용과 노출을 줄입니다. 기준 숫자와 가릴 패턴은 옵션으로 바꿀 수 있습니다. 화면의 키는 시연용 가짜 값입니다.");

  // 14. 검증
  s = content("AI 답이 형식에 안 맞으면?", "2. 실행 방법");
  const vflow = [
    ["FaBroom", HEX.accent5, "정리", "### Summary, * 불릿 같은 표기 차이를 표준 형식으로 맞춤"],
    ["FaSearch", HEX.accent4, "검사", "제목 72자 이하? 4개 섹션? 섹션마다 불릿?"],
    ["FaRedo", HEX.accent2, "1회 재요청", "틀린 점을 알려 주고 한 번만 다시 요청"],
    ["FaTools", HEX.accent1, "후처리 보정", "그래도 틀리면 제목 자르기, 빈 섹션에 '직접 작성' 표시"],
  ];
  for (let i = 0; i < 4; i++) {
    const [ic, col, h, b] = vflow[i];
    const x = 0.6 + i * 3.1;
    card(s, x, 1.55, 2.85, 3.35, HEX.lt2, `v-card-${i}`, false);
    await badge(s, ic, x + 0.3, 1.85, 0.8, col, `v-${i}`);
    text(s, h, { x: x + 0.3, y: 2.85, w: 2.4, h: 0.45, fontSize: 19, bold: true, objectName: `v-h-${i}` });
    text(s, b, { x: x + 0.3, y: 3.4, w: 2.35, h: 1.4, fontSize: 14, color: C.text2, objectName: `v-b-${i}` });
    if (i < 3) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 2.88, y: 3.05, w: 0.2, h: 0.3, fill: { color: HEX.accent5 }, line: { type: "none" }, objectName: `v-arrow-${i}` });
  }
  text(s, "최대 2회", { x: 0.6, y: 5.15, w: 3.5, h: 1.0, fontSize: 54, bold: true, color: C.accent2, objectName: "v-stat" });
  text(s, "1회 실행당 AI 호출 횟수 상한. 비용을 예측할 수 있고, 호출 횟수는 매번 화면에 표시됩니다.",
    { x: 4.2, y: 5.35, w: 8.5, h: 0.8, fontSize: 16, color: C.text2, valign: "middle", objectName: "v-stat-l" });
  s.addNotes("AI는 가끔 형식을 어깁니다. 그래서 네 단계로 처리합니다. 먼저 표기 차이처럼 내용과 상관없는 부분을 정리합니다. 다음으로 제목 길이, 섹션 네 개, 섹션마다 항목이 있는지 검사합니다. 틀렸으면 무엇이 틀렸는지 알려 주고 딱 한 번만 다시 요청합니다. 그래도 틀리면 프로그램이 직접 고칩니다. 다시 요청을 한 번으로 제한한 이유는 비용 때문입니다. 한 번 실행에 AI 호출은 최대 두 번이고, 호출 횟수가 매번 화면에 나옵니다.");

  // 15. 오류 처리
  s = content("문제가 생기면 원인을 알려 줍니다", "2. 실행 방법");
  const rows = [
    ["상황", "화면에 나오는 안내"],
    ["바뀐 내용이 없음", "변경 사항이 없습니다. 코드 설명을 생성하지 않고 종료합니다."],
    ["API Key 없음", "AI_API_KEY 환경변수가 설정되지 않았습니다. + 설정 예시"],
    ["잘못된 키 (401)", "인증 실패(401): API Key가 올바른지 확인하세요."],
    ["요청 한도 초과 (429)", "요청 한도 초과(429): 잠시 후 다시 실행하세요."],
    ["인터넷 연결 끊김", "네트워크 오류: API 서버에 연결할 수 없습니다."],
    ["엉뚱한 폴더에서 실행", "프로젝트 루트 디렉터리에서 실행하세요. (저장소 루트: …)"],
  ];
  s.addTable(rows.map((r, i) => r.map((c, j) => ({
    text: c,
    options: {
      bold: i === 0 || j === 0, color: i === 0 ? HEX.lt1 : (j === 0 ? HEX.dk1 : HEX.dk2),
      fill: { color: i === 0 ? HEX.dk1 : (i % 2 ? HEX.lt2 : HEX.lt1) }, fontSize: 15,
      fontFace: j === 1 && i > 0 ? MONO : undefined, margin: [0.08, 0.15, 0.08, 0.15], valign: "middle",
    },
  }))), { x: 0.6, y: 1.55, w: 12.1, colW: [3.4, 8.7], rowH: 0.62, border: { type: "solid", color: "D7E1DE", pt: 0.75 }, objectName: "error-table" });
  text(s, "이전 버전은 실제 API 오류에서 프로그램이 멈추며 알아보기 힘든 오류(traceback)를 냈습니다. 이번에 모두 원인 메시지로 바꿨습니다.",
    { x: 0.6, y: 6.1, w: 12.1, h: 0.6, fontSize: 14, color: C.accent5, objectName: "error-note" });
  s.addNotes("실제 서비스에서는 오류가 흔합니다. 바뀐 내용이 없거나, 키를 안 넣었거나, 키가 틀렸거나, 요청이 너무 많거나, 인터넷이 끊길 수 있습니다. 각 경우에 무엇이 문제이고 어떻게 하면 되는지 한 줄로 알려 줍니다. 처음 점검했을 때는 API 오류가 나면 프로그램이 traceback이라는 알아보기 힘든 오류를 내며 멈췄는데, 이번에 모두 원인 메시지로 바꿨습니다. 잘못된 키 사례는 실제 API에 보내서 확인했습니다.");

  // ===== 3장. 결과 =====
  sectionSlide(3, "결과는 어땠나", "실제 실행 결과, 숫자로 본 결과, 보너스, 배운 점", "3. 결과");

  // 17. 실제 실행
  s = content("실제 AI로 이번 변경을 설명해 봤습니다", "3. 결과");
  terminal(s, 0.6, 1.5, 7.4, 5.15, [
    { text: "[INFO] Git status 수집 완료: 30개 파일 변경 감지", color: "8696A3" },
    { text: "[INFO] safe-mode ON | 파일 10/30개 · diff 200/2501줄 전송", color: "8696A3" },
    { text: "[INFO] AI API 요청 중... (model=claude-opus-5-5)", color: "8696A3" },
    { text: "[DONE] 코드 설명 생성 완료", color: "13A38B", bold: true },
    "",
    { text: "--- Description Title --- (43자)", color: "8696A3" },
    { text: "Add AI code description helper CLI for b3-2", color: "F2A93B", bold: true },
    "",
    { text: "## Summary", color: "13A38B", bold: true },
    "- Git 변경과 수정 의도를 Claude API에 보내",
    "  4개 섹션 설명 초안을 출력하는 CLI를 추가",
    "- 30개 중 10개 파일만 전송되어 일부는 확인 필요",
    { text: "## What Changed  ## Why ...  ## How to Verify", color: "13A38B", bold: true },
    "",
    { text: "[OK] 제목 길이/섹션 헤더/섹션별 불릿 검증 통과", color: "13A38B" },
    { text: "[INFO] AI API 호출 횟수: 1회 (최대 2회)", color: "8696A3" },
  ], "real-term", 12);
  const real = [
    ["FaCheckCircle", HEX.accent1, "1번 만에 통과", "AI 호출 1회로 형식 검증 통과"],
    ["FaUsers", HEX.accent4, "팀 규칙도 지킴", "영어 명령형 제목 'Add …' 사용"],
    ["FaExclamationTriangle", HEX.accent2, "모르는 건 모른다고", "못 본 파일은 '확인 필요'로 표시"],
  ];
  for (let i = 0; i < 3; i++) {
    const [ic, col, h, b] = real[i];
    const y = 1.6 + i * 1.7;
    await badge(s, ic, 8.4, y, 0.8, col, `real-${i}`);
    text(s, h, { x: 9.4, y: y + 0.02, w: 3.3, h: 0.45, fontSize: 18, bold: true, objectName: `real-h-${i}` });
    text(s, b, { x: 9.4, y: y + 0.5, w: 3.3, h: 0.8, fontSize: 14, color: C.text2, objectName: `real-b-${i}` });
  }
  s.addNotes("실제 API Key로 이번 작업 자체를 설명하게 해 봤습니다. 30개 파일이 바뀌었는데 안전 모드 때문에 10개 파일, 200줄만 보냈습니다. AI는 한 번 만에 형식 검증을 통과했고, 팀 규칙대로 영어 명령형 제목을 썼습니다. 특히 좋았던 점은 보내지 않은 파일에 대해 지어내지 않고 '확인이 필요하다'고 표시한 것입니다. 프롬프트에 '근거가 없으면 지어내지 말라'고 적은 규칙이 효과를 냈습니다.");

  // 18. 숫자
  s = content("숫자로 보는 결과", "3. 결과");
  const nums = [["27개", "자동 테스트 모두 통과", HEX.accent1], ["11개", "실행 결과 증빙 파일", HEX.accent4], ["1회", "실제 생성에 든 AI 호출", HEX.accent2], ["3 / 3", "보너스 과제 완료", HEX.accent6]];
  nums.forEach(([n, l, col], i) => {
    const x = 0.6 + i * 3.1;
    card(s, x, 1.6, 2.85, 2.6, HEX.lt2, `num-card-${i}`, false);
    text(s, n, { x: x + 0.25, y: 1.85, w: 2.4, h: 1.2, fontSize: 54, bold: true, color: col === HEX.accent1 ? C.accent1 : col === HEX.accent4 ? C.accent4 : col === HEX.accent2 ? C.accent2 : C.accent6, objectName: `num-${i}` });
    text(s, l, { x: x + 0.25, y: 3.2, w: 2.4, h: 0.8, fontSize: 16, color: C.text2, objectName: `num-l-${i}` });
  });
  text(s, "테스트가 확인하는 것", { x: 0.6, y: 4.55, w: 12, h: 0.45, fontSize: 18, bold: true, objectName: "num-test-h" });
  text(s, [
    { text: "Git 수집: 수정·스테이징·새 파일 모두 수집, 루트가 아니면 안내", options: { bullet: true, breakLine: true } },
    { text: "안전 모드: 키·이메일·전화 가리기, 10개 파일/200줄 제한", options: { bullet: true, breakLine: true } },
    { text: "형식: 검사 → 재요청 → 보정, 오류 메시지 변환 (실제 API는 부르지 않음)", options: { bullet: true } },
  ], { x: 0.6, y: 5.05, w: 12.1, h: 1.6, fontSize: 15, color: C.text2, paraSpaceAfter: 6, objectName: "num-test-list" });
  s.addNotes("숫자로 정리하면, 자동 테스트 27개가 모두 통과했습니다. 테스트는 임시 Git 저장소를 만들어 수집, 안전 모드, 형식 검사와 보정, 오류 메시지를 확인합니다. 실제 API는 부르지 않아 비용이 들지 않습니다. 실행 결과 증빙은 11개 파일로 제출 폴더에 있고, 실제 설명문 생성에는 AI 호출 한 번이 들었습니다. 보너스 과제 3개도 모두 했습니다.");

  // 19. 보너스
  s = content("보너스 과제 3개", "3. 결과");
  const bonus = [
    ["FaUsers", HEX.accent4, "팀 컨벤션", "저장소의 커밋 92개를 분석해 팀 작성 규칙 파일을 만들었습니다.", ["전  feat: 세션 검증 보완", "후  Add 세션 검증 보완"]],
    ["FaShieldAlt", HEX.accent1, "안전 모드 고도화", "가릴 패턴을 늘리고, 파일 수·줄 수 기준을 옵션으로 바꿀 수 있게 했습니다.", ["OFF 14개 파일·비밀 노출", "ON  10개 파일·3건 가림"]],
    ["FaCodeBranch", HEX.accent2, "실제 저장소 적용", "이번 작업에 도구를 써서 AI 초안을 만들고, 사람이 다듬어 최종 설명을 완성했습니다.", ["초안 Add … CLI", "최종 Improve …"]],
  ];
  for (let i = 0; i < 3; i++) {
    const [ic, col, h, b, ex] = bonus[i];
    const x = 0.6 + i * 4.1;
    card(s, x, 1.55, 3.8, 4.1, HEX.lt2, `bonus-card-${i}`, false);
    await badge(s, ic, x + 0.3, 1.85, 0.8, col, `bonus-${i}`);
    text(s, h, { x: x + 1.25, y: 2.0, w: 2.4, h: 0.5, fontSize: 19, bold: true, objectName: `bonus-h-${i}` });
    text(s, b, { x: x + 0.3, y: 2.9, w: 3.2, h: 1.6, fontSize: 15, color: C.text2, objectName: `bonus-b-${i}` });
    terminal(s, x + 0.2, 4.2, 3.4, 1.25, ex.map((t, j) => ({ text: t, color: j ? "13A38B" : "D6E2E8" })), `bonus-term-${i}`, 12);
  }
  text(s, "증빙: 제출/results/06 (안전 모드 비교) · 07 (컨벤션 전후 비교) · 제출/보너스1_실제저장소_적용.md",
    { x: 0.6, y: 5.95, w: 12.1, h: 0.4, fontSize: 14, color: C.accent5, objectName: "bonus-evidence" });
  s.addNotes("보너스 과제는 세 가지입니다. 첫째, 팀 컨벤션: 이 저장소의 커밋 92개를 분석했더니 영어 명령형 동사로 제목을 시작하는 습관이 있어서, 이를 규칙 파일로 만들었습니다. 적용하면 제목이 feat: 대신 Add로 시작합니다. 둘째, 안전 모드 고도화: 가리는 패턴을 늘리고 기준을 옵션으로 조정할 수 있게 했습니다. 셋째, 실제 저장소 적용: 이번 작업에 도구를 직접 써서 AI 초안을 만들고, 사람이 고쳐 최종 설명으로 완성했습니다.");

  // 20. 초안 → 최종
  s = content("AI 초안은 출발점, 마무리는 사람", "3. 결과");
  const edits = [
    ["제목", "'새 CLI 추가'로 썼지만 실제로는 기존 도구 보완 → Improve로 수정"],
    ["What Changed", "문서 파일 위주 → 실제 로직이 바뀐 모듈로 교체"],
    ["Why It Was Needed", "수정 의도를 되풀이 → 이전 구현의 구체적인 문제를 근거로"],
    ["How to Verify", "테스트 개수 26개 → 실제 값 27개로 정정"],
  ];
  edits.forEach(([h, b], i) => {
    const y = 1.6 + i * 1.05;
    card(s, 0.6, y, 7.6, 0.85, HEX.lt2, `edit-card-${i}`, false);
    text(s, h, { x: 0.85, y: y + 0.2, w: 2.2, h: 0.45, fontSize: 16, bold: true, color: C.accent6, valign: "middle", objectName: `edit-h-${i}` });
    text(s, b, { x: 3.1, y: y + 0.12, w: 4.9, h: 0.62, fontSize: 14, color: C.text2, valign: "middle", objectName: `edit-b-${i}` });
  });
  card(s, 8.6, 1.6, 4.1, 4.0, "E3F4F0", "edit-lesson", false);
  await badge(s, "FaLightbulb", 8.9, 1.9, 0.8, HEX.accent2, "edit-lesson");
  text(s, "왜 고쳐야 했나", { x: 8.9, y: 2.9, w: 3.5, h: 0.45, fontSize: 18, bold: true, objectName: "edit-lesson-h" });
  text(s, "안전 모드가 경로 순서대로 앞 10개 파일만 보내서, 핵심 코드가 AI에 전달되지 않았습니다. AI는 본 만큼만 씁니다.",
    { x: 8.9, y: 3.45, w: 3.5, h: 2.0, fontSize: 15, color: C.text2, objectName: "edit-lesson-b" });
  text(s, "그래서 출력 마지막에 항상 \"생성된 설명은 초안입니다. 검토한 뒤 적용하세요.\"라고 표시합니다.",
    { x: 0.6, y: 5.95, w: 12.1, h: 0.6, fontSize: 15, color: C.text1, objectName: "edit-footer" });
  s.addNotes("AI 초안을 그대로 쓰지 않고 사람이 네 군데를 고쳤습니다. 제목은 '새로 추가'가 아니라 '보완'이 맞아서 Improve로 바꿨고, What Changed는 문서 파일 대신 실제 코드가 바뀐 모듈로 바꿨습니다. Why는 이전 구현의 구체적인 문제를 적었고, 테스트 개수도 정정했습니다. 원인은 안전 모드가 앞쪽 10개 파일만 보내서 핵심 코드가 AI에 전달되지 않은 것입니다. AI는 본 만큼만 쓸 수 있습니다. 그래서 이 도구는 항상 '초안이니 검토하라'고 표시합니다.");

  // 21. 정리
  pres.addSection({ title: "정리" });
  s = pres.addSlide({ masterName: "CLOSING", sectionTitle: "정리" });
  s.addText("이 과제로 설명할 수 있게 된 것", { placeholder: "title" });
  const learn = [
    ["FaCloud", "API 연동 흐름", "질문 만들기 → 보내기 → 답 해석 → 오류 대응"],
    ["FaSlidersH", "파라미터의 역할", "model·effort·max_tokens가 품질과 비용을 바꿈"],
    ["FaCodeBranch", "Git을 입력으로", "status·diff 결과를 그대로 질문지에 연결"],
    ["FaCommentDots", "프롬프트 설계", "의도 + 근거 + 형식을 함께 주면 답이 정확해짐"],
    ["FaRulerHorizontal", "검증과 다듬기", "형식 검사·재요청·보정으로 실무 품질 확보"],
  ];
  for (let i = 0; i < 5; i++) {
    const [ic, h, b] = learn[i];
    const y = 1.45 + i * 0.95;
    await badge(s, ic, 0.6, y, 0.7, HEX.accent1, `learn-${i}`);
    text(s, h, { x: 1.55, y: y + 0.12, w: 3.4, h: 0.45, fontSize: 19, bold: true, color: C.background1, objectName: `learn-h-${i}` });
    text(s, b, { x: 5.0, y: y + 0.14, w: 7.7, h: 0.45, fontSize: 16, color: C.accent5, objectName: `learn-b-${i}` });
  }
  text(s, "핵심 한 줄:  AI에게 무엇을 보여 주느냐가 결과를 결정한다", { x: 0.6, y: 6.35, w: 12.1, h: 0.45, fontSize: 18, bold: true, color: C.accent2, objectName: "learn-key" });
  s.addNotes("정리하겠습니다. 이 과제를 통해 다섯 가지를 설명할 수 있게 되었습니다. AI API에 질문을 보내고 답을 해석하고 오류에 대응하는 흐름, 파라미터가 품질과 비용에 주는 영향, Git 결과를 프로그램 입력으로 연결하는 방법, 의도와 근거와 형식을 함께 주는 프롬프트 설계, 그리고 결과를 검사하고 다듬는 이유입니다. 핵심은 한 줄입니다. AI에게 무엇을 보여 주느냐가 결과를 결정합니다. 감사합니다.");

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  await setEastAsianFont(OUT, THEME.bodyFontFace);
  console.log("written", OUT);
}

build().catch((e) => { console.error(e); process.exit(1); });
