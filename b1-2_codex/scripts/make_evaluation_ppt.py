#!/usr/bin/env python3
"""Create a PPTX deck for B1-2 evaluation prep without external packages."""

from __future__ import annotations

import html
import shutil
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "b1-2" / "B1-2_평가문항_대비자료.pptx"
OUT = ROOT / "b1-2_codex" / "reports" / "evaluation-prep.pptx"

EMU_W = 13_333_500
EMU_H = 7_500_000


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def clean_ascii(text: str) -> str:
    return text.replace("→", "->").replace("≥", ">=").replace("–", "-")


def run_xml(text: str, size: int = 1800, color: str = "1F2937", bold: bool = False) -> str:
    text = clean_ascii(text)
    b = "<a:b/>" if bold else ""
    return (
        f'<a:r><a:rPr lang="ko-KR" sz="{size}" dirty="0">{b}'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        f'<a:latin typeface="Apple SD Gothic Neo"/><a:ea typeface="Apple SD Gothic Neo"/>'
        f'</a:rPr><a:t>{esc(text)}</a:t></a:r>'
    )


def para_xml(text: str, size: int = 1800, color: str = "1F2937", bullet: bool = False) -> str:
    mar = ' marL="285750" indent="-171450"' if bullet else ""
    bu = '<a:buChar char="•"/>' if bullet else ""
    return f"<a:p><a:pPr{mar}>{bu}</a:pPr>{run_xml(text, size, color)}</a:p>"


def text_box(
    sid: int,
    name: str,
    x: int,
    y: int,
    w: int,
    h: int,
    lines: list[str],
    size: int = 1800,
    color: str = "1F2937",
    fill: str | None = None,
    border: str | None = None,
    bullet: bool = False,
    font_scale: list[int] | None = None,
) -> str:
    fill_xml = (
        f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
        if fill
        else "<a:noFill/>"
    )
    border_xml = (
        f'<a:ln w="9525"><a:solidFill><a:srgbClr val="{border}"/></a:solidFill></a:ln>'
        if border
        else "<a:ln><a:noFill/></a:ln>"
    )
    paragraphs = []
    for i, line in enumerate(lines):
        line_size = font_scale[i] if font_scale and i < len(font_scale) else size
        paragraphs.append(para_xml(line, line_size, color, bullet=bullet and bool(line)))
    body = "".join(paragraphs) or "<a:p/>"
    return f"""
    <p:sp>
      <p:nvSpPr>
        <p:cNvPr id="{sid}" name="{esc(name)}"/>
        <p:cNvSpPr txBox="1"/>
        <p:nvPr/>
      </p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
        <a:prstGeom prst="roundRect"><a:avLst/></a:prstGeom>
        {fill_xml}
        {border_xml}
      </p:spPr>
      <p:txBody>
        <a:bodyPr wrap="square" lIns="127000" tIns="91440" rIns="127000" bIns="91440"/>
        <a:lstStyle/>
        {body}
      </p:txBody>
    </p:sp>
    """


def title_box(title: str, subtitle: str | None = None) -> str:
    lines = [title] + ([subtitle] if subtitle else [])
    sizes = [3000] + ([1500] if subtitle else [])
    return text_box(
        100,
        "Title",
        520_000,
        285_000,
        12_280_000,
        700_000 if subtitle else 520_000,
        lines,
        color="111827",
        fill=None,
        font_scale=sizes,
    )


def footer(page: int) -> str:
    return text_box(
        900 + page,
        "Footer",
        520_000,
        7_060_000,
        12_280_000,
        230_000,
        [f"B1-2 평가 대비 | 원본 agent-leak-app-x86 실행 결과 | {page}"],
        size=900,
        color="6B7280",
    )


def code_box(sid: int, x: int, y: int, w: int, h: int, lines: list[str]) -> str:
    return text_box(
        sid,
        "Evidence",
        x,
        y,
        w,
        h,
        lines,
        size=1050,
        color="E5E7EB",
        fill="111827",
        border="374151",
    )


def bullet_box(sid: int, x: int, y: int, w: int, h: int, lines: list[str], fill="F8FAFC") -> str:
    return text_box(
        sid,
        "Bullets",
        x,
        y,
        w,
        h,
        lines,
        size=1420,
        color="1F2937",
        fill=fill,
        border="D1D5DB",
        bullet=True,
    )


def slide_xml(page: int, title: str, shapes: list[str], subtitle: str | None = None) -> str:
    all_shapes = [title_box(title, subtitle), *shapes, footer(page)]
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      {''.join(all_shapes)}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>
"""


def content_types_xml(n: int) -> str:
    overrides = "\n".join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, n + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="jpeg" ContentType="image/jpeg"/>
  <Default Extension="bin" ContentType="application/vnd.openxmlformats-officedocument.presentationml.printerSettings"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>
  <Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  {overrides}
</Types>
"""


def presentation_xml(n: int) -> str:
    slide_ids = "\n".join(
        f'<p:sldId id="{255 + i}" r:id="rId{i}"/>' for i in range(1, n + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                saveSubsetFonts="1">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId{n + 1}"/></p:sldMasterIdLst>
  <p:sldIdLst>{slide_ids}</p:sldIdLst>
  <p:sldSz cx="{EMU_W}" cy="{EMU_H}" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
  <p:defaultTextStyle/>
</p:presentation>
"""


def presentation_rels_xml(n: int) -> str:
    rels = [
        f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        for i in range(1, n + 1)
    ]
    rels.extend(
        [
            f'<Relationship Id="rId{n + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>',
            f'<Relationship Id="rId{n + 2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>',
            f'<Relationship Id="rId{n + 3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps" Target="presProps.xml"/>',
            f'<Relationship Id="rId{n + 4}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/viewProps" Target="viewProps.xml"/>',
            f'<Relationship Id="rId{n + 5}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/tableStyles" Target="tableStyles.xml"/>',
        ]
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {''.join(rels)}
</Relationships>
"""


def slide_rels_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>
"""


def build_slides() -> list[str]:
    slides: list[str] = []
    slides.append(
        slide_xml(
            1,
            "B1-2 평가 대비 발표자료",
            [
                bullet_box(
                    10,
                    800_000,
                    1_450_000,
                    11_700_000,
                    2_000_000,
                    [
                        "주제: Linux 프로세스 및 시스템 리소스 트러블슈팅",
                        "대상: 원본 agent-leak-app-x86 실행 결과",
                        "증거: 앱 로그, monitor.sh, ps, top, /proc, ps -L",
                        "핵심 태도: 재현 결과와 미재현 결과를 모두 증거 기반으로 설명",
                    ],
                    fill="EFF6FF",
                )
            ],
            "OOM / CPU Spike / Deadlock 결과와 평가 질문 답변",
        )
    )
    slides.append(
        slide_xml(
            2,
            "미션 요구사항과 제출물",
            [
                bullet_box(
                    11,
                    650_000,
                    1_230_000,
                    12_000_000,
                    2_850_000,
                    [
                        "3개 장애 유형별 GitHub Issue 형식 리포트 작성",
                        "각 리포트: 현상, 증거, 원인, 조치 및 검증 포함",
                        "객관 증거: monitor.sh, 앱 로그, ps/top, 스레드/프로세스 상태",
                        "제출물: oom.md, cpu-spike.md, deadlock.md, evidence/logs/*",
                    ],
                ),
                code_box(
                    12,
                    800_000,
                    4_420_000,
                    11_650_000,
                    1_170_000,
                    [
                        "b1-2_codex/reports/oom.md",
                        "b1-2_codex/reports/cpu-spike.md",
                        "b1-2_codex/reports/deadlock.md",
                        "b1-2_codex/evidence/logs/",
                    ],
                ),
            ],
        )
    )
    slides.append(
        slide_xml(
            3,
            "오늘 실행 환경",
            [
                bullet_box(
                    13,
                    650_000,
                    1_230_000,
                    5_900_000,
                    3_520_000,
                    [
                        "OrbStack Ubuntu b1-lab",
                        "실행 계정: agent-admin",
                        "앱 홈: /home/agent-admin/agent-app",
                        "포트: 15034",
                        "키 경로: api_keys/secret.key",
                    ],
                ),
                code_box(
                    14,
                    6_850_000,
                    1_230_000,
                    5_800_000,
                    3_520_000,
                    [
                        "원본 파일 동일성 확인",
                        "VM agent-leak-app",
                        "local agent-leak-app-x86",
                        "zip 내부 agent-leak-app-x86",
                        "",
                        "SHA-256:",
                        "7e0a19cfa80ece6b547a5008273661f0",
                        "d4d71e526e96b51e0d0f341dd1bb3e40",
                    ],
                ),
            ],
        )
    )
    slides.append(
        slide_xml(
            4,
            "전체 결과 요약",
            [
                bullet_box(
                    15,
                    650_000,
                    1_160_000,
                    12_050_000,
                    4_450_000,
                    [
                        "OOM: MEMORY_LIMIT=50에서 MemoryGuard 자기 종료 재현 성공",
                        "CPU: CPU_MAX_OCCUPY 값에 따라 cooldown 동작 변화 확인",
                        "CPU: Watchdog/SIGTERM 종료 로그는 원본 앱에서 미관찰",
                        "Deadlock: 경고 문구는 출력됐지만 Threads=1, WAITING/BLOCKED 로그 없음",
                        "결론: OOM은 재현, CPU/Deadlock은 교재 기대와 다른 실제 동작을 보고",
                    ],
                    fill="F9FAFB",
                )
            ],
        )
    )
    slides.append(
        slide_xml(
            5,
            "Case 1 - OOM 관찰 결과",
            [
                bullet_box(
                    16,
                    650_000,
                    1_150_000,
                    5_900_000,
                    2_550_000,
                    [
                        "Before: MEMORY_LIMIT=50",
                        "Heap 25MB -> 50MB 증가",
                        "50MB 도달 즉시 MemoryGuard 발동",
                        "프로세스 종료 후 포트도 닫힘",
                    ],
                    fill="FEF2F2",
                ),
                code_box(
                    17,
                    6_850_000,
                    1_150_000,
                    5_850_000,
                    2_950_000,
                    [
                        "17:18:00 Current Heap: 25MB",
                        "17:18:03 Current Heap: 50MB",
                        "Memory limit exceeded (50MB >= 50MB)",
                        "Self-terminating process 3114",
                    ],
                ),
                code_box(
                    18,
                    900_000,
                    4_330_000,
                    11_350_000,
                    1_100_000,
                    [
                        "monitor.sh: PID 3114 RSS 44232KB -> next snapshot PROCESS FAIL",
                        "After MEMORY_LIMIT=512: 관찰 시간 내 종료 로그 없음",
                    ],
                ),
            ],
        )
    )
    slides.append(
        slide_xml(
            6,
            "OOM 원인과 답변 포인트",
            [
                bullet_box(
                    19,
                    650_000,
                    1_200_000,
                    12_050_000,
                    4_200_000,
                    [
                        "메모리 누수: 힙에 쌓인 데이터가 해제되지 않아 사용량 증가",
                        "앱 내부 Heap 카운터와 OS RSS를 함께 관찰",
                        "MemoryGuard는 시스템 전체 불안정 방지를 위해 자기 프로세스를 종료",
                        "임시 조치: MEMORY_LIMIT 상향",
                        "근본 조치: 객체 해제, 캐시 크기 제한, 스트리밍 처리",
                    ],
                )
            ],
        )
    )
    slides.append(
        slide_xml(
            7,
            "Case 2 - CPU Spike 관찰 결과",
            [
                bullet_box(
                    20,
                    650_000,
                    1_150_000,
                    5_900_000,
                    2_800_000,
                    [
                        "Before: CPU_MAX_OCCUPY=10",
                        "10% 도달 후 Peak reached",
                        "Watchdog 종료 대신 cooldown",
                        "After: CPU_MAX_OCCUPY=50, 24.78%까지 상승",
                    ],
                    fill="FFF7ED",
                ),
                code_box(
                    21,
                    6_850_000,
                    1_150_000,
                    5_850_000,
                    3_300_000,
                    [
                        "CpuWorker Started. Maximum CPU Limit: 10%",
                        "Current Load: 5.00%",
                        "Peak reached (10.00%). Starting cooldown...",
                        "Cooldown complete (5.00%). Resuming load increase...",
                        "",
                        "After Current Load: 24.78%",
                    ],
                ),
            ],
        )
    )
    slides.append(
        slide_xml(
            8,
            "CPU 해석과 교재 예시와의 차이",
            [
                bullet_box(
                    22,
                    650_000,
                    1_150_000,
                    12_050_000,
                    4_500_000,
                    [
                        "교재 기대: CPU 임계치 초과 -> Watchdog/SIGTERM 종료",
                        "오늘 원본 앱 결과: WATCHDOG, SIGTERM, CPU Threshold Violated 로그 미관찰",
                        "확인된 사실: CPU_MAX_OCCUPY는 cooldown 임계치로 반영됨",
                        "평가 답변: CPU Spike와 환경변수 영향은 확인, 종료 재현은 실패로 정직하게 보고",
                        "도구: ps -C, top -bn1 -p, ps -L -p",
                    ],
                )
            ],
        )
    )
    slides.append(
        slide_xml(
            9,
            "Case 3 - Deadlock 관찰 결과",
            [
                bullet_box(
                    23,
                    650_000,
                    1_150_000,
                    5_900_000,
                    2_800_000,
                    [
                        "Before: MULTI_THREAD_ENABLE=true",
                        "POTENTIAL DEADLOCK 경고 출력",
                        "하지만 실제 작업 프로세스 Threads=1",
                        "WAITING/BLOCKED/lock 로그 없음",
                    ],
                    fill="ECFDF5",
                ),
                code_box(
                    24,
                    6_850_000,
                    1_150_000,
                    5_850_000,
                    3_300_000,
                    [
                        "SYSTEM WARNING: POTENTIAL DEADLOCK",
                        "Current Load: 5.00%",
                        "Current Load: 10.27%",
                        "Current Load: 21.62%",
                        "",
                        "/proc status: Threads: 1",
                        "ps -L: one TID only",
                    ],
                ),
            ],
        )
    )
    slides.append(
        slide_xml(
            10,
            "Deadlock 판단 기준",
            [
                bullet_box(
                    25,
                    650_000,
                    1_150_000,
                    12_050_000,
                    4_500_000,
                    [
                        "Deadlock은 PID 생존만으로 판단하지 않음",
                        "필요 증거: 여러 스레드, 로그 정지, WAITING/BLOCKED, lock 순환 대기",
                        "오늘 결과: PID는 있었지만 로그 진행, Threads=1",
                        "따라서 원본 앱 기준 Deadlock 미재현으로 판단",
                        "평가 답변: 경고 문구와 실제 OS 관측값을 분리해서 설명",
                    ],
                )
            ],
        )
    )
    slides.append(
        slide_xml(
            11,
            "진단 도구와 판단 흐름",
            [
                code_box(
                    26,
                    700_000,
                    1_150_000,
                    12_000_000,
                    1_700_000,
                    [
                        "monitor.sh: pgrep -x agent-leak-app; ps -p PID -o pid,ppid,user,%cpu,%mem,rss,stat,cmd",
                        "CPU: ps -C agent-leak-app; top -bn1 -p PID",
                        "Thread: ps -L -p PID; top -H -bn1 -p PID; /proc/PID/status",
                    ],
                ),
                bullet_box(
                    27,
                    700_000,
                    3_180_000,
                    12_000_000,
                    2_150_000,
                    [
                        "1. PID 존재 확인",
                        "2. CPU/RSS 변화 확인",
                        "3. 앱 로그 마지막 지점 확인",
                        "4. 스레드 수와 상태 확인",
                        "5. 환경변수 변경 전후 비교",
                    ],
                ),
            ],
        )
    )
    slides.append(
        slide_xml(
            12,
            "예상 질문 답변 1",
            [
                bullet_box(
                    28,
                    650_000,
                    1_150_000,
                    12_050_000,
                    4_700_000,
                    [
                        "Q. monitor.sh는 무엇을 봤나? A. PID별 %CPU, %MEM, RSS, STAT, CMD를 2초마다 기록",
                        "Q. RSS란? A. 실제 물리 메모리에 올라온 프로세스 resident set 크기",
                        "Q. 앱 Heap과 RSS가 왜 다른가? A. 내부 카운터와 OS 실측값은 기준이 다름",
                        "Q. CPU 도구 선택 이유? A. ps는 스냅샷, top은 실시간/순간 부하, ps -L은 스레드",
                    ],
                )
            ],
        )
    )
    slides.append(
        slide_xml(
            13,
            "예상 질문 답변 2",
            [
                bullet_box(
                    29,
                    650_000,
                    1_150_000,
                    12_050_000,
                    4_700_000,
                    [
                        "Q. CPU Watchdog은 발동했나? A. 오늘 원본 앱에서는 발동 로그가 없었고 cooldown만 확인",
                        "Q. Deadlock은 발생했나? A. 아니다. Threads=1이라 순환 대기 증거가 없음",
                        "Q. 실제 서버라면 monitor.sh 개선은? A. RSS 증가율, 임계치 알림, PID 계층 추적, 로그 로테이션",
                        "Q. 가장 치명적인 장애는? A. Deadlock은 생존 체크를 통과할 수 있어 탐지가 까다로움",
                    ],
                )
            ],
        )
    )
    slides.append(
        slide_xml(
            14,
            "마무리 멘트",
            [
                bullet_box(
                    30,
                    900_000,
                    1_350_000,
                    11_450_000,
                    3_700_000,
                    [
                        "OOM은 MemoryGuard 자기 종료가 명확히 재현됨",
                        "CPU는 임계치에 따른 cooldown은 확인, Watchdog 종료는 미재현",
                        "Deadlock은 경고만 확인, 스레드/락 대기 증거가 없어 미재현",
                        "핵심 역량: 로그와 OS 관제 데이터로 관찰 사실과 추론을 분리해 보고",
                    ],
                    fill="EEF2FF",
                )
            ],
        )
    )
    return slides


def main() -> None:
    slides = build_slides()
    OUT.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        with zipfile.ZipFile(TEMPLATE) as zf:
            zf.extractall(tmp)

        # Remove old slides and relationships.
        slides_dir = tmp / "ppt" / "slides"
        rels_dir = slides_dir / "_rels"
        if slides_dir.exists():
            for item in slides_dir.glob("slide*.xml"):
                item.unlink()
        rels_dir.mkdir(parents=True, exist_ok=True)
        for item in rels_dir.glob("slide*.xml.rels"):
            item.unlink()

        for idx, xml in enumerate(slides, start=1):
            (slides_dir / f"slide{idx}.xml").write_text(xml, encoding="utf-8")
            (rels_dir / f"slide{idx}.xml.rels").write_text(slide_rels_xml(), encoding="utf-8")

        (tmp / "[Content_Types].xml").write_text(content_types_xml(len(slides)), encoding="utf-8")
        (tmp / "ppt" / "presentation.xml").write_text(presentation_xml(len(slides)), encoding="utf-8")
        (tmp / "ppt" / "_rels" / "presentation.xml.rels").write_text(
            presentation_rels_xml(len(slides)), encoding="utf-8"
        )

        if OUT.exists():
            OUT.unlink()
        with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as out:
            for path in sorted(tmp.rglob("*")):
                if path.is_file():
                    out.write(path, path.relative_to(tmp).as_posix())

    print(OUT)


if __name__ == "__main__":
    main()
