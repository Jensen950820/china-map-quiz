"""Apply Apple-style CSS and JS canvas colors to all province map.html files."""

import os
import re

BASE = r"C:\Users\user\Desktop\共享文件夹\【项目与工具】\【代码-暂存】\互动地图"

NEW_CSS = """<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #000; color: #f5f5f7; display: flex; height: 100vh; overflow: hidden; user-select: none; }
#map-wrap { flex: 1; position: relative; display: flex; align-items: center; justify-content: center; }
canvas { display: block; cursor: pointer; border-radius: 16px; }
#panel { width: 380px; background: rgba(28,28,30,0.82); backdrop-filter: blur(50px) saturate(180%); -webkit-backdrop-filter: blur(50px) saturate(180%); display: flex; flex-direction: column; padding: 24px; gap: 16px; overflow-y: auto; border-left: 1px solid rgba(255,255,255,0.06); }
h1 { font-size: 18px; text-align: center; color: #f5f5f7; font-weight: 600; letter-spacing: 1px; }
h2 { font-size: 13px; text-align: center; color: #98989d; font-weight: 400; }
#prog-bar { background: rgba(255,255,255,0.08); border-radius: 3px; height: 4px; overflow: hidden; }
#prog-fill { height: 100%; background: linear-gradient(90deg, #FF453A, #FFD60A, #30D158); border-radius: 3px; transition: width 0.5s cubic-bezier(0.4,0,0.2,1); width: 0%; }
#prog-text { text-align: center; font-size: 12px; color: #98989d; font-weight: 500; }
#quiz-area { background: rgba(255,255,255,0.05); border-radius: 14px; padding: 16px; display: none; flex-direction: column; gap: 10px; border: 1px solid rgba(255,255,255,0.06); }
#quiz-area.active { display: flex; }
#quiz-q { font-size: 14px; text-align: center; color: #f5f5f7; font-weight: 500; }
#quiz-ops { display: flex; flex-direction: column; gap: 8px; }
.qbtn { padding: 12px 14px; border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.04); color: #f5f5f7; border-radius: 10px; cursor: pointer; font-size: 14px; transition: all 0.2s ease; text-align: center; font-weight: 500; }
.qbtn:hover { border-color: #007AFF; background: rgba(0,122,255,0.1); transform: scale(1.01); }
.qbtn.correct { background: rgba(48,209,88,0.2); border-color: #30D158; color: #30D158; }
.qbtn.wrong { background: rgba(255,69,58,0.2); border-color: #FF453A; color: #FF453A; }
.qbtn:disabled { pointer-events: none; opacity: 0.5; }
#result-t { text-align: center; font-size: 14px; min-height: 20px; color: #30D158; font-weight: 500; }
#result-t.error { color: #FF453A; }
#hint { background: rgba(255,255,255,0.04); border-radius: 14px; padding: 14px 16px; font-size: 12px; line-height: 1.7; color: #98989d; border: 1px solid rgba(255,255,255,0.06); }
#hint strong { color: #f5f5f7; font-weight: 600; }
#hint-t { font-style: italic; color: #8e8e93; }
.btn-row { display: flex; gap: 10px; }
.btn { flex: 1; padding: 10px 14px; border: none; border-radius: 10px; cursor: pointer; font-size: 13px; font-weight: 600; transition: all 0.2s ease; }
.btn-reset { background: rgba(255,69,58,0.12); color: #FF453A; }
.btn-reset:hover { background: rgba(255,69,58,0.22); }
.btn-back { background: rgba(0,122,255,0.12); color: #007AFF; display: none; }
.btn-back.show { display: block; }
.btn-back:hover { background: rgba(0,122,255,0.22); }
.mode-row { display: flex; gap: 0; border-radius: 10px; overflow: hidden; border: 1px solid rgba(255,255,255,0.08); }
.mode-btn { flex: 1; padding: 8px 0; border: none; cursor: pointer; font-size: 13px; font-weight: 600; background: rgba(255,255,255,0.03); color: #98989d; transition: all 0.2s ease; }
.mode-btn.active { background: #007AFF; color: #fff; }
.mode-btn:first-child { border-right: 1px solid rgba(255,255,255,0.08); }
.mode-btn:hover:not(.active) { background: rgba(255,255,255,0.08); color: #f5f5f7; }
.legend { display: flex; gap: 14px; justify-content: center; font-size: 11px; color: #98989d; }
.leg-dot { width: 10px; height: 10px; border-radius: 3px; display: inline-block; vertical-align: middle; margin-right: 4px; }
#score { display: flex; justify-content: space-around; font-size: 13px; color: #98989d; }
#score span { color: #f5f5f7; font-weight: 600; }
</style>"""

STYLE_PATTERN = re.compile(r"<style>.*?</style>", re.DOTALL)

# JS string replacements: (old, new)
JS_REPLACEMENTS = [
    # Canvas background
    ("ctx.fillStyle='#0a0a1a'", "ctx.fillStyle='#000'"),
    ("ctx.fillStyle = '#0a0a1a'", "ctx.fillStyle = '#000'"),
    ("ctx.fillStyle='rgba(20,50,90,0.6)'", "ctx.fillStyle='rgba(255,255,255,0.02)'"),
    (
        "ctx.fillStyle = 'rgba(20,50,90,0.6)'",
        "ctx.fillStyle = 'rgba(255,255,255,0.02)'",
    ),
    # Province fill/stroke
    ("let fc='#162447'", "let fc='#1c1c24'"),
    ("let fc = '#162447'", "let fc = '#1c1c24'"),
    ("drawFeature(f,'#3a5f8a'", "drawFeature(f,'#3a3a44'"),
    ("drawFeature(f, '#3a5f8a'", "drawFeature(f, '#3a3a44'"),
    # County fill/stroke
    ("let fc='#1e3a5f'", "let fc='#262632'"),
    ("let fc = '#1e3a5f'", "let fc = '#262632'"),
    ("drawFeature(f,'#4466aa'", "drawFeature(f,'#4a4a55'"),
    ("drawFeature(f, '#4466aa'", "drawFeature(f, '#4a4a55'"),
    # Correct/wrong fills
    ("'rgba(39,174,96,0.45)'", "'rgba(48,209,88,0.3)'"),
    ("'rgba(39,174,96,0.5)'", "'rgba(48,209,88,0.35)'"),
    ("'rgba(192,57,43,0.45)'", "'rgba(255,69,58,0.3)'"),
    ("'rgba(192,57,43,0.5)'", "'rgba(255,69,58,0.35)'"),
    # Label colors
    ("'#2ecc71'", "'#30D158'"),
    ("'#e74c3c'", "'#FF453A'"),
    # Highlight - replace #f0c040 with #007AFF, and gold fills with blue
    ("'#f0c040'", "'#007AFF'"),
    ("'rgba(240,192,64,0.08)'", "'rgba(0,122,255,0.06)'"),
    ("'rgba(240,192,64,0.1)'", "'rgba(0,122,255,0.08)'"),
    ("'rgba(240,192,64,0.12)'", "'rgba(0,122,255,0.08)'"),
    ("'rgba(240,192,64,0.18)'", "'rgba(0,122,255,0.14)'"),
    # Font in drawLabel
    (
        "'px \"Microsoft YaHei\"'",
        'px -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Microsoft YaHei", sans-serif\'',
    ),
    (
        "px 'Microsoft YaHei'",
        "px -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang SC', 'Microsoft YaHei', sans-serif",
    ),
    # Font in drawTitle
    (
        "'16px \"Microsoft YaHei\"'",
        '\'14px -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Microsoft YaHei", sans-serif\'',
    ),
    # Stroke style
    ("ctx.strokeStyle='rgba(0,0,0,0.65)'", "ctx.strokeStyle='rgba(0,0,0,0.6)'"),
    ("ctx.strokeStyle = 'rgba(0,0,0,0.65)'", "ctx.strokeStyle = 'rgba(0,0,0,0.6)'"),
    ("ctx.lineWidth=3", "ctx.lineWidth=2.5"),
    ("ctx.lineWidth = 3", "ctx.lineWidth = 2.5"),
    # Title opacity
    ("'rgba(255,255,255,0.7)'", "'rgba(255,255,255,0.4)'"),
    # Star/Yellow adjustment - but #f0c040 was already replaced with #007AFF
    # We need to put back the star color: find drawLabel with ★ and use #FFD60A
    # Actually, the ★ line in the template uses 18px and comes right after capital/cap
    # Let me target it specifically
    # Box shadow removal
    (
        "border-radius: 12px; box-shadow: 0 0 40px rgba(0,0,0,0.5);",
        "border-radius: 16px;",
    ),
    # Panel size
    ("width: 360px", "width: 380px"),
    # Paragraph style
    ("gap: 14px", "gap: 16px"),
    ("padding: 20px", "padding: 24px"),
    # Hint strong
    ("color: '#f0c040'", "color: '#f5f5f7'"),
    # lineWidth adjustments
    ("ctx.lineWidth=lw||1;ctx.stroke();", "ctx.lineWidth=lw||0.8;ctx.stroke();"),
    (
        "ctx.lineWidth = lw || 1; ctx.stroke();",
        "ctx.lineWidth = lw || 0.8; ctx.stroke();",
    ),
    # Legend inline styles (HTML, not CSS)
    ('style="background:#1e3a5f;"', 'style="background:#1c1c24;"'),
    ('style="background:#27ae60;"', 'style="background:#30D158;"'),
    ('style="background:#c0392b;"', 'style="background:#FF453A;"'),
    # drawLabel default color
    ("color||'#eee'", "color||'#f5f5f7'"),
    ("color || '#eee'", "color || '#f5f5f7'"),
    # Canvas lineWidth rendering (1.2 -> 1, 1.4 -> 1.2)
    ("drawFeature(f,'#3a3a44',fc,1.2)", "drawFeature(f,'#3a3a44',fc,1)"),
    ("drawFeature(f,'#4a4a55',fc,1.4)", "drawFeature(f,'#4a4a55',fc,1.2)"),
    # drawTitle font size adjustment
    ("ctx.font='16px", "ctx.font='14px"),
    # Score span in old CSS that may survive. Fix any leftover
    ("color: '#f0c040'", "color: '#f5f5f7'"),
    # Emoji text replacements
    ("🏙 地级", "地级"),
    ("🏘 区/县", "区/县"),
    ("💡 操作提示", "操作提示"),
    ("✅ 答对了！", "回答正确"),
    ("❌ 答错了", "回答错误"),
    ("🎉 全部答完！", "全部答完！"),
    ("🔄 重新开始", "重新开始"),
    ("🔙 返回省级", "返回上级"),
    # Quiz question in hint text
    (
        "'<strong>地级模式</strong><br>先答地级名称，再进入区/县'",
        "'地级模式<br>先答地级名称，再进入区/县'",
    ),
    (
        "'<strong>区/县模式</strong><br>点击地级行政区直接进入县级'",
        "'区/县模式<br>点击地级行政区直接进入县级'",
    ),
    # Hint h2
    ("点击区域 → 选择题 → 认识", "点击区域 \u00b7 选择题 \u00b7 认识"),
    ("点击区域 \u2192 选择题 \u2192 认识", "点击区域 \u00b7 选择题 \u00b7 认识"),
    # Strong tags in hint text show
    ("'当前：<strong>'", "'当前：'"),
    ("'<br>共 '", "'<br>共 '"),
    # Too aggressive: Only replace strong in hint-t
]


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Replace CSS block
    content = STYLE_PATTERN.sub(NEW_CSS, content)

    # Apply JS replacements
    for old, new in JS_REPLACEMENTS:
        content = content.replace(old, new)

    # Special handling: star ★ should remain yellow, not blue
    # The star is drawn with a specific label. Find drawLabel with ★
    # In the template it's: drawLabel(cx,cy-14,'★','#f0c040',18);
    # But #f0c040 was already replaced with #007AFF above
    # So we need to fix this back
    content = re.sub(
        r"(drawLabel\(.*?,'★','|drawLabel\(.*?,'\u2605',')(#007AFF)'",
        r"\1#FFD60A'",
        content,
    )
    # Also fix the star size from 18 to 16
    content = re.sub(
        r"(drawLabel\(.*?,'★','|drawLabel\(.*?,'\u2605',')(#FFD60A)',(\d+)\)",
        r"\1\2,16)",
        content,
    )

    # Fix any leftover drawLabel calls that might have old star color near caps
    # This handles the '★' case where offset might vary (cx,cy-14 or cx,cy-13)

    # Fix the mode-btn onclick values that have emojis
    content = content.replace(
        "onclick=\"setMode('prefecture')\">地级",
        "onclick=\"setMode('prefecture')\">地级",
    )
    content = content.replace(
        "onclick=\"setMode('county')\">区/县", "onclick=\"setMode('county')\">区/县"
    )

    # Fix font: remove any leftover 'bold' in drawLabel font
    content = re.sub(r"ctx\.font\s*=\s*'bold\s+", "ctx.font='", content)

    # Fix score span color which was changed from #f0c040 to something
    # In CSS, score span should be #f5f5f7

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    updated = 0
    skipped = 0

    for entry in os.listdir(BASE):
        entry_path = os.path.join(BASE, entry)
        if not os.path.isdir(entry_path):
            continue
        if entry == "china" or entry == "__pycache__":
            continue

        map_path = os.path.join(entry_path, "map.html")
        if not os.path.exists(map_path):
            continue

        if process_file(map_path):
            updated += 1
            print(f"  Updated: {entry}/map.html")
        else:
            skipped += 1
            print(f"  Skipped (no changes): {entry}/map.html")

    print(f"\nDone: {updated} updated, {skipped} skipped")


if __name__ == "__main__":
    main()
