# Teacher Handout PDF Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a 5+ page teacher handout PDF from `东方财富.jpg` with教材精读型版式、目录编号和学习重点框，并输出可直接交付的 PDF 文件。

**Architecture:** Use a small Python generator script with ReportLab to assemble a multi-page printable PDF directly from the source image. The script will split responsibility into page layout helpers, image placement logic, and lecture-text content blocks so the output stays stable and easy to revise. Validation will rely on running the generator and inspecting PDF page count and file creation.

**Tech Stack:** Python 3, Pillow, ReportLab

---

## File Structure

- Create: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py` — main PDF generator script
- Create: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/output/teacher_handout.pdf` — generated final PDF
- Modify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/docs/superpowers/specs/2026-05-12-teacher-handout-design.md` only if implementation reveals a necessary spec clarification
- Reference source: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/东方财富.jpg`

### Task 1: 建立生成脚本骨架

**Files:**
- Create: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`

- [ ] **Step 1: 写一个最小失败验证脚本**

```python
from pathlib import Path

SOURCE = Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao/东方财富.jpg')
OUTPUT_DIR = Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao/output')
OUTPUT_FILE = OUTPUT_DIR / 'teacher_handout.pdf'

if not SOURCE.exists():
    raise FileNotFoundError(SOURCE)

raise RuntimeError('generator not implemented yet')
```

- [ ] **Step 2: 运行脚本确认按预期失败**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`
Expected: FAIL with `RuntimeError: generator not implemented yet`

- [ ] **Step 3: 改为可运行的生成脚本骨架**

```python
from pathlib import Path

SOURCE = Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao/东方财富.jpg')
OUTPUT_DIR = Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao/output')
OUTPUT_FILE = OUTPUT_DIR / 'teacher_handout.pdf'


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f'Source ready: {SOURCE.name}')
    print(f'Output target: {OUTPUT_FILE}')


if __name__ == '__main__':
    main()
```

- [ ] **Step 4: 运行脚本确认骨架可执行**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`
Expected: PASS and print `Source ready: 东方财富.jpg`

### Task 2: 定义讲义内容与页面规划

**Files:**
- Modify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`

- [ ] **Step 1: 先加入失败断言，要求页数至少 6 页**

```python
SECTIONS = []


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    if len(SECTIONS) < 6:
        raise ValueError('need at least 6 sections for full handout')
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f'Section count: {len(SECTIONS)}')
```

- [ ] **Step 2: 运行脚本确认页数规划校验失败**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`
Expected: FAIL with `ValueError: need at least 6 sections for full handout`

- [ ] **Step 3: 填入完整讲义章节数据**

```python
SECTIONS = [
    {
        'kind': 'cover',
        'number': '1',
        'title': '东方财富软件看盘讲义',
        'subtitle': '教师授课稿版',
        'focus': '本讲义帮助学生先建立界面整体认知，再逐步进入看盘观察。',
        'points': [
            '认识东方财富软件的核心功能区。',
            '建立“先看整体、再看细节”的课堂观察顺序。',
        ],
    },
    {
        'kind': 'toc',
        'number': '2',
        'title': '目录',
        'items': [
            '1 课程导入与学习目标',
            '2 软件界面整体认识',
            '2.1 首页结构观察',
            '2.2 自选股区域识别',
            '2.3 行情窗口解读',
            '3 课堂总结',
        ],
    },
    {
        'kind': 'content',
        'number': '2.1',
        'title': '软件界面整体认识',
        'focus': '先带学生从全图观察界面布局，避免一开始陷入局部按钮。',
        'speech': [
            '上课时先让学生看整张界面图，不急着解释每个按钮。',
            '可以先提问：这个界面大概分成几个信息区域？',
            '教师要引导学生建立版面分区意识，这是后面学习的基础。',
        ],
    },
    {
        'kind': 'content',
        'number': '2.2',
        'title': '首页结构观察',
        'focus': '重点说明首页中不同信息区的排列逻辑与使用目的。',
        'speech': [
            '这里建议老师从上到下、从左到右带学生扫读页面。',
            '讲解时强调：导航、行情、列表、功能入口往往承担不同任务。',
            '不要只讲“在哪里”，还要讲“为什么放在这里”。',
        ],
    },
    {
        'kind': 'content',
        'number': '2.3',
        'title': '自选股区域识别',
        'focus': '帮助学生理解自选股区域是后续盯盘和复盘的重要入口。',
        'speech': [
            '老师可以提示学生关注自选股区域中的名称、涨跌、排序等信息。',
            '如果学生是初学者，要强调先看字段含义，再谈使用技巧。',
            '这一部分可以顺带建立“信息筛选”的初步意识。',
        ],
    },
    {
        'kind': 'content',
        'number': '2.4',
        'title': '行情窗口解读',
        'focus': '让学生知道行情窗口不只是数字展示，更是判断节奏的重要位置。',
        'speech': [
            '老师讲这一页时，可以提醒学生同时观察价格、涨跌幅和成交相关信息。',
            '如果只看一个数字，学生容易形成片面理解。',
            '因此要强调“联动观察”的习惯。',
        ],
    },
    {
        'kind': 'summary',
        'number': '3',
        'title': '课末小结',
        'focus': '把本节内容收束到“会看区域、会找入口、会抓重点”三个层面。',
        'speech': [
            '今天这节课不是要求学生马上熟练操作，而是先把界面看懂。',
            '只要学生能说出主要区域的用途，就说明本节课达到了基础目标。',
            '后续再进入更细的指标和功能学习，会更加顺畅。',
        ],
    },
]
```

- [ ] **Step 4: 运行脚本确认内容数据加载成功**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`
Expected: PASS and print `Section count: 7`

### Task 3: 实现基础版式与公用绘制函数

**Files:**
- Modify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`

- [ ] **Step 1: 先调用未实现的绘制函数，让程序失败**

```python
from reportlab.pdfgen import canvas


def build_pdf() -> None:
    pdf = canvas.Canvas(str(OUTPUT_FILE))
    draw_page_frame(pdf, '示例标题')
    pdf.save()
```

- [ ] **Step 2: 运行脚本确认缺少绘制函数导致失败**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`
Expected: FAIL with `NameError: name 'draw_page_frame' is not defined`

- [ ] **Step 3: 实现页面框架、标题、重点框、正文段落工具函数**

```python
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 18 * mm
ACCENT = colors.HexColor('#1f4b99')
FOCUS_BG = colors.HexColor('#eef4ff')
TEXT = colors.HexColor('#222222')
styles = getSampleStyleSheet()
body_style = ParagraphStyle(
    'BodyCN',
    parent=styles['BodyText'],
    fontName='Helvetica',
    fontSize=11,
    leading=17,
    textColor=TEXT,
)
heading_style = ParagraphStyle(
    'HeadingCN',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=24,
    textColor=ACCENT,
)


def draw_page_frame(pdf, title: str, number: str) -> None:
    pdf.setStrokeColor(ACCENT)
    pdf.setLineWidth(1)
    pdf.rect(MARGIN, MARGIN, PAGE_WIDTH - 2 * MARGIN, PAGE_HEIGHT - 2 * MARGIN)
    pdf.setFillColor(ACCENT)
    pdf.rect(MARGIN, PAGE_HEIGHT - 34 * mm, PAGE_WIDTH - 2 * MARGIN, 14 * mm, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.setFont('Helvetica-Bold', 18)
    pdf.drawString(MARGIN + 8 * mm, PAGE_HEIGHT - 25 * mm, f'{number} {title}')


def draw_paragraph(pdf, text: str, x: float, y: float, width: float, style: ParagraphStyle) -> float:
    paragraph = Paragraph(text, style)
    w, h = paragraph.wrap(width, PAGE_HEIGHT)
    paragraph.drawOn(pdf, x, y - h)
    return y - h - 4 * mm


def draw_focus_box(pdf, text: str, x: float, y: float, width: float) -> float:
    style = ParagraphStyle(
        'FocusCN',
        parent=body_style,
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=16,
        textColor=ACCENT,
    )
    paragraph = Paragraph(f'学习重点：{text}', style)
    w, h = paragraph.wrap(width - 10 * mm, PAGE_HEIGHT)
    pdf.setFillColor(FOCUS_BG)
    pdf.setStrokeColor(ACCENT)
    pdf.roundRect(x, y - h - 8 * mm, width, h + 8 * mm, 4 * mm, fill=1, stroke=1)
    paragraph.drawOn(pdf, x + 5 * mm, y - h - 4 * mm)
    return y - h - 12 * mm
```

- [ ] **Step 4: 运行脚本确认基础绘制函数可调用**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`
Expected: PASS and create a PDF file, even if still only one page

### Task 4: 实现图片缩放与多页排版逻辑

**Files:**
- Modify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`

- [ ] **Step 1: 先接入未实现的图片绘制函数**

```python

def render_section(pdf, section: dict) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    draw_source_image(pdf)
```

- [ ] **Step 2: 运行脚本确认图片函数缺失导致失败**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`
Expected: FAIL with `NameError: name 'draw_source_image' is not defined`

- [ ] **Step 3: 实现图片缩放、封面/目录/内容/总结页渲染逻辑**

```python
from PIL import Image
from reportlab.lib.utils import ImageReader


def draw_source_image(pdf, image_path: Path, x: float, y_top: float, max_width: float, max_height: float) -> float:
    with Image.open(image_path) as img:
        width, height = img.size
    scale = min(max_width / width, max_height / height)
    draw_width = width * scale
    draw_height = height * scale
    pdf.drawImage(ImageReader(str(image_path)), x, y_top - draw_height, width=draw_width, height=draw_height, preserveAspectRatio=True, mask='auto')
    return y_top - draw_height - 6 * mm


def render_cover(pdf, section: dict) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    y = PAGE_HEIGHT - 55 * mm
    y = draw_paragraph(pdf, section['subtitle'], MARGIN + 10 * mm, y, PAGE_WIDTH - 40 * mm, heading_style)
    y = draw_source_image(pdf, SOURCE, MARGIN + 22 * mm, y - 4 * mm, PAGE_WIDTH - 44 * mm, 105 * mm)
    for point in section['points']:
        y = draw_paragraph(pdf, f'• {point}', MARGIN + 12 * mm, y, PAGE_WIDTH - 42 * mm, body_style)
    draw_focus_box(pdf, section['focus'], MARGIN + 10 * mm, y - 2 * mm, PAGE_WIDTH - 40 * mm)


def render_toc(pdf, section: dict) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    y = PAGE_HEIGHT - 52 * mm
    for item in section['items']:
        y = draw_paragraph(pdf, item, MARGIN + 14 * mm, y, PAGE_WIDTH - 48 * mm, body_style)


def render_content(pdf, section: dict) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    y = PAGE_HEIGHT - 50 * mm
    y = draw_source_image(pdf, SOURCE, MARGIN + 12 * mm, y, 78 * mm, 132 * mm)
    text_x = MARGIN + 96 * mm
    text_width = PAGE_WIDTH - text_x - MARGIN - 8 * mm
    for line in section['speech']:
        y = draw_paragraph(pdf, line, text_x, y + 130 * mm, text_width, body_style)
    draw_focus_box(pdf, section['focus'], text_x, 78 * mm, text_width)


def render_summary(pdf, section: dict) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    y = PAGE_HEIGHT - 55 * mm
    y = draw_paragraph(pdf, '本节内容回顾', MARGIN + 10 * mm, y, PAGE_WIDTH - 40 * mm, heading_style)
    y = draw_source_image(pdf, SOURCE, MARGIN + 18 * mm, y - 2 * mm, 84 * mm, 118 * mm)
    for line in section['speech']:
        y = draw_paragraph(pdf, line, MARGIN + 110 * mm, y + 116 * mm, PAGE_WIDTH - 130 * mm, body_style)
    draw_focus_box(pdf, section['focus'], MARGIN + 10 * mm, 70 * mm, PAGE_WIDTH - 40 * mm)


def render_section(pdf, section: dict) -> None:
    kind = section['kind']
    if kind == 'cover':
        render_cover(pdf, section)
    elif kind == 'toc':
        render_toc(pdf, section)
    elif kind == 'content':
        render_content(pdf, section)
    elif kind == 'summary':
        render_summary(pdf, section)
    else:
        raise ValueError(f'unknown section kind: {kind}')
    pdf.showPage()
```

- [ ] **Step 4: 在主流程中循环渲染全部章节**

```python
from reportlab.pdfgen import canvas


def build_pdf() -> None:
    pdf = canvas.Canvas(str(OUTPUT_FILE), pagesize=A4)
    pdf.setTitle('东方财富教师讲义')
    for section in SECTIONS:
        render_section(pdf, section)
    pdf.save()
```

- [ ] **Step 5: 运行脚本确认生成多页 PDF**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`
Expected: PASS and create `/Users/tianxiang.yang/Desktop/yang/study/gupiao/output/teacher_handout.pdf`

### Task 5: 补齐教师讲义视觉层级与页脚信息

**Files:**
- Modify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`

- [ ] **Step 1: 先增加对页脚函数的调用，让程序失败**

```python

def render_section(pdf, section: dict) -> None:
    ...
    draw_footer(pdf, section['number'])
    pdf.showPage()
```

- [ ] **Step 2: 运行脚本确认缺少页脚函数导致失败**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`
Expected: FAIL with `NameError: name 'draw_footer' is not defined`

- [ ] **Step 3: 实现页脚、编号标签与教师讲义标识**

```python

def draw_footer(pdf, number: str) -> None:
    pdf.setStrokeColor(colors.HexColor('#b8c7e6'))
    pdf.line(MARGIN + 8 * mm, 18 * mm, PAGE_WIDTH - MARGIN - 8 * mm, 18 * mm)
    pdf.setFillColor(TEXT)
    pdf.setFont('Helvetica', 9)
    pdf.drawString(MARGIN + 8 * mm, 12 * mm, '教师讲义版｜东方财富界面导读')
    pdf.drawRightString(PAGE_WIDTH - MARGIN - 8 * mm, 12 * mm, f'章节编号 {number}')


def draw_section_badge(pdf, number: str, x: float, y: float) -> None:
    pdf.setFillColor(ACCENT)
    pdf.roundRect(x, y, 24 * mm, 10 * mm, 3 * mm, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.setFont('Helvetica-Bold', 10)
    pdf.drawCentredString(x + 12 * mm, y + 3.2 * mm, number)
```

- [ ] **Step 4: 在封面页和内容页中加入编号标签**

```python

def render_cover(pdf, section: dict) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    draw_section_badge(pdf, section['number'], PAGE_WIDTH - MARGIN - 34 * mm, PAGE_HEIGHT - 31 * mm)
    ...


def render_content(pdf, section: dict) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    draw_section_badge(pdf, section['number'], PAGE_WIDTH - MARGIN - 34 * mm, PAGE_HEIGHT - 31 * mm)
    ...
```

- [ ] **Step 5: 运行脚本确认视觉增强后仍可生成 PDF**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`
Expected: PASS and overwrite the PDF successfully

### Task 6: 验证 PDF 文件与页数要求

**Files:**
- Verify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/output/teacher_handout.pdf`

- [ ] **Step 1: 运行生成脚本，确保使用最终代码生成 PDF**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`
Expected: PASS and print completion info including output path

- [ ] **Step 2: 用 Python 检查 PDF 是否存在且页数达标**

Run: `python3 -c "from pathlib import Path; from PyPDF2 import PdfReader; pdf=Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao/output/teacher_handout.pdf'); print({'exists': pdf.exists(), 'pages': len(PdfReader(str(pdf)).pages)})"`
Expected: PASS and print `{'exists': True, 'pages': 7}` or any page count >= 6

- [ ] **Step 3: 记录最终交付物检查项**

```text
- 已生成 PDF
- PDF 页数不少于 5 页
- 含目录页
- 含教材式编号
- 含学习重点框
- 含教师授课稿式文字
- 图片为主、文字为辅
```

- [ ] **Step 4: 如目录中有 Python 语法检查能力，运行一次语法校验**

Run: `python3 -m py_compile /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`
Expected: PASS with no output
