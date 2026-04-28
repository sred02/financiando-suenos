from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models

router = APIRouter()


def _num_to_words(n: int) -> str:
    """Convierte un número entero a texto en español (simplificado hasta 999.999)."""
    unidades = ['','un','dos','tres','cuatro','cinco','seis','siete','ocho','nueve',
                'diez','once','doce','trece','catorce','quince','dieciséis',
                'diecisiete','dieciocho','diecinueve']
    decenas  = ['','','veinte','treinta','cuarenta','cincuenta','sesenta','setenta','ochenta','noventa']
    centenas = ['','ciento','doscientos','trescientos','cuatrocientos','quinientos',
                'seiscientos','setecientos','ochocientos','novecientos']

    if n == 0:   return 'cero'
    if n == 100: return 'cien'
    if n < 20:   return unidades[n]
    if n < 100:  return decenas[n//10] + (' y ' + unidades[n%10] if n%10 else '')
    if n < 1000:
        resto = n % 100
        return centenas[n//100] + (' ' + _num_to_words(resto) if resto else '')
    if n < 1_000_000:
        miles = n // 1000
        resto = n % 1000
        base  = 'mil' if miles == 1 else _num_to_words(miles) + ' mil'
        return base + (' ' + _num_to_words(resto) if resto else '')
    millones = n // 1_000_000
    resto = n % 1_000_000
    base  = 'un millón' if millones == 1 else _num_to_words(millones) + ' millones'
    return base + (' ' + _num_to_words(resto) if resto else '')


def _fmt_cop(v: float) -> str:
    return f"${int(v):,}".replace(",", ".")


@router.get("/{donacion_id}", response_class=HTMLResponse)
def generar_certificado(
    donacion_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    """
    Devuelve el HTML del certificado listo para imprimir o convertir a PDF.
    El frontend puede abrir esta URL en una ventana nueva y llamar window.print().
    
    """
    don = db.query(models.Donacion).filter_by(id=donacion_id).first()
    if not don:
        raise HTTPException(status_code=404, detail="Donación no encontrada")

    emp  = don.empresa
    ben  = don.beneficiario
    total = int(don.valor_total)

    items_html = "".join(f"""
        <tr>
          <td style='font-size:12px;color:#666'>{it.categoria or '—'}</td>
          <td>{it.descripcion or '—'}</td>
          <td style='text-align:center'>{it.cantidad} {it.unidad or ''}</td>
          <td style='text-align:right;font-weight:800'>{_fmt_cop(it.valor_est or 0)}</td>
        </tr>
    """ for it in don.items)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8"/>
  <title>Certificado {don.folio}</title>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:'Nunito',sans-serif;background:#fff;color:#1C2B3A}}
    .topbar{{height:6px;background:linear-gradient(90deg,#E84040 0%,#E84040 16.6%,#E8A020 16.6%,#E8A020 33.3%,#F5D020 33.3%,#F5D020 50%,#2BAD60 50%,#2BAD60 66.6%,#00A99D 66.6%,#00A99D 83.3%,#1B3A5C 83.3%,#1B3A5C 100%)}}
    .header{{background:#1B3A5C;color:#fff;padding:24px 40px;display:flex;justify-content:space-between;align-items:flex-start}}
    .org-name{{font-family:'Merriweather',serif;font-size:18px;font-weight:700}}
    .org-name span{{color:#00A99D}}
    .org-sub{{font-size:10px;color:rgba(255,255,255,.5);text-transform:uppercase;letter-spacing:1px;margin-top:2px}}
    .folio{{text-align:right;font-size:12px;font-weight:800;color:#00A99D}}
    .fecha{{font-size:11px;color:rgba(255,255,255,.5);margin-top:3px}}
    .title-block{{text-align:center;padding:24px 40px 18px;border-bottom:1px solid #E5E7E9}}
    .title-label{{font-size:9px;font-weight:800;color:#007f75;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px}}
    .title{{font-family:'Merriweather',serif;font-size:20px;font-weight:700;color:#1B3A5C;margin-bottom:4px}}
    .subtitle{{font-size:12px;color:#8C97A8}}
    .body{{padding:24px 40px}}
    .intro{{font-size:13px;color:#4A5568;line-height:1.75;margin-bottom:18px;text-align:justify}}
    .intro b{{color:#1B3A5C}}
    .grid{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:#D8DCE3;border:1px solid #D8DCE3;border-radius:8px;overflow:hidden;margin-bottom:18px}}
    .cell{{background:#fff;padding:10px 14px}}
    .cell.full{{grid-column:1/-1}}
    .cell-label{{font-size:9px;font-weight:800;color:#007f75;text-transform:uppercase;letter-spacing:.8px;margin-bottom:2px}}
    .cell-val{{font-size:13px;font-weight:700;color:#1B3A5C}}
    .cell-val.green{{color:#27AE60;font-size:15px}}
    .sec{{font-size:10px;font-weight:800;color:#007f75;text-transform:uppercase;letter-spacing:.8px;margin-bottom:8px;padding-bottom:5px;border-bottom:2px solid #E6F7F6}}
    table{{width:100%;border-collapse:collapse;font-size:13px;margin-bottom:16px}}
    thead th{{background:#1B3A5C;color:#fff;padding:8px 10px;text-align:left;font-size:10px;font-weight:800;text-transform:uppercase}}
    tbody tr{{border-bottom:1px solid #F0F2F5}}
    tbody td{{padding:8px 10px}}
    tfoot td{{padding:10px;background:#1B3A5C;color:#fff;font-weight:800;font-size:13px}}
    tfoot td:last-child{{text-align:right;color:#00A99D;font-family:'Merriweather',serif;font-size:15px}}
    .legal{{background:#FEF3E2;border:1px solid #F9E79F;border-radius:6px;padding:10px 14px;font-size:11px;color:#7D6608;line-height:1.55;margin-bottom:18px}}
    .sigs{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px;margin-bottom:6px}}
    .sig{{text-align:center}}
    .sig-line{{height:40px;border-bottom:1.5px solid #1B3A5C;margin-bottom:6px}}
    .sig-name{{font-size:12px;font-weight:800;color:#1B3A5C}}
    .sig-role{{font-size:10px;color:#8C97A8;margin-top:1px}}
    .seal-row{{display:flex;justify-content:center;align-items:center;gap:14px;padding:14px 40px 22px}}
    .seal{{width:68px;height:68px;border-radius:50%;border:3px solid #1B3A5C;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:8px;font-weight:800;color:#1B3A5C;text-align:center;text-transform:uppercase;line-height:1.3}}
    .seal-text{{font-size:10px;color:#8C97A8;max-width:240px;line-height:1.45;text-align:center}}
    .footer-bar{{background:#1B3A5C;padding:10px 40px;display:flex;justify-content:space-between}}
    .footer-bar span{{font-size:10px;color:rgba(255,255,255,.4)}}
    .footer-bar .v{{color:#00A99D;font-weight:800}}
    @media print{{body{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}}}
  </style>
</head>
<body>
<div class="topbar"></div>
<div class="header">
  <div>
    <div class="org-name">Financiando <span>Sueños</span></div>
    <div class="org-sub">Una iniciativa de Unbound Colombia</div>
  </div>
  <div>
    <div class="folio">Folio: {don.folio}</div>
    <div class="fecha">Bogotá D.C., {don.fecha}</div>
  </div>
</div>
<div class="title-block">
  <div class="title-label">Documento oficial de donación en especie</div>
  <div class="title">Certificado de Donación de Materiales</div>
  <div class="subtitle">Válido como soporte contable y tributario · Art. 125 E.T. · Ley 527 de 1999</div>
</div>
<div class="body">
  <p class="intro">
    La organización <b>Unbound Colombia</b>, con NIT 900.111.222-3, ejecutora del programa
    <b>Financiando Sueños</b>, certifica que la empresa
    <b>{emp.razon_social}</b>, identificada con NIT <b>{emp.nit}</b>,
    representada por <b>{emp.representante or '—'}</b> en calidad de <b>{emp.cargo or '—'}</b>,
    realizó una <b>donación en especie de materiales para mejora del hogar</b>
    a favor del adulto mayor beneficiario que se detalla a continuación:
  </p>
  <div class="grid">
    <div class="cell"><div class="cell-label">Empresa donante</div><div class="cell-val">{emp.razon_social}</div></div>
    <div class="cell"><div class="cell-label">NIT</div><div class="cell-val">{emp.nit}</div></div>
    <div class="cell"><div class="cell-label">Beneficiario</div><div class="cell-val">{ben.nombre}</div></div>
    <div class="cell"><div class="cell-label">Cédula</div><div class="cell-val">{ben.identificacion}</div></div>
    <div class="cell"><div class="cell-label">Ciudad / Barrio</div><div class="cell-val">{ben.ciudad or '—'} – {ben.barrio or '—'}</div></div>
    <div class="cell"><div class="cell-label">Fecha de donación</div><div class="cell-val">{don.fecha}</div></div>
    <div class="cell full"><div class="cell-label">Modalidad de entrega</div><div class="cell-val">{don.modalidad or '—'}</div></div>
    {"" if not don.observaciones else f'<div class="cell full"><div class="cell-label">Observaciones</div><div class="cell-val" style="font-weight:400;font-size:13px;color:#4A5568">{don.observaciones}</div></div>'}
    <div class="cell full"><div class="cell-label">Valor total estimado</div><div class="cell-val green">{_fmt_cop(don.valor_total)} COP ({_num_to_words(total)} pesos)</div></div>
  </div>
  <div class="sec">Detalle de materiales donados</div>
  <table>
    <thead><tr><th>Categoría</th><th>Descripción</th><th style="text-align:center">Cantidad</th><th style="text-align:right">Valor estimado</th></tr></thead>
    <tbody>{items_html}</tbody>
    <tfoot><tr><td colspan="3">Total estimado de la donación en especie</td><td>{_fmt_cop(don.valor_total)}</td></tr></tfoot>
  </table>
  <div class="legal"><b>Nota legal:</b> Esta donación corresponde exclusivamente a bienes en especie (materiales y elementos físicos para mejora del hogar). No incluye transferencias en efectivo ni instrumentos financieros. El valor indicado es una estimación del mercado con fines contables y tributarios, conforme al Art. 125 del Estatuto Tributario colombiano.</div>
  <div class="sec">Firmas y validación</div>
  <div class="sigs">
    <div class="sig"><div class="sig-line"></div><div class="sig-name">Directora Ejecutiva</div><div class="sig-role">Unbound Colombia</div></div>
    <div class="sig"><div class="sig-line"></div><div class="sig-name">{emp.representante or '—'}</div><div class="sig-role">{emp.cargo or '—'} · {emp.razon_social.split()[0]}</div></div>
    <div class="sig"><div class="sig-line"></div><div class="sig-name">Coordinador de Donaciones</div><div class="sig-role">Financiando Sueños – Unbound</div></div>
  </div>
</div>
<div class="seal-row">
  <div class="seal">🏠<br/>UNBOUND<br/>COLOMBIA<br/>OFICIAL</div>
  <div class="seal-text">Generado electrónicamente por <b>Financiando Sueños</b>. Válido sin firma manuscrita conforme a la Ley 527 de 1999. Código: <b>{don.folio}</b></div>
</div>
<div class="footer-bar">
  <span>Financiando Sueños · Unbound Colombia · NIT 900.111.222-3</span>
  <span class="v">✓ Documento verificado</span>
  <span>Ley 1581 de 2012 – Protección de datos</span>
</div>
</body></html>"""

    return HTMLResponse(content=html)
