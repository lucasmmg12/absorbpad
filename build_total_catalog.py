import fitz
import json
import re
import os

pdf_path = r'C:\Users\Sanatorio Argentino\Desktop\Proyectos\Absorbpad\CATALOGO TOTAL x ABSORB PAD 2026 (1).pdf'
img_dir = r'C:\Users\Sanatorio Argentino\Desktop\Proyectos\Absorbpad\public\assets\total'
json_out = r'C:\Users\Sanatorio Argentino\Desktop\Proyectos\Absorbpad\public\assets\total\total_products.json'
js_out = r'C:\Users\Sanatorio Argentino\Desktop\Proyectos\Absorbpad\public\assets\total\total_products.js'

doc = fitz.open(pdf_path)

def clean_text(txt):
    if not txt:
        return ""
    # Remove null bytes or control chars except newline
    txt = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', txt)
    # Fix broken keywords
    txt = txt.replace('CATLOGO', 'CATÁLOGO').replace('CARACTERSTICAS', 'CARACTERÍSTICAS').replace('TCNICAS', 'TÉCNICAS').replace('INALMBRICAS', 'INALÁMBRICAS').replace('ELCTRICAS', 'ELÉCTRICAS').replace('NEUMTICAS', 'NEUMÁTICAS').replace('Lnea', 'Línea').replace('Mximo', 'Máximo').replace('Batera', 'Batería').replace('batera', 'batería').replace('ilumacin', 'iluminación').replace('Opcin', 'Opción').replace('csped', 'césped').replace('Demolicin', 'Demolición').replace('demolicin', 'demolición').replace('Posicin', 'Posición').replace('Polmero', 'Polímero').replace('Pistola de Pegar', 'Pistola de Pegar').replace('Iluminacin', 'Iluminación').replace('Rotomartillo', 'Rotomartillo').replace('Automtico', 'Automático').replace('Plstico', 'Plástico').replace('Tensin', 'Tensión').replace('Imn', 'Imán').replace('Mquina', 'Máquina')
    return txt.strip()

def get_category_by_page(pno):
    if 8 <= pno <= 94:
        return "Inalámbricas"
    elif 95 <= pno <= 99:
        return "Eléctricas"
    elif 100 <= pno <= 103:
        return "Neumáticas"
    elif 104 <= pno <= 109:
        return "Nafteras"
    elif 110 <= pno <= 143:
        return "Accesorios"
    elif 144 <= pno <= 245:
        return "Manuales"
    return "General"

def extract_products():
    products = []
    available_imgs = os.listdir(img_dir) if os.path.exists(img_dir) else []
    
    for pno in range(7, len(doc)): # Page index 7 is Page 8 in PDF
        page = doc[pno]
        page_num = pno + 1
        text = clean_text(page.get_text('text'))
        lines = [clean_text(line) for line in text.split('\n') if clean_text(line)]
        
        # Web relative path (without leading public/ so it works in Vite and static servers)
        page_imgs = [
            f"public/assets/total/{img_name}"
            for img_name in sorted(available_imgs)
            if img_name.startswith(f"p{page_num:03d}_img") and not img_name.endswith('.json') and not img_name.endswith('.js')
        ]
        
        category = get_category_by_page(page_num)
        
        code_matches = re.findall(r'\b(T[A-Z0-9]{5,14}(?:-[0-9A-Z]+)?)\b', text)
        cod_internals = re.findall(r'(COD\.\s*[A-Z0-9]+)', text)
        
        title = ""
        for line in lines:
            if line.isupper() and len(line) > 4 and not line.startswith('CATÁLOGO') and not line.startswith('CARACTERÍSTICAS') and not line.startswith('INDUSTRIAL') and not line.startswith('INCLUYE') and not line.startswith('Lucas') and not line.startswith('Caja'):
                if not title or len(line) > len(title):
                    title = line

        if not title or title.startswith("CATÁLOGO"):
            title = f"Herramienta TOTAL Pág. {page_num}"
            
        voltage = ""
        if "20V" in text or "20v" in text:
            voltage = "20V"
        elif "12V" in text or "12v" in text:
            voltage = "12V"
        elif "42V" in text or "42v" in text:
            voltage = "42V"
        elif "4V" in text or "4v" in text:
            voltage = "4V"

        is_brushless = "Brushless" in text or " BL " in text or "BL " in title or title.endswith(" BL")
        
        specs = []
        for line in lines:
            if ":" in line and not line.startswith("COD.") and not line.startswith("Caja Madre:") and not line.startswith("http") and not line.startswith("www") and not line.startswith("CATÁLOGO"):
                specs.append(line)
        
        main_code = code_matches[0] if code_matches else f"TOTAL-P{page_num}"
        cod_int = cod_internals[0] if cod_internals else ""
        
        product = {
            "id": f"p{page_num}_{main_code}",
            "title": title,
            "code": main_code,
            "cod_internal": cod_int,
            "category": category,
            "page": page_num,
            "voltage": voltage,
            "is_brushless": is_brushless,
            "specs": specs[:8],
            "images": page_imgs
        }
        products.append(product)
        
    print(f"Processed {len(products)} product pages into catalog.")
    
    with open(json_out, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
        
    with open(js_out, 'w', encoding='utf-8') as f:
        f.write(f"window.TOTAL_PRODUCTS = {json.dumps(products, ensure_ascii=False, indent=2)};")

if __name__ == '__main__':
    extract_products()
