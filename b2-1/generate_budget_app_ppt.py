from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

OUT = "/Users/cspag5955/AI-SW-Basic/b2-1/budget_app_실행설명.pptx"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Theme colors
NAVY = RGBColor(18, 52, 98)
BLUE = RGBColor(24, 105, 182)
LIGHT = RGBColor(239, 246, 255)
TEXT = RGBColor(34, 34, 34)
MUTED = RGBColor(92, 102, 115)
GREEN = RGBColor(22, 163, 74)
WHITE = RGBColor(255, 255, 255)
PALE_GREEN = RGBColor(236, 253, 245)


def add_title_slide(title, subtitle):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = LIGHT
    title_box = slide.shapes.title
    title_box.text = title
    title_box.text_frame.paragraphs[0].font.size = Pt(28)
    title_box.text_frame.paragraphs[0].font.bold = True
    title_box.text_frame.paragraphs[0].font.color.rgb = NAVY
    subtitle_box = slide.placeholders[1]
    subtitle_box.text = subtitle
    subtitle_box.text_frame.paragraphs[0].font.size = Pt(18)
    subtitle_box.text_frame.paragraphs[0].font.color.rgb = MUTED


def style_title(slide, title):
    title_box = slide.shapes.title
    title_box.text = title
    p = title_box.text_frame.paragraphs[0]
    p.font.size = Pt(25)
    p.font.bold = True
    p.font.color.rgb = NAVY


def add_footer(slide):
    box = slide.shapes.add_textbox(Inches(11.8), Inches(7.08), Inches(0.8), Inches(0.2))
    p = box.text_frame.paragraphs[0]
    p.text = f"{len(prs.slides):02d}"
    p.alignment = PP_ALIGN.RIGHT
    p.font.size = Pt(9)
    p.font.color.rgb = MUTED


def add_explanation_slide(title, rows, code_title=None):
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = LIGHT
    style_title(slide, title)
    y = 1.42
    if code_title:
        label = slide.shapes.add_textbox(Inches(0.75), Inches(y), Inches(11.8), Inches(0.32))
        p = label.text_frame.paragraphs[0]
        p.text = code_title
        p.font.name = "Consolas"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = BLUE
        y += 0.48
    row_h = min(0.83, 5.35 / len(rows))
    for code, explanation in rows:
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.75), Inches(y), Inches(11.85), Inches(row_h - 0.08))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = RGBColor(218, 229, 242)
        code_box = slide.shapes.add_textbox(Inches(0.98), Inches(y + 0.09), Inches(4.35), Inches(row_h - 0.22))
        cp = code_box.text_frame.paragraphs[0]
        cp.text = code
        cp.font.name = "Consolas"
        cp.font.size = Pt(14)
        cp.font.bold = True
        cp.font.color.rgb = BLUE
        desc = slide.shapes.add_textbox(Inches(5.45), Inches(y + 0.08), Inches(6.85), Inches(row_h - 0.2))
        dp = desc.text_frame.paragraphs[0]
        dp.text = explanation
        dp.font.size = Pt(14)
        dp.font.color.rgb = TEXT
        y += row_h
    add_footer(slide)


def add_atomic_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = LIGHT
    style_title(slide, "8. 원자적 쓰기란?")
    blocks = [
        ("1  임시 파일에 완성본 작성", "기존 파일은 그대로 둔 채\n새 내용을 임시 파일에 모두 기록", BLUE, WHITE),
        ("2  파일 교체", "기록이 끝나면 os.replace로\n새 파일을 한 번에 교체", GREEN, PALE_GREEN),
    ]
    for i, (heading, body, color, fill) in enumerate(blocks):
        x = 0.8 + i * 6.15
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(2.0), Inches(5.55), Inches(2.25))
        card.fill.solid(); card.fill.fore_color.rgb = fill
        card.line.color.rgb = color
        tb = slide.shapes.add_textbox(Inches(x + 0.25), Inches(2.3), Inches(5.0), Inches(1.7))
        tf = tb.text_frame
        tf.paragraphs[0].text = heading
        tf.paragraphs[0].font.bold = True; tf.paragraphs[0].font.size = Pt(19); tf.paragraphs[0].font.color.rgb = color
        p = tf.add_paragraph(); p.text = body; p.font.size = Pt(16); p.font.color.rgb = TEXT; p.space_before = Pt(12)
    arrow = slide.shapes.add_textbox(Inches(6.18), Inches(2.83), Inches(0.65), Inches(0.5))
    ap = arrow.text_frame.paragraphs[0]; ap.text = "→"; ap.font.size = Pt(25); ap.font.bold = True; ap.font.color.rgb = MUTED
    note = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.45), Inches(4.85), Inches(10.45), Inches(1.05))
    note.fill.solid(); note.fill.fore_color.rgb = WHITE; note.line.color.rgb = RGBColor(218, 229, 242)
    nt = slide.shapes.add_textbox(Inches(1.75), Inches(5.08), Inches(9.9), Inches(0.6))
    np = nt.text_frame.paragraphs[0]
    np.text = "중간에 프로그램이 종료되어도 원본이 반쯤 기록된 상태로 남는 일을 막습니다."
    np.font.size = Pt(16); np.font.color.rgb = TEXT; np.alignment = PP_ALIGN.CENTER
    add_footer(slide)


def add_section_slide(title, bullets):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = LIGHT
    style_title(slide, title)

    body = slide.shapes.placeholders[1]
    tf = body.text_frame
    tf.clear()
    tf.word_wrap = True
    for i, bullet in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = bullet
        p.level = 0
        p.bullet = True
        p.font.size = Pt(20)
        p.font.color.rgb = TEXT
        p.space_after = Pt(10)
    add_footer(slide)


def add_command_slide(title, commands):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor(255, 255, 255)

    style_title(slide, title)

    body = slide.shapes.placeholders[1]
    tf = body.text_frame
    tf.clear()
    tf.word_wrap = True
    for cmd in commands:
        p = tf.paragraphs[0] if tf.paragraphs[0].text == "" else tf.add_paragraph()
        p.text = cmd
        p.level = 0
        p.font.size = Pt(18)
        p.font.name = "Consolas"
        p.font.color.rgb = BLUE
        p.space_after = Pt(8)
    add_footer(slide)


def add_two_col_slide(title, left_title, left_items, right_title, right_items):
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = LIGHT

    style_title(slide, title)

    left = slide.shapes.add_textbox(Inches(0.7), Inches(1.7), Inches(5.3), Inches(4.8))
    left_tf = left.text_frame
    left_tf.word_wrap = True
    left_p = left_tf.paragraphs[0]
    left_p.text = left_title
    left_p.font.bold = True
    left_p.font.size = Pt(18)
    left_p.font.color.rgb = BLUE
    for item in left_items:
        p = left_tf.add_paragraph()
        p.text = item
        p.level = 0
        p.bullet = True
        p.font.size = Pt(17)
        p.font.color.rgb = TEXT
        p.space_after = Pt(8)
    add_footer(slide)

    right = slide.shapes.add_textbox(Inches(6.8), Inches(1.7), Inches(5.7), Inches(4.8))
    right_tf = right.text_frame
    right_tf.word_wrap = True
    right_p = right_tf.paragraphs[0]
    right_p.text = right_title
    right_p.font.bold = True
    right_p.font.size = Pt(18)
    right_p.font.color.rgb = BLUE
    for item in right_items:
        p = right_tf.add_paragraph()
        p.text = item
        p.level = 0
        p.bullet = True
        p.font.size = Pt(17)
        p.font.color.rgb = TEXT
        p.space_after = Pt(8)


# Slide 1
add_title_slide("파일 기반 가계부 콘솔 프로그램", "Python CLI 과제 실행 설명 | budget_app")

# Slide 2
add_section_slide(
    "1. 과제 소개",
    [
        "Python 표준 라이브러리만으로 구현한 CLI 가계부 프로그램",
        "수입/지출 내역을 파일로 저장하고 관리하는 과제",
        "터미널 환경에서 직접 명령을 입력하여 동작",
        "데이터 검증, 검색, 예산 관리, CSV 파일 처리 포함",
    ],
)

# Slide 3
add_two_col_slide(
    "2. 주요 기능",
    "핵심 기능",
    [
        "거래 추가: add",
        "거래 목록 조회: list",
        "조건 검색: search",
        "월별 요약: summary",
        "예산 설정: budget set",
    ],
    "추가 기능",
    [
        "카테고리 관리: category add/list/remove",
        "거래 수정: update",
        "거래 삭제: delete",
        "CSV 내보내기 / 가져오기: export / import",
        "기본 카테고리 자동 생성",
    ],
)

# Slide 4
add_command_slide(
    "3. 실행 방법",
    [
        "cd /Users/cspag5955/AI-SW-Basic/b2-1",
        "python3 -m budget_app --help",
        "python3 -m budget_app add",
        "python3 -m budget_app list --limit 10",
        "python3 -m budget_app summary --month 2026-09 --top 3",
    ],
)

add_explanation_slide(
    "3. 실행 방법 | 각 명령어의 의미",
    [
        ("cd .../b2-1", "프로젝트 폴더로 이동합니다. 이 위치에서 패키지를 실행합니다."),
        ("python3 -m budget_app --help", "budget_app을 모듈로 실행하고 전체 명령 도움말을 표시합니다."),
        ("python3 -m budget_app add", "새 거래를 추가합니다. 날짜·종류·금액 등을 대화형으로 입력합니다."),
        ("... list --limit 10", "거래 목록을 조회하고 표시 건수를 최대 10건으로 제한합니다."),
        ("... summary --month 2026-09 --top 3", "2026년 9월을 요약하고 지출 상위 항목 3개를 표시합니다."),
    ],
)

add_explanation_slide(
    "3. 실행 방법 | __main__.py 한 줄씩 읽기",
    [
        ('"""... 진입점."""', "파일의 역할을 설명하는 문서 문자열입니다. python -m 실행의 진입점임을 알립니다."),
        ("import sys", "파이썬 시스템 기능을 가져옵니다. 여기서는 종료 코드 전달에 사용합니다."),
        ("from budget_app.cli import main", "CLI 모듈에서 명령을 처리하는 main 함수를 가져옵니다."),
        ('if __name__ == "__main__":', "이 파일이 직접 실행될 때만 아래 코드를 실행합니다."),
        ("sys.exit(main())", "main()을 실행하고 반환된 결과를 프로세스 종료 코드로 돌려줍니다."),
    ],
    code_title="실제 코드: __main__.py",
)

add_explanation_slide(
    "3. 실행 방법 | 5줄이 기능을 수행하는 방식",
    [
        ("터미널 명령", "python3 -m budget_app add처럼 실행하면 Python이 budget_app/__main__.py를 시작합니다."),
        ("__main__.py", "시작 파일은 cli.main()을 호출해 명령 처리에 넘깁니다. 직접 저장 로직을 담지는 않습니다."),
        ("cli.py", "명령과 옵션을 해석하고, 필요한 입력을 받아 사용자에게 결과를 출력합니다."),
        ("service.py", "입력값을 검증하고 거래 추가·수정·요약 같은 가계부 규칙을 처리합니다."),
        ("repository.py", "서비스의 요청에 따라 JSONL 파일에서 데이터를 읽고 저장합니다."),
    ],
)

# Slide 5
add_two_col_slide(
    "4. 입력 흐름",
    "대화형 입력 예시",
    [
        "날짜(YYYY-MM-DD)",
        "타입(income/expense)",
        "카테고리",
        "금액(양수)",
        "메모(선택)",
        "태그(선택)",
    ],
    "예시 입력",
    [
        "2026-09-26",
        "expense",
        "food",
        "15000",
        "점심 식사",
        "meal, workday",
    ],
)

# Slide 6
add_section_slide(
    "5. 데이터 저장 구조",
    [
        "transactions.jsonl: 거래 내역 저장",
        "categories.jsonl: 카테고리 목록 저장",
        "budgets.jsonl: 월별 예산 저장",
        "JSONL 형식: 한 줄에 JSON 객체 하나씩 기록",
        "기본 카테고리: food, transport, rent, salary, etc",
    ],
)

# Slide 7
add_section_slide(
    "6. 코드 구조",
    [
        "__main__.py: 프로그램 진입점",
        "cli.py: argparse 인자 처리 및 대화형 입력",
        "service.py: 검증, 비즈니스 로직, 월별 요약",
        "repository.py: 파일 I/O 및 JSONL 읽기/쓰기",
        "models.py: Transaction 데이터 모델",
        "decorators.py / errors.py: 로그, 예외 처리, 공통 관심사 분리",
    ],
)

# Slide 8
add_section_slide(
    "7. 안정성과 핵심 포인트",
    [
        "CLI 기반 프로그램으로 사용자가 터미널에서 쉽게 관리 가능",
        "파일 기반 저장으로 프로그램 재시작 후에도 데이터 유지",
        "입력값 검증으로 잘못된 데이터 방지",
        "원자적 쓰기와 예외 처리를 통해 안정성 확보",
        "실무형 설계: 계층 분리와 유지보수성 고려",
    ],
)

add_atomic_slide()

# Slide 9
add_title_slide("마무리", "이 과제는 파일 저장, CLI 설계, 데이터 검증, 예산 관리까지 포함한 실전형 Python 프로그램 구현 경험을 다룹니다.")

prs.save(OUT)
print(f"PPT created: {OUT}")
