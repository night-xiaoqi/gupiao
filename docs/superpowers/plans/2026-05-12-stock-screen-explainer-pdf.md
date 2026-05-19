# Stock Screen Explainer PDF Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a comparison-style PDF that uses `东方财富.jpg` to explain each visible stock-screen data area in plain Chinese with light stock-market context.

**Architecture:** Use a single Python script with Pillow and ReportLab to generate a 2–4 page PDF. The script will reuse the original screenshot, crop key regions, and render structured explanations area by area so the reader can match what they see on the screenshot with what each number or button means.

**Tech Stack:** Python 3, Pillow, ReportLab

---

## File Structure

- Create: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py` — main PDF generator for the explainer
- Create: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/output/stock_screen_explainer.pdf` — generated explanation PDF
- Reference source: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/东方财富.jpg`
- Reference spec: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/docs/superpowers/specs/2026-05-12-stock-screen-explainer-pdf-design.md`

### Task 1: 建立生成脚本骨架

**Files:**
- Create: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`

- [ ] **Step 1: 先写一个最小失败脚本**

```python
from pathlib import Path

SOURCE = Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao/东方财富.jpg')
OUTPUT_DIR = Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao/output')
OUTPUT_FILE = OUTPUT_DIR / 'stock_screen_explainer.pdf'

if not SOURCE.exists():
    raise FileNotFoundError(SOURCE)

raise RuntimeError('explainer generator not implemented yet')
```

- [ ] **Step 2: 运行脚本确认按预期失败**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`
Expected: FAIL with `RuntimeError: explainer generator not implemented yet`

- [ ] **Step 3: 改为可执行的脚本入口**

```python
from pathlib import Path

SOURCE = Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao/东方财富.jpg')
OUTPUT_DIR = Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao/output')
OUTPUT_FILE = OUTPUT_DIR / 'stock_screen_explainer.pdf'


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

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`
Expected: PASS and print `Source ready: 东方财富.jpg`

### Task 2: 定义解释区域与文案数据

**Files:**
- Modify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`

- [ ] **Step 1: 先加入失败校验，要求至少 6 个解释区域**

```python
SECTIONS = []


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    if len(SECTIONS) < 6:
        raise ValueError('need at least 6 explainer sections')
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f'Section count: {len(SECTIONS)}')
```

- [ ] **Step 2: 运行脚本确认区域校验失败**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`
Expected: FAIL with `ValueError: need at least 6 explainer sections`

- [ ] **Step 3: 填入区域定义与解释文案**

```python
SECTIONS = [
    {
        'kind': 'cover',
        'title': '东方财富截图怎么看',
        'number': '1',
        'summary': '这份 PDF 按区域解释截图里每个主要数据和按钮的含义。',
    },
    {
        'kind': 'area',
        'title': '顶部股票基本信息区',
        'number': '2',
        'crop': (0.0, 0.0, 1.0, 0.16),
        'items': [
            ('贵州茅台', '这是股票名称，表示当前查看的是哪只股票。'),
            ('600519', '这是股票代码，用来唯一识别这只股票。'),
            ('沪股通 / L1', '前者说明这只股票和互联互通有关，后者通常表示基础行情级别。'),
            ('Ai、分享、搜索', '这些是辅助功能按钮，不是行情数据本身。'),
        ],
    },
    {
        'kind': 'area',
        'title': '价格与涨跌区',
        'number': '2.1',
        'crop': (0.0, 0.08, 1.0, 0.20),
        'items': [
            ('1354.55', '这是当前显示的最新价格，表示这只股票此刻附近的成交价。'),
            ('-0.50% / -6.78', '一个是涨跌幅，一个是涨跌额，表示相对昨收是跌了。'),
            ('今开 / 最高 / 最低', '分别是今天开盘价、今天盘中最高价和最低价。'),
            ('怎么看', '一般先看最新价，再结合涨跌幅判断今天是涨是跌、波动大不大。'),
        ],
    },
    {
        'kind': 'area',
        'title': '资金与估值区',
        'number': '2.2',
        'crop': (0.0, 0.14, 1.0, 0.28),
        'items': [
            ('换手', '换手率表示股票在一段时间内被买卖的活跃程度。'),
            ('总手', '总手表示累计成交了多少手，1 手通常等于 100 股。'),
            ('金额', '金额表示累计成交额，也就是成交了多少钱。'),
            ('总值 / 流值 / 市盈', '分别可理解为总市值、流通市值和市盈率，是常见估值参考项。'),
        ],
    },
    {
        'kind': 'area',
        'title': '关联信息与切换区',
        'number': '2.3',
        'crop': (0.0, 0.19, 1.0, 0.33),
        'items': [
            ('相关基金', '表示和这只股票有关联的基金或指数信息。'),
            ('持仓占比', '通常表示某基金或组合里持有这只股票的比例。'),
            ('分时 / 五日 / 日K / 周K / 月K', '这是图表时间维度切换，不同按钮看的是不同周期。'),
            ('更多 / 设置', '是功能入口，不是交易数据。'),
        ],
    },
    {
        'kind': 'area',
        'title': '分时图主图区域',
        'number': '3',
        'crop': (0.0, 0.23, 1.0, 0.67),
        'items': [
            ('蓝线', '通常表示价格走势，能看出当天或这几天价格怎么走。'),
            ('黄线', '这里一般是均价线，用来辅助比较价格相对平均水平的高低。'),
            ('左侧价格刻度', '表示不同价位，帮助你知道曲线走到什么价格附近。'),
            ('右侧百分比刻度', '表示相对基准价格的涨跌幅区间。'),
            ('怎么看', '看这块时，重点是价格趋势、均价位置以及波动方向。'),
        ],
    },
    {
        'kind': 'area',
        'title': '成交量区域',
        'number': '3.1',
        'crop': (0.0, 0.64, 1.0, 0.82),
        'items': [
            ('成交量柱子', '柱子越高，通常表示那个时间段成交更活跃。'),
            ('成交量 / 分时量 / 现量', '分别对应累计成交、某时段成交和当前最新一笔或当前显示量。'),
            ('怎么看', '量大不一定涨，但量能常用来辅助判断走势有没有资金参与。'),
        ],
    },
    {
        'kind': 'area',
        'title': '底部功能区',
        'number': '4',
        'crop': (0.0, 0.82, 1.0, 1.0),
        'items': [
            ('股吧 / 盘口 / 资讯 / 公告 / 研报 / 财务 / 资料', '这些是围绕股票的扩展信息入口。'),
            ('交易 / 发帖 / 功能 / 加自选', '这些是操作入口，其中加自选表示把这只股票加入自选列表。'),
            ('怎么看', '底部这块主要是功能导航，帮助你切到不同信息页面。'),
        ],
    },
]
```

- [ ] **Step 4: 运行脚本确认区域数据加载成功**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`
Expected: PASS and print `Section count: 8`

### Task 3: 实现 PDF 基础绘制能力

**Files:**
- Modify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`

- [ ] **Step 1: 先调用未实现的绘制函数，让程序失败**

```python
from reportlab.pdfgen import canvas


def build_pdf() -> None:
    pdf = canvas.Canvas(str(OUTPUT_FILE))
    draw_page_frame(pdf, '示例页', '1')
    pdf.save()
```

- [ ] **Step 2: 运行脚本确认缺少绘制函数导致失败**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`
Expected: FAIL with `NameError: name 'draw_page_frame' is not defined`

- [ ] **Step 3: 实现页面框架、段落和说明列表工具函数**

```python
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 16 * mm
ACCENT = colors.HexColor('#1f4b99')
TEXT = colors.HexColor('#222222')
MUTED = colors.HexColor('#5b6573')
BORDER = colors.HexColor('#d4dceb')
FONT_REGULAR = 'STSong-Light'
FONT_BOLD = 'HeiseiMin-W3'


def register_fonts() -> None:
    pdfmetrics.registerFont(UnicodeCIDFont(FONT_REGULAR))
    pdfmetrics.registerFont(UnicodeCIDFont(FONT_BOLD))


BODY_STYLE = ParagraphStyle('Body', fontName=FONT_REGULAR, fontSize=10.5, leading=16, textColor=TEXT)
TITLE_STYLE = ParagraphStyle('Title', fontName=FONT_BOLD, fontSize=18, leading=24, textColor=ACCENT)
SMALL_STYLE = ParagraphStyle('Small', fontName=FONT_REGULAR, fontSize=9.2, leading=14, textColor=MUTED)


def draw_page_frame(pdf, title: str, number: str) -> None:
    pdf.setStrokeColor(BORDER)
    pdf.roundRect(MARGIN, MARGIN, PAGE_WIDTH - 2 * MARGIN, PAGE_HEIGHT - 2 * MARGIN, 5 * mm, stroke=1, fill=0)
    pdf.setFillColor(ACCENT)
    pdf.roundRect(MARGIN, PAGE_HEIGHT - 31 * mm, PAGE_WIDTH - 2 * MARGIN, 14 * mm, 4 * mm, stroke=0, fill=1)
    pdf.setFillColor(colors.white)
    pdf.setFont(FONT_BOLD, 17)
    pdf.drawString(MARGIN + 8 * mm, PAGE_HEIGHT - 22.5 * mm, title)
    pdf.drawRightString(PAGE_WIDTH - MARGIN - 8 * mm, PAGE_HEIGHT - 22.5 * mm, number)


def draw_paragraph(pdf, text: str, x: float, y_top: float, width: float, style: ParagraphStyle) -> float:
    paragraph = Paragraph(text.replace('\n', '<br/>'), style)
    _, height = paragraph.wrap(width, PAGE_HEIGHT)
    paragraph.drawOn(pdf, x, y_top - height)
    return y_top - height - 3.5 * mm
```

- [ ] **Step 4: 运行脚本确认基础绘制函数可调用**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`
Expected: PASS and create a basic PDF file

### Task 4: 实现截图裁剪与区域解释页渲染

**Files:**
- Modify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`

- [ ] **Step 1: 先接入未实现的截图裁剪函数**

```python

def render_area_page(pdf, section: dict) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    crop_reader = build_crop_reader(SOURCE, section['crop'])
```

- [ ] **Step 2: 运行脚本确认截图裁剪函数缺失导致失败**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`
Expected: FAIL with `NameError: name 'build_crop_reader' is not defined`

- [ ] **Step 3: 实现截图裁剪与图片绘制函数**

```python
from io import BytesIO
from PIL import Image
from reportlab.lib.utils import ImageReader


def build_crop_reader(image_path: Path, crop: tuple[float, float, float, float]) -> tuple[ImageReader, int, int]:
    with Image.open(image_path) as image:
        rgb = image.convert('RGB')
        width, height = rgb.size
        left = int(width * crop[0])
        top = int(height * crop[1])
        right = int(width * crop[2])
        bottom = int(height * crop[3])
        piece = rgb.crop((left, top, right, bottom))
        buffer = BytesIO()
        piece.save(buffer, format='PNG')
        buffer.seek(0)
        crop_width, crop_height = piece.size
    return ImageReader(buffer), crop_width, crop_height


def draw_image(pdf, image_reader: ImageReader, image_width: int, image_height: int, x: float, y_top: float, max_width: float, max_height: float) -> float:
    scale = min(max_width / image_width, max_height / image_height)
    draw_width = image_width * scale
    draw_height = image_height * scale
    pdf.drawImage(image_reader, x, y_top - draw_height, width=draw_width, height=draw_height, preserveAspectRatio=True, mask='auto')
    return y_top - draw_height - 5 * mm
```

- [ ] **Step 4: 实现封面页、区域解释页和汇总页**

```python

def render_cover(pdf, section: dict) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    full_reader, full_w, full_h = build_crop_reader(SOURCE, (0.0, 0.0, 1.0, 1.0))
    y = PAGE_HEIGHT - 48 * mm
    y = draw_paragraph(pdf, section['summary'], MARGIN + 10 * mm, y, PAGE_WIDTH - 40 * mm, BODY_STYLE)
    draw_image(pdf, full_reader, full_w, full_h, MARGIN + 32 * mm, y, PAGE_WIDTH - 64 * mm, 150 * mm)
    pdf.showPage()


def render_area_page(pdf, section: dict) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    reader, w, h = build_crop_reader(SOURCE, section['crop'])
    draw_image(pdf, reader, w, h, MARGIN + 10 * mm, PAGE_HEIGHT - 52 * mm, 78 * mm, 140 * mm)
    text_x = MARGIN + 96 * mm
    y = PAGE_HEIGHT - 50 * mm
    for name, explanation in section['items']:
        y = draw_paragraph(pdf, f'<b>{name}</b>：{explanation}', text_x, y, PAGE_WIDTH - text_x - MARGIN - 8 * mm, BODY_STYLE)
    pdf.showPage()


def render_summary(pdf) -> None:
    draw_page_frame(pdf, '快速回顾', '5')
    y = PAGE_HEIGHT - 50 * mm
    summary_lines = [
        '先看股票名称、代码，确认自己看的是什么标的。',
        '再看最新价、涨跌额、涨跌幅，判断当天整体表现。',
        '随后看换手率、成交量和金额，感受交易活跃度。',
        '最后结合分时图和均价线，理解当天走势强弱。',
    ]
    for line in summary_lines:
        y = draw_paragraph(pdf, line, MARGIN + 12 * mm, y, PAGE_WIDTH - 42 * mm, BODY_STYLE)
    pdf.showPage()
```

- [ ] **Step 5: 在主流程中循环渲染所有页面**

```python
from reportlab.pdfgen import canvas


def build_pdf() -> None:
    register_fonts()
    pdf = canvas.Canvas(str(OUTPUT_FILE), pagesize=A4)
    render_cover(pdf, SECTIONS[0])
    for section in SECTIONS[1:]:
        render_area_page(pdf, section)
    render_summary(pdf)
    pdf.save()
```

- [ ] **Step 6: 运行脚本确认生成多页 PDF**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`
Expected: PASS and create `/Users/tianxiang.yang/Desktop/yang/study/gupiao/output/stock_screen_explainer.pdf`

### Task 5: 增强可读性并加入页脚信息

**Files:**
- Modify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`

- [ ] **Step 1: 先增加对页脚函数的调用，让程序失败**

```python

def render_area_page(pdf, section: dict) -> None:
    ...
    draw_footer(pdf, section['number'])
    pdf.showPage()
```

- [ ] **Step 2: 运行脚本确认缺少页脚函数导致失败**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`
Expected: FAIL with `NameError: name 'draw_footer' is not defined`

- [ ] **Step 3: 实现页脚与区域提示说明**

```python

def draw_footer(pdf, page_label: str) -> None:
    pdf.setStrokeColor(BORDER)
    pdf.line(MARGIN + 6 * mm, 15 * mm, PAGE_WIDTH - MARGIN - 6 * mm, 15 * mm)
    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_REGULAR, 8.8)
    pdf.drawString(MARGIN + 6 * mm, 9.5 * mm, '股票截图解释型 PDF')
    pdf.drawRightString(PAGE_WIDTH - MARGIN - 6 * mm, 9.5 * mm, f'区域 {page_label}')


def draw_hint_box(pdf, text: str, x: float, y_top: float, width: float) -> float:
    hint_style = ParagraphStyle('Hint', fontName=FONT_REGULAR, fontSize=9.6, leading=14, textColor=MUTED)
    paragraph = Paragraph(f'怎么看：{text}', hint_style)
    _, height = paragraph.wrap(width - 8 * mm, PAGE_HEIGHT)
    pdf.setStrokeColor(BORDER)
    pdf.roundRect(x, y_top - height - 8 * mm, width, height + 8 * mm, 3 * mm, stroke=1, fill=0)
    paragraph.drawOn(pdf, x + 4 * mm, y_top - height - 4 * mm)
    return y_top - height - 10 * mm
```

- [ ] **Step 4: 在区域解释页中加入提示框，并给每页加页脚**

```python

def render_area_page(pdf, section: dict) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    reader, w, h = build_crop_reader(SOURCE, section['crop'])
    draw_image(pdf, reader, w, h, MARGIN + 10 * mm, PAGE_HEIGHT - 52 * mm, 78 * mm, 140 * mm)
    text_x = MARGIN + 96 * mm
    y = PAGE_HEIGHT - 50 * mm
    hint_text = ''
    for name, explanation in section['items']:
        y = draw_paragraph(pdf, f'<b>{name}</b>：{explanation}', text_x, y, PAGE_WIDTH - text_x - MARGIN - 8 * mm, BODY_STYLE)
        if name == '怎么看':
            hint_text = explanation
    if hint_text:
        draw_hint_box(pdf, hint_text, text_x, 72 * mm, PAGE_WIDTH - text_x - MARGIN - 8 * mm)
    draw_footer(pdf, section['number'])
    pdf.showPage()
```

- [ ] **Step 5: 运行脚本确认增强后仍可生成 PDF**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`
Expected: PASS and overwrite the PDF successfully

### Task 6: 验证成品文件

**Files:**
- Verify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/output/stock_screen_explainer.pdf`

- [ ] **Step 1: 运行最终生成命令**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`
Expected: PASS and print output path

- [ ] **Step 2: 检查 PDF 文件存在且页数不少于 3 页**

Run: `mdls -name kMDItemNumberOfPages -name kMDItemFSSize /Users/tianxiang.yang/Desktop/yang/study/gupiao/output/stock_screen_explainer.pdf`
Expected: PASS and show `kMDItemNumberOfPages` >= 3

- [ ] **Step 3: 运行脚本语法校验**

Run: `python3 -c "import py_compile; py_compile.compile('/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py', doraise=True); print('py_compile: ok')"`
Expected: PASS and print `py_compile: ok`

- [ ] **Step 4: 交付检查项**

```text
- 已生成 PDF
- 使用原图做对照解释
- 按区域分块讲解
- 风格为白话 + 一点股票常识
- 覆盖截图核心数据项与功能区
- 可直接打开阅读
```
