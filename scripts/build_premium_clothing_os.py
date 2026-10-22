import json
from pathlib import Path
import subprocess
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from product_qa.checks import check_product

TARGET_DIR = Path(r"C:\Users\YM\Desktop\PROJECT SERIUS\Digital Product Factory\products\kalkulator-hpp-clothing")
TARGET_DIR.mkdir(parents=True, exist_ok=True)

wb = openpyxl.Workbook()

# Typography & Colors
FONT_NAME = "Segoe UI"
COLOR_PRIMARY_DARK = "0F172A"   # Slate 900
COLOR_HEADER_BG = "1E293B"      # Slate 800
COLOR_SECTION_BG = "334155"     # Slate 700
COLOR_LIGHT_BG = "F8FAFC"       # Slate 50
COLOR_INPUT_BG = "FEF9C3"       # Amber/Yellow 100 (Soft Input)
COLOR_KPI_BG = "DCFCE7"         # Emerald 100 (Success/KPI)
COLOR_CARD_BG = "F1F5F9"        # Slate 100
COLOR_BORDER = "CBD5E1"         # Slate 300
COLOR_BORDER_DARK = "94A3B8"    # Slate 400

font_title = Font(name=FONT_NAME, size=14, bold=True, color="FFFFFF")
font_subtitle = Font(name=FONT_NAME, size=10, italic=True, color="E2E8F0")
font_sec_header = Font(name=FONT_NAME, size=11, bold=True, color="FFFFFF")
font_tbl_header = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
font_bold = Font(name=FONT_NAME, size=10, bold=True, color="0F172A")
font_normal = Font(name=FONT_NAME, size=10, color="334155")
font_small = Font(name=FONT_NAME, size=9, color="64748B")
font_kpi_value = Font(name=FONT_NAME, size=15, bold=True, color="047857")
font_kpi_label = Font(name=FONT_NAME, size=9, bold=True, color="475569")

fill_header = PatternFill(start_color=COLOR_HEADER_BG, end_color=COLOR_HEADER_BG, fill_type="solid")
fill_sec = PatternFill(start_color=COLOR_SECTION_BG, end_color=COLOR_SECTION_BG, fill_type="solid")
fill_input = PatternFill(start_color=COLOR_INPUT_BG, end_color=COLOR_INPUT_BG, fill_type="solid")
fill_kpi = PatternFill(start_color=COLOR_KPI_BG, end_color=COLOR_KPI_BG, fill_type="solid")
fill_card = PatternFill(start_color=COLOR_CARD_BG, end_color=COLOR_CARD_BG, fill_type="solid")
fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

thin_side = Side(border_style="thin", color=COLOR_BORDER)
dark_side = Side(border_style="thin", color=COLOR_BORDER_DARK)
double_bottom = Side(border_style="double", color=COLOR_PRIMARY_DARK)

box_border = Border(top=thin_side, left=thin_side, right=thin_side, bottom=thin_side)
total_border = Border(top=thin_side, left=thin_side, right=thin_side, bottom=double_bottom)
kpi_border = Border(top=dark_side, left=dark_side, right=dark_side, bottom=dark_side)

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")

# List of input cells to register in product.json
INPUT_CELLS = []


# ==========================================
# 1. SHEET: Instructions
# ==========================================
ws1 = wb.active
ws1.title = "Instructions"
ws1.views.sheetView[0].showGridLines = True

ws1.row_dimensions[2].height = 28
ws1.row_dimensions[3].height = 20
ws1.merge_cells("B2:G2")
ws1["B2"] = "CLOTHING BRAND FINANCIAL & PRODUCTION OPERATING SYSTEM"
ws1["B2"].font = font_title
ws1["B2"].fill = fill_header
ws1["B2"].alignment = align_left

ws1.merge_cells("B3:G3")
ws1["B3"] = "Panduan Operasional, Manajemen HPP, Struktur Pricing & Analisis Impas (BEP) Koleksi"
ws1["B3"].font = font_subtitle
ws1["B3"].fill = fill_header
ws1["B3"].alignment = align_left

# Color Legend Cards
legend_rows = [
    ("B5:C5", "KODE WARNA SEL", "D5:G5", "PANDUAN PENGISIAN & ATURAN PENGGUNAAN", True),
    ("B6", "Sel Berwarna Kuning", "D6:G6", "Sel Input Manual: Masukkan angka real biaya vendor, harga bahan, dan target margin Anda.", False, fill_input, font_bold),
    ("B7", "Sel Putih / Abu-abu", "D7:G7", "Sel Formula Otomatis: Dihitung langsung oleh spreadsheet. Jangan hapus atau ketik manual.", False, fill_zebra, font_bold),
    ("B8", "Sel Berwarna Hijau", "D8:G8", "Key Indicator / Output Kunci: Menampilkan rekomendasi harga, laba bersih, dan titik impas.", False, fill_kpi, font_bold),
]

for item in legend_rows:
    if len(item) == 5:
        c1, t1, c2, t2, is_head = item
        ws1.merge_cells(c1)
        ws1.merge_cells(c2)
        ws1[c1.split(":")[0]] = t1
        ws1[c2.split(":")[0]] = t2
        cell1 = ws1[c1.split(":")[0]]
        cell2 = ws1[c2.split(":")[0]]
        cell1.font = font_sec_header
        cell1.fill = fill_sec
        cell1.alignment = align_left
        cell2.font = font_sec_header
        cell2.fill = fill_sec
        cell2.alignment = align_left
    else:
        c1, t1, c2, t2, _, fill_c1, font_c1 = item
        ws1[c1] = t1
        ws1.merge_cells(c2)
        ws1[c2.split(":")[0]] = t2
        ws1[c1].font = font_c1
        ws1[c1].fill = fill_c1
        ws1[c1].border = box_border
        ws1[c1].alignment = align_center
        cell2 = ws1[c2.split(":")[0]]
        cell2.font = font_normal
        cell2.border = box_border
        cell2.alignment = align_left

# SOP Steps
ws1.merge_cells("B10:G10")
ws1["B10"] = "ALUR KERJA PENGGUNAAN SPREADSHEET (SOP 5 LANGKAH)"
ws1["B10"].font = font_sec_header
ws1["B10"].fill = fill_sec
ws1["B10"].alignment = align_left

sop_steps = [
    ("Langkah 1: Riset Vendor", "Buka sheet 'Vendor_Database'. Catat nama vendor bahan, konveksi jahit, sablon, aksesoris, dan kontak WA."),
    ("Langkah 2: Hitung HPP Pokok", "Buka sheet 'HPP_Calculator'. Isi rincian kain, ongkos jahit, sablon, label, dan packaging per helai."),
    ("Langkah 3: Atur Target Margin", "Tentukan target margin kotor (rekomendasi retail 60%-70% untuk D2C, dan 30%-40% untuk reseller)."),
    ("Langkah 4: Rancang Batch Rilis", "Buka sheet 'Batch_Planner'. Tentukan kuantiti rilis dan masukkan biaya tetap peluncuran (sample, foto, ads)."),
    ("Langkah 5: Pantau KPI Dashboard", "Buka sheet 'Dashboard' untuk memantau performa portofolio produk, total investasi, dan target titik impas."),
]

for idx, (step_t, step_d) in enumerate(sop_steps, start=11):
    ws1[f"B{idx}"] = step_t
    ws1[f"B{idx}"].font = font_bold
    ws1[f"B{idx}"].border = box_border
    ws1[f"B{idx}"].alignment = align_left
    ws1.merge_cells(f"C{idx}:G{idx}")
    ws1[f"C{idx}"] = step_d
    ws1[f"C{idx}"].font = font_normal
    ws1[f"C{idx}"].border = box_border
    ws1[f"C{idx}"].alignment = align_left

# Definitions Table
ws1.merge_cells("B17:G17")
ws1["B17"] = "GLOSARIUM & DEFINISI METRIK FINANSIAL"
ws1["B17"].font = font_sec_header
ws1["B17"].fill = fill_sec
ws1["B17"].alignment = align_left

glossary = [
    ("HPP (Cost of Goods Sold)", "Total biaya modal langsung yang melekat pada 1 helai baju (Kain + Jahit + Sablon + Aksesoris + Kemasan)."),
    ("Margin Kotor (Gross Margin %)", "Persentase keuntungan sebelum dipotong operasional tetap: (Harga Jual - HPP) / Harga Jual."),
    ("Titik Impas (BEP Unit)", "Jumlah minimal helai pakaian yang wajib terjual habis agar modal awal batch kembali 100% tanpa rugi."),
    ("Titik Impas (BEP Rupiah)", "Jumlah omzet minimal yang harus masuk ke rekening sebelum bisnis menghasilkan laba bersih."),
    ("ROI (Return on Investment %)", "Tingkat pengembalian modal investasi peluncuran: (Proyeksi Laba Bersih / Total Investasi) x 100%."),
]

for idx, (term, desc) in enumerate(glossary, start=18):
    ws1[f"B{idx}"] = term
    ws1[f"B{idx}"].font = font_bold
    ws1[f"B{idx}"].border = box_border
    ws1[f"B{idx}"].alignment = align_left
    ws1.merge_cells(f"C{idx}:G{idx}")
    ws1[f"C{idx}"] = desc
    ws1[f"C{idx}"].font = font_normal
    ws1[f"C{idx}"].border = box_border
    ws1[f"C{idx}"].alignment = align_left

ws1.column_dimensions["A"].width = 4
ws1.column_dimensions["B"].width = 28
ws1.column_dimensions["C"].width = 24
ws1.column_dimensions["D"].width = 20
ws1.column_dimensions["E"].width = 20
ws1.column_dimensions["F"].width = 20
ws1.column_dimensions["G"].width = 24


# ==========================================
# 2. SHEET: Dashboard
# ==========================================
ws2 = wb.create_sheet(title="Dashboard")
ws2.views.sheetView[0].showGridLines = True

ws2.row_dimensions[2].height = 28
ws2.row_dimensions[3].height = 18
ws2.merge_cells("B2:G2")
ws2["B2"] = "EXECUTIVE BRAND FINANCIAL DASHBOARD"
ws2["B2"].font = font_title
ws2["B2"].fill = fill_header
ws2["B2"].alignment = align_left

ws2.merge_cells("B3:G3")
ws2["B3"] = "Ringkasan Eksekutif Kinerja Portofolio Produk & Proyeksi Batch Produksi"
ws2["B3"].font = font_subtitle
ws2["B3"].fill = fill_header
ws2["B3"].alignment = align_left

# 6 KPI Summary Cards (B5 to G6)
kpi_cards = [
    ("B5", "B6", "SKU AKTIF", "=COUNTA(HPP_Calculator!C6:C10)", "0 \"SKU\""),
    ("C5", "C6", "RATA-RATA HPP", "=AVERAGE(HPP_Calculator!N6:N10)", "\"IDR \"#,##0"),
    ("D5", "D6", "AVG MARGIN RETAIL", "=AVERAGE(HPP_Calculator!R6:R10)", "0.0%"),
    ("E5", "E6", "MODAL INVESTASI BATCH", "=Batch_Planner!E18", "\"IDR \"#,##0"),
    ("F5", "F6", "PROYEKSI OMZET (SOLD OUT)", "=Batch_Planner!E23", "\"IDR \"#,##0"),
    ("G5", "G6", "PROYEKSI LABA BERSIH", "=Batch_Planner!E24", "\"IDR \"#,##0"),
]

ws2.row_dimensions[5].height = 18
ws2.row_dimensions[6].height = 28

for c_lbl, c_val, label, formula, num_fmt in kpi_cards:
    ws2[c_lbl] = label
    ws2[c_lbl].font = font_kpi_label
    ws2[c_lbl].fill = fill_card
    ws2[c_lbl].alignment = align_center
    ws2[c_lbl].border = Border(top=dark_side, left=dark_side, right=dark_side)

    ws2[c_val] = formula
    ws2[c_val].font = font_kpi_value
    ws2[c_val].fill = fill_card
    ws2[c_val].alignment = align_center
    ws2[c_val].number_format = num_fmt
    ws2[c_val].border = Border(bottom=dark_side, left=dark_side, right=dark_side)

# Table 1: Portofolio Comparison
ws2.merge_cells("B8:G8")
ws2["B8"] = "RINGKASAN HARGA & PROFITABILITAS PER PRODUK"
ws2["B8"].font = font_sec_header
ws2["B8"].fill = fill_sec
ws2["B8"].alignment = align_left

port_headers = [
    ("B9", "Nama Produk"),
    ("C9", "Kategori"),
    ("D9", "HPP Satuan"),
    ("E9", "Harga Retail"),
    ("F9", "Laba Kotor (Retail)"),
    ("G9", "Margin Retail Real"),
]

ws2.row_dimensions[9].height = 24
for c_pos, h_text in port_headers:
    ws2[c_pos] = h_text
    ws2[c_pos].font = font_tbl_header
    ws2[c_pos].fill = fill_sec
    ws2[c_pos].alignment = align_center
    ws2[c_pos].border = box_border

for idx in range(1, 6):
    r_dash = 9 + idx
    r_calc = 5 + idx
    ws2.row_dimensions[r_dash].height = 20

    ws2[f"B{r_dash}"] = f"=HPP_Calculator!C{r_calc}"
    ws2[f"B{r_dash}"].font = font_bold
    ws2[f"B{r_dash}"].border = box_border
    ws2[f"B{r_dash}"].alignment = align_left

    ws2[f"C{r_dash}"] = f"=HPP_Calculator!D{r_calc}"
    ws2[f"C{r_dash}"].font = font_normal
    ws2[f"C{r_dash}"].border = box_border
    ws2[f"C{r_dash}"].alignment = align_left

    ws2[f"D{r_dash}"] = f"=HPP_Calculator!N{r_calc}"
    ws2[f"D{r_dash}"].font = font_normal
    ws2[f"D{r_dash}"].border = box_border
    ws2[f"D{r_dash}"].alignment = align_right
    ws2[f"D{r_dash}"].number_format = "\"IDR \"#,##0"

    ws2[f"E{r_dash}"] = f"=HPP_Calculator!P{r_calc}"
    ws2[f"E{r_dash}"].font = font_bold
    ws2[f"E{r_dash}"].border = box_border
    ws2[f"E{r_dash}"].alignment = align_right
    ws2[f"E{r_dash}"].number_format = "\"IDR \"#,##0"

    ws2[f"F{r_dash}"] = f"=HPP_Calculator!Q{r_calc}"
    ws2[f"F{r_dash}"].font = font_bold
    ws2[f"F{r_dash}"].fill = fill_kpi
    ws2[f"F{r_dash}"].border = box_border
    ws2[f"F{r_dash}"].alignment = align_right
    ws2[f"F{r_dash}"].number_format = "\"IDR \"#,##0"

    ws2[f"G{r_dash}"] = f"=HPP_Calculator!R{r_calc}"
    ws2[f"G{r_dash}"].font = font_bold
    ws2[f"G{r_dash}"].fill = fill_kpi
    ws2[f"G{r_dash}"].border = box_border
    ws2[f"G{r_dash}"].alignment = align_right
    ws2[f"G{r_dash}"].number_format = "0.0%"

# Table 2: Scenario Analysis
ws2.merge_cells("B16:G16")
ws2["B16"] = "ANALISIS SKENARIO PENJUALAN BATCH (STRESS TEST)"
ws2["B16"].font = font_sec_header
ws2["B16"].fill = fill_sec
ws2["B16"].alignment = align_left

scen_headers = [
    ("B17", "Skenario Penjualan"),
    ("C17", "Tingkat Keterjualan"),
    ("D17", "Total Helai Terjual"),
    ("E17", "Total Omzet Masuk"),
    ("F17", "Laba / Rugi Bersih"),
    ("G17", "ROI Batch"),
]

ws2.row_dimensions[17].height = 24
for c_pos, h_text in scen_headers:
    ws2[c_pos] = h_text
    ws2[c_pos].font = font_tbl_header
    ws2[c_pos].fill = fill_sec
    ws2[c_pos].alignment = align_center
    ws2[c_pos].border = box_border

scenarios = [
    ("Skenario 1: Sold Out Penuh (Optimis)", 1.0, 18),
    ("Skenario 2: Terjual 75% (Moderat)", 0.75, 19),
    ("Skenario 3: Terjual 50% (Konservatif / Titik Impas)", 0.50, 20),
    ("Skenario 4: Terjual 30% (Skenario Buruk)", 0.30, 21),
]

for name, pct, r_scen in scenarios:
    ws2.row_dimensions[r_scen].height = 20
    ws2[f"B{r_scen}"] = name
    ws2[f"B{r_scen}"].font = font_bold
    ws2[f"B{r_scen}"].border = box_border
    ws2[f"B{r_scen}"].alignment = align_left

    ws2[f"C{r_scen}"] = pct
    ws2[f"C{r_scen}"].font = font_normal
    ws2[f"C{r_scen}"].border = box_border
    ws2[f"C{r_scen}"].alignment = align_center
    ws2[f"C{r_scen}"].number_format = "0%"

    ws2[f"D{r_scen}"] = f"=ROUND(Batch_Planner!E10*{pct}, 0)"
    ws2[f"D{r_scen}"].font = font_normal
    ws2[f"D{r_scen}"].border = box_border
    ws2[f"D{r_scen}"].alignment = align_center
    ws2[f"D{r_scen}"].number_format = "#,##0 \"pcs\""

    ws2[f"E{r_scen}"] = f"=ROUND(Batch_Planner!E23*{pct}, -2)"
    ws2[f"E{r_scen}"].font = font_bold
    ws2[f"E{r_scen}"].border = box_border
    ws2[f"E{r_scen}"].alignment = align_right
    ws2[f"E{r_scen}"].number_format = "\"IDR \"#,##0"

    ws2[f"F{r_scen}"] = f"=E{r_scen}-Batch_Planner!E18"
    ws2[f"F{r_scen}"].font = font_bold
    ws2[f"F{r_scen}"].border = box_border
    ws2[f"F{r_scen}"].alignment = align_right
    ws2[f"F{r_scen}"].number_format = "\"IDR \"#,##0"
    if pct >= 0.5:
        ws2[f"F{r_scen}"].fill = fill_kpi

    ws2[f"G{r_scen}"] = f"=ROUND((F{r_scen}/Batch_Planner!E18)*100, 1)"
    ws2[f"G{r_scen}"].font = font_bold
    ws2[f"G{r_scen}"].border = box_border
    ws2[f"G{r_scen}"].alignment = align_right
    ws2[f"G{r_scen}"].number_format = "0.0\"%\""

ws2.column_dimensions["A"].width = 4
ws2.column_dimensions["B"].width = 34
ws2.column_dimensions["C"].width = 24
ws2.column_dimensions["D"].width = 24
ws2.column_dimensions["E"].width = 26
ws2.column_dimensions["F"].width = 26
ws2.column_dimensions["G"].width = 24


# ==========================================
# 3. SHEET: HPP_Calculator
# ==========================================
ws3 = wb.create_sheet(title="HPP_Calculator")
ws3.views.sheetView[0].showGridLines = True

ws3.row_dimensions[2].height = 28
ws3.row_dimensions[3].height = 18
ws3.merge_cells("B2:T2")
ws3["B2"] = "KALKULATOR HPP & PENETAPAN HARGA MULTI-PRODUK (COST OF GOODS SOLD)"
ws3["B2"].font = font_title
ws3["B2"].fill = fill_header
ws3["B2"].alignment = align_left

ws3.merge_cells("B3:T3")
ws3["B3"] = "Rincian Biaya Pokok Kain, Jahit, Sablon, Aksesoris, Kemasan & Struktur Pricing Retail/Reseller"
ws3["B3"].font = font_subtitle
ws3["B3"].fill = fill_header
ws3["B3"].alignment = align_left

hpp_headers = [
    ("B4:B5", "No", align_center),
    ("C4:C5", "Nama Produk", align_left),
    ("D4:D5", "Kategori", align_left),
    ("E4:E5", "Material Kain", align_left),
    ("F4:G4", "Biaya Bahan Kain", align_center),
    ("H4:H5", "Ongkos Jahit", align_right),
    ("I4:I5", "Sablon / Bordir", align_right),
    ("J4:J5", "Label & Hangtag", align_right),
    ("K4:K5", "Plastik Ziplock", align_right),
    ("L4:L5", "Polymailer Kurir", align_right),
    ("M4:M5", "QC & Finishing", align_right),
    ("N4:N5", "Total HPP Satuan", align_right),
    ("O4:O5", "Target Margin (%)", align_center),
    ("P4:P5", "Harga Retail", align_right),
    ("Q4:Q5", "Laba Kotor Retail", align_right),
    ("R4:R5", "Margin Retail Real", align_center),
    ("S4:S5", "Harga Reseller", align_right),
    ("T4:T5", "Margin Reseller", align_center),
]

ws3.row_dimensions[4].height = 20
ws3.row_dimensions[5].height = 20

for item in hpp_headers:
    cell_range, text, algn = item
    if ":" in cell_range:
        ws3.merge_cells(cell_range)
    top_cell = ws3[cell_range.split(":")[0]]
    top_cell.value = text
    top_cell.font = font_tbl_header
    top_cell.fill = fill_header
    top_cell.alignment = algn

# Sub-headers for F and G
ws3["F5"] = "Harga/Kg/Yd"
ws3["F5"].font = font_tbl_header
ws3["F5"].fill = fill_header
ws3["F5"].alignment = align_right

ws3["G5"] = "Konsumsi"
ws3["G5"].font = font_tbl_header
ws3["G5"].fill = fill_header
ws3["G5"].alignment = align_center

products_data = [
    ("Boxy Heavy T-Shirt", "Kaos", "Combed 16s (240 gsm)", 58000, 0.38, 16000, 13000, 2200, 2500, 800, 1500, 0.65),
    ("Classic Regular T-Shirt", "Kaos", "Combed 24s (180 gsm)", 48000, 0.33, 14000, 11000, 2200, 2500, 800, 1200, 0.60),
    ("Pullover Heavy Hoodie", "Outerwear", "Cotton Fleece 330 gsm", 85000, 0.85, 32000, 18000, 3000, 3500, 1200, 2500, 0.65),
    ("Worker Utility Overshirt", "Kemeja", "Baby Canvas Twill", 42000, 1.40, 35000, 12000, 3000, 3000, 1000, 2500, 0.60),
    ("Tactical Cargo Pants", "Celana", "Cotton Ripstop", 40000, 1.60, 42000, 8000, 3500, 3000, 1000, 3000, 0.60),
]

for idx, p in enumerate(products_data, start=1):
    r = 5 + idx
    name, cat, mat, p_fab, c_fab, c_sew, c_prt, c_lbl, c_zip, c_pol, c_qc, m_target = p
    ws3.row_dimensions[r].height = 22

    ws3[f"B{r}"] = idx
    ws3[f"B{r}"].alignment = align_center

    ws3[f"C{r}"] = name
    ws3[f"C{r}"].alignment = align_left

    ws3[f"D{r}"] = cat
    ws3[f"D{r}"].alignment = align_left

    ws3[f"E{r}"] = mat
    ws3[f"E{r}"].alignment = align_left

    # Input Cells
    ws3[f"F{r}"] = p_fab
    ws3[f"F{r}"].number_format = "#,##0"
    ws3[f"F{r}"].fill = fill_input
    ws3[f"F{r}"].alignment = align_right
    INPUT_CELLS.append(f"HPP_Calculator!F{r}")

    ws3[f"G{r}"] = c_fab
    ws3[f"G{r}"].number_format = "0.00"
    ws3[f"G{r}"].fill = fill_input
    ws3[f"G{r}"].alignment = align_center
    INPUT_CELLS.append(f"HPP_Calculator!G{r}")

    ws3[f"H{r}"] = c_sew
    ws3[f"H{r}"].number_format = "#,##0"
    ws3[f"H{r}"].fill = fill_input
    ws3[f"H{r}"].alignment = align_right
    INPUT_CELLS.append(f"HPP_Calculator!H{r}")

    ws3[f"I{r}"] = c_prt
    ws3[f"I{r}"].number_format = "#,##0"
    ws3[f"I{r}"].fill = fill_input
    ws3[f"I{r}"].alignment = align_right
    INPUT_CELLS.append(f"HPP_Calculator!I{r}")

    ws3[f"J{r}"] = c_lbl
    ws3[f"J{r}"].number_format = "#,##0"
    ws3[f"J{r}"].fill = fill_input
    ws3[f"J{r}"].alignment = align_right
    INPUT_CELLS.append(f"HPP_Calculator!J{r}")

    ws3[f"K{r}"] = c_zip
    ws3[f"K{r}"].number_format = "#,##0"
    ws3[f"K{r}"].fill = fill_input
    ws3[f"K{r}"].alignment = align_right
    INPUT_CELLS.append(f"HPP_Calculator!K{r}")

    ws3[f"L{r}"] = c_pol
    ws3[f"L{r}"].number_format = "#,##0"
    ws3[f"L{r}"].fill = fill_input
    ws3[f"L{r}"].alignment = align_right
    INPUT_CELLS.append(f"HPP_Calculator!L{r}")

    ws3[f"M{r}"] = c_qc
    ws3[f"M{r}"].number_format = "#,##0"
    ws3[f"M{r}"].fill = fill_input
    ws3[f"M{r}"].alignment = align_right
    INPUT_CELLS.append(f"HPP_Calculator!M{r}")

    # Calculations
    ws3[f"N{r}"] = f"=ROUND((F{r}*G{r})+SUM(H{r}:M{r}), 0)"
    ws3[f"N{r}"].number_format = "\"IDR \"#,##0"
    ws3[f"N{r}"].fill = fill_card
    ws3[f"N{r}"].font = font_bold
    ws3[f"N{r}"].alignment = align_right

    ws3[f"O{r}"] = m_target
    ws3[f"O{r}"].number_format = "0.0%"
    ws3[f"O{r}"].fill = fill_input
    ws3[f"O{r}"].alignment = align_center
    INPUT_CELLS.append(f"HPP_Calculator!O{r}")

    ws3[f"P{r}"] = f"=ROUND(N{r}/(1-O{r}), -2)"
    ws3[f"P{r}"].number_format = "\"IDR \"#,##0"
    ws3[f"P{r}"].fill = fill_card
    ws3[f"P{r}"].font = font_bold
    ws3[f"P{r}"].alignment = align_right

    ws3[f"Q{r}"] = f"=P{r}-N{r}"
    ws3[f"Q{r}"].number_format = "\"IDR \"#,##0"
    ws3[f"Q{r}"].fill = fill_kpi
    ws3[f"Q{r}"].font = font_bold
    ws3[f"Q{r}"].alignment = align_right

    ws3[f"R{r}"] = f"=Q{r}/P{r}"
    ws3[f"R{r}"].number_format = "0.0%"
    ws3[f"R{r}"].fill = fill_kpi
    ws3[f"R{r}"].font = font_bold
    ws3[f"R{r}"].alignment = align_center

    ws3[f"S{r}"] = f"=ROUND(N{r}*1.35, -2)"
    ws3[f"S{r}"].number_format = "\"IDR \"#,##0"
    ws3[f"S{r}"].alignment = align_right

    ws3[f"T{r}"] = f"=(S{r}-N{r})/S{r}"
    ws3[f"T{r}"].number_format = "0.0%"
    ws3[f"T{r}"].alignment = align_center

    for col_letter in [get_column_letter(c) for c in range(2, 21)]:
        cell = ws3[f"{col_letter}{r}"]
        cell.border = box_border
        if cell.font == font_normal and cell.fill != fill_input:
            cell.font = font_normal

ws3.column_dimensions["A"].width = 3
ws3.column_dimensions["B"].width = 5
ws3.column_dimensions["C"].width = 25
ws3.column_dimensions["D"].width = 12
ws3.column_dimensions["E"].width = 22
ws3.column_dimensions["F"].width = 14
ws3.column_dimensions["G"].width = 11
ws3.column_dimensions["H"].width = 14
ws3.column_dimensions["I"].width = 15
ws3.column_dimensions["J"].width = 15
ws3.column_dimensions["K"].width = 15
ws3.column_dimensions["L"].width = 15
ws3.column_dimensions["M"].width = 15
ws3.column_dimensions["N"].width = 18
ws3.column_dimensions["O"].width = 16
ws3.column_dimensions["P"].width = 17
ws3.column_dimensions["Q"].width = 18
ws3.column_dimensions["R"].width = 18
ws3.column_dimensions["S"].width = 17
ws3.column_dimensions["T"].width = 16


# ==========================================
# 4. SHEET: Batch_Planner
# ==========================================
ws4 = wb.create_sheet(title="Batch_Planner")
ws4.views.sheetView[0].showGridLines = True

ws4.row_dimensions[2].height = 28
ws4.row_dimensions[3].height = 18
ws4.merge_cells("B2:G2")
ws4["B2"] = "PERENCANAAN BATCH PRODUKSI & TITIK IMPAS (BEP)"
ws4["B2"].font = font_title
ws4["B2"].fill = fill_header
ws4["B2"].alignment = align_left

ws4.merge_cells("B3:G3")
ws4["B3"] = "Alokasi Volume Batch, Rincian Biaya Tetap Peluncuran & Analisis Titik Impas (BEP)"
ws4["B3"].font = font_subtitle
ws4["B3"].fill = fill_header
ws4["B3"].alignment = align_left

# Section 1: Allocation
ws4.merge_cells("B4:G4")
ws4["B4"] = "BAGIAN 1: ALOKASI RENCANA KUANTITI PRODUKSI SATU BATCH (DROP)"
ws4["B4"].font = font_sec_header
ws4["B4"].fill = fill_sec
ws4["B4"].alignment = align_left

sec1_headers = [
    ("B5", "No"),
    ("C5", "Nama Produk"),
    ("D5", "Target Qty (Pcs)"),
    ("E5", "HPP per Helai"),
    ("F5", "Total Modal Fisik"),
    ("G5", "Porsi Volume (%)"),
]

ws4.row_dimensions[5].height = 22
for c_pos, h_text in sec1_headers:
    ws4[c_pos] = h_text
    ws4[c_pos].font = font_tbl_header
    ws4[c_pos].fill = fill_sec
    ws4[c_pos].alignment = align_center
    ws4[c_pos].border = box_border

qtys = [100, 100, 50, 40, 40]
for idx, qty in enumerate(qtys, start=1):
    r_batch = 5 + idx
    r_calc = 5 + idx
    ws4.row_dimensions[r_batch].height = 20

    ws4[f"B{r_batch}"] = idx
    ws4[f"B{r_batch}"].alignment = align_center
    ws4[f"B{r_batch}"].border = box_border

    ws4[f"C{r_batch}"] = f"=HPP_Calculator!C{r_calc}"
    ws4[f"C{r_batch}"].font = font_bold
    ws4[f"C{r_batch}"].alignment = align_left
    ws4[f"C{r_batch}"].border = box_border

    ws4[f"D{r_batch}"] = qty
    ws4[f"D{r_batch}"].font = font_bold
    ws4[f"D{r_batch}"].fill = fill_input
    ws4[f"D{r_batch}"].alignment = align_center
    ws4[f"D{r_batch}"].number_format = "#,##0"
    ws4[f"D{r_batch}"].border = box_border
    INPUT_CELLS.append(f"Batch_Planner!D{r_batch}")

    ws4[f"E{r_batch}"] = f"=HPP_Calculator!N{r_calc}"
    ws4[f"E{r_batch}"].font = font_normal
    ws4[f"E{r_batch}"].alignment = align_right
    ws4[f"E{r_batch}"].number_format = "\"IDR \"#,##0"
    ws4[f"E{r_batch}"].border = box_border

    ws4[f"F{r_batch}"] = f"=D{r_batch}*E{r_batch}"
    ws4[f"F{r_batch}"].font = font_bold
    ws4[f"F{r_batch}"].fill = fill_card
    ws4[f"F{r_batch}"].alignment = align_right
    ws4[f"F{r_batch}"].number_format = "\"IDR \"#,##0"
    ws4[f"F{r_batch}"].border = box_border

    ws4[f"G{r_batch}"] = f"=D{r_batch}/$D$11"
    ws4[f"G{r_batch}"].font = font_normal
    ws4[f"G{r_batch}"].alignment = align_center
    ws4[f"G{r_batch}"].number_format = "0.0%"
    ws4[f"G{r_batch}"].border = box_border

# Total Row Section 1
ws4.row_dimensions[11].height = 22
ws4.merge_cells("B11:C11")
ws4["B11"] = "TOTAL MODAL FISIK BATCH"
ws4["B11"].font = font_bold
ws4["B11"].alignment = align_left
ws4["B11"].border = total_border
ws4["C11"].border = total_border

ws4["D11"] = "=SUM(D6:D10)"
ws4["D11"].font = font_bold
ws4["D11"].alignment = align_center
ws4["D11"].number_format = "#,##0 \"pcs\""
ws4["D11"].border = total_border

ws4["E11"] = ""
ws4["E11"].border = total_border

ws4["F11"] = "=SUM(F6:F10)"
ws4["F11"].font = font_bold
ws4["F11"].fill = fill_card
ws4["F11"].alignment = align_right
ws4["F11"].number_format = "\"IDR \"#,##0"
ws4["F11"].border = total_border

ws4["G11"] = "=SUM(G6:G10)"
ws4["G11"].font = font_bold
ws4["G11"].alignment = align_center
ws4["G11"].number_format = "0.0%"
ws4["G11"].border = total_border

# Section 2: Fixed Costs
ws4.merge_cells("B13:G13")
ws4["B13"] = "BAGIAN 2: BIAYA TETAP PELUNCURAN KOLEKSI (FIXED COSTS)"
ws4["B13"].font = font_sec_header
ws4["B13"].fill = fill_sec
ws4["B13"].alignment = align_left

fixed_costs = [
    ("Pembuatan Pola Mentah & Prototyping Sample", "Biaya jasa tukang pola & sample awal 5 produk", 750000),
    ("Sewa Studio & Model Foto Lookbook", "Sewa 1 shift studio foto & model katalog komersial", 1800000),
    ("Anggaran Iklan Digital (Meta/TikTok Ads)", "Anggaran ads berbayar untuk periode rilis 14 hari", 1500000),
    ("Seeding Influencer & Creator Gifting", "Biaya logistik & gift box khusus 10 kreator fesyen", 600000),
    ("Buffer Operasional & Lakban/Dus Cadangan", "Dana darurat operasional packing dan retur awal", 350000),
]

for idx, (fc_name, fc_desc, fc_val) in enumerate(fixed_costs, start=14):
    ws4.row_dimensions[idx].height = 20
    ws4.merge_cells(f"B{idx}:C{idx}")
    ws4[f"B{idx}"] = fc_name
    ws4[f"B{idx}"].font = font_bold
    ws4[f"B{idx}"].border = box_border
    ws4[f"B{idx}"].alignment = align_left
    ws4[f"C{idx}"].border = box_border

    ws4.merge_cells(f"D{idx}:E{idx}")
    ws4[f"D{idx}"] = fc_desc
    ws4[f"D{idx}"].font = font_normal
    ws4[f"D{idx}"].border = box_border
    ws4[f"D{idx}"].alignment = align_left
    ws4[f"E{idx}"].border = box_border

    ws4.merge_cells(f"F{idx}:G{idx}")
    ws4[f"F{idx}"] = fc_val
    ws4[f"F{idx}"].font = font_bold
    ws4[f"F{idx}"].fill = fill_input
    ws4[f"F{idx}"].border = box_border
    ws4[f"F{idx}"].alignment = align_right
    ws4[f"F{idx}"].number_format = "\"IDR \"#,##0"
    ws4[f"G{idx}"].border = box_border
    INPUT_CELLS.append(f"Batch_Planner!F{idx}")

# Total Fixed Cost Row
ws4.row_dimensions[19].height = 22
ws4.merge_cells("B19:E19")
ws4["B19"] = "TOTAL BIAYA TETAP PELUNCURAN"
ws4["B19"].font = font_bold
ws4["B19"].border = total_border
ws4["B19"].alignment = align_left
for c_extra in ["C19", "D19", "E19"]:
    ws4[c_extra].border = total_border

ws4.merge_cells("F19:G19")
ws4["F19"] = "=SUM(F14:F18)"
ws4["F19"].font = font_bold
ws4["F19"].fill = fill_card
ws4["F19"].border = total_border
ws4["F19"].alignment = align_right
ws4["F19"].number_format = "\"IDR \"#,##0"
ws4["G19"].border = total_border

# Section 3: BEP & Investment Summary Table
ws4.merge_cells("B21:G21")
ws4["B21"] = "BAGIAN 3: ANALISIS TITIK IMPAS (BEP) & PROYEKSI LABA BATCH"
ws4["B21"].font = font_sec_header
ws4["B21"].fill = fill_sec
ws4["B21"].alignment = align_left

fin_metrics = [
    ("TOTAL MODAL INVESTASI BATCH (FISIK + BIAYA TETAP)", "=F11+F19", "\"IDR \"#,##0", fill_card, font_bold),
    ("Rata-Rata Margin Kotor Retail per Helai", "=AVERAGE(HPP_Calculator!Q6:Q10)", "\"IDR \"#,##0", fill_card, font_bold),
    ("Rata-Rata Harga Jual Retail Koleksi", "=AVERAGE(HPP_Calculator!P6:P10)", "\"IDR \"#,##0", fill_card, font_bold),
    ("TITIK IMPAS (BEP) DALAM UNIT HELAI", "=ROUNDUP(F19/F23, 0)", "0 \"pcs\"", fill_kpi, font_kpi_value),
    ("TITIK IMPAS (BEP) DALAM OMZET PENJUALAN", "=F25*F24", "\"IDR \"#,##0", fill_kpi, font_bold),
    ("POTENSI OMZET MAKSIMAL (100% SOLD OUT)", "=SUMPRODUCT(D6:D10, HPP_Calculator!P6:P10)", "\"IDR \"#,##0", fill_card, font_bold),
    ("PROYEKSI LABA BERSIH BATCH (NET PROFIT)", "=F27-F22", "\"IDR \"#,##0", fill_kpi, font_kpi_value),
    ("ESTIMASI ROI INVESTASI BATCH (%)", "=ROUND((F28/F22)*100, 1)", "0.0\"%\"", fill_kpi, font_bold),
]

for idx, (m_label, m_formula, m_fmt, m_fill, m_fnt) in enumerate(fin_metrics, start=22):
    ws4.row_dimensions[idx].height = 24
    ws4.merge_cells(f"B{idx}:E{idx}")
    ws4[f"B{idx}"] = m_label
    ws4[f"B{idx}"].font = font_bold
    ws4[f"B{idx}"].border = box_border
    ws4[f"B{idx}"].alignment = align_left
    for col_e in [f"C{idx}", f"D{idx}", f"E{idx}"]:
        ws4[col_e].border = box_border

    ws4.merge_cells(f"F{idx}:G{idx}")
    ws4[f"F{idx}"] = m_formula
    ws4[f"F{idx}"].font = m_fnt
    ws4[f"F{idx}"].fill = m_fill
    ws4[f"F{idx}"].border = box_border
    ws4[f"F{idx}"].alignment = align_right
    ws4[f"F{idx}"].number_format = m_fmt
    ws4[f"G{idx}"].border = box_border

# Update Dashboard KPI references to match the exact cells in Batch_Planner!
ws2["E6"] = "=Batch_Planner!F22"
ws2["F6"] = "=Batch_Planner!F27"
ws2["G6"] = "=Batch_Planner!F28"

for r_scen, pct in [(18, 1.0), (19, 0.75), (20, 0.50), (21, 0.30)]:
    ws2[f"D{r_scen}"] = f"=ROUND(Batch_Planner!D11*{pct}, 0)"
    ws2[f"E{r_scen}"] = f"=ROUND(Batch_Planner!F27*{pct}, -2)"
    ws2[f"F{r_scen}"] = f"=E{r_scen}-Batch_Planner!F22"
    ws2[f"G{r_scen}"] = f"=ROUND((F{r_scen}/Batch_Planner!F22)*100, 1)"

ws4.column_dimensions["A"].width = 4
ws4.column_dimensions["B"].width = 8
ws4.column_dimensions["C"].width = 30
ws4.column_dimensions["D"].width = 22
ws4.column_dimensions["E"].width = 22
ws4.column_dimensions["F"].width = 24
ws4.column_dimensions["G"].width = 20


# ==========================================
# 5. SHEET: Vendor_Database
# ==========================================
ws5 = wb.create_sheet(title="Vendor_Database")
ws5.views.sheetView[0].showGridLines = True

ws5.row_dimensions[2].height = 28
ws5.row_dimensions[3].height = 18
ws5.merge_cells("B2:I2")
ws5["B2"] = "DATABASE VENDOR & REKANAN PRODUKSI CLOTHING"
ws5["B2"].font = font_title
ws5["B2"].fill = fill_header
ws5["B2"].alignment = align_left

ws5.merge_cells("B3:I3")
ws5["B3"] = "Katalog Mitra Kain, Konveksi Jahit, Sablon, Aksesoris & Packaging Terverifikasi"
ws5["B3"].font = font_subtitle
ws5["B3"].fill = fill_header
ws5["B3"].alignment = align_left

v_headers = [
    ("B4", "No"),
    ("C4", "Nama Vendor / Toko"),
    ("D4", "Kategori Layanan"),
    ("E4", "Kontak / WhatsApp"),
    ("F4", "Kota / Lokasi"),
    ("G4", "Min. Order (MOQ)"),
    ("H4", "Lead Time (Hari)"),
    ("I4", "Catatan Kualitas & Keahlian"),
]

ws5.row_dimensions[4].height = 22
for c_pos, h_text in v_headers:
    ws5[c_pos] = h_text
    ws5[c_pos].font = font_tbl_header
    ws5[c_pos].fill = fill_sec
    ws5[c_pos].alignment = align_center
    ws5[c_pos].border = box_border

vendor_data = [
    ("Kain Utama Tekstil", "Toko Bahan Kain", "0812-8899-1122", "Bandung", "1 Roll (25 kg)", 3, "Spesialis Combed 16s/24s & Cotton Fleece reaktif."),
    ("Garment Kreasi Prima", "Konveksi Jahit", "0813-7766-3344", "Bandung", "50 pcs per model", 14, "Jahitan rapi standar distro, overdeck 3 jarum & rantai."),
    ("Studio Sablon Pro", "Sablon Screenprint", "0815-5544-2211", "Tangerang", "24 pcs per desain", 7, "Ahlian tinta Plastisol doff, Discharge & High-Density."),
    ("Woven Label Nusantara", "Label & Hangtag", "0817-2233-9900", "Jakarta Barat", "100 lusin (1200 pcs)", 10, "Damask HD kerapatan benang tinggi, tidak gatal di leher."),
    ("Packbox Mandiri", "Kemasan Ziplock", "0818-4455-6677", "Surabaya", "500 pcs", 7, "Ziplock frosted semi-buram dengan cetak sablon 1 warna."),
    ("Mitra Ekspedisi Kargo", "Logistik Distribusi", "0819-3322-1100", "Jakarta Pusat", "10 kg", 2, "Tarif kargo ekonomis untuk pengiriman bahan antar kota."),
]

for idx, v in enumerate(vendor_data, start=1):
    r_v = 4 + idx
    name, cat, phone, city, moq, lt, notes = v
    ws5.row_dimensions[r_v].height = 20

    ws5[f"B{r_v}"] = idx
    ws5[f"B{r_v}"].alignment = align_center
    ws5[f"B{r_v}"].border = box_border

    ws5[f"C{r_v}"] = name
    ws5[f"C{r_v}"].font = font_bold
    ws5[f"C{r_v}"].alignment = align_left
    ws5[f"C{r_v}"].border = box_border

    ws5[f"D{r_v}"] = cat
    ws5[f"D{r_v}"].alignment = align_left
    ws5[f"D{r_v}"].border = box_border

    ws5[f"E{r_v}"] = phone
    ws5[f"E{r_v}"].alignment = align_center
    ws5[f"E{r_v}"].border = box_border

    ws5[f"F{r_v}"] = city
    ws5[f"F{r_v}"].alignment = align_left
    ws5[f"F{r_v}"].border = box_border

    ws5[f"G{r_v}"] = moq
    ws5[f"G{r_v}"].alignment = align_left
    ws5[f"G{r_v}"].border = box_border

    ws5[f"H{r_v}"] = lt
    ws5[f"H{r_v}"].alignment = align_center
    ws5[f"H{r_v}"].border = box_border
    ws5[f"H{r_v}"].number_format = "0 \"hari\""

    ws5[f"I{r_v}"] = notes
    ws5[f"I{r_v}"].alignment = align_left
    ws5[f"I{r_v}"].border = box_border

ws5.column_dimensions["A"].width = 4
ws5.column_dimensions["B"].width = 6
ws5.column_dimensions["C"].width = 26
ws5.column_dimensions["D"].width = 20
ws5.column_dimensions["E"].width = 18
ws5.column_dimensions["F"].width = 16
ws5.column_dimensions["G"].width = 22
ws5.column_dimensions["H"].width = 16
ws5.column_dimensions["I"].width = 45


# Save Workbook
out_file = TARGET_DIR / "kalkulator-clothing.xlsx"
wb.save(out_file)
print(f"Workbook berhasil disimpan di: {out_file}")

# Write product.json with exact input cells
metadata = {
    "title": "Clothing Brand Financial & Production OS",
    "author": "Digital Product Factory",
    "version": "1.0.0",
    "license": "CC0-1.0",
    "input_cells": INPUT_CELLS,
}
(TARGET_DIR / "product.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"product.json diperbarui dengan {len(INPUT_CELLS)} input cells.")

# Run QA check
report = check_product(TARGET_DIR, "xlsx")
print("\n=== HASIL QA CHECK ===")
print("Exit Code:", report.exit_code)
for f in report.findings:
    print(f"[{f.status.upper()}] {f.id}: {f.message}")

assert report.exit_code == 0, "QA Check Gagal!"
print("\nSTATUS: 100% PASS - SIAP JUAL!")
