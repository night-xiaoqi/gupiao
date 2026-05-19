from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao')
IMAGES_DIR = BASE_DIR / 'images'

WIDTH = 1400
HEIGHT = 900
PADDING = 72
PRICE_TOP = 150
PRICE_HEIGHT = 260
MACD_TOP = 500
MACD_HEIGHT = 240
BG = '#f7f9fc'
PANEL = '#ffffff'
GRID = '#d9e2f2'
TEXT = '#223047'
SUBTEXT = '#5b6573'
BLUE = '#2f6fed'
ORANGE = '#f39c12'
RED = '#e74c3c'
GREEN = '#16a085'
ZERO = '#8b95a7'
BORDER = '#d4dceb'
LABEL_BG = '#eef4ff'
PRICE_LINE = '#3d7eff'

SCENARIOS = [
    {
        'filename': 'macd-golden-cross-example.png',
        'title': 'MACD 金叉示意图',
        'subtitle': 'DIF 自下向上穿越 DEA，短期走势开始转强',
        'price': [10.8, 10.6, 10.3, 10.1, 10.0, 10.05, 10.2, 10.45, 10.8, 11.1, 11.35, 11.6],
        'dif': [-0.9, -0.95, -0.85, -0.65, -0.45, -0.18, 0.05, 0.28, 0.48, 0.65, 0.78, 0.88],
        'dea': [-0.55, -0.62, -0.65, -0.58, -0.48, -0.3, -0.08, 0.1, 0.25, 0.4, 0.52, 0.63],
        'bars': [-0.35, -0.33, -0.2, -0.07, 0.03, 0.12, 0.18, 0.22, 0.23, 0.25, 0.26, 0.25],
        'label': '金叉',
        'notes': [{'text': '低位企稳后转强', 'type': 'price', 'index': 8}],
    },
    {
        'filename': 'macd-death-cross-example.png',
        'title': 'MACD 死叉示意图',
        'subtitle': 'DIF 自上向下跌破 DEA，短线开始转弱',
        'price': [10.2, 10.5, 10.9, 11.2, 11.45, 11.55, 11.5, 11.35, 11.1, 10.88, 10.7, 10.5],
        'dif': [0.72, 0.82, 0.92, 0.98, 1.0, 0.92, 0.74, 0.48, 0.22, -0.05, -0.22, -0.35],
        'dea': [0.48, 0.58, 0.68, 0.78, 0.86, 0.88, 0.82, 0.66, 0.42, 0.18, -0.02, -0.18],
        'bars': [0.24, 0.24, 0.24, 0.2, 0.14, 0.04, -0.08, -0.18, -0.2, -0.23, -0.2, -0.17],
        'label': '死叉',
        'notes': [{'text': '高位转弱', 'type': 'price', 'index': 7}],
    },
    {
        'filename': 'macd-second-golden-cross-above-zero-example.png',
        'title': '零轴上方二次金叉示意图',
        'subtitle': '强势趋势中的回调后再次转强',
        'price': [10.0, 10.4, 10.9, 11.3, 11.0, 10.85, 11.05, 11.35, 11.7, 12.0, 12.25, 12.5],
        'dif': [0.18, 0.38, 0.62, 0.78, 0.52, 0.3, 0.34, 0.5, 0.7, 0.88, 1.02, 1.12],
        'dea': [0.08, 0.22, 0.4, 0.55, 0.5, 0.4, 0.32, 0.36, 0.48, 0.64, 0.8, 0.92],
        'bars': [0.1, 0.16, 0.22, 0.23, 0.02, -0.1, 0.02, 0.14, 0.22, 0.24, 0.22, 0.2],
        'label': '二次金叉',
        'notes': [
            {'text': '零轴上方', 'type': 'macd', 'index': 9},
            {'text': '趋势延续', 'type': 'price', 'index': 9},
        ],
    },
    {
        'filename': 'macd-weak-golden-cross-below-zero-example.png',
        'title': '零轴下方弱势金叉示意图',
        'subtitle': '弱势背景下的技术性反弹，持续性往往有限',
        'price': [12.0, 11.6, 11.2, 10.9, 10.6, 10.75, 10.95, 11.05, 10.98, 10.86, 10.76, 10.68],
        'dif': [-1.05, -1.1, -1.0, -0.86, -0.72, -0.56, -0.42, -0.35, -0.38, -0.48, -0.6, -0.7],
        'dea': [-0.82, -0.88, -0.92, -0.9, -0.82, -0.7, -0.55, -0.42, -0.36, -0.38, -0.48, -0.58],
        'bars': [-0.23, -0.22, -0.08, 0.04, 0.1, 0.14, 0.13, 0.07, -0.02, -0.1, -0.12, -0.12],
        'label': '弱势金叉',
        'notes': [
            {'text': '零轴下方', 'type': 'macd', 'index': 8},
            {'text': '反弹力度偏弱', 'type': 'price', 'index': 7},
        ],
    },
    {
        'filename': 'macd-red-bars-expanding-example.png',
        'title': '红柱放大趋势增强示意图',
        'subtitle': '红柱逐步放大，通常表示多头动能增强',
        'price': [9.8, 10.0, 10.15, 10.35, 10.65, 10.95, 11.28, 11.6, 11.96, 12.3, 12.68, 13.0],
        'dif': [0.08, 0.14, 0.2, 0.28, 0.38, 0.52, 0.68, 0.84, 1.0, 1.14, 1.28, 1.38],
        'dea': [0.02, 0.06, 0.1, 0.16, 0.22, 0.3, 0.4, 0.52, 0.66, 0.8, 0.94, 1.08],
        'bars': [0.06, 0.08, 0.1, 0.12, 0.16, 0.22, 0.28, 0.32, 0.34, 0.34, 0.34, 0.3],
        'label': '红柱放大',
        'notes': [{'text': '动能增强', 'type': 'macd', 'index': 8}],
    },
    {
        'filename': 'macd-top-divergence-example.png',
        'title': '顶背离示意图',
        'subtitle': '股价创新高，但 MACD 未同步走强，提示高位风险增加',
        'price': [10.3, 10.7, 11.15, 11.55, 11.9, 12.15, 12.0, 12.18, 12.42, 12.65, 12.78, 12.92],
        'dif': [0.35, 0.55, 0.82, 1.05, 1.18, 1.22, 1.08, 1.02, 0.96, 0.9, 0.84, 0.76],
        'dea': [0.2, 0.36, 0.56, 0.76, 0.92, 1.02, 1.04, 1.02, 0.98, 0.94, 0.88, 0.82],
        'bars': [0.15, 0.19, 0.26, 0.29, 0.26, 0.2, 0.04, 0.0, -0.02, -0.04, -0.04, -0.06],
        'label': '顶背离',
        'notes': [
            {'text': '前高', 'type': 'price', 'index': 5},
            {'text': '新高但动能减弱', 'type': 'price', 'index': 11},
        ],
    },
    {
        'filename': 'macd-bottom-divergence-example.png',
        'title': '底背离示意图',
        'subtitle': '股价创新低，但 MACD 未同步走弱，提示跌势衰减',
        'price': [13.0, 12.5, 12.0, 11.55, 11.15, 10.82, 10.96, 10.7, 10.46, 10.22, 10.3, 10.58],
        'dif': [-0.42, -0.66, -0.92, -1.12, -1.24, -1.26, -1.06, -0.94, -0.82, -0.72, -0.52, -0.3],
        'dea': [-0.26, -0.46, -0.68, -0.9, -1.06, -1.16, -1.14, -1.06, -0.96, -0.84, -0.68, -0.5],
        'bars': [-0.16, -0.2, -0.24, -0.22, -0.18, -0.1, 0.08, 0.12, 0.14, 0.12, 0.16, 0.2],
        'label': '底背离',
        'notes': [
            {'text': '前低', 'type': 'price', 'index': 5},
            {'text': '新低但动能改善', 'type': 'price', 'index': 9},
        ],
    },
    {
        'filename': 'macd-high-level-blunt-example.png',
        'title': '高位钝化示意图',
        'subtitle': '指标长时间停留高位，趋势虽强，但要警惕追高风险',
        'price': [9.9, 10.4, 10.95, 11.55, 12.1, 12.58, 12.96, 13.2, 13.36, 13.48, 13.56, 13.62],
        'dif': [0.16, 0.38, 0.66, 0.98, 1.24, 1.42, 1.56, 1.62, 1.64, 1.62, 1.58, 1.52],
        'dea': [0.08, 0.22, 0.42, 0.68, 0.92, 1.12, 1.28, 1.42, 1.52, 1.56, 1.56, 1.54],
        'bars': [0.08, 0.16, 0.24, 0.3, 0.32, 0.3, 0.28, 0.2, 0.12, 0.06, 0.02, -0.02],
        'label': '高位钝化',
        'notes': [
            {'text': '高位钝化', 'type': 'macd', 'index': 8},
            {'text': '警惕追高', 'type': 'price', 'index': 10},
        ],
    },
]


def load_font(size: int):
    candidates = [
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
        '/System/Library/Fonts/Supplemental/Songti.ttc',
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def create_canvas(title: str, subtitle: str):
    image = Image.new('RGB', (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((28, 28, WIDTH - 28, HEIGHT - 28), radius=28, fill=PANEL, outline=BORDER, width=3)
    title_font = load_font(42)
    subtitle_font = load_font(24)
    body_font = load_font(22)
    draw.text((PADDING, 48), title, fill=TEXT, font=title_font)
    draw.text((PADDING, 98), subtitle, fill=SUBTEXT, font=subtitle_font)
    draw.text((PADDING + 8, PRICE_TOP - 36), '价格走势示意', fill=TEXT, font=body_font)
    draw.text((PADDING + 8, MACD_TOP - 36), 'MACD 指标区', fill=TEXT, font=body_font)
    return image, draw


def draw_panels(draw: ImageDraw.ImageDraw):
    draw.rounded_rectangle((PADDING, PRICE_TOP, WIDTH - PADDING, PRICE_TOP + PRICE_HEIGHT), radius=20, outline=BORDER, width=2, fill='#fbfdff')
    draw.rounded_rectangle((PADDING, MACD_TOP, WIDTH - PADDING, MACD_TOP + MACD_HEIGHT), radius=20, outline=BORDER, width=2, fill='#fbfdff')
    for idx in range(1, 5):
        y = PRICE_TOP + idx * PRICE_HEIGHT / 5
        draw.line((PADDING + 24, y, WIDTH - PADDING - 24, y), fill=GRID, width=1)
    for idx in range(1, 4):
        y = MACD_TOP + idx * MACD_HEIGHT / 4
        draw.line((PADDING + 24, y, WIDTH - PADDING - 24, y), fill=GRID, width=1)
    zero_y = MACD_TOP + MACD_HEIGHT / 2
    draw.line((PADDING + 24, zero_y, WIDTH - PADDING - 24, zero_y), fill=ZERO, width=2)
    axis_font = load_font(18)
    draw.text((WIDTH - PADDING - 78, zero_y - 30), '零轴', fill=ZERO, font=axis_font)
    return zero_y


def scale_series(values, top, height):
    low = min(values)
    high = max(values)
    span = max(high - low, 1e-6)
    return [top + height - ((value - low) / span) * height for value in values]


def x_points(count: int):
    left = PADDING + 36
    right = WIDTH - PADDING - 36
    step = (right - left) / (count - 1)
    return [left + index * step for index in range(count)]


def draw_price_line(draw: ImageDraw.ImageDraw, values):
    xs = x_points(len(values))
    ys = scale_series(values, PRICE_TOP + 28, PRICE_HEIGHT - 56)
    draw.line(list(zip(xs, ys)), fill=PRICE_LINE, width=6)
    for x, y in zip(xs, ys):
        draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=PRICE_LINE)
    return xs, ys


def draw_histogram(draw: ImageDraw.ImageDraw, bars):
    xs = x_points(len(bars))
    zero_y = MACD_TOP + MACD_HEIGHT / 2
    scale = (MACD_HEIGHT / 2 - 32) / max(max(abs(v) for v in bars), 1e-6)
    for x, value in zip(xs, bars):
        top = zero_y - value * scale
        color = RED if value >= 0 else GREEN
        draw.rectangle((x - 14, min(top, zero_y), x + 14, max(top, zero_y)), fill=color)


def draw_macd_lines(draw: ImageDraw.ImageDraw, dif, dea):
    xs = x_points(len(dif))
    combined = list(dif) + list(dea)
    low = min(combined)
    high = max(combined)
    span = max(high - low, 1e-6)

    def to_y(value):
        return MACD_TOP + 28 + (1 - (value - low) / span) * (MACD_HEIGHT - 56)

    dif_y = [to_y(value) for value in dif]
    dea_y = [to_y(value) for value in dea]
    draw.line(list(zip(xs, dif_y)), fill=BLUE, width=5)
    draw.line(list(zip(xs, dea_y)), fill=ORANGE, width=5)
    legend_font = load_font(20)
    draw.text((WIDTH - PADDING - 230, MACD_TOP + 20), 'DIF', fill=BLUE, font=legend_font)
    draw.text((WIDTH - PADDING - 150, MACD_TOP + 20), 'DEA', fill=ORANGE, font=legend_font)
    return xs, dif_y, dea_y


def add_annotation(draw: ImageDraw.ImageDraw, text: str, xy, width=250, color=TEXT):
    font = load_font(22)
    x, y = int(xy[0]), int(xy[1])
    draw.rounded_rectangle((x, y, x + width, y + 46), radius=14, fill=LABEL_BG, outline=BORDER, width=2)
    draw.text((x + 16, y + 10), text, fill=color, font=font)


def connect_annotation(draw: ImageDraw.ImageDraw, start, end, color=SUBTEXT):
    draw.line((start[0], start[1], end[0], end[1]), fill=color, width=2)


def add_note(draw: ImageDraw.ImageDraw, xs, price_y, macd_y, note):
    index = note['index']
    if note['type'] == 'price':
        box_x = xs[index] - 100
        box_y = max(PRICE_TOP + 18, price_y[index] - 88)
        add_annotation(draw, note['text'], (box_x, box_y), width=260)
        connect_annotation(draw, (box_x + 130, box_y + 46), (xs[index], price_y[index] + 6))
    else:
        box_x = min(WIDTH - PADDING - 280, xs[index] - 120)
        box_y = max(MACD_TOP + 20, macd_y[index] - 84)
        add_annotation(draw, note['text'], (box_x, box_y), width=260)
        connect_annotation(draw, (box_x + 130, box_y + 46), (xs[index], macd_y[index]))


def find_cross_index(dif, dea):
    for index in range(1, len(dif)):
        prev = dif[index - 1] - dea[index - 1]
        curr = dif[index] - dea[index]
        if prev <= 0 < curr or prev >= 0 > curr:
            return index
    return len(dif) // 2


def render_scenario(scenario):
    image, draw = create_canvas(scenario['title'], scenario['subtitle'])
    draw_panels(draw)
    price_xs, price_y = draw_price_line(draw, scenario['price'])
    draw_histogram(draw, scenario['bars'])
    xs, dif_y, dea_y = draw_macd_lines(draw, scenario['dif'], scenario['dea'])
    cross_index = find_cross_index(scenario['dif'], scenario['dea'])
    label_x = max(PADDING + 20, min(WIDTH - PADDING - 230, xs[cross_index] - 110))
    label_y = PRICE_TOP + 20
    add_annotation(draw, scenario['label'], (label_x, label_y), width=220)
    connect_annotation(draw, (label_x + 110, label_y + 46), (xs[cross_index], dif_y[cross_index]))
    for note in scenario.get('notes', []):
        add_note(draw, xs, price_y, dif_y, note)
    output_path = IMAGES_DIR / scenario['filename']
    image.save(output_path, format='PNG')


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    for scenario in SCENARIOS:
        render_scenario(scenario)


if __name__ == '__main__':
    main()
