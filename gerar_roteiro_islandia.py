#!/usr/bin/env python3
"""Gera o PDF do Roteiro Islândia Agosto 2026 - Versão Final Revisada"""

from fpdf import FPDF

FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
FONT_NAME = "ArialUni"


class RoteiroPDF(FPDF):
    def header(self):
        pass

    def footer(self):
        if self.page_no() > 0:
            self.set_y(-15)
            self.set_font(FONT_NAME, "", 8)
            self.set_text_color(140, 140, 140)
            self.cell(0, 10, f"Roteiro Isl\u00e2ndia 2026 \u2014 P\u00e1gina {self.page_no()}", align="C")

    def setup_fonts(self):
        self.add_font(FONT_NAME, "", FONT_PATH)
        self.add_font(FONT_NAME, "B", FONT_PATH)
        self.add_font(FONT_NAME, "I", FONT_PATH)

    def day_header(self, date, route, sleep):
        self.set_fill_color(35, 35, 35)
        self.set_text_color(255, 255, 255)
        self.set_font(FONT_NAME, "B", 10)
        text = f"{date} \u2014 {route} | Dormir: {sleep}"
        self.cell(0, 10, text, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def table_header(self):
        self.set_fill_color(180, 180, 180)
        self.set_text_color(30, 30, 30)
        self.set_font(FONT_NAME, "B", 8.5)
        w = [58, 22, 22, 28, 60]
        headers = ["Parada", "Desloc.", "Chegada", "Perm.", "Atividades"]
        for i, h in enumerate(headers):
            self.cell(w[i], 7, h, border=1, fill=True, align="C")
        self.ln()

    def table_row(self, row, highlight=False, is_night=False):
        w = [58, 22, 22, 28, 60]
        self.set_text_color(30, 30, 30)
        if highlight:
            self.set_fill_color(255, 243, 205)
            fill = True
        elif is_night:
            self.set_fill_color(230, 240, 250)
            fill = True
        else:
            self.set_fill_color(255, 255, 255)
            fill = False
        self.set_font(FONT_NAME, "B" if (highlight or is_night) else "", 8)
        for i, val in enumerate(row):
            align = "L" if i in [0, 4] else "C"
            self.cell(w[i], 7, f" {val}" if (i in [0, 4] and align == "L") else val,
                      border=1, fill=fill, align=align)
        self.ln()

    def add_day(self, date, route, sleep, rows, highlights=None):
        if highlights is None:
            highlights = set()
        needed = 22 + len(rows) * 7 + 10
        if self.get_y() + needed > 268:
            self.add_page()
        self.day_header(date, route, sleep)
        self.table_header()
        for i, row in enumerate(rows):
            is_night = (row[3] == "Noite" or row[3] == "Tarde")
            self.table_row(row, highlight=(i in highlights), is_night=is_night)
        self.ln(5)


def main():
    pdf = RoteiroPDF(orientation="P", unit="mm", format="A4")
    pdf.setup_fonts()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Title
    pdf.set_font(FONT_NAME, "B", 24)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 15, "Roteiro Completo \u2014 Isl\u00e2ndia", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font(FONT_NAME, "", 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 9, "Agosto 2026", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(2)
    pdf.set_font(FONT_NAME, "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, "Vers\u00e3o final revisada \u2014 todas as paradas, hor\u00e1rios e pernoites", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    # Day 1
    pdf.add_day(
        "01/08", "Chegada na Isl\u00e2ndia", "Reykjav\u00edk",
        [
            ["Aeroporto KEF", "-", "18:20", "1h", "Imigra\u00e7\u00e3o, bagagem, carro"],
            ["Reykjav\u00edk (hotel)", "45 min", "20:05", "Noite", "Check-in, jantar, caminhada"],
        ]
    )

    # Day 2 — sem Kolugljúfur
    pdf.add_day(
        "02/08", "Sn\u00e6fellsnes \u2192 Akureyri", "Akureyri",
        [
            ["Ytri Tunga", "2h", "08:30", "30 min", "Praia das focas"],
            ["Arnarstapi", "35 min", "09:35", "1h", "Fal\u00e9sias e trilha"],
            ["Almo\u00e7o", "10 min", "10:45", "1h", "Restaurante local"],
            ["Dj\u00fapal\u00f3nssandur", "15 min", "12:00", "45 min", "Praia de lava"],
            ["Kirkjufell", "50 min", "13:35", "45 min", "Fotos"],
            ["Akureyri", "4h45", "19:05", "Noite", "Check-in e jantar"],
        ]
    )

    # Day 3
    pdf.add_day(
        "03/08", "Akureyri \u2192 Go\u00f0afoss \u2192 M\u00fdvatn \u2192 Dettifoss \u2192 Borgarfj\u00f6r\u00f0ur", "Borgarfj\u00f6r\u00f0ur eystri",
        [
            ["Go\u00f0afoss", "45 min", "08:15", "45 min", "Cachoeira"],
            ["Earth Lagoon M\u00fdvatn", "1h15", "10:15", "2h", "Banho geotermal"],
            ["Almo\u00e7o", "15 min", "12:30", "1h", "Restaurante local"],
            ["Dimmuborgir", "20 min", "13:50", "1h", "Forma\u00e7\u00f5es de lava"],
            ["Sk\u00fatusta\u00f0ag\u00edgar", "15 min", "15:05", "45 min", "Pseudocrateras"],
            ["Hverir", "20 min", "16:10", "30 min", "\u00c1rea geotermal"],
            ["Dettifoss", "1h", "17:40", "1h", "Cachoeira"],
            ["Borgarfj\u00f6r\u00f0ur eystri", "2h30", "21:10", "Noite", "Check-in"],
        ]
    )

    # Day 4
    pdf.add_day(
        "04/08", "Puffins \u2192 V\u00f6k Baths \u2192 Rj\u00fakandi \u2192 H\u00f6fn", "H\u00f6fn",
        [
            ["Borgarfjar\u00f0arh\u00f6fn", "-", "07:30", "1h", "Puffins"],
            ["V\u00f6k Baths", "1h20", "09:50", "2h", "Banho geotermal"],
            ["Almo\u00e7o", "10 min", "12:00", "1h", "Restaurante local"],
            ["Rj\u00fakandi", "45 min", "13:45", "15 min", "Cascata na Ring Road"],
            ["Dj\u00fapivogur", "1h30", "15:30", "20 min", "Vilarejo"],
            ["Eggin \u00ed Gle\u00f0iv\u00edk", "5 min", "15:55", "10 min", "Esculturas"],
            ["H\u00f6fn", "1h25", "17:30", "Noite", "Check-in e jantar"],
        ]
    )

    # Day 5 — glaciar 4h
    pdf.add_day(
        "05/08", "Vestrahorn \u2192 J\u00f6kuls\u00e1rl\u00f3n \u2192 Glaciar 14h \u2192 Kirkjub\u00e6jarklaustur", "Kirkjub\u00e6jarklaustur",
        [
            ["Vestrahorn / Stokksnes", "15 min", "07:45", "45 min", "Fotos + dunas negras"],
            ["J\u00f6kuls\u00e1rl\u00f3n", "1h", "09:30", "45 min", "Fotos"],
            ["Diamond Beach", "5 min", "10:20", "30 min", "Praia de gelo"],
            ["Almo\u00e7o", "15 min", "11:05", "1h", "Restaurante local"],
            ["Fjalls\u00e1rl\u00f3n", "10 min", "13:30", "4h30", "Passeio no glaciar (14h-18h)"],
            ["Fja\u00f0r\u00e1rglj\u00fafur", "2h", "20:00", "30 min", "C\u00e2nion"],
            ["Kirkjub\u00e6jarklaustur", "15 min", "20:45", "Noite", "Check-in e jantar"],
        ],
        highlights={0, 4}
    )

    # Day 6
    pdf.add_day(
        "06/08", "Kirkjub\u00e6jarklaustur \u2192 Cachoeiras \u2192 Golden Circle \u2192 Reykjav\u00edk", "Reykjav\u00edk",
        [
            ["Dyrh\u00f3laey", "1h15", "08:15", "30 min", "Mirante"],
            ["Sk\u00f3gafoss", "30 min", "09:15", "45 min", "Cachoeira"],
            ["Seljalandsfoss", "30 min", "10:30", "45 min", "Caminhar atr\u00e1s"],
            ["Fri\u00f0heimar", "2h", "13:15", "1h", "Almo\u00e7o (estufas de tomate)"],
            ["Geysir", "15 min", "14:30", "30 min", "\u00c1rea geotermal"],
            ["Gullfoss", "15 min", "15:15", "45 min", "Cachoeira"],
            ["Keri\u00f0", "45 min", "16:45", "30 min", "Cratera"],
            ["Reykjav\u00edk", "1h30", "18:45", "Noite", "Check-in e jantar"],
        ]
    )

    # Day 7
    pdf.add_day(
        "07/08", "Silfra + Reykjav\u00edk", "Reykjav\u00edk",
        [
            ["Silfra", "45 min", "09:00", "3h", "Snorkeling"],
            ["Reykjav\u00edk", "45 min", "13:00", "Tarde", "Cidade / Sky Lagoon"],
        ]
    )

    # ---- Summary page ----
    pdf.add_page()
    pdf.set_font(FONT_NAME, "B", 18)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 12, "Resumo dos 7 dias", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # Summary table
    pdf.set_fill_color(35, 35, 35)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font(FONT_NAME, "B", 8.5)
    sw = [20, 95, 25, 50]
    sheaders = ["Dia", "Rota", "Chegada", "Pernoite"]
    for i, h in enumerate(sheaders):
        pdf.cell(sw[i], 8, h, border=1, fill=True, align="C")
    pdf.ln()

    summary = [
        ["01/08", "KEF \u2192 Reykjav\u00edk", "20:05", "Reykjav\u00edk"],
        ["02/08", "Sn\u00e6fellsnes \u2192 Akureyri", "19:05", "Akureyri"],
        ["03/08", "Go\u00f0afoss \u2192 M\u00fdvatn \u2192 Dettifoss \u2192 Borgarfj\u00f6r\u00f0ur", "21:10", "Borgarfj\u00f6r\u00f0ur eystri"],
        ["04/08", "Puffins \u2192 V\u00f6k Baths \u2192 Rj\u00fakandi \u2192 H\u00f6fn", "17:30", "H\u00f6fn"],
        ["05/08", "Vestrahorn \u2192 J\u00f6kuls\u00e1rl\u00f3n \u2192 Glaciar \u2192 Kirkjub\u00e6jarklaustur", "20:45", "Kirkjub\u00e6jarklaustur"],
        ["06/08", "Kirkjub\u00e6jarklaustur \u2192 Cachoeiras \u2192 Golden Circle \u2192 Reykjav\u00edk", "18:45", "Reykjav\u00edk"],
        ["07/08", "Silfra + Reykjav\u00edk / Sky Lagoon", "13:00", "Reykjav\u00edk"],
    ]

    pdf.set_text_color(30, 30, 30)
    for j, row in enumerate(summary):
        if j % 2 == 0:
            pdf.set_fill_color(245, 245, 245)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.set_font(FONT_NAME, "", 8.5)
        for i, val in enumerate(row):
            align = "L" if i == 1 else "C"
            v = f" {val}" if i == 1 else val
            pdf.cell(sw[i], 7, v, border=1, fill=True, align=align)
        pdf.ln()

    pdf.ln(10)

    # Highlights section
    pdf.set_font(FONT_NAME, "B", 14)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, "Destaques do roteiro", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    highlights_data = [
        ("Natureza", "Dettifoss, Go\u00f0afoss, Gullfoss, Sk\u00f3gafoss, Seljalandsfoss, Rj\u00fakandi, Fja\u00f0r\u00e1rglj\u00fafur, Keri\u00f0"),
        ("Geotermal", "Earth Lagoon M\u00fdvatn, V\u00f6k Baths, Hverir, Geysir, Sky Lagoon"),
        ("Aventura", "Passeio no glaciar 4h (Fjalls\u00e1rl\u00f3n), Snorkeling em Silfra"),
        ("Fauna", "Puffins em Borgarfjar\u00f0arh\u00f6fn, Focas em Ytri Tunga"),
        ("Paisagens", "Vestrahorn/Stokksnes, Diamond Beach, J\u00f6kuls\u00e1rl\u00f3n, Kirkjufell, Dyrh\u00f3laey, Dj\u00fapal\u00f3nssandur"),
        ("Cultura", "Arnarstapi, Dimmuborgir, Eggin \u00ed Gle\u00f0iv\u00edk, Fri\u00f0heimar, Reykjav\u00edk"),
    ]

    for cat, items in highlights_data:
        pdf.set_font(FONT_NAME, "B", 9)
        pdf.cell(28, 7, f"  {cat}:", align="L")
        pdf.set_font(FONT_NAME, "", 8.5)
        pdf.cell(0, 7, items, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(10)

    # Notes
    pdf.set_font(FONT_NAME, "B", 14)
    pdf.cell(0, 10, "Observa\u00e7\u00f5es importantes", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font(FONT_NAME, "", 8.5)
    notes = [
        "Todos os hor\u00e1rios consideram agosto (20h+ de luz solar di\u00e1ria).",
        "Dia 02 \u00e9 o mais intenso em estrada (~8h de deslocamento). Saia \u00e0s 06:30.",
        "Dia 03 chega mais tarde (~21h) por incluir Dettifoss. Ainda h\u00e1 sol pleno nesse hor\u00e1rio.",
        "Dia 04 \u00e9 o mais tranquilo. Aproveite o jantar em H\u00f6fn \u2014 famosa pela lagosta.",
        "Dia 05: passeio no glaciar das 14h \u00e0s 18h (4h). Chegar em Fjalls\u00e1rl\u00f3n at\u00e9 13:30 para check-in.",
        "Dia 05 termina em Kirkjub\u00e6jarklaustur (~20:45), perto de Fja\u00f0r\u00e1rglj\u00fafur. Hotel Geirland.",
        "Vestrahorn/Stokksnes: pagar taxa no Viking Caf\u00e9 (~900 ISK por pessoa). Sem reserva.",
        "Clima island\u00eas \u00e9 imprevis\u00edvel. Tenha sempre plano B e roupas imperme\u00e1veis.",
        "Abaste\u00e7a o carro sempre que poss\u00edvel. Postos podem ser distantes no leste e norte.",
    ]
    for note in notes:
        pdf.cell(5, 6.5, "\u2022")
        pdf.cell(0, 6.5, f" {note}", new_x="LMARGIN", new_y="NEXT")

    # Save
    output_path = "/Users/vitorsampaio/Downloads/Roteiro_Islandia_2026_FINAL.pdf"
    pdf.output(output_path)
    print(f"PDF gerado: {output_path}")


if __name__ == "__main__":
    main()
