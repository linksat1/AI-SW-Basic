"""검증된 발표 콘텐츠로 편집 가능한 PPTX와 동일 레이아웃의 PDF를 생성한다.

PowerPoint 파일은 표준 OOXML로 작성하며 외부 변환기 없이 생성한다.
Pillow는 미리보기/PDF 렌더링에만 사용한다. 과제 프로그램의 의존성이 아니다.
"""
import json
import math
import posixpath
import re
from pathlib import Path
from xml.sax.saxutils import escape
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'deck_content.json').read_text())
SLIDES = DATA['slides']
W, H, EMU = 1920, 1080, 6350
C = dict(navy='142536', teal='168B82', ivory='F5F2EA', gold='E9B55B',
         white='FFFFFF', muted='566979', line='D7DFDB', surface='EBEEE8')
FONT = '/System/Library/Fonts/AppleSDGothicNeo.ttc'
MONO = '/System/Library/Fonts/Menlo.ttc'
NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')
XML = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
RELBASE = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
BLANK = ('<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
         '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
         '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>')
CANVASES = []
VALIDATION = []


def font(size, bold=False, mono=False):
    return ImageFont.truetype(MONO if mono else FONT, round(size), index=0 if mono else 6 if bold else 0)


def wrap(text, size, width, bold=False, mono=False):
    f = font(size, bold, mono)
    result = []
    for paragraph in text.split('\n'):
        line = ''
        for char in paragraph:
            if line and f.getlength(line + char) > width:
                result.append(line.rstrip())
                line = char.lstrip()
            else:
                line += char
        result.append(line)
    return result


class Canvas:
    def __init__(self, index, slide):
        self.index, self.slide = index, slide
        self.dark = slide['kind'] in ('cover', 'closing')
        self.bg = C['navy'] if self.dark else C['ivory']
        self.fg = C['white'] if self.dark else C['navy']
        self.image = Image.new('RGB', (W, H), '#' + self.bg)
        self.draw = ImageDraw.Draw(self.image)
        self.parts, self.elements = [], []
        self.next_id = 2
        self.compact = False
        self.content_scale = 1
        self.content_top = 255

    def content_y(self, y):
        return self.content_top + (y-self.content_top)*self.content_scale

    def ident(self):
        value = self.next_id
        self.next_id += 1
        return value

    def geometry(self, x, y, w, h):
        return (f'<a:xfrm><a:off x="{round(x*EMU)}" y="{round(y*EMU)}"/>'
                f'<a:ext cx="{round(w*EMU)}" cy="{round(h*EMU)}"/></a:xfrm>')

    def shape(self, x, y, w, h, fill, geom='rect', stroke=None):
        if self.compact:
            y, h = self.content_y(y), h*self.content_scale
        sid = self.ident()
        paint = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
        line = (f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{stroke}"/></a:solidFill></a:ln>'
                if stroke else '<a:ln><a:noFill/></a:ln>')
        self.parts.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Shape {sid}"/>'
                          '<p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr>' +
                          self.geometry(x,y,w,h) + f'<a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>' +
                          paint + line + '</p:spPr></p:sp>')
        box = (x,y,x+w,y+h)
        if geom == 'ellipse':
            self.draw.ellipse(box, fill='#'+fill, outline='#'+stroke if stroke else None, width=2)
        elif geom == 'roundRect':
            self.draw.rounded_rectangle(box, radius=18, fill='#'+fill,
                                        outline='#'+stroke if stroke else None, width=2)
        else:
            self.draw.rectangle(box, fill='#'+fill, outline='#'+stroke if stroke else None, width=2)
        self.elements.append(dict(type='shape',id=sid,x=x,y=y,w=w,h=h))

    def text(self, text, x, y, w, h, size=38, color=None, bold=False, mono=False, center=False):
        if self.compact:
            y, h = self.content_y(y), h*self.content_scale
            size = max(18, round(size*math.sqrt(self.content_scale)))
        color = color or self.fg
        original_size = size
        # Menlo에는 한글 글리프가 없으므로 혼합 문장의 미리보기는 한글 폰트로 그린다.
        render_mono = mono and not any('\uac00' <= ch <= '\ud7a3' for ch in text)
        lines = wrap(text,size,w,bold,render_mono)
        while len(lines)*size*1.3 > h and size > 15:
            size -= 1
            lines = wrap(text,size,w,bold,render_mono)
        assert len(lines)*size*1.3 <= h, (self.index,text,size,h)
        sid = self.ident()
        paragraphs = []
        for line in lines:
            paragraphs.append(f'<a:p><a:pPr algn="{"ctr" if center else "l"}"><a:lnSpc>'
                              f'<a:spcPts val="{round(size*1.3*50)}"/></a:lnSpc></a:pPr>'
                              f'<a:r><a:rPr lang="ko-KR" sz="{round(size*50)}" b="{int(bold)}">'
                              f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
                              f'<a:latin typeface="{"Menlo" if mono else "Arial"}"/>'
                              '<a:ea typeface="Malgun Gothic"/><a:cs typeface="Arial"/></a:rPr>'
                              f'<a:t xml:space="preserve">{escape(line)}</a:t></a:r>'
                              f'<a:endParaRPr lang="ko-KR" sz="{round(size*50)}"/></a:p>')
        self.parts.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Text {sid}"/>'
                          '<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr>' +
                          self.geometry(x,y,w,h) + '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
                          '<a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody>'
                          '<a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t">'
                          '<a:noAutofit/></a:bodyPr><a:lstStyle/>' + ''.join(paragraphs) +
                          '</p:txBody></p:sp>')
        f = font(size,bold,render_mono)
        for i,line in enumerate(lines):
            dx = (w-f.getlength(line))/2 if center else 0
            self.draw.text((x+dx,y+i*size*1.3),line,font=f,fill='#'+color)
        self.elements.append(dict(type='text',id=sid,x=x,y=y,w=w,h=h,
                                  fontPx=size,originalFontPx=original_size,text=text))

    def edge(self, x1, y1, x2, y2, color=None, arrow=False, width=5):
        if self.compact:
            y1, y2 = self.content_y(y1), self.content_y(y2)
        color = color or C['teal']
        sid = self.ident()
        x,y = min(x1,x2), min(y1,y2)
        w,h = max(abs(x2-x1),1), max(abs(y2-y1),1)
        flip = f' flipH="{int(x2<x1)}" flipV="{int(y2<y1)}"'
        xf = self.geometry(x,y,w,h).replace('<a:xfrm>', '<a:xfrm'+flip+'>')
        self.parts.append(f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{sid}" name="Edge {sid}"/>'
                          '<p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr><p:spPr>' + xf +
                          '<a:prstGeom prst="line"><a:avLst/></a:prstGeom>'
                          f'<a:ln w="{round(width*EMU)}"><a:solidFill><a:srgbClr val="{color}"/>'
                          '</a:solidFill>' + ('<a:tailEnd type="triangle" w="med" len="med"/>' if arrow else '') +
                          '</a:ln></p:spPr></p:cxnSp>')
        self.draw.line((x1,y1,x2,y2),fill='#'+color,width=width)
        if arrow:
            angle=math.atan2(y2-y1,x2-x1)
            points=[(x2,y2)]
            for sign in (-1,1):
                points.append((x2-18*math.cos(angle)+sign*9*math.sin(angle),
                               y2-18*math.sin(angle)-sign*9*math.cos(angle)))
            self.draw.polygon(points,fill='#'+color)
        self.elements.append(dict(type='edge',id=sid,x=x,y=y,w=w,h=h))

    def node(self, label, x, y, fill=None, w=210, h=100):
        self.shape(x,y,w,h,fill or C['teal'],'roundRect')
        self.text(label,x+10,y+22,w-20,h-26,38,C['white'],True,center=True)

    def block(self, block, x, y, w, h, size=37, fill=None):
        if fill:
            self.shape(x,y,w,h,fill,'roundRect')
        pad = 24 if fill else 0
        self.text(block['label'],x+pad,y+pad,w-2*pad,52,29,
                  C['gold'] if self.dark else C['teal'],True)
        self.text(block['text'],x+pad,y+pad+62,w-2*pad,h-2*pad-62,size,
                  self.fg)

    def render(self):
        s=self.slide
        self.shape(80,65,70,8,C['gold'] if self.dark else C['teal'])
        self.text(s['section']+'  /  B3-2 MINI GIT',170,50,1400,45,25,
                  C['gold'] if self.dark else C['teal'],True)
        self.text(f'{self.index:02d} / {len(SLIDES):02d}',1650,50,190,45,25,
                  C['white'] if self.dark else C['muted'],center=True)
        # 설명 전체의 실제 행 수에 맞춰 같은 페이지 안의 공간을 배분한다.
        execution = s.get('execution')
        note_size = 24 if s['kind']=='dag' else 26 if execution else 30
        note_text = re.sub(r'\s+', ' ', s['notes']).strip()
        note_height = len(wrap(note_text,note_size,1690))*note_size*1.3
        execution_text = ''
        execution_height = 0
        if execution:
            commands = execution['commands'].replace('\n', '  →  ')
            execution_text = (execution['environment'] + '\n' + commands +
                              '\n확인: ' + execution['expected'])
            execution_height = len(wrap(execution_text,26,1690))*26*1.3 + 12
        note_top = 910 - note_height - execution_height - 68
        self.content_top = 125 if s['kind']=='cover' else 255
        self.content_scale = (note_top-24-self.content_top)/(890-self.content_top)
        if s['kind']=='cover':
            self.compact = True
            self.text(s['title'],95,195,1100,300,100,bold=True)
            self.text(s['takeaway'],100,530,1080,135,47,C['gold'])
            for i,b in enumerate(s['blocks']):
                self.block(b,100+i*565,735,520,150,32)
            self.edge(1325,360,1540,230,C['gold'],True)
            self.edge(1325,360,1540,490,C['teal'],True)
            self.node('COMMIT',1210,310,C['teal'],w=225)
            self.node('LOG',1540,180,C['gold'])
            self.node('SEARCH',1540,440,C['teal'])
        else:
            self.text(s['title'],80,125,1760,95,64,bold=True)
            self.compact = True
            blocks=s['blocks']
            if s['kind']=='closing':
                self.block(blocks[0],90,285,1150,550,45)
                self.block(blocks[1],1320,330,510,460,39)
            elif s['kind']=='tree':
                self.shape(80,255,1760,635,C['navy'],'roundRect')
                self.text(blocks[0]['label'],115,282,1650,50,32,C['gold'],True)
                self.text(blocks[0]['text'],115,345,1650,505,36,C['white'],mono=True)
            elif s['kind']=='terminal':
                self.shape(80,255,1120,625,C['navy'],'roundRect')
                self.text(blocks[0]['label'],115,280,1040,60,30,C['gold'],True)
                self.text(blocks[0]['text'],115,360,1040,475,39,C['white'],mono=True)
                n=len(blocks)-1
                for i,b in enumerate(blocks[1:]):
                    self.block(b,1260,280+i*(590/n),580,570/n-15,36)
            elif s['kind']=='metrics':
                self.shape(80,270,1130,210,C['navy'],'roundRect')
                self.text(blocks[0]['label'],110,292,1070,50,30,C['gold'],True)
                self.text(blocks[0]['text'],110,370,1070,80,32,C['white'],mono=True)
                self.block(blocks[2],90,560,1100,295,39)
                self.text('15',1310,260,450,210,190,C['teal'],True,center=True)
                self.text('TESTS PASSED',1290,520,480,70,40,C['teal'],True,center=True)
                self.text(blocks[1]['text'],1300,650,460,160,47,center=True)
            elif s['kind']=='table':
                self.text(blocks[0]['label'],90,255,1710,60,31,C['teal'],True)
                rows=blocks[0]['text'].split('\n')
                row_h=min(82,550/len(rows))
                for i,row in enumerate(rows):
                    y=330+i*row_h
                    self.shape(80,y,1760,row_h-5,C['white'] if i%2==0 else C['surface'],'roundRect')
                    self.text(row,105,y+12,1710,row_h-14,33)
            elif s['kind'] in ('dag','branches','kahn','bfs','diamond','ancestors','merge','index'):
                self.diagram(s['kind'])
                n=len(blocks)
                for i,b in enumerate(blocks):
                    self.block(b,1030,265+i*(625/n),790,610/n-10,35)
            elif s['kind']=='pipeline':
                for i,b in enumerate(blocks):
                    x=80+i*605
                    self.shape(x,360,550,365,C['white'],'roundRect',C['line'])
                    self.block(b,x+28,390,494,300,37)
                    if i<2:
                        self.edge(x+555,535,x+594,535,arrow=True,width=6)
            else:
                n=len(blocks)
                if n==3:
                    for i,b in enumerate(blocks):
                        self.block(b,80+i*605,330,550,450,40,C['surface'])
                else:
                    for i,b in enumerate(blocks):
                        self.block(b,80+i*910,290,850,575,40,C['surface'])
        self.compact = False
        self.shape(80,note_top,1760,note_height+execution_height+68,'234456' if self.dark else C['surface'],'roundRect')
        self.text('실행 확인 · 명령은 한 줄씩 입력' if execution else '상세 설명',115,note_top+12,1690,35,24,
                  C['gold'] if self.dark else C['teal'],True)
        if execution:
            self.text(execution_text,115,note_top+54,1690,execution_height-12,26)
        self.text(note_text,115,note_top+54+execution_height,1690,note_height,note_size)
        if s['kind']!='cover':
            self.shape(80,935,1760,80,C['teal'] if not self.dark else '234456','roundRect')
            self.text(s['takeaway'],105,956,1700,55,32,C['white'],True)
        self.text('근거: '+s['source'],80,1033,1760,36,20,
                  C['line'] if self.dark else C['muted'])
        for e in self.elements:
            assert e['x']>=0 and e['y']>=0 and e['x']+e['w']<=W and e['y']+e['h']<=H, (self.index,e)
        texts=[e for e in self.elements if e['type']=='text']
        overlaps=[]
        for i,a in enumerate(texts):
            for b in texts[i+1:]:
                ix=min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])
                iy=min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])
                if ix>3 and iy>3:
                    overlaps.append([a['id'],b['id']])
        assert not overlaps, (self.index,overlaps)
        VALIDATION.append(dict(slide=self.index,title=s['title'],elements=len(self.elements),
                               textClipping=False,textOverlaps=overlaps,outOfBounds=False))

    def diagram(self, kind):
        self.shape(80,265,850,625,C['white'],'roundRect',C['line'])
        self.text('한눈에 이해하기',110,285,780,60,30,C['teal'],True)
        if kind in ('dag','kahn','bfs','ancestors','diamond'):
            diamond=kind in ('ancestors','diamond')
            labels=['000000','000001','000002','000003'] if kind=='diamond' else ['A','B','C','D']
            if diamond:
                places=[(190,530),(440,390),(440,670),(690,530)]
                for a,b in [(0,1),(0,2),(1,3),(2,3)]:
                    x1,y1=places[a];x2,y2=places[b]
                    if kind=='ancestors':
                        x1,y1,x2,y2=x2,y2,x1,y1
                    self.edge(x1+80,y1+50,x2+80,y2+50,
                              C['gold'] if kind=='diamond' and (a,b) in ((0,1),(1,3)) else C['teal'],
                              arrow=kind=='ancestors')
                for i,(x,y) in enumerate(places):
                    self.node(labels[i],x,y,w=170)
                self.text('테스트용 다중 부모 그래프',120,815,760,45,27,C['muted'],center=True)
            else:
                places=[(160,540),(565,405),(565,675)]
                if kind=='dag':
                    self.text('생성 순서: A 먼저, 그다음 B와 C',120,360,760,45,30,C['muted'],center=True)
                for i in (1,2):
                    if kind=='dag':
                        self.edge(places[i][0],places[i][1]+50,places[0][0]+210,places[0][1]+50,arrow=True)
                    else:
                        self.edge(places[0][0]+210,places[0][1]+50,places[i][0],places[i][1]+50,
                                  arrow=kind=='kahn')
                for i,(x,y) in enumerate(places):
                    self.node(labels[i],x,y)
                caption={'dag':'B → A, C → A: 자식에서 부모로',
                         'kahn':'A를 먼저 출력 → B와 C가 후보',
                         'bfs':'B ↔ A ↔ C: 간선 2개'}[kind]
                self.text(caption,120,805,760,50,30,C['muted'],center=True)
        elif kind=='branches':
            self.node('A',160,590);self.node('B',610,590)
            self.edge(610,640,370,640,arrow=True)
            self.text('main',175,395,200,65,46,C['teal'],True,center=True)
            self.edge(265,475,265,580,arrow=True)
            self.text('feature',615,395,200,65,46,C['teal'],True,center=True)
            self.edge(715,475,715,580,arrow=True)
            self.text('現在 브랜치: feature'.replace('現在','현재'),150,805,650,50,32,C['muted'],center=True)
        elif kind=='merge':
            stages=[('[4, 1, 3, 2]',280,380,440),('[4, 1]   [3, 2]',140,490,730),
                    ('[4] [1] [3] [2]',140,595,730),('[1, 4]   [2, 3]',140,700,730),
                    ('[1, 2, 3, 4]',280,805,440)]
            for label,x,y,w in stages:
                self.text(label,x,y,w,58,42,C['teal'] if y==805 else C['navy'],True,center=True)
        elif kind=='index':
            for i,(label,value) in enumerate([('login','[B]'),('feature','[B, C]'),('Alice Kim','[A, B, C]')]):
                y=405+i*140
                self.node(label,130,y,w=295)
                self.edge(430,y+50,535,y+50,arrow=True)
                self.text(value,560,y+20,300,80,45,C['navy'],True)

    def xml(self):
        return XML+f'<p:sld {NS}><p:cSld name="{escape(self.slide["title"].replace(chr(10)," "))}">' \
            f'<p:bg><p:bgPr><a:solidFill><a:srgbClr val="{self.bg}"/></a:solidFill><a:effectLst/>' \
            '</p:bgPr></p:bg><p:spTree>'+BLANK+''.join(self.parts)+ \
            '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'


def relationships(items):
    return XML+'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(
        f'<Relationship Id="rId{i}" Type="{RELBASE}{kind}" Target="{target}"/>'
        for i,kind,target in items)+'</Relationships>'


def notes_xml(slide, number):
    text='발표 '+str(number)+' · '+slide['title'].replace('\n',' ')+'\n\n'+slide['notes']+'\n\n근거: '+slide['source']
    paras=''.join('<a:p><a:r><a:rPr lang="ko-KR" sz="1800"/><a:t>'+escape(line)+
                  '</a:t></a:r></a:p>' for line in text.split('\n'))
    return XML+f'<p:notes {NS}><p:cSld><p:spTree>'+BLANK+ \
        '<p:sp><p:nvSpPr><p:cNvPr id="2" name="Speaker Notes"/><p:cNvSpPr/>' \
        '<p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr><p:spPr/>' \
        '<p:txBody><a:bodyPr/><a:lstStyle/>'+paras+ \
        '</p:txBody></p:sp></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:notes>'


def package():
    entries={}
    def put(name,content): entries[name]=content
    put('_rels/.rels',relationships([(1,'officeDocument','ppt/presentation.xml'),
                                    (2,'metadata/core-properties','docProps/core.xml'),
                                    (3,'extended-properties','docProps/app.xml')]).replace(
        RELBASE+'metadata/core-properties','http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties'))
    put('docProps/core.xml',XML+'<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>'+escape(DATA['title'])+
        '</dc:title><dc:subject>Mini Git 초보자 실행·검증·평가 발표</dc:subject>'
        '<dc:creator>Mini Git Project</dc:creator><dc:description>26장, 편집 가능한 도형·텍스트와 발표자 노트</dc:description>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">2026-10-09T00:00:00Z</dcterms:created></cp:coreProperties>')
    put('docProps/app.xml',XML+'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        f'<Application>Mini Git presentation builder</Application><PresentationFormat>Widescreen</PresentationFormat>'
        f'<Slides>{len(SLIDES)}</Slides><Notes>{len(SLIDES)}</Notes></Properties>')
    ids=''.join(f'<p:sldId id="{256+i}" r:id="rId{i+3}"/>' for i in range(len(SLIDES)))
    put('ppt/presentation.xml',XML+f'<p:presentation {NS}><p:sldMasterIdLst>'
        '<p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
        '<p:notesMasterIdLst><p:notesMasterId r:id="rId2"/></p:notesMasterIdLst>'
        '<p:sldIdLst>'+ids+'</p:sldIdLst>'
        f'<p:sldSz cx="{W*EMU}" cy="{H*EMU}" type="custom"/>'
        '<p:notesSz cx="6858000" cy="9144000"/><p:defaultTextStyle/></p:presentation>')
    put('ppt/_rels/presentation.xml.rels',relationships([(1,'slideMaster','slideMasters/slideMaster1.xml'),
        (2,'notesMaster','notesMasters/notesMaster1.xml')]+[(i+3,'slide',f'slides/slide{i+1}.xml') for i in range(len(SLIDES))]))
    clr='<p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/>'
    put('ppt/slideMasters/slideMaster1.xml',XML+f'<p:sldMaster {NS}><p:cSld><p:spTree>'+BLANK+
        '</p:spTree></p:cSld>'+clr+'<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/>'
        '</p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>')
    put('ppt/slideMasters/_rels/slideMaster1.xml.rels',relationships([(1,'slideLayout','../slideLayouts/slideLayout1.xml'),(2,'theme','../theme/theme1.xml')]))
    put('ppt/slideLayouts/slideLayout1.xml',XML+f'<p:sldLayout {NS} type="blank" preserve="1"><p:cSld name="Blank"><p:spTree>'+BLANK+'</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')
    put('ppt/slideLayouts/_rels/slideLayout1.xml.rels',relationships([(1,'slideMaster','../slideMasters/slideMaster1.xml')]))
    put('ppt/notesMasters/notesMaster1.xml',XML+f'<p:notesMaster {NS}><p:cSld><p:spTree>'+BLANK+
        '<p:sp><p:nvSpPr><p:cNvPr id="2" name="Notes Body"/><p:cNvSpPr/><p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr>'
        '<p:spPr><a:xfrm><a:off x="685800" y="3505200"/><a:ext cx="5486400" cy="4800600"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/><a:p/>'
        '</p:txBody></p:sp></p:spTree></p:cSld>'+clr+'<p:notesStyle/></p:notesMaster>')
    put('ppt/notesMasters/_rels/notesMaster1.xml.rels',relationships([(1,'theme','../theme/theme1.xml')]))
    colors=dict(dk1=C['navy'],lt1=C['white'],dk2=C['muted'],lt2=C['ivory'],accent1=C['teal'],accent2=C['gold'],accent3='42677E',accent4='85A99C',accent5='CCA66F',accent6='77919C',hlink=C['teal'],folHlink='765A91')
    theme=XML+'<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Mini Git"><a:themeElements><a:clrScheme name="Mini Git">'+''.join(
        f'<a:{role}><a:srgbClr val="{value}"/></a:{role}>' for role,value in colors.items())+'</a:clrScheme>'
    theme+='<a:fontScheme name="Korean Learning">'+''.join(f'<a:{role}><a:latin typeface="Arial"/><a:ea typeface="Malgun Gothic"/><a:cs typeface="Arial"/></a:{role}>' for role in ('majorFont','minorFont'))+'</a:fontScheme>'
    fill='<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    theme+='<a:fmtScheme name="Simple"><a:fillStyleLst>'+fill*3+'</a:fillStyleLst><a:lnStyleLst>'+('<a:ln w="12700">'+fill+'<a:prstDash val="solid"/></a:ln>')*3+'</a:lnStyleLst><a:effectStyleLst>'+('<a:effectStyle><a:effectLst/></a:effectStyle>')*3+'</a:effectStyleLst><a:bgFillStyleLst>'+fill*3+'</a:bgFillStyleLst></a:fmtScheme></a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/></a:theme>'
    put('ppt/theme/theme1.xml',theme)
    for i,c in enumerate(CANVASES,1):
        put(f'ppt/slides/slide{i}.xml',c.xml())
        put(f'ppt/slides/_rels/slide{i}.xml.rels',relationships([(1,'slideLayout','../slideLayouts/slideLayout1.xml'),(2,'notesSlide',f'../notesSlides/notesSlide{i}.xml')]))
        put(f'ppt/notesSlides/notesSlide{i}.xml',notes_xml(c.slide,i))
        put(f'ppt/notesSlides/_rels/notesSlide{i}.xml.rels',relationships([(1,'notesMaster','../notesMasters/notesMaster1.xml'),(2,'slide',f'../slides/slide{i}.xml')]))
    content_types={'ppt/presentation.xml':'presentation','ppt/slideMasters/slideMaster1.xml':'slideMaster',
                   'ppt/slideLayouts/slideLayout1.xml':'slideLayout','ppt/notesMasters/notesMaster1.xml':'notesMaster'}
    for i in range(1,len(SLIDES)+1):
        content_types[f'ppt/slides/slide{i}.xml']='slide'
        content_types[f'ppt/notesSlides/notesSlide{i}.xml']='notesSlide'
    ct=XML+'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    ct+='<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    ct+='<Default Extension="xml" ContentType="application/xml"/>'
    ct+=''.join(f'<Override PartName="/{path}" ContentType="application/vnd.openxmlformats-officedocument.presentationml.{kind}+xml"/>' for path,kind in content_types.items())
    ct+='<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
    ct+='<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
    ct+='<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>'
    put('[Content_Types].xml',ct)
    for name,content in entries.items():
        ET.fromstring(content)
        if name.endswith('.rels'):
            base=posixpath.dirname(posixpath.dirname(name)) if name!='_rels/.rels' else ''
            for relation in ET.fromstring(content):
                target=posixpath.normpath(posixpath.join(base,relation.attrib['Target']))
                assert target in entries, (name,target)
    dest=ROOT/'MiniGit_실행검증_평가설명.pptx'
    with ZipFile(dest,'w',ZIP_DEFLATED) as z:
        for name,content in entries.items():
            z.writestr(name,content.encode('utf-8'))
    with ZipFile(dest) as z:
        assert z.testzip() is None
    return len(entries)


if __name__=='__main__':
    previews=ROOT/'미리보기'
    previews.mkdir(exist_ok=True)
    for i,slide in enumerate(SLIDES,1):
        canvas=Canvas(i,slide)
        canvas.render()
        canvas.image.save(previews/f'{i:02d}.png')
        CANVASES.append(canvas)
    part_count=package()
    images=[c.image for c in CANVASES]
    images[0].save(ROOT/'MiniGit_실행검증_평가설명.pdf',save_all=True,
                   append_images=images[1:],resolution=144,title=DATA['title'])
    contact=Image.new('RGB',(1600,math.ceil(len(images)/4)*255),'#E5E8E4')
    draw=ImageDraw.Draw(contact)
    for i,image in enumerate(images):
        thumb=image.resize((384,216))
        x=(i%4)*400+8;y=(i//4)*255+8
        contact.paste(thumb,(x,y))
        draw.text((x,y+220),f'{i+1:02d}. '+SLIDES[i]['title'].replace('\n',' ')[:22],font=font(18),fill='#142536')
    contact.save(ROOT/'전체슬라이드_미리보기.png')
    notes=[]
    for i,s in enumerate(DATA['slides'],1):
        notes.append(f'{i:02d}. {s["title"].replace(chr(10)," ")}\n핵심: {s["takeaway"]}\n\n발표자 노트\n{s["notes"]}\n\n근거: {s["source"]}')
    (ROOT/'발표자_설명노트.txt').write_text('\n\n'+'\n\n'+'\n\n'.join(notes))
    report=dict(slides=len(SLIDES),speakerNotes=len(SLIDES),ooxmlParts=part_count,
                xmlWellFormed=True,internalRelationshipsValid=True,zipCRCValid=True,
                allSlideBoundsValid=True,textOverlapCount=0,clippedTextCount=0,
                rendering='동일한 레이아웃 데이터로 PPTX와 Pillow 미리보기/PDF 생성; PowerPoint 앱 렌더링 아님',
                details=VALIDATION)
    (ROOT/'발표자료_검증결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=False))
