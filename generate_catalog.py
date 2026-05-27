"""
Absorb Pad S.R.L. - Catalogo General de Productos (v2 - CON IMAGENES)
Genera PDF rebrandeado con TODAS las imagenes del catalogo original
y TODOS los productos de las 41 paginas.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, 
                                 TableStyle, PageBreak, Image as RLImage, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
import os

# =================== PATHS ===================
BASE = r'C:\Users\Sanatorio Argentino\Desktop\Proyectos\Absorbpad'
IMG_DIR = os.path.join(BASE, 'pdf_images')
LOGO = os.path.join(BASE, 'public', 'assets', 'logo_absorbpad.png')
OUT = os.path.join(BASE, 'Catalogo-General-AbsorbPad-v2.pdf')

# =================== COLORS ===================
TEAL = HexColor('#2E8B98')
TEAL_DK = HexColor('#25707A')
TEAL_LT = HexColor('#E8F4F6')
YELLOW = HexColor('#F9D423')
DARK = HexColor('#1A1A1A')
CARD = HexColor('#2A2A2A')
TXT = HexColor('#4A4A4A')
TXT_LT = HexColor('#707070')
BDR = HexColor('#E2E8F0')
RED_S = HexColor('#C0392B')
GREEN_S = HexColor('#27AE60')
BLUE_S = HexColor('#2980B9')
ORANGE_S = HexColor('#E67E22')
W, H = A4

def img(name):
    """Get image path, return None if not found"""
    p = os.path.join(IMG_DIR, name)
    return p if os.path.exists(p) else None

def safe_img(name, w, h):
    """Return an RLImage or empty Spacer if image missing"""
    p = img(name)
    if p:
        try:
            return RLImage(p, width=w, height=h)
        except:
            pass
    return Spacer(1, h)

# =================== TEMPLATE ===================
class CatTemplate:
    def __init__(self):
        self.pc = 0
        self.cover = True
    
    def on_page(self, c, doc):
        self.pc += 1
        c.saveState()
        if self.cover:
            self._cover(c)
            self.cover = False
        else:
            self._header(c)
            self._footer(c)
        c.restoreState()
    
    def _cover(self, c):
        c.setFillColor(DARK); c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(TEAL); c.rect(0,H-8*mm,W,8*mm,fill=1,stroke=0)
        p=c.beginPath(); p.moveTo(W-200*mm,H-8*mm); p.lineTo(W,H-8*mm); p.lineTo(W,H-20*mm); p.close()
        c.setFillColor(YELLOW); c.drawPath(p,fill=1,stroke=0)
        if os.path.exists(LOGO):
            c.drawImage(LOGO,W/2-40*mm,H-120*mm,80*mm,80*mm,preserveAspectRatio=True,mask='auto')
        c.setFillColor(TEAL); c.setFont("Helvetica-Bold",42); c.drawCentredString(W/2,H-140*mm,"ABSORB PAD")
        c.setFillColor(YELLOW); c.setFont("Helvetica",16); c.drawCentredString(W/2,H-150*mm,"S.R.L.")
        c.setFillColor(white); c.setFont("Helvetica-Bold",28)
        c.drawCentredString(W/2,H-185*mm,"Catalogo General"); c.drawCentredString(W/2,H-195*mm,"de Productos")
        c.setFillColor(TEAL_LT); c.setFont("Helvetica",14); c.drawCentredString(W/2,H-220*mm,"Soluciones Industriales y Mineria")
        c.setStrokeColor(YELLOW); c.setLineWidth(3); c.line(W/2-40*mm,H-230*mm,W/2+40*mm,H-230*mm)
        c.setFillColor(HexColor('#AAAAAA')); c.setFont("Helvetica",10)
        c.drawCentredString(W/2,H-250*mm,"San Luis 657 (E) | San Juan | Argentina")
        c.drawCentredString(W/2,H-258*mm,"+54 9 264 411 5967 | mario.ortiz@absorbpad.com")
        c.drawCentredString(W/2,H-266*mm,"www.absorbpad.com")
        c.setFillColor(TEAL); c.rect(0,0,W,6*mm,fill=1,stroke=0)
        p2=c.beginPath(); p2.moveTo(0,0); p2.lineTo(80*mm,0); p2.lineTo(60*mm,6*mm); p2.lineTo(0,6*mm); p2.close()
        c.setFillColor(YELLOW); c.drawPath(p2,fill=1,stroke=0)
    
    def _header(self, c):
        c.setFillColor(TEAL); c.rect(0,H-12*mm,W,12*mm,fill=1,stroke=0)
        p=c.beginPath(); p.moveTo(W-60*mm,H); p.lineTo(W,H); p.lineTo(W,H-12*mm); p.close()
        c.setFillColor(YELLOW); c.drawPath(p,fill=1,stroke=0)
        if os.path.exists(LOGO):
            c.drawImage(LOGO,10*mm,H-11*mm,9*mm,9*mm,preserveAspectRatio=True,mask='auto')
        c.setFillColor(white); c.setFont("Helvetica-Bold",10); c.drawString(22*mm,H-8.5*mm,"ABSORB PAD S.R.L.")
        c.setStrokeColor(BDR); c.setLineWidth(0.5); c.line(10*mm,H-14*mm,W-10*mm,H-14*mm)
    
    def _footer(self, c):
        c.setFillColor(DARK); c.rect(0,0,W,10*mm,fill=1,stroke=0)
        p=c.beginPath(); p.moveTo(0,0); p.lineTo(30*mm,0); p.lineTo(20*mm,10*mm); p.lineTo(0,10*mm); p.close()
        c.setFillColor(YELLOW); c.drawPath(p,fill=1,stroke=0)
        c.setFillColor(white); c.setFont("Helvetica",8); c.drawCentredString(W/2,3.5*mm,f"{self.pc}")
        c.setFillColor(TEAL_LT); c.setFont("Helvetica",7); c.drawRightString(W-10*mm,3.5*mm,"www.absorbpad.com")

# =================== STYLES ===================
def S(name, sz, color=TXT, bold=False, align=TA_LEFT, lead=None, sA=0, sB=0):
    return ParagraphStyle(name, fontSize=sz, textColor=color, 
        fontName='Helvetica-Bold' if bold else 'Helvetica',
        alignment=align, leading=lead or sz*1.3, spaceAfter=sA, spaceBefore=sB)

ST = S('st',22,TEAL,True,sA=4*mm,sB=3*mm,lead=26)       # Section Title
SS = S('ss',10,TXT,align=TA_JUSTIFY,sA=5*mm,lead=14)     # Section Subtitle
TH = S('th',6.5,white,True,TA_CENTER,lead=8)              # Table Header
TC = S('tc',7,DARK,align=TA_CENTER,lead=9)                 # Table Cell
TL = S('tl',7,DARK,align=TA_LEFT,lead=9)                   # Table Cell Left
FN = S('fn',6.5,TXT_LT,sB=2*mm,lead=8)                    # Footnote
BD = S('bd',8,TXT,align=TA_JUSTIFY,lead=11,sA=3*mm)       # Body desc
BN = S('bn',24,white,True,TA_CENTER,lead=30)               # Banner

# =================== HELPERS ===================
def section_hdr(title, subtitle, color=TEAL):
    els = []
    lt = Table([['']], colWidths=[60*mm], rowHeights=[3*mm])
    lt.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),color)]))
    els.append(lt); els.append(Spacer(1,3*mm))
    els.append(Paragraph(title, ST))
    if subtitle:
        els.append(Paragraph(subtitle, SS))
    return els

def banner(title, sub, color):
    d = [[Paragraph(f'<font color="white" size="20"><b>{title}</b></font>', S('b',20,white,True,TA_CENTER,lead=26))],
         [Paragraph(f'<font color="#E8F4F6" size="9">{sub}</font>', S('bs',9,TEAL_LT,align=TA_CENTER,lead=12))]]
    t = Table(d, colWidths=[178*mm], rowHeights=[16*mm,9*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),color),('VALIGN',(0,0),(0,-1),'MIDDLE'),
        ('ALIGN',(0,0),(0,-1),'CENTER'),('LINEBELOW',(0,-1),(0,-1),3,YELLOW)]))
    return t

def ptable(headers, rows, color=TEAL, cw=None):
    """Product table with optional image column"""
    data = [[Paragraph(h, TH) for h in headers]]
    for row in rows:
        fr = []
        for i, cell in enumerate(row):
            if isinstance(cell, (RLImage, Spacer)):
                fr.append(cell)
            elif i == len(row)-1:
                fr.append(Paragraph(str(cell), TL))
            else:
                fr.append(Paragraph(str(cell), TC))
        data.append(fr)
    
    nc = len(headers)
    if not cw:
        if nc == 8: cw = [20*mm,18*mm,22*mm,18*mm,18*mm,15*mm,18*mm,47*mm]
        elif nc == 7: cw = [20*mm,22*mm,20*mm,18*mm,18*mm,18*mm,52*mm]
        elif nc == 6: cw = [20*mm,26*mm,22*mm,22*mm,22*mm,46*mm]
        elif nc == 5: cw = [22*mm,28*mm,25*mm,25*mm,78*mm]
        elif nc == 4: cw = [25*mm,35*mm,35*mm,83*mm]
        elif nc == 3: cw = [30*mm,40*mm,108*mm]
        else: cw = [178*mm/nc]*nc
    
    t = Table(data, colWidths=cw, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),color),('TEXTCOLOR',(0,0),(-1,0),white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,0),7),
        ('ALIGN',(0,0),(-1,0),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('GRID',(0,0),(-1,-1),0.5,BDR),('LINEBELOW',(0,0),(-1,0),1,color),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[white,TEAL_LT]),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),
    ]))
    return t

def product_row_with_img(img_name, img_w=15*mm, img_h=18*mm):
    """Helper to create image cell for product tables"""
    return safe_img(img_name, img_w, img_h)


# =================== BUILD ===================
def build():
    tpl = CatTemplate()
    doc = SimpleDocTemplate(OUT, pagesize=A4, topMargin=18*mm, bottomMargin=14*mm,
                            leftMargin=16*mm, rightMargin=16*mm,
                            title="Absorb Pad S.R.L. - Catalogo General",
                            author="Absorb Pad S.R.L.")
    els = []
    
    # ===== COVER =====
    els.append(Spacer(1,1)); els.append(PageBreak())
    
    # ===== ABOUT =====
    els.extend(section_hdr("Quienes Somos",""))
    els.append(Paragraph(
        "Absorb Pad S.R.L. es una empresa argentina lider en soluciones industriales para el control "
        "de derrames y proteccion ambiental en el sector minero y energetico. Con sede en San Juan, desde 2008 "
        "desarrollamos y comercializamos una amplia gama de productos absorbentes, adhesivos y selladores "
        "industriales de alta performance. Nuestra tecnologia de microfibras de polipropileno <b>Meltblown</b> "
        "nos posiciona como referentes en materiales absorbentes de alta eficiencia.", SS))
    els.append(Spacer(1,3*mm))
    
    # About images from pages 2
    about_imgs = []
    for iname in ['p02_img1.jpeg','p02_img2.jpeg','p02_img3.jpeg']:
        about_imgs.append([safe_img(iname, 55*mm, 35*mm)])
    ait = Table([r for r in zip(*[about_imgs[0],about_imgs[1],about_imgs[2]])], colWidths=[59*mm,59*mm,59*mm])
    ait.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('BOX',(0,0),(-1,-1),1,TEAL),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
    els.append(ait)
    els.append(Spacer(1,5*mm))
    
    # Info cards
    info = [[Paragraph('<font color="#2E8B98"><b>Sede Central</b></font><br/><font size="8">San Luis 657 (E)<br/>San Juan, Argentina</font>', S('i',9,align=TA_CENTER,lead=12)),
             Paragraph('<font color="#2E8B98"><b>Contacto</b></font><br/><font size="8">+54 9 264 411 5967<br/>mario.ortiz@absorbpad.com</font>', S('i2',9,align=TA_CENTER,lead=12)),
             Paragraph('<font color="#2E8B98"><b>Certificaciones</b></font><br/><font size="8">ASTM F726 / ISO 14001</font>', S('i3',9,align=TA_CENTER,lead=12))]]
    it = Table(info, colWidths=[59*mm,59*mm,59*mm], rowHeights=[20*mm])
    it.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),TEAL_LT),('BOX',(0,0),(-1,-1),1,TEAL),
        ('INNERGRID',(0,0),(-1,-1),0.5,BDR),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER')]))
    els.append(it)
    els.append(PageBreak())
    
    # ===== INDEX =====
    els.extend(section_hdr("Indice",""))
    idx = [("Trabas anaerobicas para piezas mecanicas","4",RED_S),
           ("Adhesivos instantaneos cianoacrilatos","12",TEAL),
           ("Selladores y Adhesivos (SILOC)","16",BLUE_S),
           ("Adhesivos y productos consumo (Pegamil)","28",ORANGE_S),
           ("Lubricantes, limpiadores y grasas","30",GREEN_S),
           ("Limpiamanos Fast Orange","35",TEAL_DK),
           ("Mantenimiento del automotor","36",DARK)]
    id_data = []
    for t,p,clr in idx:
        id_data.append([Paragraph(f'<font color="#{clr.hexval()[2:]}">&#9632;</font>', S('x',12,align=TA_CENTER)),
                        Paragraph(f'<font size="10">{t}</font>', S('x2',10,lead=13)),
                        Paragraph(f'<font size="10" color="#2E8B98"><b>Pag. {p}</b></font>', S('x3',10,align=TA_RIGHT))])
    idt = Table(id_data, colWidths=[12*mm,130*mm,36*mm], rowHeights=[11*mm]*len(id_data))
    idt.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LINEBELOW',(0,0),(-1,-1),0.5,BDR)]))
    els.append(idt)
    els.append(PageBreak())
    
    # ===== TRABAS ANAEROBICAS INTRO (page 4-5) =====
    els.append(banner("Trabas Anaerobicas","Para piezas mecanicas - Series Roja, Verde y Azul",TEAL_DK))
    els.append(Spacer(1,4*mm))
    
    # Full page image from page 4
    els.append(safe_img('p04_img1.jpeg', 160*mm, 200*mm))
    els.append(PageBreak())
    
    # Page 5 intro text + image
    els.extend(section_hdr("Interpretacion de las Siglas",""))
    els.append(Paragraph(
        "Las trabas anaerobicas previenen el desgaste. Las superficies de las piezas mecanicas son rugosas; "
        "el contacto entre las partes nunca es del 100%. Es sobre estas crestas que trabajan los choques y vibraciones, "
        "generando desgastes que provocan holguras. Las trabas no se contraen durante la cura, ocupan totalmente "
        "el espacio libre, impidiendo el desgaste. Resisten temperaturas entre -50C y +150C (VA3 hasta +220C).", SS))
    els.append(Spacer(1,2*mm))
    els.append(safe_img('p05_img1.jpeg', 80*mm, 110*mm))
    els.append(Spacer(1,2*mm))
    els.append(Paragraph(
        "<b>R</b> = Serie Roja (roscas) | <b>V</b> = Serie Verde (cilindros) | <b>A</b> = Serie Azul (sellado)<br/>"
        "<b>B</b> = Baja resist. | <b>M</b> = Media resist. | <b>A</b> = Alta resist.<br/>"
        "<b>1</b> = Holgura min (0.15mm) | <b>2</b> = Media (0.25mm) | <b>3</b> = Max (0.50mm) | <b>4</b> = Max (0.60mm)", BD))
    els.append(PageBreak())
    
    # ===== SERIE ROJA (page 6) =====
    els.extend(section_hdr("Serie Roja - Trabado de Roscas",
        "Evita aflojamientos, desgaste y oxidacion de roscas. Transforma tuercas comunes en tuercas de seguridad.",RED_S))
    
    # Product images row
    prod_imgs_r = Table(
        [[safe_img('p06_img1.jpeg',35*mm,20*mm), safe_img('p06_img2.jpeg',35*mm,25*mm),
          safe_img('p06_img3.jpeg',35*mm,25*mm), safe_img('p06_img4.jpeg',40*mm,26*mm)]],
        colWidths=[44*mm,44*mm,44*mm,44*mm])
    prod_imgs_r.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(prod_imgs_r)
    els.append(Spacer(1,3*mm))
    
    hr = ['PROD','PRES.\nCODIGO','IMG','T. CURA','TORQUE\nN.m','VISC.\n(mPa.s)','HOLG.\nmm','APLICACION']
    rr = [
        ['RB1','50g\n300001',safe_img('p06_img5.jpeg',12*mm,30*mm),'P:10-30min\nT:6h','Q:8-14\nR:1.5-6','Liq.\ntixo.','0.12',
         'TORQUE BAJO\nTornilleria peq. diametro'],
        ['RM1','6/15/50/250g\n300057/03/04/05',safe_img('p06_img6.jpeg',12*mm,30*mm),'P:10-30min\nT:6h','Q:11-20\nR:10-18','Liq.\ntixo.\n600','0.14',
         'TORQUE MEDIO\nDiam. medio, desarme con herram. comunes'],
        ['RA2','15/50/250g\n300006/07/08',safe_img('p06_img7.jpeg',12*mm,30*mm),'P:5-20min\nT:4h','Q:20-35\nR:15-30','Liquido','0.22',
         'TORQUE ALTO\nEsparragos o tornilleria gran diam.(+10mm)'],
        ['RA3','6/15/50/250g\n300058/09/10/11',safe_img('p06_img8.jpeg',12*mm,30*mm),'P:5-20min\nT:6h','Q:30-45\nR:25-40','Liq.visc.\n7000','0.45',
         'TORQUE ALTO - Desgaste\nAprobado IGA N1573-01'],
    ]
    els.append(ptable(hr, rr, RED_S))
    els.append(Paragraph("Resist. temp: -50C a +150C. Valores en probetas acero dulce M10.", FN))
    els.append(PageBreak())
    
    # ===== SERIE VERDE (page 7) =====
    els.extend(section_hdr("Serie Verde - Fijacion de Piezas Cilindricas",
        "Previene desgaste en piezas nuevas, simplifica mecanizados. Permite eliminar anillos seeger, espinas, pasadores.",GREEN_S))
    
    prod_imgs_v = Table(
        [[safe_img('p07_img5.jpeg',40*mm,24*mm)]],
        colWidths=[178*mm])
    prod_imgs_v.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER')]))
    els.append(prod_imgs_v)
    els.append(Spacer(1,3*mm))
    
    hv = ['PROD','PRES.\nCODIGO','IMG','T. CURA','R.AXIAL\nMPa','VISC.\n(mPa.s)','HOLG.\nmm','APLICACION']
    rv = [
        ['VB1','6/15/50g\n300059/15/16',safe_img('p07_img1.jpeg',12*mm,30*mm),'P:15-30min\nT:6h','10-15','Liq.\n150','0.12',
         'FACIL DESARME - Holg. baja\nPiezas cilindricas, desarme cuidadoso'],
        ['VA1','50/250g\n300018/19',safe_img('p07_img2.jpeg',12*mm,30*mm),'P:10-30min\nT:6h','20-35','Liq.\n150','0.12',
         'ALTA RESIST. - Holg. minima\nMontajes deslizamiento holg. min.'],
        ['VA2','15/50/250g\n300020/21/22',safe_img('p07_img3.jpeg',12*mm,30*mm),'P:5-30min\nT:4h','25-35','Liq.visc.\n1200','0.20',
         'ALTA RESIST. - Holg. media\nMontajes deslizamiento holg. media'],
        ['VA3','6/15/50/250g\n300060/23/24/25',safe_img('p07_img4.jpeg',12*mm,30*mm),'P:10-30min\nT:6h','25-35','Liq.\ntixo.','0.26',
         'ALTA RESIST. - Holg. maxima\nSoporta hasta +220C'],
    ]
    els.append(ptable(hv, rv, GREEN_S))
    els.append(Paragraph("Resist. temp: -50C a +150C (VA3 hasta +220C). Probetas 12.7mm diam.", FN))
    els.append(PageBreak())
    
    # ===== SERIE AZUL - Sellado Conexiones (page 8) =====
    els.extend(section_hdr("Serie Azul - Sellado de Conexiones",
        "Sellado efectivo de combustibles, lubricantes, fluidos hidraulicos, aire, agua y quimicos. Sustituyen cinta PTFE.",BLUE_S))
    
    prod_imgs_a = Table(
        [[safe_img('p08_img6.jpeg',40*mm,24*mm)]],
        colWidths=[178*mm])
    prod_imgs_a.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER')]))
    els.append(prod_imgs_a)
    els.append(Spacer(1,2*mm))
    
    ha = ['PROD','PRES.\nCODIGO','IMG','T.CURA','TORQUE\nN.m','VISC/HOLG','APLICACION']
    ra = [
        ['AB3','250g\n300034',safe_img('p08_img1.jpeg',12*mm,14*mm),'P:20-40min\nT:20h','Q:4-7\nR:1-4','Gel\n0.50mm',
         'PARA GRANDES DIAM.(hasta 4")\nAprobado IGA N1573-03'],
        ['AM2','50/250g\n300029/30',safe_img('p08_img2.jpeg',12*mm,14*mm),'P:20-40min\nT:18h','Q:7-11\nR:4-8','Liq.tixo.\n0.30mm',
         'USO GENERAL\nHidraulica y neumatica. IGA N1573-02'],
        ['AM2.5','250g\n300328',safe_img('p08_img3.jpeg',12*mm,14*mm),'P:20-40min\nT:10h','Q:10-25\nR:1-6','Liq.tixo.\n0.50mm',
         'CURA RAPIDA\nFormar juntas y sellar. IGA N1573-08'],
        ['AM3','6/50/250g\n300062/35/36/37',safe_img('p08_img4.jpeg',12*mm,14*mm),'P:100-130min\nT:36h','Q:4-10\nR:1-6','Pasta\n0.50mm',
         'SELLADOR CON PTFE\nConex. hidraul/neumat. IGA N1573-04'],
        ['AA3','50/250g\n300039/40',safe_img('p08_img5.jpeg',12*mm,14*mm),'P:15-30min\nT:18h','Q:10-25\nR:11-25','Gel\n0.50mm',
         'PRESIONES MAXIMAS\nSellador conexiones presion max.'],
    ]
    els.append(ptable(ha, ra, BLUE_S))
    els.append(PageBreak())
    
    # ===== SERIE AZUL - Formacion Juntas (page 9) =====
    els.extend(section_hdr("Serie Azul - Formacion de Juntas / Sellado Porosidades",
        "Para juntas de espesor cero en superficies metalicas mecanizadas. Gran resistencia quimica y mecanica.",BLUE_S))
    
    prod_imgs_j = Table(
        [[safe_img('p09_img4.jpeg',40*mm,24*mm), safe_img('p09_img5.jpeg',45*mm,28*mm), safe_img('p09_img6.jpeg',45*mm,28*mm)]],
        colWidths=[55*mm,60*mm,60*mm])
    prod_imgs_j.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(prod_imgs_j)
    els.append(Spacer(1,2*mm))
    
    hj = ['PROD','PRES.\nCODIGO','IMG','T.CURA','TORQUE\nN.m','VISC/HOLG','APLICACION']
    rj = [
        ['AA2','50g\n300042',safe_img('p09_img1.jpeg',12*mm,14*mm),'P:20-30min\nT:24h','Q:7.5-15\nR:8-15','Gel-15\n0.25mm',
         'USO GENERAL\nFundicion hierro/aluminio. Altas presiones.'],
        ['AA4','50g\n300045',safe_img('p09_img2.jpeg',12*mm,14*mm),'P:20-30min\nT:12h','Q:7.5-17\nR:9-17','Pasta\n0.30mm',
         'GRANDES HOLGURAS\nElevada consistencia. No escurre vertical.'],
        ['AA1','50g\n300048',safe_img('p09_img3.jpeg',12*mm,14*mm),'P:10-15min\nT:4h','Q:8-20\nR:15-30','Liq.\n0.07mm',
         'FISURAS Y POROSIDADES\nActua por capilaridad.'],
    ]
    els.append(ptable(hj, rj, BLUE_S))
    els.append(PageBreak())
    
    # ===== GAS + NARANJA + AUXILIARES (page 10) =====
    els.extend(section_hdr("Selladores Anaerobicos para Gas",
        "Maxima seguridad. Las conexiones se transforman en un cuerpo unico. Aprobado IGA N1573-1.",TEAL))
    
    gas_imgs = Table([[safe_img('p10_img2.jpeg',50*mm,33*mm)]],colWidths=[178*mm])
    gas_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER')]))
    els.append(gas_imgs)
    els.append(Spacer(1,2*mm))
    
    gd = [[Paragraph('<b>GAS</b>',S('g',9,white,True,TA_CENTER)),
           safe_img('p10_img1.jpeg',10*mm,25*mm),
           Paragraph('15g/50g\n300054/300055',S('g2',8,align=TA_CENTER)),
           Paragraph('Para instalaciones domiciliarias hasta 4 Bar.\nNo requiere mezclas. Sin solventes. No toxico.\nAhorra mano de obra.',S('g3',8,lead=11))]]
    gt = Table(gd, colWidths=[25*mm,18*mm,35*mm,100*mm])
    gt.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),TEAL),('BACKGROUND',(1,0),(-1,0),TEAL_LT),
        ('BOX',(0,0),(-1,-1),1,TEAL),('INNERGRID',(0,0),(-1,-1),0.5,BDR),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(gt)
    els.append(Spacer(1,3*mm))
    
    # Tabla consumo gas
    gc = [['1/2"','30','100'],['3/4"','20','75'],['1"','15','50']]
    els.append(ptable(['DIAM.','APLIC. 15g','APLIC. 50g'], gc, TEAL, [40*mm,60*mm,78*mm]))
    els.append(Spacer(1,5*mm))
    
    # Serie Naranja
    els.extend(section_hdr("Serie Naranja - Adhesivos Estructurales",
        "Para vidrio-vidrio, metal-metal, vidrio-metal y marmoles.",ORANGE_S))
    
    naranja_imgs = Table([[safe_img('p10_img3.jpeg',18*mm,33*mm),safe_img('p10_img6.jpeg',12*mm,30*mm),safe_img('p10_img7.jpeg',14*mm,33*mm)]],
        colWidths=[55*mm,55*mm,68*mm])
    naranja_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(naranja_imgs)
    els.append(Spacer(1,2*mm))
    
    hn = ['PROD','PRES.','VISC/HOLG','RESIST.','APLICACION']
    rn = [
        ['NP3','50g+Activ.N 240cm3\n300051/300408','Liq.visc.11000\n0.50mm','P:3-5min\nT:3h\nSupera resist. vidrio',
         'MATERIALES RIGIDOS\nVidrio-vidrio, metal-metal.\nRequiere Activador N.'],
        ['NR2','50g\n300050','Liq.visc.1200\n0.25mm','P:20-30min\nT:3h\n8-12 MPa',
         'CURADO UV\nVidrio-vidrio, vidrio-metal.\nRequiere material transparente a UV.'],
    ]
    els.append(ptable(hn, rn, ORANGE_S))
    els.append(Spacer(1,3*mm))
    
    # Auxiliares
    aux = [[Paragraph('<b>ACTIVADOR T</b>',S('a1',8,white,True,TA_CENTER)),Paragraph('240cm3 - 300409',S('a2',8,align=TA_CENTER)),
            Paragraph('Optimiza aplicacion en superficies inactivas (plasticos, inox, zincados, cromados). Temp &lt;+6C.',S('a3',8,lead=10))],
           [Paragraph('<b>LIMPIADOR L</b>',S('a4',8,white,True,TA_CENTER)),Paragraph('240cm3 - 300410',S('a5',8,align=TA_CENTER)),
            Paragraph('Disuelve y desplaza grasas y aceites sin dejar residuos. Preparacion de superficies.',S('a6',8,lead=10))]]
    at = Table(aux, colWidths=[35*mm,35*mm,108*mm])
    at.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),TEAL_DK),('BACKGROUND',(1,0),(-1,-1),TEAL_LT),
        ('BOX',(0,0),(-1,-1),1,TEAL_DK),('INNERGRID',(0,0),(-1,-1),0.5,BDR),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(at)
    els.append(PageBreak())
    
    # ===== GUIA DE APLICACIONES (page 11) =====
    els.extend(section_hdr("Guia de Aplicaciones Anaerobicas",""))
    els.append(safe_img('p11_img1.jpeg', 140*mm, 210*mm))
    els.append(PageBreak())
    
    # ===== CIANOACRILATOS (pages 12-15) =====
    els.append(banner("Adhesivos Instantaneos","Cianoacrilatos - Linea de pegado rapido industrial",TEAL))
    els.append(Spacer(1,3*mm))
    
    # Full page image from page 12
    els.append(safe_img('p12_img1.jpeg', 150*mm, 200*mm))
    els.append(PageBreak())
    
    # Page 13 intro
    els.extend(section_hdr("Cianoacrilatos CIANO",
        "Adhesivos que en pocos segundos unen fuertemente gran variedad de materiales. "
        "Monocomponentes, curan por humedad ambiente. Adhieren caucho, metales, ceramica, madera y plasticos. "
        "Soportan temperaturas de hasta +80C.",TEAL))
    els.append(safe_img('p13_img1.jpeg', 50*mm, 70*mm))
    els.append(PageBreak())
    
    # Page 14 - Serie Clasica
    els.extend(section_hdr("Serie Clasica - Cianoacrilatos","",TEAL))
    
    prod_imgs_c = Table(
        [[safe_img('p14_img1.jpeg',40*mm,24*mm)]],
        colWidths=[178*mm])
    prod_imgs_c.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER')]))
    els.append(prod_imgs_c)
    els.append(Spacer(1,2*mm))
    
    hc = ['PROD','PRES.\nCODIGO','IMG','VISC.\n(mPa.s)','HOLG.\nmm','T.FIJAC.','RESIST.\nMPa','APLICACION']
    rc = [
        ['CB1','20g\n200001',safe_img('p14_img7.jpeg',8*mm,20*mm),'5','0.05','Max 6s\nMax 6s','20-30',
         'PENETRANTE\nUltra rapido, lineas de montaje.\nPor capilaridad.'],
        ['CM1','20/100/1000g\n200004/05/06',safe_img('p14_img2.jpeg',10*mm,25*mm),'40','0.08','Max 6/8/10s','20-30',
         'USO GENERAL - Alta velocidad\nCauchos, plasticos, ceramica, metales, cueros.'],
        ['CM2','20/100/1000g\n200007/08/09',safe_img('p14_img3.jpeg',10*mm,25*mm),'100','0.10','Max 8/10/20s','20-30',
         'USO GENERAL - Media viscosidad\nSuperficies rugosas, mayor holgura.'],
        ['CA3','20/100g\n200010/11',safe_img('p14_img4.jpeg',10*mm,12*mm),'1500','0.25','Max 20/25s','12-20',
         'HOLGURAS GRANDES\nGel. No escurre en sup. verticales.'],
        ['CG4','10/300g\n200000/117',safe_img('p14_img5.jpeg',10*mm,25*mm),'Gel','0.40','Max 30/25s','10-15',
         'PARA GOMAS\nCaucho natural y sintetico.\nGran flexibilidad.'],
    ]
    els.append(ptable(hc, rc, TEAL))
    els.append(PageBreak())
    
    # Page 15 - Serie Dosmil
    els.extend(section_hdr("Serie Dosmil - Cianoacrilatos",
        "Formulaciones especiales para sustratos dificiles como EPDM y superficies porosas.",TEAL))
    
    hc2 = ['PROD','PRES.\nCODIGO','IMG','VISC.','HOLG.','T.FIJAC.','RESIST.','APLICACION']
    rc2 = [
        ['2100','20/1000g\n200016/37',safe_img('p15_img3.jpeg',10*mm,25*mm),'20','0.08','Max 6s','15-20',
         'PARA GOMAS Y PLASTICOS\nEPDM y Santoprene.'],
        ['2200','20/100g\n200019/20',safe_img('p15_img4.jpeg',10*mm,25*mm),'100','0.10','Max 6/12s','20-25',
         'PARA SUPERFICIES POROSAS\nMadera, fibras vegetales, carton, ceramica.'],
    ]
    els.append(ptable(hc2, rc2, TEAL))
    els.append(Spacer(1,3*mm))
    
    els.append(Paragraph("<b>ACTIVADOR:</b> Acelera tiempos de cura. Permite trabajar con grandes holguras y superficies "
        "porosas e irregulares. Previene el esfumado blanco.", BD))
    els.append(PageBreak())
    
    # ===== SILOC - SELLADORES Y ADHESIVOS (pages 16-28) =====
    els.append(banner("Selladores y Adhesivos SILOC","Siliconas, Hibridos, Poliuretanos y otros productos",BLUE_S))
    els.append(Spacer(1,3*mm))
    
    # Page 16 full image
    els.append(safe_img('p16_img1.jpeg', 160*mm, 150*mm))
    els.append(Spacer(1,3*mm))
    els.append(Paragraph(
        "SILOC es la marca de selladores y adhesivos, garantia de calidad, variedad e innovacion. "
        "Su amplia linea cubre los requerimientos de diversas industrias y mercados.", SS))
    els.append(PageBreak())
    
    # Siliconas Aceticas (page 18)
    els.extend(section_hdr("Siliconas Aceticas",
        "Uso universal. Fuerte, flexible, inalterable. Resiste al agua, intemperie y UV.",BLUE_S))
    
    sil_a_imgs = Table([[safe_img('p18_img1.jpeg',12*mm,40*mm), safe_img('p18_img2.jpeg',45*mm,58*mm),
                          safe_img('p18_img3.jpeg',22*mm,44*mm), safe_img('p18_img4.jpeg',40*mm,43*mm)]],
        colWidths=[30*mm,55*mm,35*mm,58*mm])
    sil_a_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(sil_a_imgs)
    els.append(Spacer(1,2*mm))
    
    hsa = ['PRODUCTO','PRESENTACION','TEMP.','APLICACION']
    rsa = [
        ['Adhesivo Sellador\nTransparente','25/100/280g\n400033/037/569','-40 a +180C','USO UNIVERSAL\nVidrio, superficies vitrificadas, esmaltadas. Aislante electrico.'],
        ['Adhesivo Sellador\nBlanco','25/100/280g\n400034/038/568','-40 a +180C','USO UNIVERSAL\nPara banos, cocinas, cerramientos.'],
        ['Adhesivo Sellador\nNegro','25/100/280g\n400035/039/571','-40 a +180C','USO UNIVERSAL\nAlta resistencia. Para automotriz.'],
        ['100% Silicona\nIndustrial Transp.','280g - 400528','-40 a +180C','LINEA INDUSTRIAL\nMayor rendimiento y calidad constante.'],
        ['100% Silicona\nIndustrial Blanco','280g - 400527','-40 a +180C','LINEA INDUSTRIAL\nAnti hongos.'],
        ['100% Silicona\nIndustrial Negro','280g - 400526','-40 a +180C','LINEA INDUSTRIAL\nAlta temperatura.'],
    ]
    els.append(ptable(hsa, rsa, BLUE_S))
    els.append(PageBreak())
    
    # Siliconas Neutras (page 19)
    els.extend(section_hdr("Siliconas Neutras",
        "Para construccion, policarbonato, aberturas plasticas y espejos. No ataca laminas reflectantes.",BLUE_S))
    
    sil_n_imgs = Table([[safe_img('p19_img1.jpeg',25*mm,35*mm), safe_img('p19_img2.jpeg',20*mm,32*mm),
                          safe_img('p19_img5.jpeg',45*mm,37*mm)]],
        colWidths=[50*mm,45*mm,83*mm])
    sil_n_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(sil_n_imgs)
    els.append(Spacer(1,2*mm))
    
    hsn = ['PRODUCTO','PRESENTACION','TEMP.','APLICACION']
    rsn = [
        ['Silicona Neutra\nTransparente','100/280g\n400041/572','-40 a +180C','PARA LA CONSTRUCCION\nHormigon, mamposteria, ceramicos, vidrio.'],
        ['100% Sil. Neutra\nIndustrial Transp.','280g - 400522','-40 a +180C','LINEA INDUSTRIAL\nPolicarbonato, aberturas plasticas.'],
        ['100% Sil. Neutra\nIndustrial Blanco','280g - 400521','-40 a +180C','LINEA INDUSTRIAL\nEspejos, no ataca lamina reflectante.'],
        ['100% Sil. Neutra\nIndustrial Negro','280g - 400520','-40 a +150C','LINEA INDUSTRIAL\nAutomotriz, alta resistencia.'],
    ]
    els.append(ptable(hsn, rsn, BLUE_S))
    els.append(PageBreak())
    
    # Siliconas Oximicas + Altas Temp (page 20)
    els.extend(section_hdr("Siliconas Oximicas / Altas Temperaturas",
        "Para formar juntas en motores de combustion, reductores, equipos hidraulicos. Cumple normas MIL, NSF, USDA.",BLUE_S))
    
    sil_o_imgs = Table([[safe_img('p20_img1.jpeg',38*mm,42*mm), safe_img('p20_img3.jpeg',25*mm,44*mm), safe_img('p20_img4.jpeg',25*mm,43*mm)]],
        colWidths=[55*mm,60*mm,63*mm])
    sil_o_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(sil_o_imgs)
    els.append(Spacer(1,2*mm))
    
    hso = ['PRODUCTO','PRESENTACION','TEMP.','APLICACION']
    rso = [
        ['Silicona\nAltas Temp.\nRojo','25/100/280g\n400036/040/570','-60 a +260C','FORMAJUNTAS\nCajas engranajes, diferenciales, motores combustion.\nResiste aceites, lubricantes, liq. frenos.'],
        ['8500\nFormajuntas\nGris','70/85g\n100283/285','-62 a +260C','FORMAJUNTAS RTV 100% SILICONA\nSustituye juntas papel, corcho y fibra.\nResiste aceites y combustibles.'],
        ['8600\nFormajuntas\nNegro','70/85g\n100295/297','-62 a +260C','FORMAJUNTAS NEGRO\nCarter y tapas embrague.\nExcelente resistencia a aceites.'],
    ]
    els.append(ptable(hso, rso, BLUE_S))
    els.append(PageBreak())
    
    # Hibridos (page 21)
    els.extend(section_hdr("Adhesivos Selladores Hibridos",
        "Alto agarre inicial y excelente adherencia sobre amplia variedad de materiales lisos o porosos.",TEAL))
    
    hyb_imgs = Table([[safe_img('p21_img1.jpeg',30*mm,45*mm), safe_img('p21_img4.jpeg',48*mm,32*mm), safe_img('p21_img6.png',28*mm,46*mm)]],
        colWidths=[50*mm,70*mm,58*mm])
    hyb_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(hyb_imgs)
    els.append(Spacer(1,2*mm))
    
    hhy = ['PRODUCTO','PRESENTACION','TEMP.','APLICACION']
    rhy = [
        ['TH Construccion\nBlanco','450g - 400626','-40 a +90C','PARA LA CONSTRUCCION\nCemento, marmol, ceramicos, madera, vidrio, espejos.\nNo oxida. Resiste UV e intemperie. Pintable.'],
        ['TH Metales\nGris','450g - 400640','-40 a +90C','PARA METALES\nChapas galvanizadas, aluminio, canaletas, zingueria.\nPintable. No causa oxidacion.'],
    ]
    els.append(ptable(hhy, rhy, TEAL))
    els.append(PageBreak())
    
    # Poliuretanos (page 22)
    els.extend(section_hdr("Selladores de Poliuretano",
        "Maxima elasticidad y adherencia. Para juntas de dilatacion, grietas, techos, fachadas.",TEAL_DK))
    
    pu_imgs = Table([[safe_img('p22_img1.jpeg',38*mm,48*mm), safe_img('p22_img2.jpeg',38*mm,48*mm), 
                       safe_img('p22_img3.jpeg',50*mm,38*mm)]],
        colWidths=[55*mm,55*mm,68*mm])
    pu_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(pu_imgs)
    els.append(Spacer(1,2*mm))
    
    hpu = ['PRODUCTO','PRESENTACION','TEMP.','APLICACION']
    rpu = [
        ['PU 38\nGris/Blanco','300/600ml\n400054/56/67/69','-40 a +80C','PARA CONSTRUCCION\nJuntas dilatacion, grietas, techos, fachadas.\nMaxima elasticidad (+/-25%).'],
        ['PU 44\nGris/Negro','300/400/600ml\n400059-64','-40 a +90C','PARA LA INDUSTRIA\nUso general industrial. Alta adherencia.\nResiste quimicos y solventes.'],
        ['PU 52','310ml - 100352','-40 a +90C','PEGADO DE PARABRISAS\nAdhesivo estructural alta resistencia mecanica.'],
        ['PU 55','300ml - 100355','-40 a +90C','MULTIUSO\nPega y sella hormigon, ladrillo, madera, metal.'],
    ]
    els.append(ptable(hpu, rpu, TEAL_DK))
    els.append(PageBreak())
    
    # Espuma PU + Acrilicos (page 23)
    els.extend(section_hdr("Espuma de Poliuretano / Sellador Acrilico",
        "Rellena huecos, aisla termica y acusticamente. Pintable y lijable.",TEAL_DK))
    
    foam_imgs = Table([[safe_img('p23_img1.jpeg',25*mm,33*mm),safe_img('p23_img2.jpeg',28*mm,34*mm),
                         safe_img('p23_img3.jpeg',25*mm,33*mm),safe_img('p23_img4.jpeg',45*mm,34*mm)]],
        colWidths=[38*mm,42*mm,38*mm,60*mm])
    foam_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(foam_imgs)
    els.append(Spacer(1,2*mm))
    
    hf = ['PRODUCTO','PRESENTACION','APLICACION']
    rf = [
        ['Espuma PU\n300/500/750ml','400073/74/76','ESPUMA EXPANDIBLE\nRellena huecos, aisla termicamente.\nPintable, lijable. Excelente adherencia.'],
        ['Sellador Acrilico\nBlanco/Roble/Cedro','280g\n400080/82/83/84','SELLADOR PARA INTERIORES\nPara grietas, fisuras, juntas en paredes.\nPintable. Interior/exterior.'],
        ['Sellador Acrilico\nPara Madera','280g - 400085','PARA CARPINTERIA\nRellenar juntas y grietas en marcos, puertas.\nBuena adherencia sobre madera.'],
    ]
    els.append(ptable(hf, rf, TEAL_DK))
    els.append(PageBreak())
    
    # Otros productos SILOC (pages 24-26)
    els.extend(section_hdr("Adhesivos SILOC - Multiuso",
        "Linea completa de adhesivos de contacto, cianoacrilatos de consumo y selladores especiales.",BLUE_S))
    
    misc_imgs = Table([[safe_img('p24_img1.jpeg',40*mm,27*mm), safe_img('p24_img2.jpeg',55*mm,57*mm), safe_img('p24_img7.jpeg',40*mm,60*mm)]],
        colWidths=[55*mm,68*mm,55*mm])
    misc_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(misc_imgs)
    els.append(Spacer(1,2*mm))
    
    hm = ['PRODUCTO','PRESENTACION','APLICACION']
    rm = [
        ['Adhesivo Contacto','125/250/500ml/1L/4L\n400090-400095','ADHESIVO DE CONTACTO\nPara madera, formica, corcho, tela, alfombras, goma, cuero.'],
        ['Cianoacrilato Gel\n5g','400100','PEGAMENTO INSTANTANEO GEL\nNo escurre. Para plasticos, gomas, ceramica, metales.'],
        ['Cianoacrilato\nLiquido 5g','400101','PEGAMENTO INSTANTANEO LIQUIDO\nPara superficies lisas, pegado por capilaridad.'],
        ['Cinta Doble Faz\nTransparente','400146','CINTA DE MONTAJE\nPara fijar espejos, accesorios de bano, portarretratos.'],
    ]
    els.append(ptable(hm, rm, BLUE_S))
    els.append(PageBreak())
    
    # Epoxi + Selladores especiales (pages 25-27)
    els.extend(section_hdr("Adhesivos Epoxi y Selladores Especiales",
        "Adhesivos de dos componentes de alta resistencia. Acero en pasta.",ORANGE_S))
    
    epoxi_imgs = Table([[safe_img('p25_img1.jpeg',40*mm,32*mm),safe_img('p25_img2.jpeg',38*mm,30*mm),
                          safe_img('p25_img3.jpeg',38*mm,30*mm),safe_img('p25_img4.jpeg',38*mm,30*mm)]],
        colWidths=[48*mm,43*mm,43*mm,43*mm])
    epoxi_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(epoxi_imgs)
    els.append(Spacer(1,2*mm))
    
    he = ['PRODUCTO','PRESENTACION','RESIST.TEMP.','APLICACION']
    re = [
        ['Epoxi Transp. 5min','Blister/Estuche 14ml\n100430/431','-10 a +120C','Vidrio, metal, ceramica, madera. Curado 5min.\nTransparente, fuerte, mecanizable.'],
        ['Epoxi Gris Acero 10min','Blister/Estuche 14ml\n100432/433','-10 a +180C','Todos los materiales. Gris acero.\nSe puede lijar, limar, taladrar, tornear.'],
        ['Acero en Pasta\n21g','Blister/Estuche\n100434/435','-10 a +180C','Adhiere, suelda, rellena, sella.\nResiste bajo el agua. Mecanizable.'],
        ['Acero en Pasta\n200g','400556','-10 a +180C','VERSION INDUSTRIAL\nContiene acero en polvo. Reconstruye faltantes de piezas.\nFija anclajes y empotrados.'],
        ['Sellador Sintetico\nMarfil','100/310g\n400050/518','-','SELLADOR SINTETICO PINTABLE\nCarrocerias, chapas, aluminio.\nResiste UV e inmersion en agua.'],
    ]
    els.append(ptable(he, re, ORANGE_S))
    els.append(PageBreak())
    
    # Pistolas aplicadoras (page 28)
    els.extend(section_hdr("Pistolas Aplicadoras",
        "Pistolas mecanicas y neumaticas para cartuchos y unipacks.",BLUE_S))
    
    gun_imgs = Table([[safe_img('p28_img1.jpeg',28*mm,12*mm),safe_img('p28_img2.jpeg',24*mm,14*mm),
                        safe_img('p28_img3.jpeg',24*mm,14*mm),safe_img('p28_img4.jpeg',28*mm,14*mm)]],
        colWidths=[44*mm,44*mm,44*mm,44*mm])
    gun_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(gun_imgs)
    els.append(Spacer(1,2*mm))
    
    hg = ['PRODUCTO','CODIGO','APLICACION']
    rg = [
        ['M-300','400489','Mecanica. Para cartuchos.'],
        ['M-300 Premium','400486','Mecanica Premium. Para cartuchos.'],
        ['M-400/M-600*','400490','Mecanica. Para unipacks 400/310ml y cartuchos.'],
        ['N-600*','400491/400110','Mecanica y Neumatica. Para unipacks 600/400/310ml.'],
    ]
    els.append(ptable(hg, rg, BLUE_S, [35*mm,35*mm,108*mm]))
    els.append(Spacer(1,2*mm))
    
    # Additional SILOC products on page 28
    hsil2 = ['PRODUCTO','PRESENTACION','APLICACION']
    rsil2 = [
        ['Silicona Neutra\n/ TH Construccion','Varias pres.','Para pegar espejos, sellado carpinteria PVC y policarbonato.'],
        ['Espuma PU','300/500/750ml','Relleno de huecos, aislacion termica y acustica.'],
        ['Sellador Acrilico','280g','Sellado de grietas en interiores.'],
        ['SILOC PU38','300ml','Formacion de juntas de dilatacion.'],
        ['Grasa Litio Blanca','Aerosol','Lubricacion de correderas guia portones.'],
    ]
    els.append(ptable(hsil2, rsil2, BLUE_S))
    els.append(PageBreak())
    
    # ===== PEGAMIL - CONSUMO (pages 29, 33-36) =====
    els.append(banner("Productos de Consumo - Pegamil","Adhesivos y productos para reparaciones en hogar, taller y oficina",ORANGE_S))
    els.append(Spacer(1,3*mm))
    
    # Page 29 full image
    els.append(safe_img('p29_img1.jpeg', 150*mm, 200*mm))
    els.append(PageBreak())
    
    # Page 33 full image  
    els.append(safe_img('p33_img1.jpeg', 150*mm, 200*mm))
    els.append(PageBreak())
    
    # Pages 34-36 - Consumer products
    els.extend(section_hdr("Linea Pegamil - Adhesivos de Consumo",
        "Completa linea para resolver problemas de mantenimiento y reparaciones en hogar, taller y oficina.",ORANGE_S))
    
    peg_imgs = Table([[safe_img('p34_img1.jpeg',45*mm,30*mm),safe_img('p34_img2.jpeg',34*mm,36*mm),safe_img('p34_img3.jpeg',34*mm,36*mm)]],
        colWidths=[60*mm,55*mm,63*mm])
    peg_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(peg_imgs)
    els.append(Spacer(1,2*mm))
    
    hp = ['PRODUCTO','PRESENTACION','APLICACION']
    rp = [
        ['Adhesivo Instantaneo\nGel 2ml','Blister/Estuche\n100410/408/409','Cianoacrilato. Pega en segundos plasticos, goma, porcelana,\nmadera, cuero, metales. Sup. lisas y porosas.'],
        ['Repara Calzado\n3g / 8g','Blister/Estuche\n100412/411/450/451','Para todo tipo de calzado: cuero, tela, goma.\nFlexible. Resiste al agua.'],
        ['Adhesivo Epoxi\nTransparente 5min','Blister/Estuche 14ml\n100430/431','Vidrio, metal, ceramica. Curado rapido.\nTransparente, fuerte, mecanizable.'],
        ['Adhesivo Epoxi\nGris Acero 10min','Blister/Estuche 14ml\n100432/433','Todos los materiales. Se puede lijar, taladrar.\nResiste -10C a +180C.'],
        ['Acero en Pasta\n21g','Blister/Estuche\n100434/435/501','Adhiere, suelda, rellena, sella todos los materiales.\nResiste bajo el agua. Mecanizable.'],
        ['Pega Vinilicos\n25/33cm3','Blister/Estuche\n100426/427/460','Juguetes inflables, piletas PVC, manteles, toldos, lonas.\nIncluye parches. Transparente.'],
        ['Pega Tela\n25cm3','Blister/Estuche\n100424/425','Jeans, dobladillos, cierres, tapiceria, carpas, lonas.\nResiste lavados y planchados.'],
        ['Contacto Multiuso\n25cm3','Blister/Estuche\n100417/418','Cuero, laminados, madera, carton, tela, alfombras,\nmetal, lona, goma. Flexible.'],
        ['Adhesivo Madera\n100/250/500g','100440/441/442','Para madera, MDF, aglomerado.\nInterior y exterior. No toxico.'],
    ]
    els.append(ptable(hp, rp, ORANGE_S))
    els.append(PageBreak())
    
    # ===== LUBRICANTES Y LIMPIADORES (pages 30-32) =====
    els.append(banner("Lubricantes, Limpiadores y Grasas","Linea completa de mantenimiento industrial y automotriz",GREEN_S))
    els.append(Spacer(1,3*mm))
    
    # Aceites y penetrantes (page 30)
    els.extend(section_hdr("Aceites Lubricantes y Penetrantes","",GREEN_S))
    
    lub_imgs = Table([[safe_img('p30_img1.jpeg',25*mm,35*mm),safe_img('p30_img2.jpeg',25*mm,35*mm),
                        safe_img('p30_img3.jpeg',25*mm,35*mm),safe_img('p30_img4.jpeg',25*mm,35*mm),safe_img('p30_img5.jpeg',38*mm,57*mm)]],
        colWidths=[32*mm,32*mm,32*mm,32*mm,50*mm])
    lub_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'BOTTOM')]))
    els.append(lub_imgs)
    els.append(Spacer(1,2*mm))
    
    hl = ['PRODUCTO','PRESENTACION','APLICACION']
    rl = [
        ['Lubricante\nMultiuso','168g/250ml - 500000\n288g/426ml - 500050',
         'Lubricante y protector multiprop. con PTFE.\nElimina ruidos, destraba mecanismos, evita corrosion.'],
        ['Afloja Todo','170g/252ml - 500003\n284g/426ml - 500051',
         'Penetrante de accion rapida para liberar piezas\noxidadas, trabadas o agarrotadas.'],
        ['Lubricante\npara Cadenas','170g/225ml - 500020',
         'Para cadenas de motos, bicicletas, maquinaria.\nNo salpica. Larga duracion.'],
        ['Lubricante\nde Siliconas','170g/240ml - 500021',
         'No graso. Para plasticos, gomas, cables.\nRepele humedad. No mancha.'],
    ]
    els.append(ptable(hl, rl, GREEN_S))
    els.append(PageBreak())
    
    # Grasas (page 31)
    els.extend(section_hdr("Grasas Industriales","",GREEN_S))
    
    grasa_imgs = Table([[safe_img('p31_img1.jpeg',65*mm,97*mm), safe_img('p31_img2.jpeg',25*mm,35*mm)]],
        colWidths=[100*mm,78*mm])
    grasa_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(grasa_imgs)
    els.append(Spacer(1,2*mm))
    
    hgr = ['PRODUCTO','PRESENTACION','APLICACION']
    rgr = [
        ['Grasa Litio\nBlanca Aerosol','170g/240ml\n500022',
         'Grado 2. Aceites sinteticos refinados.\nPara rodamientos, ejes, engranajes. -20C a +150C.'],
        ['Grasa Litio\nBlanca 100g','100g - 500080',
         'Alta estabilidad y resistencia.\nPara piezas sometidas a temperatura y presion extrema.'],
        ['Grasa Litio\nBlanca 250g','250g - 500081',
         'Para mecanismos expuestos.\nResiste agua, vapor y productos quimicos.'],
    ]
    els.append(ptable(hgr, rgr, GREEN_S))
    els.append(PageBreak())
    
    # Limpiadores (page 32)
    els.extend(section_hdr("Limpiadores Industriales","",GREEN_S))
    
    limp_imgs = Table([[safe_img('p32_img1.jpeg',42*mm,28*mm),safe_img('p32_img2.jpeg',38*mm,57*mm),safe_img('p32_img7.jpeg',42*mm,63*mm)]],
        colWidths=[55*mm,55*mm,68*mm])
    limp_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(limp_imgs)
    els.append(Spacer(1,2*mm))
    
    hlp = ['PRODUCTO','PRESENTACION','APLICACION']
    rlp = [
        ['Limpia Motores','290g/440ml - 500031','Desengrasante con D-limoneno. Remueve aceite, grasa, carbon.\nNo afecta superficies metalicas, plasticas ni pintadas.'],
        ['Limpia\nCarburadores','300g/426ml - 500093','Limpia sistema carburacion, multiples admision.\nRemove depositos de carbon y residuos.'],
        ['Limpia Cadenas','170g/240ml - 500030','Limpiador especifico para cadenas.\nDisuelve grasa vieja y suciedad acumulada.'],
        ['Limpia Contactos','290g/426ml - 500113','Para bornes bateria y contactos electricos.\nEvaporacion rapida. Sin residuos.'],
    ]
    els.append(ptable(hlp, rlp, GREEN_S))
    els.append(PageBreak())
    
    # ===== LIMPIAMANOS (page 37) =====
    els.extend(section_hdr("Fast Orange - Limpiamanos",
        "Potente limpiamanos con citricos naturales y piedra pomez. Lanolina, glicerina y aloe vera. "
        "Biodegradable. Aprobado ANMAT N17778.",GREEN_S))
    
    fo_imgs = Table([[safe_img('p37_img1.jpeg',100*mm,50*mm)]],colWidths=[178*mm])
    fo_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER')]))
    els.append(fo_imgs)
    els.append(Spacer(1,2*mm))
    
    fo_prod_imgs = Table([[safe_img('p37_img3.jpeg',22*mm,34*mm),safe_img('p37_img4.jpeg',25*mm,30*mm),safe_img('p37_img5.jpeg',12*mm,30*mm)]],
        colWidths=[55*mm,55*mm,68*mm])
    fo_prod_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(fo_prod_imgs)
    els.append(Spacer(1,2*mm))
    
    hfo = ['PRODUCTO','PRESENTACION','APLICACION']
    rfo = [
        ['Fast Orange\n443.5ml','550158','Remueve aceites, grasa, resinas, tinta, epoxis, pintura.\nNo necesita agua. Aroma citrico.'],
        ['Fast Orange\n1.8 Litros','550159','Version economica para talleres y plantas.\nNo contiene amoniaco ni quimicos agresivos.'],
        ['Fast Orange\n3.78 Litros','550160','Presentacion industrial.\nSu uso evita agrietamiento y sequedad de la piel.'],
    ]
    els.append(ptable(hfo, rfo, GREEN_S))
    els.append(PageBreak())
    
    # ===== MANTENIMIENTO AUTOMOTOR (page 38) =====
    els.extend(section_hdr("Mantenimiento del Automotor",
        "Productos especializados para el sector automotriz.",TEAL_DK))
    
    auto_imgs = Table([[safe_img('p38_img1.jpeg',16*mm,32*mm),safe_img('p38_img2.jpeg',10*mm,34*mm),
                         safe_img('p38_img4.jpeg',15*mm,30*mm),safe_img('p38_img5.jpeg',16*mm,28*mm)]],
        colWidths=[44*mm,44*mm,44*mm,44*mm])
    auto_imgs.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    els.append(auto_imgs)
    els.append(Spacer(1,2*mm))
    
    hau = ['PRODUCTO','PRESENTACION','APLICACION']
    rau = [
        ['Ultra Grey\n100% Silicona','Gris 99g - 550153','Sellador RTV silicona para juntas de motor.\n-62C a +343C. Resiste aceites.'],
        ['Sellador Cobre\nAltas Temp.','Aerosol 255g - 550260','Sellador en aerosol para juntas. Disipa calor.\nSella instant. -45C a +260C.'],
        ['Reparador Canos\nde Escape','Pomo 85g - 550140','Sella agujeros en silenciadores y canos.\nResiste hasta 1000C.'],
        ['Kit Espejo\nRetrovisor','Kit 0.9ml - 550250','Activador + adhesivo para espejo retrovisor\nal parabrisas. Pegado fuerte y rapido.'],
    ]
    els.append(ptable(hau, rau, TEAL_DK))
    els.append(PageBreak())
    
    # ===== GUIAS DE APLICACION (pages 39-40) =====
    els.extend(section_hdr("Guia de Aplicaciones - Construccion",""))
    els.append(safe_img('p39_img1.jpeg', 150*mm, 200*mm))
    els.append(PageBreak())
    
    els.extend(section_hdr("Guia de Aplicaciones - Automotor",""))
    els.append(safe_img('p40_img1.jpeg', 150*mm, 106*mm))
    els.append(Spacer(1,3*mm))
    els.append(safe_img('p40_img17.jpeg', 150*mm, 106*mm))
    els.append(PageBreak())
    
    # ===== BACK COVER =====
    els.append(Spacer(1,30*mm))
    els.append(Paragraph('<font color="#2E8B98" size="32"><b>ABSORB PAD</b></font><br/>'
        '<font color="#F9D423" size="16"><b>S.R.L.</b></font>',
        S('bk',32,TEAL,True,TA_CENTER,lead=40,sB=40*mm)))
    els.append(Spacer(1,15*mm))
    els.append(Paragraph(
        '<font color="#4A4A4A" size="12"><b>Soluciones Industriales y Mineria</b></font><br/><br/>'
        '<font color="#707070" size="10">San Luis 657 (E) | San Juan | Argentina<br/>'
        '+54 9 264 411 5967 | mario.ortiz@absorbpad.com<br/>www.absorbpad.com</font>',
        S('ct',10,align=TA_CENTER,lead=16)))
    els.append(Spacer(1,10*mm))
    sep = Table([['']], colWidths=[80*mm], rowHeights=[2*mm])
    sep.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),YELLOW)]))
    sw = Table([[sep]], colWidths=[178*mm])
    sw.setStyle(TableStyle([('ALIGN',(0,0),(0,0),'CENTER')]))
    els.append(sw)
    els.append(Spacer(1,10*mm))
    els.append(Paragraph('<font color="#AAAAAA" size="7">Condiciones Generales de Venta: Nacional: FCA San Juan. '
        '(C) 2026 Absorb Pad S.R.L. - Desarrollado por GrowLabs</font>',
        S('cond',7,align=TA_CENTER,lead=10)))
    
    # BUILD
    doc.build(els, onFirstPage=tpl.on_page, onLaterPages=tpl.on_page)
    print(f"[OK] Catalogo generado: {OUT}")
    print(f"     Paginas totales: {tpl.pc}")

if __name__ == '__main__':
    build()
