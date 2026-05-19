from io import BytesIO
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

SOURCE = Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao/东方财富.jpg')
OUTPUT_DIR = Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao/output')
OUTPUT_FILE = OUTPUT_DIR / 'stock_screen_explainer.pdf'
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 16 * mm
ACCENT = colors.HexColor('#1f4b99')
ACCENT_LIGHT = colors.HexColor('#eef4ff')
TEXT = colors.HexColor('#222222')
MUTED = colors.HexColor('#5b6573')
BORDER = colors.HexColor('#d4dceb')
FONT_REGULAR = 'STSong-Light'
FONT_BOLD = 'HeiseiMin-W3'

SECTIONS = [
    {
        'kind': 'cover',
        'title': '东方财富截图怎么看',
        'number': '1',
        'summary': '这份 PDF 按区域解释截图里每个主要数据和按钮的含义，帮助你把图上的数字和功能区一一对上。',
    },
    {
        'kind': 'area',
        'title': '顶部股票基本信息区',
        'number': '2',
        'crop': (0.0, 0.0, 1.0, 0.16),
        'items': [
            ('贵州茅台', '这是股票名称，表示当前查看的是哪只股票。'),
            ('600519', '这是股票代码，用来唯一识别这只股票。'),
            ('沪股通 / L1', '前者一般表示这只股票和互联互通有关，后者通常表示基础行情级别。'),
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
            ('-0.50% / -6.78', '一个是涨跌幅，一个是涨跌额，说明相对昨收是下跌状态。'),
            ('今开 / 最高 / 最低', '分别是今天开盘价、今天盘中最高价和最低价。'),
            ('怎么看', '先看最新价，再结合涨跌幅，能快速判断今天整体是涨是跌、波动大不大。'),
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
            ('总值 / 流值 / 市盈', '一般可理解为总市值、流通市值和市盈率，是常见估值参考项。'),
        ],
    },
    {
        'kind': 'area',
        'title': '关联信息与切换区',
        'number': '2.3',
        'crop': (0.0, 0.18, 1.0, 0.33),
        'items': [
            ('相关基金', '表示和这只股票有关联的基金或指数信息。'),
            ('持仓占比', '通常表示某基金或组合里持有这只股票的比例。'),
            ('分时 / 五日 / 日K / 周K / 月K', '这是图表时间维度切换，不同按钮看的是不同周期。'),
            ('更多 / 设置', '这是功能入口，不是交易数据。'),
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
            ('成交量 / 分时量 / 现量', '分别对应累计成交、某时段成交和当前显示的即时量。'),
            ('怎么看', '量大不一定涨，但量能常用来辅助判断走势背后是否有更多资金参与。'),
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


def register_fonts() -> None:
    pdfmetrics.registerFont(UnicodeCIDFont(FONT_REGULAR))
    pdfmetrics.registerFont(UnicodeCIDFont(FONT_BOLD))


BODY_STYLE = ParagraphStyle(
    'Body',
    fontName=FONT_REGULAR,
    fontSize=10.5,
    leading=16,
    textColor=TEXT,
)

TITLE_STYLE = ParagraphStyle(
    'Title',
    fontName=FONT_BOLD,
    fontSize=18,
    leading=24,
    textColor=ACCENT,
)

SUBTITLE_STYLE = ParagraphStyle(
    'Subtitle',
    fontName=FONT_REGULAR,
    fontSize=11,
    leading=17,
    textColor=MUTED,
)

SMALL_STYLE = ParagraphStyle(
    'Small',
    fontName=FONT_REGULAR,
    fontSize=9.2,
    leading=14,
    textColor=MUTED,
)

HINT_STYLE = ParagraphStyle(
    'Hint',
    fontName=FONT_REGULAR,
    fontSize=9.6,
    leading=14,
    textColor=MUTED,
)


def draw_page_frame(pdf: canvas.Canvas, title: str, number: str) -> None:
    pdf.setFillColor(colors.white)
    pdf.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    pdf.setStrokeColor(BORDER)
    pdf.roundRect(MARGIN, MARGIN, PAGE_WIDTH - 2 * MARGIN, PAGE_HEIGHT - 2 * MARGIN, 5 * mm, stroke=1, fill=0)
    pdf.setFillColor(ACCENT)
    pdf.roundRect(MARGIN, PAGE_HEIGHT - 31 * mm, PAGE_WIDTH - 2 * MARGIN, 14 * mm, 4 * mm, stroke=0, fill=1)
    pdf.setFillColor(colors.white)
    pdf.setFont(FONT_BOLD, 17)
    pdf.drawString(MARGIN + 8 * mm, PAGE_HEIGHT - 22.5 * mm, title)
    pdf.drawRightString(PAGE_WIDTH - MARGIN - 8 * mm, PAGE_HEIGHT - 22.5 * mm, number)


def draw_footer(pdf: canvas.Canvas, page_label: str) -> None:
    pdf.setStrokeColor(BORDER)
    pdf.line(MARGIN + 6 * mm, 15 * mm, PAGE_WIDTH - MARGIN - 6 * mm, 15 * mm)
    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_REGULAR, 8.8)
    pdf.drawString(MARGIN + 6 * mm, 9.5 * mm, '股票截图解释型 PDF')
    pdf.drawRightString(PAGE_WIDTH - MARGIN - 6 * mm, 9.5 * mm, f'区域 {page_label}')


def draw_paragraph(pdf: canvas.Canvas, text: str, x: float, y_top: float, width: float, style: ParagraphStyle) -> float:
    paragraph = Paragraph(text.replace('\n', '<br/>'), style)
    _, height = paragraph.wrap(width, PAGE_HEIGHT)
    paragraph.drawOn(pdf, x, y_top - height)
    return y_top - height - 3.5 * mm


def draw_hint_box(pdf: canvas.Canvas, text: str, x: float, y_top: float, width: float) -> float:
    paragraph = Paragraph(f'怎么看：{text}', HINT_STYLE)
    _, height = paragraph.wrap(width - 8 * mm, PAGE_HEIGHT)
    box_height = height + 8 * mm
    pdf.setFillColor(ACCENT_LIGHT)
    pdf.setStrokeColor(BORDER)
    pdf.roundRect(x, y_top - box_height, width, box_height, 3 * mm, stroke=1, fill=1)
    paragraph.drawOn(pdf, x + 4 * mm, y_top - height - 4 * mm)
    return y_top - box_height - 4 * mm


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


def draw_image(pdf: canvas.Canvas, image_reader: ImageReader, image_width: int, image_height: int, x: float, y_top: float, max_width: float, max_height: float) -> float:
    scale = min(max_width / image_width, max_height / image_height)
    draw_width = image_width * scale
    draw_height = image_height * scale
    pdf.drawImage(image_reader, x, y_top - draw_height, width=draw_width, height=draw_height, preserveAspectRatio=True, mask='auto')
    pdf.setStrokeColor(BORDER)
    pdf.roundRect(x - 1.5 * mm, y_top - draw_height - 1.5 * mm, draw_width + 3 * mm, draw_height + 3 * mm, 2 * mm, stroke=1, fill=0)
    return y_top - draw_height - 5 * mm


def render_cover(pdf: canvas.Canvas, section: dict) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    full_reader, full_w, full_h = build_crop_reader(SOURCE, (0.0, 0.0, 1.0, 1.0))
    y = PAGE_HEIGHT - 48 * mm
    y = draw_paragraph(pdf, section['summary'], MARGIN + 10 * mm, y, PAGE_WIDTH - 40 * mm, SUBTITLE_STYLE)
    y = draw_image(pdf, full_reader, full_w, full_h, MARGIN + 42 * mm, y, PAGE_WIDTH - 84 * mm, 150 * mm)
    y = draw_paragraph(pdf, '阅读方法：先看左侧截图局部，再对照右侧说明，就能知道每块数据一般表示什么。', MARGIN + 10 * mm, y, PAGE_WIDTH - 40 * mm, BODY_STYLE)
    draw_footer(pdf, section['number'])
    pdf.showPage()


def render_area_page(pdf: canvas.Canvas, section: dict) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    reader, image_width, image_height = build_crop_reader(SOURCE, section['crop'])
    draw_image(pdf, reader, image_width, image_height, MARGIN + 10 * mm, PAGE_HEIGHT - 52 * mm, 78 * mm, 142 * mm)
    text_x = MARGIN + 96 * mm
    text_width = PAGE_WIDTH - text_x - MARGIN - 8 * mm
    y = PAGE_HEIGHT - 50 * mm
    hint_text = ''
    for name, explanation in section['items']:
        if name == '怎么看':
            hint_text = explanation
            continue
        y = draw_paragraph(pdf, f'<b>{name}</b>：{explanation}', text_x, y, text_width, BODY_STYLE)
    if hint_text:
        draw_hint_box(pdf, hint_text, text_x, max(74 * mm, y - 2 * mm), text_width)
    draw_footer(pdf, section['number'])
    pdf.showPage()


def render_summary(pdf: canvas.Canvas) -> None:
    draw_page_frame(pdf, '快速回顾', '5')
    y = PAGE_HEIGHT - 48 * mm
    lines = [
        '先看股票名称和代码，确认自己看的是什么标的。',
        '再看最新价、涨跌额、涨跌幅，这是最直观的涨跌信息。',
        '接着看换手率、成交量和金额，它们更偏向活跃度和交易热度。',
        '最后看分时图、均价线和底部功能区，理解走势和常用入口。',
    ]
    y = draw_paragraph(pdf, '如果你是新手，这四步基本就能把一张股票软件截图读明白。', MARGIN + 10 * mm, y, PAGE_WIDTH - 40 * mm, SUBTITLE_STYLE)
    for index, line in enumerate(lines, start=1):
        y = draw_paragraph(pdf, f'{index}. {line}', MARGIN + 12 * mm, y, PAGE_WIDTH - 42 * mm, BODY_STYLE)
    draw_footer(pdf, '5')
    pdf.showPage()


def build_pdf() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    register_fonts()
    pdf = canvas.Canvas(str(OUTPUT_FILE), pagesize=A4)
    pdf.setTitle('股票截图解释型 PDF')
    render_cover(pdf, SECTIONS[0])
    for section in SECTIONS[1:]:
        render_area_page(pdf, section)
    render_summary(pdf)
    pdf.save()


def main() -> None:
    build_pdf()
    print(f'PDF generated: {OUTPUT_FILE}')
    print(f'Page count planned: {len(SECTIONS) + 1}')


if __name__ == '__main__':
    main()
