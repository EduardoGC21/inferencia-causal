"""Tablas y figuras del diseño final; todas las cifras proceden de CSV regenerados."""
import numpy as np
import pandas as pd
from .analisis import table, fmt, texesc


METHOD = {"emparejada": "1:muchos", "emparejada_1a1": "1:1", "mismos_tratados": "Sin emparejar",
          "sin_covariables": "Calibre individual", "comun_m0_m3": "Completos, calibre"}
SCENARIO = {"principal": "Principal", "persistencia": "Aislamiento posterior", "placebo": "Placebo 28 días antes",
            "sin_cinco": "Cinco fechas de auditoría", "sin_laborales": "Sin feriados LFT",
            "sin_laborales_escolares": "Sin LFT ni recesos SEP", "sin_pendientes": "Sin dos tratados pendientes",
            "sin_todos_pendientes": "Sin cuatro casos pendientes", "sin_senales": "Sin dos señales en controles"}
SPAN_LABELS = {"d0": "Día 0", "d1": "Día 1", "d0..1": "Días 0–1", "d2..6": "Días 2–6",
               "wk0": "Sem. 0", "wk+1": "Sem. +1"}
MODEL_LABELS = {"M0": "Base (M0)", "M1": "+ Población", "M2": "+ Empleo", "M3": "+ Autos"}
STATE_NAMES = dict(enumerate([
    "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Coahuila",
    "Colima", "Chiapas", "Chihuahua", "Ciudad de México", "Durango", "Guanajuato",
    "Guerrero", "Hidalgo", "Jalisco", "Estado de México", "Michoacán", "Morelos", "Nayarit",
    "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí",
    "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"], 1))


def result(row, uncertainty=True):
    if row is None:
        return "---"
    return (f"{fmt(row.efecto,3)} [{fmt(row.ic_inf,3)}; {fmt(row.ic_sup,3)}]" if uncertainty
            else f"{fmt(row.efecto,3)} ({fmt(row.ee,3)})")


def pvalue(value):
    return r"\(<0{,}001\)" if np.isfinite(value) and value < .001 else fmt(value,3)


def interval(row):
    return f"[{fmt(row.ic_inf,3)}; {fmt(row.ic_sup,3)}]"


def tables(config):
    out = config["paths"]["outputs"]
    mod, tab = out / "modelos", out / "tablas"
    tab.mkdir(parents=True, exist_ok=True)
    e = pd.read_csv(mod / "causal_efectos.csv", dtype={"tramo": str})
    if set(e.base) != {"tres_semanas"} or set(e.escala) != {"niveles"}:
        raise ValueError("Las tablas requieren niveles y la base de 21 días")

    def get(scenario="principal", method="emparejada", span="d0..1", cluster="entidad", model="M0"):
        rows = e.loc[e.escenario.eq(scenario) & e.muestra.eq(method) & e.tramo.eq(span)
                     & e.agrupacion.eq(cluster) & e.modelo.eq(model)]
        return rows.iloc[0] if len(rows) else None

    main = get()
    two, level = get(cluster="entidad_fecha"), get()
    macros = {}
    def put(name, value, digits=3):
        macros[name] = (pvalue(value) if name.endswith('P') else fmt(value,digits)) if isinstance(value,(int,float,np.number)) else str(value)
    for name, row in [("Main",main),("Doble",two),("Nivel",level),("NivelDoble",get(cluster="entidad_fecha")),
                      ("Previa",get(span="wk-1")),("PreviaDoble",get(span="wk-1",cluster="entidad_fecha")),
                      ("MenosDos",get(span="-2")),("MenosCinco",get(span="-5")),
                      ("CRVTres",get(cluster="CRV3")),("Placebo",get(scenario="placebo",cluster="entidad_fecha"))]:
        for field in ("efecto","ee","ic_inf","ic_sup","p","mde","efecto_sigma"):
            put(name+field.replace('_','').title(), row[field] if row is not None else np.nan)
    for field,name in [("tratados","Trat"),("controles","Cont"),("fechas","Fechas"),("episodios","Epis"),
                       ("estados_tratados","EstadosTrat"),("estados","Estados"),("n","MuestraN")]:
        put(name,main[field],0)
    put("EstadosEf",main.estados_tratados_efectivos,1)
    put("MediaPre",level.media_pre,2);put("SigmaPre",level.sigma_pre,2)
    put("MdePctNivel",100*level.mde/level.media_pre,1)
    put("MdePctNivelDoble",100*get(cluster="entidad_fecha").mde/level.media_pre,1)
    direction = "una caída" if main.efecto < 0 else "un aumento"
    evidence = ("El contraste inmediato es negativo y su intervalo de dos vías excluye cero."
                if two.ic_sup < 0 else "El intervalo inmediato de dos vías incluye cero; la evidencia no permite afirmar una reducción con ese criterio.")
    put("LecturaPrincipal", evidence)
    put("Direccion",direction)
    put("LecturaCRV", "El intervalo CRV3 también excluye cero." if get(cluster="CRV3").ic_sup < 0 else
        "El intervalo CRV3 incluye cero: la conclusión estadística es sensible a la inferencia con pocos conglomerados.")
    late=[get(span=s,cluster="entidad_fecha") for s in ("d2..6","wk+1")]
    put("LecturaPersistencia", "Ambos intervalos posteriores de dos vías incluyen cero; ello indica ausencia de persistencia detectable, no equivalencia demostrada con cero."
        if all(r.ic_inf<=0<=r.ic_sup for r in late) else
        "Al menos un intervalo posterior de dos vías excluye cero. El rediseño no sostiene una desaparición completa del cambio desde el día 2.")
    weekly=pd.read_csv(mod/'causal_wald_semanal.csv')
    joint=weekly.loc[weekly.escenario.eq('principal') & weekly.muestra.eq('emparejada') & weekly.escala.eq('niveles') & weekly.restricciones.eq('wk-4;wk-3;wk-1')]
    for cluster,name in [('entidad','Wald'),('entidad_fecha','WaldDoble')]:
        r=joint.loc[joint.agrupacion.eq(cluster)].iloc[0]
        put(name+'P',r.p);put(name+'Estado',texesc(r.estado))
    rows=[]
    for span in SPAN_LABELS:
        a,b=get(span=span),get(span=span,cluster='entidad_fecha')
        rows.append([SPAN_LABELS[span],result(a,False),interval(b),fmt(a.efecto_sigma,3),fmt(b.mde,3)])
    table(tab/'causal_principales.tex',['Tramo',r'$\hat\tau$ (EE estatal)',r'IC 95\% doble',r'$\tau/\sigma$', 'MDE doble'],rows)
    # Progresión con muestra fija, incluido el ajuste sin matching para los mismos tratados.
    rows=[]
    for method in ['comun_m0_m3','mismos_tratados','emparejada','emparejada_1a1']:
        for model in ['M0','M1','M2','M3']:
            r=get(method=method,model=model,cluster='entidad_fecha')
            rows.append([METHOD[method],MODEL_LABELS[model],fmt(r.tratados,0),fmt(r.n,0),result(r)])
    table(tab/'causal_modelos.tex',['Controles','Modelo','Trat.',r'$N$','Estimación e IC doble'],rows)
    c = pd.read_csv(mod/'causal_coeficientes.csv')
    c = c.loc[c.escenario.eq('principal') & c.muestra.eq('emparejada')].set_index(['termino','modelo'])
    terms = {"tratado": "Tratado × Después", "log_poblacion": "Logaritmo de la población",
             "empleo_mil": "Empleo por cada mil habitantes", "autos_mil": "Automóviles por cada mil habitantes"}
    rows = []
    for k, (term, label) in enumerate(terms.items()):
        row = [label]
        for model in MODEL_LABELS:
            if (term, model) not in c.index:
                row.append('—')
                continue
            r = c.loc[term, model]
            digits = 6 if k >= 2 else 3
            row.append(r'\shortstack{' + r'\\'.join([fmt(r.efecto,digits),f'({fmt(r.ee,digits)})',
                        f'[{fmt(r.ic_inf,digits)}; {fmt(r.ic_sup,digits)}]', '$p='+fmt(r.p,3).replace(',','{,}')+'$']) + '}')
        rows.append(row)
    table(tab/'causal_progresion_principal.tex',['Término'] + [f'$M_{j}$' for j in range(4)],rows)
    # Balance: denominador común fijado en la muestra con calibre individual.
    bal=pd.read_csv(mod/'causal_balance.csv')
    bal=bal.loc[bal.escenario.eq('principal')]
    rows=[]
    for cov,label in [('poblacion','Población'),('empleo_mil','Empleo / mil'),('autos_mil','Autos / mil'),('pre_nivel','Accidentes previos')]:
        a=bal.loc[bal.muestra.eq('emparejada') & bal.covariable.eq(cov)].set_index('tratado')
        b=bal.loc[bal.muestra.eq('emparejada_1a1') & bal.covariable.eq(cov) & bal.tratado.eq(0)].iloc[0]
        rows.append([label,f'{fmt(a.loc[1,"media"],2)} ({fmt(a.loc[1,"de"],2)})',
                     f'{fmt(a.loc[0,"media"],2)} ({fmt(a.loc[0,"de"],2)})',fmt(a.loc[0,'dme'],3),fmt(b.dme,3)])
    table(tab/'causal_balance.tex',['Variable','Tratados: media (DE)','Controles 1:muchos','DME 1:muchos','DME 1:1'],rows)
    before_after=[]
    for cov,label in [('poblacion','Población'),('empleo_mil','Empleo / mil'),('autos_mil','Autos / mil'),('pre_nivel','Accidentes previos')]:
        before_after.append([label]+[fmt(bal.loc[bal.muestra.eq(m) & bal.covariable.eq(cov) & bal.tratado.eq(0),'dme'].iloc[0],3)
                                    for m in ['mismos_tratados','emparejada','emparejada_1a1']])
    table(tab/'causal_balance_prepost.tex',['Variable','Antes de emparejar','1:muchos','1:1'],before_after)
    # Uniones del universo elegible, antes de imponer covariables completas.
    unions=pd.read_csv(mod/'causal_uniones.csv')
    rows=[]
    for source,label in [('censo','EIC / ITER'),('saic','SAIC'),('vmrc','VMRC')]:
        for role,name in [(1,'T'),(0,'C')]:
            r=unions.loc[unions.especificacion.eq('principal') & unions.fuente.eq(source) & unions.tratado.eq(role)]
            n,matched,usable=r.pares.sum(),r.unidas.sum(),r.utilizables.sum()
            if source == 'censo':
                for cut,group in r.groupby('corte'):
                    total,joined,finite=group.pares.sum(),group.unidas.sum(),group.utilizables.sum()
                    rows.append(['EIC 2015' if cut == 2015 else 'ITER 2020','Tratados' if role else 'Controles',f'{fmt(joined,0)}/{fmt(total,0)}',fmt(100*joined/total,1),f'{fmt(finite,0)}/{fmt(total,0)}'])
            else:
                rows.append([label,'Tratados' if role else 'Controles',f'{fmt(matched,0)}/{fmt(n,0)}',fmt(100*matched/n,1),f'{fmt(usable,0)}/{fmt(n,0)}'])
            put('Union'+source.title()+name,f'{fmt(matched,0)}/{fmt(n,0)}')
    table(tab/'causal_uniones.tex',['Fuente','Rol','Unidas / elegibles',r'\%','Valor utilizable / elegibles'],rows)
    support=pd.read_csv(mod/'causal_soporte.csv')
    table(tab/'causal_soporte.tex',['Escenario','Matching','Trat.','Cont.','Fechas','Episodios'],
          [[SCENARIO[r.escenario],METHOD[r.muestra],fmt(r.tratados,0),fmt(r.controles,0),fmt(r.fechas,0),fmt(r.episodios,0)]
           for r in support.loc[support.muestra.isin(['emparejada','emparejada_1a1'])].itertuples()])
    rows=[]
    for scenario in ['principal','sin_cinco','sin_laborales','sin_laborales_escolares','sin_pendientes','sin_todos_pendientes','sin_senales']:
        for method in ['emparejada','emparejada_1a1']:
            a=get(scenario=scenario,method=method,cluster='entidad_fecha')
            rows.append([SCENARIO[scenario],METHOD[method],fmt(a.tratados,0),fmt(a.fechas,0),result(a)])
    table(tab/'causal_sensibilidades.tex',['Exclusión / muestra','Matching','Trat.','Fechas','Estimación e IC doble'],rows)
    rows=[]
    for scenario in ['principal','persistencia','placebo']:
        for method in ['emparejada','emparejada_1a1']:
            a=get(scenario=scenario,method=method,cluster='entidad_fecha')
            rows.append([SCENARIO[scenario],METHOD[method],fmt(a.tratados,0)]+[
                result(get(scenario=scenario,method=method,span=span,cluster='entidad_fecha')) for span in ['d0..1','d2..6','wk+1']])
    table(tab/'causal_persistencia.tex',['Selección','Matching','Trat.','Días 0–1','Días 2–6','Sem. +1'],rows)
    rows=[]
    for span in SPAN_LABELS:
        row=[SPAN_LABELS[span]]
        for method in ['emparejada','emparejada_1a1']:
            a=get(scenario='placebo',method=method,span=span)
            b=get(scenario='placebo',method=method,span=span,cluster='entidad_fecha')
            row += [result(b),pvalue(b.p),pvalue(a.p)]
        rows.append(row)
    table(tab/'causal_placebo.tex',['Horizonte','1:muchos, IC doble',r'$p$ doble',r'$p$ estatal',
                                   '1:1, IC doble',r'$p$ doble',r'$p$ estatal'],rows)
    rows=[]
    for method in ['emparejada','emparejada_1a1']:
        for cluster,name in [('entidad','CRV1 estatal'),('entidad_fecha','CRV1: estado y fecha'),('CRV3','CRV3 estatal')]:
            r=get(method=method,cluster=cluster)
            rows.append([METHOD[method],name,result(r),fmt(r.gl,0),fmt(r.mde,3)])
    table(tab/'causal_inferencia.tex',['Matching','Inferencia',r'Días 0–1, IC 95\%','gl','MDE'],rows)
    rows=[]
    for method in ['emparejada','emparejada_1a1']:
        r=weekly.loc[weekly.escenario.eq('principal') & weekly.muestra.eq(method) & weekly.restricciones.eq('wk-4;wk-3;wk-1')]
        for item in r.itertuples():
            rows.append([METHOD[method],'Estatal' if item.agrupacion=='entidad' else 'Estado y fecha',
                         fmt(item.f,3),pvalue(item.p),fmt(item.rango,0),fmt(item.condicion,1),texesc(item.estado)])
    table(tab/'causal_previos.tex',['Matching','Agrupación','F','p','Rango','Condición','Cálculo'],rows)
    # Donantes de Morelia en el modelo principal y sin señales en controles.
    final_edges=pd.read_csv(mod/'causal_vinculos.csv',
                            dtype={'tratado_clave':str,'control_clave':str},parse_dates=['indice'])
    morelia=final_edges.loc[final_edges.escenario.isin(['principal','sin_senales'])
                            & final_edges.muestra.eq('emparejada') & final_edges.tratado_clave.eq('16053')
                            & final_edges.indice.eq('2025-04-23'), ['escenario','control_clave','contribucion']]
    morelia.to_csv(mod/'causal_morelia_donantes.csv',index=False)
    for scenario,name in [('principal','MoreliaDespues'),('sin_senales','MoreliaSenales')]:
        put(name,morelia.escenario.eq(scenario).sum(),0)
    losses=pd.read_csv(mod/'causal_descartes.csv',dtype={'clave':str},parse_dates=['indice'])
    more=losses.loc[losses.escenario.eq('principal') & losses.clave.eq('16053') & losses.indice.eq('2025-04-23')].iloc[0]
    put('MoreliaUniverso',more.controles_auditados,0);put('MoreliaCalibre',more.despues_pre_nivel,0)
    # Cruce exploratorio actualizado a la misma muestra y base del principal.
    cross=pd.read_csv(mod/'causal_cruce.csv')
    table(tab/'causal_cruce.tex',['Gravedad','1:muchos: noche menos día','1:1: noche menos día'],
          [[label]+[result(cross.loc[cross.muestra.eq(m) & cross.franja.eq('noche_menos_dia') & cross.gravedad.eq(g) & cross.agrupacion.eq('entidad_fecha')].iloc[0])
                    for m in ['emparejada','emparejada_1a1']] for g,label in [('fatal','Fatal'),('heridos','Con heridos'),('danos','Solo daños')]])
    # Calendario por fecha, con las causas concretas de exclusión.
    calendar=pd.read_csv(mod/'causal_exclusiones_calendario.csv',parse_dates=['indice'])
    dates=calendar.groupby('indice',sort=True).agg(tratados=('clave','size'),laboral=('laboral','max'),escolar=('escolar','max'),cinco=('audit_cinco','max'))
    table(tab/'causal_calendario.tex',['Inicio','Trat.','LFT en días 0–1','SEP en días 0–1','Cinco fechas'],
          [[str(d.date()),fmt(r.tratados,0),'Sí' if r.laboral else 'No','Sí' if r.escolar else 'No','Sí' if r.cinco else 'No'] for d,r in dates.iterrows()])
    # Omisiones estatales del principal, sin rematching ni renormalizar pesos.
    loo=pd.read_csv(mod/'causal_omision_estado.csv',dtype={'estado_omitido':str,'tramo':str})
    pick=loo.loc[loo.muestra.eq('emparejada') & loo.modelo.eq('M0') & loo.tramo.eq('d0..1')].sort_values('estado_omitido')
    table(tab/'causal_omision.tex',['Estado omitido','Días 0–1'],
          [[STATE_NAMES[int(r.estado_omitido)],fmt(r.efecto,3)] for r in pick.itertuples()])
    # Cobertura/territorio como operaciones de unión distintas del matching estadístico.
    sample=pd.read_csv(mod/'causal_muestras.csv', low_memory=False)
    pool=sample.loc[sample.escenario.eq('principal') & sample.muestra.eq('emparejada')]
    source_rows=[]
    for column,label in [('saic_conapo_union','CONAPO en SAIC'),('vmrc_conapo_union','CONAPO en VMRC')]:
        n=len(pool);num=pool[column].eq('unida').sum();source_rows.append([label,f'{fmt(num,0)}/{fmt(n,0)}',fmt(100*num/n,1),'Pares de la muestra final'])
    audit=pd.read_csv(mod/'causal_elegibilidad.csv')
    a=audit.loc[audit.escenario.eq('principal')]
    n=len(a);num=a.territorio_compatible.sum()
    source_rows.append(['AGEEML: perímetro estable',f'{fmt(num,0)}/{fmt(n,0)}',fmt(100*num/n,1),'Municipio-fechas candidatos'])
    table(tab/'causal_uniones_aux.tex',['Operación','Numerador / denominador',r'\%','Universo'],source_rows)
    treated_a=a.loc[a.tratado.eq(1)]
    n=len(treated_a)
    loss_rows=[['Candidatos del catálogo',fmt(n,0),'---']]
    for label,mask in [('Sin historia de cobertura',~treated_a.cobertura_predicha),
                       ('Exposición previa, tras cobertura',treated_a.cobertura_predicha & treated_a.exposicion_en_ventana),
                       ('Territorio, tras filtros anteriores',treated_a.cobertura_predicha & ~treated_a.exposicion_en_ventana & ~treated_a.territorio_compatible)]:
        removed=int(mask.sum());n-=removed;loss_rows.append([label,fmt(n,0),fmt(removed,0)])
    for reason,label in [('faltantes_tratado','Covariables faltantes'),('datos_completos','Controles completos insuficientes'),
                         ('pre_nivel','Calibre individual sin soporte'),('poblacion','Población sin soporte'),
                         ('empleo_mil','Empleo sin soporte'),('autos_mil','Autos sin soporte')]:
        removed=int(losses.loc[losses.escenario.eq('principal'),'motivo'].eq(reason).sum())
        n-=removed
        loss_rows.append([label,fmt(n,0),fmt(removed,0)])
    if n != main.tratados:
        raise ValueError('La contabilidad de pérdidas no concilia con los tratados finales')
    table(tab/'causal_perdidas.tex',['Paso, orden jerárquico','Trat. restantes','Trat. excluidos'],loss_rows)
    (tab/'causal_cifras.tex').write_text(''.join(r'\newcommand{\R'+k+'}{'+v+'}\n' for k,v in macros.items()),encoding='utf-8')
    print('Tablas autocontenidas del diseño final generadas.')


def figures(config):
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    from .graficas import save, BLUE, ACCENT

    out = config["paths"]["outputs"]
    e = pd.read_csv(out / "modelos/causal_efectos.csv", dtype={"tramo": str})
    e = e.loc[e.escenario.eq("principal") & e.base.eq("tres_semanas")
              & e.modelo.eq("M0") & e.agrupacion.eq("entidad_fecha")]
    fig, ax = plt.subplots(figsize=(7.35, 3.35))
    fig.subplots_adjust(left=.15, right=.97, bottom=.19, top=.80)
    methods = [
        ("emparejada", BLUE, -.10, "1:muchos", "o-"),
        ("emparejada_1a1", ACCENT, .10, "1:1", "^--"),
    ]
    for method, color, offset, name, style in methods:
        rows = e.loc[e.muestra.eq(method) & e.tramo.isin([str(h) for h in range(-7, 14)])].copy()
        rows["h"] = rows.tramo.astype(int)
        rows = rows.sort_values("h")
        ax.errorbar(
            rows.h + offset, rows.efecto,
            yerr=[rows.efecto - rows.ic_inf, rows.ic_sup - rows.efecto],
            fmt=style, color=color, markersize=3.2, linewidth=.9,
            elinewidth=.8, capsize=1.5, label=name,
        )
    ax.axhline(0, color="#555555", linewidth=.6)
    ax.axvline(0, color="#555555", linestyle="--", linewidth=.8)
    ax.set_ylabel("Siniestros registrados\npor municipio y día", fontsize=9)
    ax.set_xlabel("Día respecto al inicio local", fontsize=9)
    ax.set_xticks([-7, -5, -2, 0, 1, 3, 6, 9, 13])
    ax.tick_params(labelsize=8.5)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:g}".replace(".", ",")))
    ax.grid(axis="y", alpha=.2)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower center", bbox_to_anchor=(.5, 1.05), frameon=False, ncols=2, fontsize=9)
    (out / "figuras").mkdir(parents=True, exist_ok=True)
    save(fig, out / "figuras", "causal_dinamica")
    # El reporte usa la copia local de esta figura. La presentación conserva la suya.
    from shutil import copyfile
    copyfile(out / "figuras" / "causal_dinamica.png",
             config["root"] / "reporte" / "figuras" / "trayectoria-siniestros.png")
