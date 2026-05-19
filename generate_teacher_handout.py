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
OUTPUT_FILE = OUTPUT_DIR / 'teacher_handout.pdf'
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
        'number': '1',
        'title': '东方财富教师讲义',
        'subtitle': '教材精读型 · 图片主导版',
        'focus': '先建立软件界面的整体认知，再进入功能区观察与课堂讲解。',
        'points': [
            '认识东方财富软件界面的主要信息区域。',
            '掌握教师课堂讲授时的观察顺序与讲解重心。',
            '为后续看盘、选股与复盘学习打下界面基础。',
        ],
    },
    {
        'kind': 'toc',
        'number': '1.1',
        'title': '目录',
        'items': [
            '1 课程导入与学习目标',
            '1.1 目录与学习路径',
            '2 软件界面整体认识',
            '2.1 首页结构观察',
            '2.2 自选股区域识别',
            '2.3 行情窗口解读',
            '3 课末小结与教学提醒',
        ],
    },
    {
        'kind': 'content',
        'number': '2',
        'title': '软件界面整体认识',
        'focus': '先让学生形成“界面分区”概念，不急于解释局部按钮。',
        'speech': [
            '老师在这一页应先带学生整体观察界面，不要一开始就进入细节功能。',
            '可以先提问学生：这张图大致可以分成几个区域？每个区域像是在承担什么任务？',
            '通过先看全局，再看局部，学生会更容易建立后续学习中的位置感和结构感。',
            '这一部分的授课目标不是记忆按钮名称，而是建立软件界面的整体框架意识。',
        ],
        'crop': (0.0, 0.0, 1.0, 0.36),
    },
    {
        'kind': 'content',
        'number': '2.1',
        'title': '首页结构观察',
        'focus': '帮助学生理解首页各功能区的排布逻辑与阅读顺序。',
        'speech': [
            '老师可以按“上到下、左到右”的顺序引导学生浏览页面。',
            '讲解时要让学生知道：首页中的导航、行情信息、列表区域和功能入口各自承担不同职责。',
            '建议边指图边讲，让学生同步在图中找到对应位置，这样课堂跟进效果会更好。',
            '如果学生对页面感到复杂，老师要反复强调：先分区，再识别，最后再谈使用。',
        ],
        'crop': (0.0, 0.18, 1.0, 0.52),
    },
    {
        'kind': 'content',
        'number': '2.2',
        'title': '自选股区域识别',
        'focus': '把自选股区域讲清楚，便于后续盯盘与个股追踪。',
        'speech': [
            '老师在这一页可以重点提示学生关注名称、涨跌、排序和分组等常见信息。',
            '对于初学者，不必马上讲复杂操作，而是先讲清楚这些字段在课堂中分别代表什么。',
            '自选股区域往往是学生后续最常使用的入口，因此要尽早培养他们的信息筛选意识。',
            '授课时可补充一句：会看自选股，不等于会分析个股，但这是进入分析的第一步。',
        ],
        'crop': (0.0, 0.42, 1.0, 0.72),
    },
    {
        'kind': 'content',
        'number': '2.3',
        'title': '行情窗口解读',
        'focus': '强调价格、涨跌幅与成交相关信息需要联动观察。',
        'speech': [
            '这一页老师要提醒学生，行情窗口不是单看一个数字，而是要看一组相互关联的数据。',
            '讲解时可让学生同步观察价格变化、涨跌幅变化以及成交相关指标的对应关系。',
            '如果学生只盯住一个指标，很容易形成片面理解，因此老师要主动建立“联动观察”的课堂习惯。',
            '等学生先把这些位置认清楚，后面再讲指标意义与应用场景，会更加顺畅。',
        ],
        'crop': (0.0, 0.68, 1.0, 1.0),
    },
    {
        'kind': 'summary',
        'number': '3',
        'title': '课末小结与教学提醒',
        'focus': '把本节课收束到“会看区域、会找入口、会抓重点”三个层面。',
        'speech': [
            '今天这节课的核心，不是要求学生马上熟练操作，而是先把界面结构真正看懂。',
            '只要学生能够说出主要区域在哪里、主要入口在哪里、重点信息怎么看，本节课就达到了基础目标。',
            '老师在收尾时可以再强调一次：先建立界面认知，再进入细节功能，学习效率会更高。',
            '下一步教学就可以围绕某个具体区域继续展开，例如分时、K线或自选股管理。',
        ],
    },
]


def register_fonts() -> None:
    pdfmetrics.registerFont(UnicodeCIDFont(FONT_REGULAR))
    pdfmetrics.registerFont(UnicodeCIDFont(FONT_BOLD))


BODY_STYLE = ParagraphStyle(
    'BodyStyle',
    fontName=FONT_REGULAR,
    fontSize=10.5,
    leading=16,
    textColor=TEXT,
)

SMALL_STYLE = ParagraphStyle(
    'SmallStyle',
    fontName=FONT_REGULAR,
    fontSize=9.2,
    leading=14,
    textColor=MUTED,
)

HEADING_STYLE = ParagraphStyle(
    'HeadingStyle',
    fontName=FONT_BOLD,
    fontSize=18,
    leading=24,
    textColor=ACCENT,
)

SUBTITLE_STYLE = ParagraphStyle(
    'SubtitleStyle',
    fontName=FONT_REGULAR,
    fontSize=12,
    leading=18,
    textColor=MUTED,
)

FOCUS_STYLE = ParagraphStyle(
    'FocusStyle',
    fontName=FONT_BOLD,
    fontSize=10.5,
    leading=16,
    textColor=ACCENT,
)


def draw_page_frame(pdf: canvas.Canvas, title: str, number: str) -> None:
    pdf.setFillColor(colors.white)
    pdf.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(1)
    pdf.roundRect(MARGIN, MARGIN, PAGE_WIDTH - 2 * MARGIN, PAGE_HEIGHT - 2 * MARGIN, 5 * mm, stroke=1, fill=0)
    pdf.setFillColor(ACCENT)
    pdf.roundRect(MARGIN, PAGE_HEIGHT - 31 * mm, PAGE_WIDTH - 2 * MARGIN, 14 * mm, 4 * mm, stroke=0, fill=1)
    pdf.setFillColor(colors.white)
    pdf.setFont(FONT_BOLD, 17)
    pdf.drawString(MARGIN + 8 * mm, PAGE_HEIGHT - 22.5 * mm, title)
    draw_section_badge(pdf, number, PAGE_WIDTH - MARGIN - 33 * mm, PAGE_HEIGHT - 29.5 * mm)


def draw_section_badge(pdf: canvas.Canvas, number: str, x: float, y: float) -> None:
    pdf.setFillColor(colors.white)
    pdf.roundRect(x, y, 25 * mm, 9.5 * mm, 3 * mm, stroke=0, fill=1)
    pdf.setFillColor(ACCENT)
    pdf.setFont(FONT_BOLD, 9.5)
    pdf.drawCentredString(x + 12.5 * mm, y + 2.8 * mm, number)


def draw_footer(pdf: canvas.Canvas, page_index: int) -> None:
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(0.8)
    pdf.line(MARGIN + 6 * mm, 15 * mm, PAGE_WIDTH - MARGIN - 6 * mm, 15 * mm)
    pdf.setFillColor(MUTED)
    pdf.setFont(FONT_REGULAR, 8.8)
    pdf.drawString(MARGIN + 6 * mm, 9.5 * mm, '教师讲义版｜东方财富界面导读')
    pdf.drawRightString(PAGE_WIDTH - MARGIN - 6 * mm, 9.5 * mm, f'第 {page_index} 页')


def draw_paragraph(pdf: canvas.Canvas, text: str, x: float, y_top: float, width: float, style: ParagraphStyle) -> float:
    paragraph = Paragraph(text.replace('\n', '<br/>'), style)
    _, height = paragraph.wrap(width, PAGE_HEIGHT)
    paragraph.drawOn(pdf, x, y_top - height)
    return y_top - height - 3.5 * mm


def draw_focus_box(pdf: canvas.Canvas, text: str, x: float, y_top: float, width: float) -> float:
    paragraph = Paragraph(f'学习重点：{text}', FOCUS_STYLE)
    _, height = paragraph.wrap(width - 10 * mm, PAGE_HEIGHT)
    box_height = height + 10 * mm
    pdf.setFillColor(ACCENT_LIGHT)
    pdf.setStrokeColor(ACCENT)
    pdf.roundRect(x, y_top - box_height, width, box_height, 4 * mm, fill=1, stroke=1)
    paragraph.drawOn(pdf, x + 5 * mm, y_top - height - 5.2 * mm)
    return y_top - box_height - 4 * mm


def crop_reader(image_path: Path, crop: tuple[float, float, float, float]) -> tuple[ImageReader, int, int]:
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
        cropped_width, cropped_height = piece.size
    return ImageReader(buffer), cropped_width, cropped_height


def draw_image_block(pdf: canvas.Canvas, image_reader: ImageReader, width: int, height: int, x: float, y_top: float, max_width: float, max_height: float) -> float:
    scale = min(max_width / width, max_height / height)
    draw_width = width * scale
    draw_height = height * scale
    pdf.drawImage(image_reader, x, y_top - draw_height, width=draw_width, height=draw_height, preserveAspectRatio=True, mask='auto')
    pdf.setStrokeColor(BORDER)
    pdf.roundRect(x - 1.5 * mm, y_top - draw_height - 1.5 * mm, draw_width + 3 * mm, draw_height + 3 * mm, 2 * mm, stroke=1, fill=0)
    return y_top - draw_height - 5 * mm


def draw_full_image(pdf: canvas.Canvas, x: float, y_top: float, max_width: float, max_height: float) -> float:
    with Image.open(SOURCE) as image:
        width, height = image.size
    return draw_image_block(pdf, ImageReader(str(SOURCE)), width, height, x, y_top, max_width, max_height)


def render_cover(pdf: canvas.Canvas, section: dict, page_index: int) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    y = PAGE_HEIGHT - 44 * mm
    y = draw_paragraph(pdf, section['subtitle'], MARGIN + 10 * mm, y, PAGE_WIDTH - 40 * mm, SUBTITLE_STYLE)
    y = draw_full_image(pdf, MARGIN + 24 * mm, y - 2 * mm, PAGE_WIDTH - 48 * mm, 108 * mm)
    y = draw_paragraph(pdf, '教学目标', MARGIN + 10 * mm, y, 45 * mm, HEADING_STYLE)
    for idx, point in enumerate(section['points'], start=1):
        y = draw_paragraph(pdf, f'{idx}. {point}', MARGIN + 12 * mm, y, PAGE_WIDTH - 44 * mm, BODY_STYLE)
    draw_focus_box(pdf, section['focus'], MARGIN + 10 * mm, 66 * mm, PAGE_WIDTH - 40 * mm)
    draw_footer(pdf, page_index)
    pdf.showPage()


def render_toc(pdf: canvas.Canvas, section: dict, page_index: int) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    y = PAGE_HEIGHT - 50 * mm
    y = draw_paragraph(pdf, '本讲义按照“整体认识—结构观察—重点辨识—课堂总结”的路径展开。', MARGIN + 12 * mm, y, PAGE_WIDTH - 42 * mm, BODY_STYLE)
    for item in section['items']:
        y = draw_paragraph(pdf, item, MARGIN + 20 * mm, y - 1 * mm, PAGE_WIDTH - 58 * mm, BODY_STYLE)
    draw_focus_box(pdf, '目录页的作用是帮助学生形成学习路线，老师在开讲前应先把主线交代清楚。', MARGIN + 12 * mm, 88 * mm, PAGE_WIDTH - 42 * mm)
    draw_footer(pdf, page_index)
    pdf.showPage()


def render_content(pdf: canvas.Canvas, section: dict, page_index: int) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    image_reader, img_w, img_h = crop_reader(SOURCE, section['crop'])
    image_x = MARGIN + 8 * mm
    image_top = PAGE_HEIGHT - 48 * mm
    draw_image_block(pdf, image_reader, img_w, img_h, image_x, image_top, 86 * mm, 150 * mm)
    text_x = MARGIN + 100 * mm
    y = PAGE_HEIGHT - 48 * mm
    y = draw_paragraph(pdf, '教师讲授要点', text_x, y, PAGE_WIDTH - text_x - MARGIN - 8 * mm, HEADING_STYLE)
    for line in section['speech']:
        y = draw_paragraph(pdf, line, text_x, y, PAGE_WIDTH - text_x - MARGIN - 8 * mm, BODY_STYLE)
    draw_focus_box(pdf, section['focus'], text_x, 77 * mm, PAGE_WIDTH - text_x - MARGIN - 8 * mm)
    draw_footer(pdf, page_index)
    pdf.showPage()


def render_summary(pdf: canvas.Canvas, section: dict, page_index: int) -> None:
    draw_page_frame(pdf, section['title'], section['number'])
    y = PAGE_HEIGHT - 50 * mm
    y = draw_paragraph(pdf, '本节知识小结', MARGIN + 10 * mm, y, 60 * mm, HEADING_STYLE)
    y = draw_full_image(pdf, MARGIN + 10 * mm, y - 2 * mm, 82 * mm, 120 * mm)
    summary_x = MARGIN + 100 * mm
    text_y = PAGE_HEIGHT - 62 * mm
    for line in section['speech']:
        text_y = draw_paragraph(pdf, line, summary_x, text_y, PAGE_WIDTH - summary_x - MARGIN - 8 * mm, BODY_STYLE)
    draw_focus_box(pdf, section['focus'], MARGIN + 10 * mm, 63 * mm, PAGE_WIDTH - 40 * mm)
    draw_footer(pdf, page_index)
    pdf.showPage()


def build_pdf() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    register_fonts()
    pdf = canvas.Canvas(str(OUTPUT_FILE), pagesize=A4)
    pdf.setTitle('东方财富教师讲义')
    for index, section in enumerate(SECTIONS, start=1):
        if section['kind'] == 'cover':
            render_cover(pdf, section, index)
        elif section['kind'] == 'toc':
            render_toc(pdf, section, index)
        elif section['kind'] == 'content':
            render_content(pdf, section, index)
        elif section['kind'] == 'summary':
            render_summary(pdf, section, index)
        else:
            raise ValueError(f"unknown section kind: {section['kind']}")
    pdf.save()


def main() -> None:
    build_pdf()
    print(f'PDF generated: {OUTPUT_FILE}')
    print(f'Page count planned: {len(SECTIONS)}')


if __name__ == '__main__':
    main()
