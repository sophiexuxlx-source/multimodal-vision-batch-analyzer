import os
from fpdf import FPDF

class PDFReportZH(FPDF):
    def header(self):
        self.set_font("SimHei", "B", 14)
        self.set_text_color(44, 62, 80)
        self.cell(0, 8, "北美野火棕碳烟羽 AI 分析报告 (中文版)", border=False, new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_draw_color(52, 152, 219)
        self.set_line_width(0.8)
        self.line(10, 16, 200, 16)
        self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_font("SimHei", "", 9)
        self.set_text_color(127, 140, 141)
        self.cell(0, 8, f"第 {self.page_no()} 页 / 共 {{nb}} 页", align="C")

def build_pdf(pdf_path="AI_ANALYSIS_REPORT_ZH.pdf"):
    pdf = PDFReportZH()
    pdf.alias_nb_pages()
    
    # Add Chinese SimHei Font
    font_path = "C:/Windows/Fonts/simhei.ttf"
    if os.path.exists(font_path):
        pdf.add_font("SimHei", "", font_path)
        pdf.add_font("SimHei", "B", font_path)
    else:
        # Fallback to SimSun
        pdf.add_font("SimHei", "", "C:/Windows/Fonts/simsun.ttc")
        pdf.add_font("SimHei", "B", "C:/Windows/Fonts/simsun.ttc")

    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    # Intro
    pdf.set_font("SimHei", "", 9.5)
    pdf.set_text_color(44, 62, 80)
    pdf.multi_cell(0, 4.8, "这四幅图像序列展示了 2026年7月 跨越北美大陆为期五天的 棕碳（mg/m^2） 浓度随时间变化的模拟演变过程。")
    pdf.ln(2)

    # 1. 地图布局与图例说明
    pdf.set_font("SimHei", "B", 11)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 6, "1. 地图布局与图例说明 (Map Layout & Visual Key)", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("SimHei", "", 9)
    pdf.set_text_color(44, 62, 80)
    pdf.multi_cell(0, 4.5, (
        "- 底图：北美洲（包含加拿大、美国及大西洋与太平洋部分海域）的灰度地形阴影图。州界、省界和国界线清晰可见。\n"
        "- 色标图例：位于每张图的底部正中央。\n"
        "  * 白色 / 浅蓝色：清洁空气或极低浓度（0 至 50 mg/m^2）。\n"
        "  * 蓝色 / 黄橙色：中等浓度（50 至 100 mg/m^2）。\n"
        "  * 红色 / 深棕色：高至极高浓度（>=150 mg/m^2）。\n"
        "- 科学意义：棕碳是野火烟雾的核心组成部分。该序列直观展现了大层风场输送下野火烟羽的移动路径、扩散范围及聚集强度。"
    ))
    pdf.ln(2)

    # 2. 时间线演变与动态路径
    pdf.set_font("SimHei", "B", 11)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 6, "2. 时间线演变与动态路径 (Chronological Progression)", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("SimHei", "B", 9.5)
    pdf.set_text_color(52, 73, 94)
    pdf.cell(0, 5, "[1] 图 1：2026年7月14日 01:30 UTC", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("SimHei", "", 9)
    pdf.set_text_color(44, 62, 80)
    pdf.multi_cell(0, 4.5, "  在加拿大西北部（阿拉斯加、育空地区、BC省及西北地区）集中出现大面积极高棕碳浓度区（>=150 mg/m^2，深棕色）。大陆其余大部相对晴朗。")
    pdf.ln(1)

    pdf.set_font("SimHei", "B", 9.5)
    pdf.set_text_color(52, 73, 94)
    pdf.cell(0, 5, "[2] 图 2：2026年7月15日 16:30 UTC（约 39 小时后）", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("SimHei", "", 9)
    pdf.set_text_color(44, 62, 80)
    pdf.multi_cell(0, 4.5, "  西北部烟羽呈对角线向东南拉长穿过艾伯塔与萨斯喀彻温省。五大湖及中西部地区爆发性形成高度浓缩的主烟羽并向纽约/宾州推进。美西俄勒冈-加州交界处演变为深棕色高危斑块。")
    pdf.ln(1)

    pdf.set_font("SimHei", "B", 9.5)
    pdf.set_text_color(52, 73, 94)
    pdf.cell(0, 5, "[3] 图 3：2026年7月17日 10:30 UTC（约 42 小时后）", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("SimHei", "", 9)
    pdf.set_text_color(44, 62, 80)
    pdf.multi_cell(0, 4.5, "  烟羽合并为蛇形绵延的超高密度连贯走廊（>=150 mg/m^2），从加拿大中部横跨五大湖区，横扫大西洋中岸各州（马里兰、弗吉尼亚、北卡）并倾泻入大西洋。展示了高空风场横跨数千英里的远距离传输。")
    pdf.ln(1)

    pdf.set_font("SimHei", "B", 9.5)
    pdf.set_text_color(52, 73, 94)
    pdf.cell(0, 5, "[4] 图 4：2026年7月19日 01:30 UTC（约 39 小时后）", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("SimHei", "", 9)
    pdf.set_text_color(44, 62, 80)
    pdf.multi_cell(0, 4.5, "  美东/中西部及魁北克上空主烟羽停滞拓宽，保持高浓度。太平洋西北区（俄勒冈、华盛顿、爱达荷及BC省）野火剧烈复苏，爆发大面积深棕色烟羽。")
    pdf.ln(2)

    # 3. 背景与总结
    pdf.set_font("SimHei", "B", 11)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 6, "3. 背景与总结 (Context & Summary)", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("SimHei", "", 9)
    pdf.set_text_color(44, 62, 80)
    pdf.multi_cell(0, 4.5, "该序列完整揭示了一次严重的野火烟雾跨区域输送过程。它突出了加拿大西部、西北部及太平洋西北地区的野火排放不仅局限于发源地本地；相反，高空强风将高危浓度的棕碳烟羽沿固定走廊推向整个北美大陆，严重破坏了美国中西部、大西洋中岸及加拿大东部各大人口密集区的空气质量。")

    pdf.output(pdf_path)
    print(f"Chinese PDF Report successfully generated: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    build_pdf()
