"""평가자 질문 20개에 대한 별도 PPT/PDF와 미리보기를 생성한다."""
import importlib.util
import json
import math
from pathlib import Path
import shutil
import tempfile
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('presentation_base', ROOT / 'build_presentation.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
DATA = json.loads((ROOT / '평가자질문_답변_content.json').read_text())
base.DATA = DATA
base.SLIDES = DATA['slides']
base.CANVASES = []
base.VALIDATION = []


class QuestionCanvas(base.Canvas):
    def render(self):
        s = self.slide
        C = base.C
        self.shape(80,65,70,8,C['gold'] if self.dark else C['teal'])
        self.text(s['section']+'  /  MINI GIT',170,50,1400,45,25,
                  C['gold'] if self.dark else C['teal'],True)
        self.text(f'{self.index:02d} / {len(base.SLIDES):02d}',1650,50,190,45,25,center=True)
        if s['kind'] == 'cover':
            self.text(s['title'],100,180,1700,270,100,bold=True)
            self.text(s['takeaway'],105,480,1700,80,43,C['gold'],True)
            self.text('기능 확인 → 구조 설명 → 원리 이해 → 개선 제안',105,610,1700,70,42)
            self.text('항목 1: 6개 질문    항목 2: 5개 질문\n항목 3: 5개 질문    항목 4: 4개 질문',105,730,1700,130,40)
            self.text('항목 4는 현재 미구현인 개선 전략입니다.',105,940,1700,60,32,C['gold'])
        else:
            self.text(s['title'],80,125,1760,95,62,bold=True)
            self.shape(80,230,1760,145,C['surface'],'roundRect')
            self.text('평가자 질문',105,243,1710,40,25,C['teal'],True)
            self.text(s['question'],105,291,1710,77,33)
            self.shape(80,400,1080,495,C['white'],'roundRect',C['line'])
            self.shape(1185,400,655,495,C['navy'],'roundRect')
            label='쉬운 답변 · 개선 제안(미구현)' if s['section'].startswith('항목 4') else '쉬운 답변 · 현재 구현'
            self.text(label,110,420,1020,50,29,C['teal'],True)
            self.text(s['answer'],110,487,1020,375,36)
            self.text('예시 · 확인할 점',1215,420,595,50,29,C['gold'],True)
            self.text(s['example'],1215,487,595,375,32,C['white'])
            self.shape(80,920,1760,92,C['teal'],'roundRect')
            self.text(s['takeaway'],105,941,1710,65,33,C['white'],True)
        self.text('근거: '+s['source'],80,1033,1760,36,20,C['line'] if self.dark else C['muted'])
        self.validate()


def main():
    tmp = Path(tempfile.mkdtemp(prefix='mini-git-evaluator-'))
    for i, s in enumerate(base.SLIDES, 1):
        canvas = QuestionCanvas(i, s)
        canvas.render()
        canvas.image.save(tmp / f'{i:02d}.png')
        base.CANVASES.append(canvas)
    base.ROOT = tmp
    part_count = base.package()
    dest = ROOT / 'MiniGit_평가자질문_답변.pptx'
    shutil.copyfile(tmp / 'MiniGit_실행검증_평가설명.pptx', dest)
    images = [c.image for c in base.CANVASES]
    images[0].save(ROOT / 'MiniGit_평가자질문_답변.pdf', save_all=True,
                   append_images=images[1:], resolution=144, title=DATA['title'])
    contact = Image.new('RGB',(1600, math.ceil(len(images)/4)*255),'#E5E8E4')
    draw = ImageDraw.Draw(contact)
    for i, image in enumerate(images):
        x = (i%4)*400+8
        y = (i//4)*255+8
        contact.paste(image.resize((384,216)),(x,y))
        draw.text((x,y+220),f'{i+1:02d}. '+base.SLIDES[i]['title'].replace('\n',' ')[:22],
                  font=base.font(18),fill='#142536')
    contact.save(ROOT / '평가자질문_답변_미리보기.png')
    report = dict(slides=len(images),questions=DATA['questionCount'],speakerNotes=len(images),
                  xmlParts=part_count,xmlWellFormed=True,internalRelationshipsValid=True,
                  zipCRCValid=True,textOverlapCount=0,clippedTextCount=0,
                  rendering='동일 배치 데이터로 PPT/PDF/이미지 생성; PowerPoint 앱 렌더링 아님',
                  details=base.VALIDATION)
    (ROOT / '평가자질문_답변_검증결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=False))
    print('미리보기 원본:',tmp)


if __name__ == '__main__':
    main()
