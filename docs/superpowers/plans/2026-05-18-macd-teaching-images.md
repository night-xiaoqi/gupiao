# MACD Teaching Images Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 生成一套统一风格的 MACD 教学示意图，并把它们插入到现有 Markdown 教程中。

**Architecture:** 使用现有代码库里已经存在的 Python + Pillow 绘图方式，新增一个独立脚本生成 8 张 MACD 教学图。图片输出到 `images/` 目录，Markdown 文档继续引用既定文件名，不改整体文档结构，只把占位图变成实际可显示图片。

**Tech Stack:** Python 3、Pillow、pathlib、Markdown

---

### Task 1: 确定图片生成脚本骨架

**Files:**
- Create: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_macd_teaching_images.py`
- Reference: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_teacher_handout.py`
- Reference: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_stock_screen_explainer_pdf.py`

- [ ] **Step 1: 写出最小脚本骨架**

```python
from pathlib import Path

BASE_DIR = Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao')
IMAGES_DIR = BASE_DIR / 'images'

OUTPUT_FILES = [
    'macd-golden-cross-example.png',
    'macd-death-cross-example.png',
    'macd-second-golden-cross-above-zero-example.png',
    'macd-weak-golden-cross-below-zero-example.png',
    'macd-red-bars-expanding-example.png',
    'macd-top-divergence-example.png',
    'macd-bottom-divergence-example.png',
    'macd-high-level-blunt-example.png',
]


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    for name in OUTPUT_FILES:
        path = IMAGES_DIR / name
        path.write_bytes(b'')


if __name__ == '__main__':
    main()
```

- [ ] **Step 2: 运行脚本骨架，确认目录与文件创建逻辑可执行**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_macd_teaching_images.py`
Expected: 正常退出，无报错

- [ ] **Step 3: 删除空文件写法，准备进入真实绘图实现**

```python
def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
```

### Task 2: 实现统一风格绘图底座

**Files:**
- Modify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_macd_teaching_images.py`

- [ ] **Step 1: 添加 Pillow 画布、颜色、字体和通用布局常量**

```python
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1400
HEIGHT = 900
PADDING = 72
PRICE_TOP = 110
PRICE_HEIGHT = 300
MACD_TOP = 500
MACD_HEIGHT = 250
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
```

- [ ] **Step 2: 添加字体加载与基础画布函数**

```python
def load_font(size: int, bold: bool = False):
    candidates = [
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
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
    title_font = load_font(44, bold=True)
    subtitle_font = load_font(24)
    draw.text((PADDING, 42), title, fill=TEXT, font=title_font)
    draw.text((PADDING, 92), subtitle, fill=SUBTEXT, font=subtitle_font)
    return image, draw
```

- [ ] **Step 3: 添加价格区、MACD 区、网格线、零轴绘制函数**

```python
def draw_panels(draw):
    draw.rounded_rectangle((PADDING, PRICE_TOP, WIDTH - PADDING, PRICE_TOP + PRICE_HEIGHT), radius=20, outline=BORDER, width=2, fill='#fbfdff')
    draw.rounded_rectangle((PADDING, MACD_TOP, WIDTH - PADDING, MACD_TOP + MACD_HEIGHT), radius=20, outline=BORDER, width=2, fill='#fbfdff')
    for idx in range(1, 5):
        y = PRICE_TOP + idx * PRICE_HEIGHT / 5
        draw.line((PADDING + 24, y, WIDTH - PADDING - 24, y), fill=GRID, width=1)
    zero_y = MACD_TOP + MACD_HEIGHT / 2
    draw.line((PADDING + 24, zero_y, WIDTH - PADDING - 24, zero_y), fill=ZERO, width=2)
    return zero_y
```

### Task 3: 实现通用序列绘制函数

**Files:**
- Modify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_macd_teaching_images.py`

- [ ] **Step 1: 添加数列归一化与折线坐标转换函数**

```python
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
```

- [ ] **Step 2: 添加价格线、DIF/DEA 线、柱状图绘制函数**

```python
def draw_price_line(draw, values):
    xs = x_points(len(values))
    ys = scale_series(values, PRICE_TOP + 28, PRICE_HEIGHT - 56)
    draw.line(list(zip(xs, ys)), fill=BLUE, width=6)


def draw_macd_lines(draw, dif, dea):
    xs = x_points(len(dif))
    dif_y = scale_series(dif, MACD_TOP + 28, MACD_HEIGHT - 56)
    dea_y = scale_series(dea, MACD_TOP + 28, MACD_HEIGHT - 56)
    draw.line(list(zip(xs, dif_y)), fill=BLUE, width=5)
    draw.line(list(zip(xs, dea_y)), fill=ORANGE, width=5)
    return xs, dif_y, dea_y


def draw_histogram(draw, bars):
    xs = x_points(len(bars))
    zero_y = MACD_TOP + MACD_HEIGHT / 2
    scale = (MACD_HEIGHT / 2 - 36) / max(max(abs(v) for v in bars), 1e-6)
    for x, value in zip(xs, bars):
        top = zero_y - value * scale
        color = RED if value >= 0 else GREEN
        draw.rectangle((x - 10, min(top, zero_y), x + 10, max(top, zero_y)), fill=color)
```

- [ ] **Step 3: 添加标注函数**

```python
def add_annotation(draw, text, xy, color=TEXT):
    font = load_font(26)
    draw.rounded_rectangle((xy[0], xy[1], xy[0] + 250, xy[1] + 48), radius=14, fill='#eef4ff', outline=BORDER, width=2)
    draw.text((xy[0] + 16, xy[1] + 10), text, fill=color, font=font)
```

### Task 4: 定义 8 张教学图的数据模板并生成图片

**Files:**
- Modify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_macd_teaching_images.py`

- [ ] **Step 1: 为 8 类 MACD 场景定义数据模板**

```python
SCENARIOS = [
    {
        'filename': 'macd-golden-cross-example.png',
        'title': 'MACD 金叉示意图',
        'subtitle': 'DIF 自下向上穿越 DEA，短期走势开始转强',
        'price': [10.8, 10.6, 10.3, 10.1, 10.0, 10.1, 10.3, 10.5, 10.8, 11.1, 11.4, 11.7],
        'dif':   [-0.8, -0.9, -0.8, -0.6, -0.4, -0.2,  0.1,  0.3,  0.5,  0.7,  0.8,  0.9],
        'dea':   [-0.5, -0.6, -0.6, -0.55,-0.45,-0.3, -0.1,  0.05, 0.2,  0.35, 0.5,  0.62],
        'bars':  [-0.3, -0.3, -0.2, -0.1,  0.0,  0.1,  0.2,  0.25, 0.3,  0.35, 0.3,  0.28],
        'label': '金叉',
    },
]
```

- [ ] **Step 2: 按同样结构补齐其余 7 个场景**

```python
# 其余场景需补齐：
# macd-death-cross-example.png
# macd-second-golden-cross-above-zero-example.png
# macd-weak-golden-cross-below-zero-example.png
# macd-red-bars-expanding-example.png
# macd-top-divergence-example.png
# macd-bottom-divergence-example.png
# macd-high-level-blunt-example.png
```

- [ ] **Step 3: 实现单图渲染与批量导出**

```python
def render_scenario(scenario):
    image, draw = create_canvas(scenario['title'], scenario['subtitle'])
    draw_panels(draw)
    draw_price_line(draw, scenario['price'])
    draw_histogram(draw, scenario['bars'])
    xs, dif_y, dea_y = draw_macd_lines(draw, scenario['dif'], scenario['dea'])
    cross_index = len(xs) // 2
    add_annotation(draw, scenario['label'], (int(xs[cross_index] - 80), 150))
    output_path = IMAGES_DIR / scenario['filename']
    image.save(output_path, format='PNG')


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    for scenario in SCENARIOS:
        render_scenario(scenario)
```

- [ ] **Step 4: 运行脚本并生成图片**

Run: `python3 /Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_macd_teaching_images.py`
Expected: `images/` 目录下生成 8 张 PNG 图片，无报错

### Task 5: 为关键场景增加更明确的视觉标注

**Files:**
- Modify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/generate_macd_teaching_images.py`

- [ ] **Step 1: 为顶背离、底背离添加高低点标识**

```python
def add_peak_labels(draw, xs, price_values, text_left, text_right):
    price_y = scale_series(price_values, PRICE_TOP + 28, PRICE_HEIGHT - 56)
    left_index = len(xs) // 3
    right_index = len(xs) * 2 // 3
    add_annotation(draw, text_left, (int(xs[left_index] - 120), int(price_y[left_index] - 80)))
    add_annotation(draw, text_right, (int(xs[right_index] - 120), int(price_y[right_index] - 80)))
```

- [ ] **Step 2: 为零轴上方/下方场景添加“零轴上方”“零轴下方”提示**

```python
def add_zero_axis_note(draw, text):
    font = load_font(24)
    draw.text((WIDTH - PADDING - 220, MACD_TOP + MACD_HEIGHT / 2 - 42), text, fill=SUBTEXT, font=font)
```

- [ ] **Step 3: 为红柱放大与高位钝化增加趋势说明标签**

```python
# 示例标签文案
# '红柱持续放大'
# '高位钝化，警惕追高'
```

### Task 6: 验证图片尺寸与文件产出

**Files:**
- Verify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/images/*.png`

- [ ] **Step 1: 列出生成结果，确认 8 张图片全部存在**

Run: `ls -1 /Users/tianxiang.yang/Desktop/yang/study/gupiao/images`
Expected: 输出 8 个以 `macd-` 开头的 PNG 文件名

- [ ] **Step 2: 抽查图片元数据，确认尺寸一致**

Run: `python3 - <<'PY'
from pathlib import Path
from PIL import Image
for path in sorted(Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao/images').glob('macd-*.png')):
    print(path.name, Image.open(path).size)
PY`
Expected: 每张图片输出 `(1400, 900)`

### Task 7: 将生成图片接入 Markdown 文档

**Files:**
- Modify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/MACD入门教程与实战详解.md`

- [ ] **Step 1: 保持现有 Markdown 图片路径不变，只确认图片文件实际存在**

```md
![金叉实例分析图](images/macd-golden-cross-example.png)
![死叉实例分析图](images/macd-death-cross-example.png)
![零轴上方二次金叉实例分析图](images/macd-second-golden-cross-above-zero-example.png)
![零轴下方弱势金叉实例分析图](images/macd-weak-golden-cross-below-zero-example.png)
![红柱放大趋势增强实例分析图](images/macd-red-bars-expanding-example.png)
![顶背离实例分析图](images/macd-top-divergence-example.png)
![底背离实例分析图](images/macd-bottom-divergence-example.png)
![高位钝化实例分析图](images/macd-high-level-blunt-example.png)
```

- [ ] **Step 2: 如果有未命中的命名，统一修正为与图片文件一致**

```md
# 仅在脚本生成文件名与 Markdown 引用不一致时修改
```

### Task 8: 最终验证

**Files:**
- Verify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/MACD入门教程与实战详解.md`
- Verify: `/Users/tianxiang.yang/Desktop/yang/study/gupiao/images/*.png`

- [ ] **Step 1: 搜索文档中的图片引用，确认全部 8 条存在**

Run: `python3 - <<'PY'
from pathlib import Path
text = Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao/MACD入门教程与实战详解.md').read_text(encoding='utf-8')
for line in text.splitlines():
    if '![‘' in line or '![' in line:
        print(line)
PY`
Expected: 输出 8 条 `images/macd-*.png` 的 Markdown 图片引用

- [ ] **Step 2: 人工抽查文档与图片目录是否匹配**

Run: `python3 - <<'PY'
from pathlib import Path
import re
text = Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao/MACD入门教程与实战详解.md').read_text(encoding='utf-8')
paths = re.findall(r'\((images/[^)]+)\)', text)
for rel in paths:
    full = Path('/Users/tianxiang.yang/Desktop/yang/study/gupiao') / rel
    print(rel, 'OK' if full.exists() else 'MISSING')
PY`
Expected: 8 条引用全部显示 `OK`
