from math import sin, cos, pi
from pathlib import Path

from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "NT132-adaptive-threshold-presentation.pdf"

W, H = 1920, 1080
MARGIN = 110

BLUE = colors.HexColor("#2563EB")
BLUE_DARK = colors.HexColor("#1D4ED8")
BLUE_LIGHT = colors.HexColor("#DBEAFE")
SLATE = colors.HexColor("#64748B")
TEXT = colors.HexColor("#111827")
MUTED = colors.HexColor("#6B7280")
RED = colors.HexColor("#DC2626")
RED_LIGHT = colors.HexColor("#FEE2E2")
GRAY_50 = colors.HexColor("#F8FAFC")
GRAY_100 = colors.HexColor("#F1F5F9")
GRAY_200 = colors.HexColor("#E5E7EB")
GRAY_300 = colors.HexColor("#CBD5E1")
GREEN = colors.HexColor("#16A34A")
GREEN_LIGHT = colors.HexColor("#DCFCE7")


def register_fonts():
    fonts = Path("C:/Windows/Fonts")
    try:
        pdfmetrics.registerFont(TTFont("Deck", str(fonts / "segoeui.ttf")))
        pdfmetrics.registerFont(TTFont("Deck-Bold", str(fonts / "segoeuib.ttf")))
        pdfmetrics.registerFont(TTFont("Deck-Italic", str(fonts / "segoeuii.ttf")))
    except Exception:
        pass


def set_font(c, size, bold=False, italic=False, color=TEXT):
    name = "Deck-Bold" if bold else "Deck-Italic" if italic else "Deck"
    c.setFont(name, size)
    c.setFillColor(color)


def header(c, title, page):
    c.setFillColor(colors.white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    set_font(c, 46, True)
    c.drawString(MARGIN, H - 100, title)
    c.setStrokeColor(GRAY_200)
    c.setLineWidth(2)
    c.line(MARGIN, H - 132, W - MARGIN, H - 132)
    set_font(c, 18, False, color=MUTED)
    c.drawRightString(W - MARGIN, 46, f"NT132 | Temporal NIDS Benchmark | {page:02d}")


def pill(c, x, y, w, h, text, fill=GRAY_100, stroke=GRAY_300, color=TEXT, size=24):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(2)
    c.roundRect(x, y, w, h, 16, fill=1, stroke=1)
    set_font(c, size, True, color=color)
    c.drawCentredString(x + w / 2, y + h / 2 - size * 0.36, text)


def box(c, x, y, w, h, title, body=None, fill=colors.white, stroke=GRAY_300, title_color=TEXT):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(2)
    c.roundRect(x, y, w, h, 18, fill=1, stroke=1)
    set_font(c, 28, True, color=title_color)
    c.drawString(x + 28, y + h - 48, title)
    if body:
        set_font(c, 22, False, color=MUTED)
        draw_lines(c, body, x + 28, y + h - 88, w - 56, 28)


def arrow(c, x1, y1, x2, y2, color=BLUE, width=4):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)
    angle = pi if x2 < x1 else 0
    size = 16
    c.setFillColor(color)
    c.line(x2, y2, x2 - size * cos(angle + pi / 6), y2 - size * sin(angle + pi / 6))
    c.line(x2, y2, x2 - size * cos(angle - pi / 6), y2 - size * sin(angle - pi / 6))


def draw_lines(c, lines, x, y, width, leading, size=22, color=MUTED):
    set_font(c, size, False, color=color)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def neural_icon(c, cx, cy, scale=1, label="MLP"):
    c.setStrokeColor(BLUE)
    c.setLineWidth(2.2)
    xs = [cx - 46 * scale, cx, cx + 46 * scale]
    ys = [[cy - 35 * scale, cy, cy + 35 * scale], [cy - 25 * scale, cy + 25 * scale], [cy]]
    for i in range(2):
        for y1 in ys[i]:
            for y2 in ys[i + 1]:
                c.line(xs[i], y1, xs[i + 1], y2)
    for i, col in enumerate(ys):
        for y in col:
            c.setFillColor(colors.white)
            c.circle(xs[i], y, 10 * scale, fill=1, stroke=1)
    set_font(c, 23, True, color=BLUE_DARK)
    c.drawCentredString(cx, cy - 72 * scale, label)


def traffic_icon(c, x, y):
    c.setStrokeColor(BLUE)
    c.setLineWidth(3)
    for i in range(4):
        yy = y + i * 32
        c.line(x, yy, x + 180, yy + (12 if i % 2 else -12))
        c.circle(x, yy, 7, fill=0, stroke=1)
        c.circle(x + 180, yy + (12 if i % 2 else -12), 7, fill=0, stroke=1)


def mini_distribution(c, x, y, w, h, shifted=False):
    c.setStrokeColor(GRAY_300)
    c.setLineWidth(2)
    c.line(x, y, x + w, y)
    c.line(x, y, x, y + h)
    c.setStrokeColor(BLUE if not shifted else RED)
    c.setLineWidth(4)
    p = c.beginPath()
    p.moveTo(x + 10, y + 6)
    peak = x + (w * 0.42 if not shifted else w * 0.65)
    p.curveTo(x + w * 0.20, y + h * 0.18, peak - 80, y + h * 0.96, peak, y + h * 0.92)
    p.curveTo(peak + 80, y + h * 0.86, x + w * 0.82, y + h * 0.18, x + w - 12, y + 8)
    c.drawPath(p)


def chart_axes(c, x, y, w, h, title=None):
    c.setStrokeColor(GRAY_300)
    c.setLineWidth(2)
    c.line(x, y, x + w, y)
    c.line(x, y, x, y + h)
    for i in range(1, 5):
        yy = y + h * i / 5
        c.setStrokeColor(GRAY_100)
        c.line(x, yy, x + w, yy)
    if title:
        set_font(c, 22, True, color=TEXT)
        c.drawString(x, y + h + 28, title)


def slide1(c):
    header(c, "Problem Introduction", 1)
    set_font(c, 30, False, color=MUTED)
    c.drawString(MARGIN, H - 184, "When data distribution shifts over time, fixed NIDS models lose detection reliability.")

    box(c, 135, 360, 430, 300, "Training period", ["Monday-Tuesday", "Stable traffic distribution"], fill=GRAY_50, stroke=BLUE_LIGHT)
    mini_distribution(c, 210, 410, 260, 120, shifted=False)
    traffic_icon(c, 210, 540)
    neural_icon(c, 450, 548, 0.72, "MLP")
    neural_icon(c, 520, 448, 0.68, "CNN")

    c.setStrokeColor(BLUE)
    c.setLineWidth(5)
    c.line(620, 510, 1300, 510)
    for i, txt in enumerate(["t0", "t1", "t2", "t3"]):
        x = 680 + i * 170
        c.circle(x, 510, 8, fill=1, stroke=0)
        set_font(c, 20, False, color=MUTED)
        c.drawCentredString(x, 472, txt)
    arrow(c, 1240, 510, 1325, 510)
    set_font(c, 26, True, color=BLUE_DARK)
    c.drawCentredString(970, 565, "Temporal drift")

    box(c, 1355, 360, 430, 300, "Shifted period", ["Wednesday-Friday", "Domain shift + lower F1"], fill=GRAY_50, stroke=RED_LIGHT)
    mini_distribution(c, 1430, 410, 260, 120, shifted=True)
    pill(c, 1450, 560, 260, 64, "F1 declines", fill=RED_LIGHT, stroke=RED_LIGHT, color=RED, size=24)


def slide2(c):
    header(c, "Experimental Benchmark Pipeline", 2)
    c.setStrokeColor(BLUE_LIGHT)
    c.setLineWidth(4)
    c.roundRect(95, 180, 1730, 690, 28, fill=0, stroke=1)
    pill(c, 130, 830, 380, 58, "PyTorch Benchmark Framework", fill=BLUE_LIGHT, stroke=BLUE_LIGHT, color=BLUE_DARK, size=24)

    box(c, 155, 425, 300, 280, "Baseline models", fill=colors.white, stroke=GRAY_200)
    neural_icon(c, 245, 565, 0.78, "MLP")
    neural_icon(c, 365, 565, 0.78, "CNN")
    arrow(c, 485, 565, 605, 565)

    box(c, 625, 310, 640, 430, "CICIDS-2017 temporal split", fill=GRAY_50, stroke=GRAY_200)
    c.setStrokeColor(BLUE)
    c.setLineWidth(3)
    c.roundRect(670, 390, 215, 245, 18, fill=0, stroke=1)
    pill(c, 700, 605, 155, 42, "TRAIN SET", fill=BLUE_LIGHT, stroke=BLUE_LIGHT, color=BLUE_DARK, size=18)
    c.setStrokeColor(RED)
    c.roundRect(915, 390, 305, 245, 18, fill=0, stroke=1)
    pill(c, 985, 605, 170, 42, "TEST SET", fill=RED_LIGHT, stroke=RED_LIGHT, color=RED, size=18)
    for x, day, col in [(690, "Mon", BLUE), (790, "Tue", BLUE), (940, "Wed", RED), (1040, "Thu", RED), (1140, "Fri", RED)]:
        pill(c, x, 455, 76, 86, day, fill=colors.white, stroke=col, color=col, size=22)

    arrow(c, 1295, 565, 1415, 565)
    box(c, 1435, 425, 310, 280, "Evaluation", ["F1-score", "Mean", "Standard deviation", "Performance comparison"], fill=colors.white, stroke=GRAY_200)


def slide3(c):
    header(c, "Performance Degradation Under Temporal Distribution Shift", 3)
    set_font(c, 28, False, color=MUTED)
    c.drawString(MARGIN, H - 184, "Benchmark results will be inserted after experiments; structure emphasizes trend and temporal shift.")
    x, y, w, h = 250, 250, 1320, 520
    chart_axes(c, x, y, w, h, "F1-score across testing days")
    days = ["Wed", "Thu", "Fri"]
    vals_mlp = [0.88, 0.76, 0.63]
    vals_cnn = [0.91, 0.79, 0.66]
    for i, day in enumerate(days):
        px = x + 260 + i * 380
        set_font(c, 24, False, color=MUTED)
        c.drawCentredString(px, y - 42, day)
        for val, offset, col in [(vals_mlp[i], -32, BLUE), (vals_cnn[i], 32, SLATE)]:
            bh = h * val
            c.setFillColor(col)
            c.roundRect(px + offset - 24, y, 48, bh, 10, fill=1, stroke=0)
    pill(c, 1260, 815, 135, 42, "MLP", fill=BLUE_LIGHT, stroke=BLUE_LIGHT, color=BLUE_DARK, size=18)
    pill(c, 1410, 815, 135, 42, "CNN", fill=GRAY_100, stroke=GRAY_200, color=SLATE, size=18)
    pill(c, 725, 155, 470, 58, "Temporal split reveals degradation trend", fill=RED_LIGHT, stroke=RED_LIGHT, color=RED, size=22)


def slide4(c):
    header(c, "Adaptive Threshold Estimation via Extreme Value Theory", 4)
    steps = ["Anomaly Scores", "Tail Extraction", "GPD Fitting", "Threshold Estimation", "Adaptive Calibration", "Final Decision"]
    x0, y = 135, 520
    for i, step in enumerate(steps):
        x = x0 + i * 290
        box(c, x, y, 230, 130, step, fill=GRAY_50, stroke=BLUE_LIGHT, title_color=BLUE_DARK)
        if i < len(steps) - 1:
            arrow(c, x + 235, y + 65, x + 280, y + 65)
    box(c, 260, 285, 420, 115, "EVT principle", ["Rare-event probability is estimated from the tail."], fill=colors.white, stroke=GRAY_200)
    box(c, 750, 285, 420, 115, "GPD model", ["Excess scores above threshold u model the tail."], fill=colors.white, stroke=GRAY_200)
    box(c, 1240, 285, 420, 115, "Outlier filtering", ["KS-test removes target-contaminated tail samples."], fill=colors.white, stroke=GRAY_200)
    set_font(c, 24, False, italic=True, color=MUTED)
    c.drawCentredString(W / 2, 190, "Detailed theoretical foundation presented in the following slides.")


def slide5(c):
    header(c, "Classical Foundation: Fisher-Tippett Theorem", 5)
    box(c, 130, 285, 620, 470, "Maxima convergence", [
        "Let M_n = max(X_1, ..., X_n) for i.i.d. samples.",
        "With normalizing constants a_n > 0 and b_n:",
        "(M_n - b_n) / a_n  ->  H(x)",
        "H must be one of: Gumbel, Frechet, Weibull.",
    ], fill=GRAY_50, stroke=GRAY_200)
    x, y, w, h = 900, 300, 760, 420
    chart_axes(c, x, y, w, h, "Intuition: maxima approach a limiting family")
    for j, col in enumerate([GRAY_300, SLATE, BLUE]):
        c.setStrokeColor(col)
        c.setLineWidth(3 if col == BLUE else 2)
        p = c.beginPath()
        p.moveTo(x + 40, y + 20)
        peak = x + 230 + j * 110
        p.curveTo(x + 160 + j * 45, y + 105, peak - 90, y + 350, peak, y + 330)
        p.curveTo(peak + 100, y + 310, x + 560 + j * 25, y + 110, x + 700, y + 30)
        c.drawPath(p)
    pill(c, 1010, 190, 560, 62, "Foundation for modeling distribution extremes", fill=BLUE_LIGHT, stroke=BLUE_LIGHT, color=BLUE_DARK, size=24)


def slide6(c):
    header(c, "Generalized Pareto Distribution", 6)
    box(c, 125, 320, 610, 380, "Tail model above threshold u", [
        "For excess x = X - u, x >= 0:",
        "G_{xi,beta}(x) = 1 - (1 + xi x / beta)^(-1/xi)",
        "Shape xi controls tail heaviness.",
        "Scale beta controls spread of excesses.",
    ], fill=GRAY_50, stroke=GRAY_200)
    x, y, w, h = 880, 285, 780, 470
    chart_axes(c, x, y, w, h, "Distribution tail modeled by GPD")
    c.setStrokeColor(BLUE)
    c.setLineWidth(4)
    p = c.beginPath()
    p.moveTo(x + 30, y + 20)
    p.curveTo(x + 150, y + 390, x + 300, y + 420, x + 390, y + 300)
    p.curveTo(x + 510, y + 145, x + 640, y + 80, x + 735, y + 45)
    c.drawPath(p)
    ux = x + 470
    c.setStrokeColor(RED)
    c.setLineWidth(3)
    c.line(ux, y, ux, y + h)
    set_font(c, 24, True, color=RED)
    c.drawCentredString(ux, y - 42, "threshold u")
    c.setFillColor(RED_LIGHT)
    c.rect(ux, y, x + w - ux, h, fill=1, stroke=0)
    c.setStrokeColor(BLUE)
    c.drawPath(p)


def slide7(c):
    header(c, "GPD-based Threshold Estimation", 7)
    steps = ["Scores", "Tail Selection", "Fit xi, beta", "Tail Probability", "Compute tau_q"]
    y = 565
    for i, step in enumerate(steps):
        x = 175 + i * 340
        box(c, x, y, 260, 120, step, fill=GRAY_50, stroke=BLUE_LIGHT, title_color=BLUE_DARK)
        if i < len(steps) - 1:
            arrow(c, x + 265, y + 60, x + 325, y + 60)
    box(c, 245, 290, 1430, 150, "Threshold equation", [
        "tau_q = u + (beta_hat / xi_hat) [ ((N / n)(1 - q))^(-xi_hat) - 1 ]",
        "u isolates the upper tail; n is the number of samples above u; q sets the target cdf level.",
    ], fill=colors.white, stroke=GRAY_200)
    pill(c, 685, 190, 550, 62, "Adaptive threshold output for low false-alarm operation", fill=BLUE_LIGHT, stroke=BLUE_LIGHT, color=BLUE_DARK, size=23)


def slide8(c):
    header(c, "Adaptive Calibration via Outlier Identification", 8)
    steps = ["Validation Scores", "KS Statistical Test", "Outlier Detection", "Remove Suspicious Samples", "Refit Distribution", "Updated Threshold"]
    x0, y = 135, 560
    for i, step in enumerate(steps):
        x = x0 + i * 290
        box(c, x, y, 230, 115, step, fill=GRAY_50, stroke=BLUE_LIGHT if i != 2 else RED_LIGHT, title_color=RED if i == 2 else BLUE_DARK)
        if i < len(steps) - 1:
            arrow(c, x + 235, y + 58, x + 280, y + 58, color=RED if i in [1, 2, 3] else BLUE)
    c.setStrokeColor(BLUE)
    c.setLineWidth(4)
    c.arc(1120, 390, 1470, 660, 200, 130)
    arrow(c, 1115, 462, 1015, 560, color=BLUE)
    box(c, 275, 295, 430, 145, "Normal samples", ["Empirical tail agrees with fitted GPD."], fill=GREEN_LIGHT, stroke=GREEN, title_color=GREEN)
    box(c, 775, 295, 430, 145, "Attack outliers", ["Largest scores make the tail fail the KS test."], fill=RED_LIGHT, stroke=RED, title_color=RED)
    box(c, 1275, 295, 430, 145, "Iterative refinement", ["Minimize KS statistic after pruning top scores."], fill=colors.white, stroke=GRAY_200)


def slide9(c):
    header(c, "Performance After Adaptive Threshold Calibration", 9)
    set_font(c, 28, False, color=MUTED)
    c.drawString(MARGIN, H - 184, "Final experiment values will be inserted after calibration runs.")
    x, y, w, h = 230, 295, 680, 440
    chart_axes(c, x, y, w, h, "Before vs after F1-score")
    groups = [("Baseline", 0.64, RED), ("EVT calibrated", 0.84, BLUE)]
    for i, (lab, val, col) in enumerate(groups):
        px = x + 220 + i * 250
        c.setFillColor(col)
        c.roundRect(px - 42, y, 84, h * val, 12, fill=1, stroke=0)
        set_font(c, 24, False, color=MUTED)
        c.drawCentredString(px, y - 44, lab)
    x2, y2 = 1110, 345
    box(c, x2, y2 + 230, 500, 115, "Reduced false positives", ["Threshold tracks the clean tail after outlier removal."], fill=GREEN_LIGHT, stroke=GREEN, title_color=GREEN)
    box(c, x2, y2 + 75, 500, 115, "Improved robustness", ["Calibration counters temporal distribution shift."], fill=BLUE_LIGHT, stroke=BLUE_LIGHT, title_color=BLUE_DARK)
    box(c, x2, y2 - 80, 500, 115, "Baseline comparison", ["Report F1, FPR, mean and standard deviation."], fill=colors.white, stroke=GRAY_200)


def main():
    register_fonts()
    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    c.setTitle("Adaptive Threshold NIDS Presentation")
    for fn in [slide1, slide2, slide3, slide4, slide5, slide6, slide7, slide8, slide9]:
        fn(c)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
