"""Build the portfolio review workbook from the API data and the six review results."""
import glob
import json
import os
import re
import sys
import unicodedata

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
SITE = "https://dev.sabergroup-eg.com/portfolio/"

projects = {p["_id"]: p for p in json.load(open(f"{HERE}/projects.json"))["projects"] if not p.get("deleted")}
flat = {p["id"]: p for p in json.load(open(f"{HERE}/flat.json"))}
results = {}
for f in sorted(glob.glob(f"{HERE}/result*.json")):
    for r in json.load(open(f)):
        results[r["id"]] = r
missing = [i for i in flat if i not in results]
if missing:
    print("WARNING: no review for", len(missing), "projects")

FONT = "Arial"
HEAD = PatternFill("solid", fgColor="1F1F1F")
INPUT = PatternFill("solid", fgColor="FFF2B3")
SUGG = PatternFill("solid", fgColor="E8F3EA")
thin = Side(style="thin", color="D9D9D9")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")
SEV_ORDER = {"high": 0, "medium": 1, "low": 2}
TYPE_AR = {
    "spelling": "خطأ إملائي", "grammar": "قواعد", "wording": "صياغة", "translation_mismatch": "الترجمة مختلفة",
    "missing_translation": "ترجمة ناقصة", "wrong_language": "لغة غلط", "placeholder": "نص مؤقت/تجريبي",
    "inconsistent": "غير متسق", "formatting": "تنسيق", "generic": "عام وغير معبر", "claim": "ادعاء/علامة تجارية",
}
SEV_AR = {"high": "عالي", "medium": "متوسط", "low": "منخفض"}
FIELD_AR = {"name": "الاسم", "description": "الوصف", "location": "المكان", "cast": "فريق العمل"}


def field_ar(f):
    if f in FIELD_AR:
        return FIELD_AR[f]
    m = re.match(r"section(\d+)\.(\w+)", f or "")
    if m:
        part = {"caption": "عنوان", "description": "وصف", "text": "نص", "before_label": "ليبل قبل", "after_label": "ليبل بعد"}.get(m.group(2), m.group(2))
        return f"سكشن {m.group(1)} – {part}"
    return f or ""


def slugify(t):
    t = unicodedata.normalize("NFD", t or "")
    t = "".join(c for c in t if unicodedata.category(c) != "Mn").lower().strip()
    return re.sub(r"\s+", "-", re.sub(r"[^a-z0-9\s-]", "", t))


def counts(p):
    photos = videos = 0
    for m in p.get("material") or []:
        if m["type"] == "video" and m.get("url"):
            videos += 1
        elif m["type"] == "before_after":
            photos += 2
        else:
            items = m.get("items") or ([m] if m.get("url") else [])
            for it in items:
                if it.get("type") == "video" or (it.get("mimeType") or "").startswith("video"):
                    videos += 1
                else:
                    photos += 1
    return photos, videos, len(p.get("material") or [])


def style_header(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(name=FONT, bold=True, color="FFFFFF", size=10)
        cell.fill = HEAD
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        cell.border = BORDER
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def body(cell, fill=None, bold=False):
    cell.font = Font(name=FONT, size=10, bold=bold)
    cell.alignment = WRAP
    cell.border = BORDER
    if fill:
        cell.fill = fill


wb = Workbook()

# ---------------- Projects (one row per project) ----------------
ws = wb.active
ws.title = "المشاريع"
ws.sheet_view.rightToLeft = True
cols = [
    ("#", 5), ("الأولوية (اكتبها)", 10), ("القرار (اختار)", 13), ("ملاحظاتك", 26),
    ("الاسم الحالي EN", 28), ("الاسم الحالي AR", 26), ("الاسم المقترح EN", 32), ("الاسم المقترح AR", 30), ("ليه الاسم محتاج يتغير", 28),
    ("العميل", 14), ("القطاع", 14), ("الخدمات", 26), ("صور", 7), ("فيديو", 7), ("سكاشن", 7),
    ("جاهزية النص 1-5", 9), ("عدد الملاحظات", 9), ("ملاحظات عالية الخطورة", 9), ("الناقص في المشروع", 32), ("ملاحظة المراجع", 32),
    ("منشور؟", 8), ("اللينك", 30), ("ID", 26),
]
for i, (h, w) in enumerate(cols, 1):
    ws.cell(row=1, column=i, value=h)
    ws.column_dimensions[get_column_letter(i)].width = w
style_header(ws, 1, len(cols))
ws.row_dimensions[1].height = 34

order = sorted(flat.values(), key=lambda p: (p.get("published") is not True, (p["texts"][0]["text"] if p["texts"] else "").lower()))
index = {}
for n, fp in enumerate(order, 1):
    p = projects[fp["id"]]
    r = results.get(fp["id"], {})
    index[fp["id"]] = n
    photos, videos, sections = counts(p)
    name = p.get("name") or {}
    slug = fp["slug"] or slugify(name.get("en"))
    row = n + 1
    vals = [
        n, None, None, None,
        name.get("en", ""), name.get("ar", ""), r.get("suggested_name_en", ""), r.get("suggested_name_ar", ""), r.get("name_reason", ""),
        fp.get("client", ""), ", ".join(fp.get("sector") or []), ", ".join(s.split(" / ")[0] for s in fp.get("services") or []),
        photos, videos, sections,
        r.get("quality_score"),
        f'=COUNTIFS(\'الملاحظات\'!$A:$A,A{row})',
        f'=COUNTIFS(\'الملاحظات\'!$A:$A,A{row},\'الملاحظات\'!$G:$G,"عالي")',
        "، ".join(r.get("missing_content") or []), r.get("note", ""),
        "نعم" if p.get("published") else "لا", SITE + slug, fp["id"],
    ]
    for c, v in enumerate(vals, 1):
        cell = ws.cell(row=row, column=c, value=v)
        body(cell, INPUT if c in (2, 3, 4) else SUGG if c in (7, 8) else None, bold=c in (5, 7))
    ws.cell(row=row, column=22).hyperlink = SITE + slug
    ws.cell(row=row, column=22).font = Font(name=FONT, size=10, color="0563C1", underline="single")
last = len(order) + 1
dv = DataValidation(type="list", formula1='"ابقيه زي ما هو,غيّر الاسم,عدّل النصوص,أعد بناءه,اخفيه"', allow_blank=True)
ws.add_data_validation(dv)
dv.add(f"C2:C{last}")
dvp = DataValidation(type="whole", operator="between", formula1="1", formula2="999", allow_blank=True)
ws.add_data_validation(dvp)
dvp.add(f"B2:B{last}")
ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{last}"
red = PatternFill("solid", fgColor="F8D7DA")
ws.conditional_formatting.add(f"P2:P{last}", FormulaRule(formula=["AND(ISNUMBER(P2),P2<=2)"], fill=red))
ws.conditional_formatting.add(f"R2:R{last}", FormulaRule(formula=["R2>0"], fill=red))

# ---------------- Issues (one row per problem) ----------------
wi = wb.create_sheet("الملاحظات")
wi.sheet_view.rightToLeft = True
icols = [("#", 5), ("المشروع", 30), ("الحقل", 16), ("اللغة", 6), ("نوع المشكلة", 15), ("type", 14), ("الخطورة", 9),
         ("الموجود دلوقتي", 45), ("المقترح", 50), ("قرارك (اختار)", 12), ("ملاحظاتك", 24)]
for i, (h, w) in enumerate(icols, 1):
    wi.cell(row=1, column=i, value=h)
    wi.column_dimensions[get_column_letter(i)].width = w
style_header(wi, 1, len(icols))
rows = []
for fid, r in results.items():
    n = index.get(fid)
    if n is None:
        continue
    pname = (projects[fid].get("name") or {}).get("en", "")
    for it in r.get("issues") or []:
        rows.append((n, pname, it))
rows.sort(key=lambda x: (SEV_ORDER.get(x[2].get("severity"), 3), x[0]))
for k, (n, pname, it) in enumerate(rows, 2):
    vals = [n, pname, field_ar(it.get("field")), (it.get("lang") or "").upper(), TYPE_AR.get(it.get("type"), it.get("type")),
            it.get("type"), SEV_AR.get(it.get("severity"), it.get("severity")), it.get("current", ""), it.get("suggestion", ""), None, None]
    for c, v in enumerate(vals, 1):
        body(wi.cell(row=k, column=c, value=v), INPUT if c in (10, 11) else SUGG if c == 9 else None)
ilast = len(rows) + 1
dvi = DataValidation(type="list", formula1='"موافق,مرفوض,محتاج تعديل"', allow_blank=True)
wi.add_data_validation(dvi)
dvi.add(f"J2:J{max(ilast, 2)}")
wi.auto_filter.ref = f"A1:K{max(ilast, 2)}"
wi.conditional_formatting.add(f"G2:G{max(ilast, 2)}", FormulaRule(formula=['G2="عالي"'], fill=red))

# ---------------- Tags ----------------
wt = wb.create_sheet("التاجز")
wt.sheet_view.rightToLeft = True
tcols = [("#", 5), ("المشروع", 28), ("عدد التاجز EN", 8), ("التاجز الحالية EN", 45), ("عدد التاجز AR", 8), ("التاجز الحالية AR", 45),
         ("المقترح EN", 40), ("المقترح AR", 40), ("مشاكل التاجز", 45)]
for i, (h, w) in enumerate(tcols, 1):
    wt.cell(row=1, column=i, value=h)
    wt.column_dimensions[get_column_letter(i)].width = w
style_header(wt, 1, len(tcols))
for fp in order:
    n = index[fp["id"]]
    r = results.get(fp["id"], {})
    probs = "\n".join(f"• {t.get('current', '')} ← {t.get('suggestion', '')}".strip() for t in r.get("tag_issues") or [])
    vals = [n, (projects[fp["id"]].get("name") or {}).get("en", ""), len(fp["tagsEn"]), "، ".join(fp["tagsEn"]),
            len(fp["tagsAr"]), "، ".join(fp["tagsAr"]), "، ".join(r.get("suggested_tags_en") or []),
            "، ".join(r.get("suggested_tags_ar") or []), probs]
    for c, v in enumerate(vals, 1):
        body(wt.cell(row=n + 1, column=c, value=v), SUGG if c in (7, 8) else None)

# ---------------- All current text ----------------
wx = wb.create_sheet("النصوص الحالية")
wx.sheet_view.rightToLeft = True
xcols = [("#", 5), ("المشروع", 28), ("الحقل", 18), ("اللغة", 6), ("النص الحالي كامل", 110)]
for i, (h, w) in enumerate(xcols, 1):
    wx.cell(row=1, column=i, value=h)
    wx.column_dimensions[get_column_letter(i)].width = w
style_header(wx, 1, len(xcols))
k = 2
for fp in order:
    n = index[fp["id"]]
    pname = (projects[fp["id"]].get("name") or {}).get("en", "")
    texts = list(fp["texts"]) + [{"field": "cast", "lang": "en", "text": c} for c in fp.get("cast") or []]
    texts += [{"field": "services", "lang": "", "text": s} for s in fp.get("services") or []]
    for t in texts:
        for c, v in enumerate([n, pname, field_ar(t["field"]) if t["field"] != "services" else "الخدمات", t["lang"].upper(), t["text"]], 1):
            body(wx.cell(row=k, column=c, value=v))
        k += 1
wx.auto_filter.ref = f"A1:E{k - 1}"

# ---------------- Summary (formulas over the issues sheet) ----------------
wsum = wb.create_sheet("الملخص", 0)
wsum.sheet_view.rightToLeft = True
wsum.column_dimensions["A"].width = 30
for col in "BCDE":
    wsum.column_dimensions[col].width = 14
wsum["A1"] = "مراجعة نصوص مشاريع البورتفوليو"
wsum["A1"].font = Font(name=FONT, size=16, bold=True)
wsum["A2"] = "مصدر الداتا: الـ API العام للمشاريع (projects/public) وقت المراجعة. مفيش أي تعديل اتعمل على الداشبورد أو الموقع."
wsum["A2"].font = Font(name=FONT, size=10, italic=True)
wsum["A4"], wsum["B4"] = "عدد المشاريع", "=COUNTA('المشاريع'!A:A)-1"
wsum["A5"], wsum["B5"] = "المنشور منها", "=COUNTIF('المشاريع'!U:U,\"نعم\")"
wsum["A6"], wsum["B6"] = "إجمالي الملاحظات", "=COUNTA('الملاحظات'!A:A)-1"
wsum["A7"], wsum["B7"] = "متوسط جاهزية النص (من 5)", "=IFERROR(ROUND(AVERAGE('المشاريع'!P:P),1),\"-\")"
wsum["A8"], wsum["B8"] = "مشاريع جاهزيتها 2 أو أقل", "=COUNTIF('المشاريع'!P:P,\"<=2\")"
for r in range(4, 9):
    wsum[f"A{r}"].font = Font(name=FONT, size=11, bold=True)
    wsum[f"B{r}"].font = Font(name=FONT, size=11)
wsum["A10"], wsum["B10"], wsum["C10"], wsum["D10"], wsum["E10"] = "نوع المشكلة", "الإجمالي", "عالي", "متوسط", "منخفض"
for c in "ABCDE":
    cell = wsum[f"{c}10"]
    cell.font = Font(name=FONT, bold=True, color="FFFFFF")
    cell.fill = HEAD
r = 11
for key, ar in TYPE_AR.items():
    wsum[f"A{r}"] = ar
    wsum[f"B{r}"] = f"=COUNTIF('الملاحظات'!$F:$F,\"{key}\")"
    for col, sev in zip("CDE", ("عالي", "متوسط", "منخفض")):
        wsum[f"{col}{r}"] = f"=COUNTIFS('الملاحظات'!$F:$F,\"{key}\",'الملاحظات'!$G:$G,\"{sev}\")"
    for c in "ABCDE":
        wsum[f"{c}{r}"].font = Font(name=FONT, size=10)
        wsum[f"{c}{r}"].border = BORDER
    r += 1
r += 1
legend = [
    "إزاي تستخدم الشيت:",
    "• الخانات الصفرا بتاعتك: الأولوية، القرار، ملاحظاتك (في شيت المشاريع)، وقرارك على كل ملاحظة (في شيت الملاحظات).",
    "• الأولوية: رقم، 1 = أهم مشروع. مثال: اكتب 1 قدام المشروع اللي عايزه يظهر أول حاجة في البورتفوليو.",
    "• الخانات الخضرا: اقتراحاتي (أسماء، تصحيحات، تاجز). مفيش منها حاجة اتطبقت.",
    "• شيت \"الملاحظات\" مرتب من الأخطر للأقل، وفيه فلتر على كل عمود.",
    "• شيت \"النصوص الحالية\" فيه كل كلمة مكتوبة في كل مشروع زي ما هي، للرجوع ليها.",
    "• عدد الملاحظات والملخص بيتحسبوا بمعادلات من شيت الملاحظات.",
]
for line in legend:
    wsum[f"A{r}"] = line
    wsum[f"A{r}"].font = Font(name=FONT, size=10, bold=line.endswith(":"))
    wsum.merge_cells(f"A{r}:E{r}")
    r += 1

wb.save(OUT)
print("rows: projects", len(order), "issues", len(rows), "texts", k - 2)
