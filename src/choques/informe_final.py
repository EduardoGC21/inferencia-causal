"""Tablas y figuras del diseño final; todas las cifras proceden de CSV regenerados."""
import numpy as np
import pandas as pd
from .analisis import table, fmt, texesc


METHOD = {"emparejada": "1:muchos", "emparejada_1a1": "1:1", "mismos_tratados": "Sin matching",
          "sin_covariables": "Calibre individual", "comun_m0_m3": "Completos, calibre"}
SCENARIO = {"principal": "Principal", "persistencia": "Aislamiento posterior", "placebo": "Placebo -28",
            "sin_cinco": "Cinco fechas de auditoría", "sin_laborales": "Sin feriados LFT",
            "sin_laborales_escolares": "Sin LFT ni recesos SEP", "sin_pendientes": "Sin dos tratados pendientes",
            "sin_todos_pendientes": "Sin cuatro casos pendientes", "sin_senales": "Sin dos señales en controles"}


def result(row, uncertainty=True):
    if row is None:
        return "---"
    return (f"{fmt(row.efecto,3)} [{fmt(row.ic_inf,3)}; {fmt(row.ic_sup,3)}]" if uncertainty
            else f"{fmt(row.efecto,3)} ({fmt(row.ee,3)})")


def pvalue(value):
    return r"\(<0{,}001\)" if np.isfinite(value) and value < .001 else fmt(value,3)


def tables(config):
    out = config["paths"]["outputs"]
    mod, tab = out / "modelos", out / "tablas"
    e = pd.read_csv(mod / "causal_efectos.csv", dtype={"tramo": str})
    def get(scenario="principal", method="emparejada", scale="log1p", span="d0..1", cluster="entidad", model="M0", base="tres_semanas"):
        rows = e.loc[e.escenario.eq(scenario) & e.muestra.eq(method) & e.escala.eq(scale) & e.tramo.eq(span)
                     & e.agrupacion.eq(cluster) & e.modelo.eq(model) & e.base.eq(base)]
        return rows.iloc[0] if len(rows) else None

    main = get()
    two, level = get(cluster="entidad_fecha"), get(scale="niveles")
    macros = {}
    def put(name, value, digits=3):
        macros[name] = (pvalue(value) if name.endswith('P') else fmt(value,digits)) if isinstance(value,(int,float,np.number)) else str(value)
    for name, row in [("Main",main),("Doble",two),("Nivel",level),("NivelDoble",get(scale="niveles",cluster="entidad_fecha")),
                      ("Previa",get(span="wk-1")),("PreviaDoble",get(span="wk-1",cluster="entidad_fecha")),
                      ("MenosDos",get(span="-2")),("MenosCinco",get(span="-5")),
                      ("CRVTres",get(cluster="CRV3")),("Placebo",get(scenario="placebo",cluster="entidad_fecha")),
                      ("BaseSemana",get(base="wk-1",cluster="entidad_fecha"))]:
        for field in ("efecto","ee","ic_inf","ic_sup","p","mde","efecto_sigma"):
            put(name+field.replace('_','').title(), row[field] if row is not None else np.nan)
    for field,name in [("tratados","Trat"),("controles","Cont"),("fechas","Fechas"),("episodios","Epis"),
                       ("estados_tratados","EstadosTrat"),("estados","Estados"),("n","N")]:
        put(name,main[field],0)
    put("EstadosEf",main.estados_tratados_efectivos,1)
    put("MediaPre",level.media_pre,2);put("SigmaPre",level.sigma_pre,2)
    put("PorcentajeUnoMas",100*np.expm1(main.efecto),1)
    put("MdePctNivel",100*level.mde/level.media_pre,1)
    put("MdePctNivelDoble",100*get(scale="niveles",cluster="entidad_fecha").mde/level.media_pre,1)
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
    joint=weekly.loc[weekly.escenario.eq('principal') & weekly.muestra.eq('emparejada') & weekly.escala.eq('log1p') & weekly.restricciones.eq('wk-4;wk-3;wk-1')]
    for cluster,name in [('entidad','Wald'),('entidad_fecha','WaldDoble')]:
        r=joint.loc[joint.agrupacion.eq(cluster)].iloc[0]
        put(name+'P',r.p);put(name+'Estado',texesc(r.estado))
    # Principal: niveles y log, d0 y d1 separados, y horizontes de persistencia.
    rows=[]
    for scale,label in [('log1p',r'$\log(1+Y)$'),('niveles','Niveles')]:
        for span in ['d0','d1','d0..1','d2..6','wk+1']:
            a,b=get(scale=scale,span=span),get(scale=scale,span=span,cluster='entidad_fecha')
            rows.append([label,span,result(a,False),result(b),fmt(a.efecto_sigma,3),fmt(b.mde,3)])
    table(tab/'causal_principales.tex',['Escala','Tramo',r'$\hat\beta$ (EE)',r'IC 95\% doble',r'$\beta/\sigma$', 'MDE doble'],rows)
    # Progresión con muestra fija, incluido el ajuste sin matching para los mismos tratados.
    rows=[]
    for method in ['comun_m0_m3','mismos_tratados','emparejada','emparejada_1a1']:
        for model in ['M0','M1','M2','M3']:
            log=get(method=method,model=model,cluster='entidad_fecha');lev=get(method=method,model=model,scale='niveles',cluster='entidad_fecha')
            rows.append([METHOD[method],model,fmt(log.tratados,0),fmt(log.n,0),result(log),result(lev)])
    table(tab/'causal_modelos.tex',['Controles','Modelo','T',r'$N$',r'$\log(1+Y)$, IC doble','Niveles, IC doble'],rows)
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
    table(tab/'causal_balance_prepost.tex',['Variable','Sin matching, mismos T','1:muchos','1:1'],before_after)
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
                    rows.append(['EIC 2015' if cut == 2015 else 'ITER 2020',name,f'{fmt(joined,0)}/{fmt(total,0)}',fmt(100*joined/total,1),f'{fmt(finite,0)}/{fmt(total,0)}'])
            else:
                rows.append([label,name,f'{fmt(matched,0)}/{fmt(n,0)}',fmt(100*matched/n,1),f'{fmt(usable,0)}/{fmt(n,0)}'])
            put('Union'+source.title()+name,f'{fmt(matched,0)}/{fmt(n,0)}')
    table(tab/'causal_uniones.tex',['Fuente','Rol','Unidas / elegibles',r'\%','Valor utilizable / elegibles'],rows)
    support=pd.read_csv(mod/'causal_soporte.csv')
    table(tab/'causal_soporte.tex',['Escenario','Método','T','C','Fechas','Episodios'],
          [[SCENARIO[r.escenario],METHOD[r.muestra],fmt(r.tratados,0),fmt(r.controles,0),fmt(r.fechas,0),fmt(r.episodios,0)]
           for r in support.loc[support.muestra.isin(['emparejada','emparejada_1a1'])].itertuples()])
    rows=[]
    for scenario in ['principal','sin_cinco','sin_laborales','sin_laborales_escolares','sin_pendientes','sin_todos_pendientes','sin_senales']:
        for method in ['emparejada','emparejada_1a1']:
            a=get(scenario=scenario,method=method,cluster='entidad_fecha')
            b=get(scenario=scenario,method=method,scale='niveles',cluster='entidad_fecha')
            rows.append([SCENARIO[scenario],METHOD[method],fmt(a.tratados,0),fmt(a.fechas,0),result(a),result(b)])
    table(tab/'causal_sensibilidades.tex',['Exclusión / muestra','Método','T','Fechas','Log, IC doble','Niveles, IC doble'],rows)
    rows=[]
    for scenario in ['principal','persistencia','placebo']:
        for method in ['emparejada','emparejada_1a1']:
            a=get(scenario=scenario,method=method,cluster='entidad_fecha')
            rows.append([SCENARIO[scenario],METHOD[method],fmt(a.tratados,0)]+[
                result(get(scenario=scenario,method=method,span=span,cluster='entidad_fecha')) for span in ['d0..1','d2..6','wk+1']])
    table(tab/'causal_persistencia.tex',['Selección','Método','T','d0..1','d2..6','wk+1'],rows)
    rows=[]
    for scale,label in [('log1p','Log'),('niveles','Niveles')]:
        for span in ['d0','d1','d0..1','d2..6','wk0','wk+1']:
            row=[label,span]
            for method in ['emparejada','emparejada_1a1']:
                row += [result(get(scenario='placebo',method=method,scale=scale,span=span,cluster='entidad_fecha')),
                        pvalue(get(scenario='placebo',method=method,scale=scale,span=span).p)]
            rows.append(row)
    table(tab/'causal_placebo.tex',['Escala','Horizonte','1:muchos, IC doble',r'$p_E$','1:1, IC doble',r'$p_E$'],rows)
    rows=[]
    for method in ['emparejada','emparejada_1a1']:
        for scale,label in [('log1p','Log'),('niveles','Niveles')]:
            for cluster,name in [('entidad','CRV1 estatal'),('entidad_fecha','CRV1 doble'),('CRV3','CRV3 estatal')]:
                r=get(method=method,scale=scale,cluster=cluster)
                rows.append([METHOD[method],label,name,result(r),fmt(r.gl,0),fmt(r.mde,3)])
    table(tab/'causal_inferencia.tex',['Método','Escala','Inferencia',r'd0..1, IC 95\%','gl','MDE'],rows)
    rows=[]
    for method in ['emparejada','emparejada_1a1']:
        for scale,label in [('log1p','Log'),('niveles','Niveles')]:
            r=weekly.loc[weekly.escenario.eq('principal') & weekly.muestra.eq(method) & weekly.escala.eq(scale) & weekly.restricciones.eq('wk-4;wk-3;wk-1')]
            for item in r.itertuples():
                rows.append([METHOD[method],label,'Estatal' if item.agrupacion=='entidad' else 'Doble',fmt(item.f,3),pvalue(item.p),fmt(item.rango,0),fmt(item.condicion,1),texesc(item.estado)])
    table(tab/'causal_previos.tex',['Método','Escala','Agrupación','F','p','Rango',r'$\kappa$','Estado'],rows)
    # Referencia b=-2 separa cambio de base, muestra e inventario.
    legacy=pd.read_csv(mod/'comparaciones_municipales.csv')
    rows=[]
    for method in ['emparejada','emparejada_1a1']:
        old=legacy.loc[legacy.diseno.eq('principal') & legacy.muestra.eq(method) & legacy.h.eq(0)].iloc[0]
        a=get(method=method,scale='niveles',span='d0',base='-2')
        b=get(method=method,scale='niveles',span='d0')
        rows.append([METHOD[method],fmt(old.tratados,0),result(old),fmt(a.tratados,0),result(a),result(b)])
    table(tab/'causal_trazabilidad.tex',['Método','T auditada','Auditada: d0, b=-2','T final','Final: d0, b=-2','Final: d0, base limpia'],rows)
    rows=[]
    for method in ['emparejada','emparejada_1a1']:
        for scale,label in [('log1p','Log'),('niveles','Niveles')]:
            rows.append([METHOD[method],label]+[result(get(method=method,scale=scale,base=base,cluster='entidad_fecha'))
                                               for base in ['-2','tres_semanas','wk-1']])
    table(tab/'causal_bases.tex',['Método','Escala','b=-2','Tres semanas','wk-1'],rows)
    # Donantes de Morelia: listas completas y todas las etapas reproducibles.
    final_edges=pd.read_csv(mod/'causal_vinculos.csv',dtype={'tratado_clave':str,'control_clave':str},parse_dates=['indice'])
    old_edges=pd.read_csv(mod/'reparto_controles.csv',dtype={'tratado_clave':str,'control_clave':str},parse_dates=['indice'])
    morelia=[]
    for scenario,frame,field in [('auditada',old_edges,'diseno'),('principal',final_edges,'escenario'),('sin_senales',final_edges,'escenario')]:
        subset=frame.loc[frame[field].eq('principal' if scenario=='auditada' else scenario) & frame.muestra.eq('emparejada') & frame.tratado_clave.eq('16053') & frame.indice.eq('2025-04-23')]
        for r in subset.itertuples(): morelia.append(dict(escenario=scenario,control_clave=r.control_clave,contribucion=r.contribucion))
    pd.DataFrame(morelia).to_csv(mod/'causal_morelia_donantes.csv',index=False)
    for scenario,name in [('auditada','MoreliaAntes'),('principal','MoreliaDespues'),('sin_senales','MoreliaSenales')]:
        put(name,len([r for r in morelia if r['escenario']==scenario]),0)
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
    table(tab/'causal_calendario.tex',['Inicio','T','LFT en d0..1','SEP en d0..1','Cinco auditadas'],
          [[str(d.date()),fmt(r.tratados,0),'Sí' if r.laboral else 'No','Sí' if r.escolar else 'No','Sí' if r.cinco else 'No'] for d,r in dates.iterrows()])
    # Omisiones estatales del principal, sin rematching ni renormalizar pesos.
    loo=pd.read_csv(mod/'causal_omision_estado.csv',dtype={'estado_omitido':str,'tramo':str})
    pick=loo.loc[loo.muestra.eq('emparejada') & loo.modelo.eq('M0') & loo.tramo.eq('d0..1')].pivot(index='estado_omitido',columns='escala',values='efecto')
    table(tab/'causal_omision.tex',['Estado omitido','Log d0..1','Niveles d0..1'],[[state,fmt(r.log1p,3),fmt(r.niveles,3)] for state,r in pick.iterrows()])
    cul=pd.read_csv(mod/'culiacan_soporte.csv').iloc[0]
    gap=pd.read_csv(mod/'culiacan.csv')
    observed=gap.loc[gap.semana.ge(0) & gap.brecha.notna()]
    for name,value in [('CulDonantes',cul.comparadores_usados),('CulObs',cul.semanas_post_observadas),('CulTotal',cul.semanas_post_totales)]: put(name,value,0)
    put('CulBrecha',observed.brecha.mean(),2)
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
    table(tab/'causal_perdidas.tex',['Paso, orden jerárquico','T restantes','T excluidos'],loss_rows)
    (tab/'causal_cifras.tex').write_text(''.join(r'\newcommand{\R'+k+'}{'+v+'}\n' for k,v in macros.items()),encoding='utf-8')
    print('Tablas autocontenidas del diseño final generadas.')


def figures(config):
    import matplotlib.pyplot as plt
    from .graficas import save, BLUE, ACCENT
    out=config['paths']['outputs']
    e=pd.read_csv(out/'modelos/causal_efectos.csv',dtype={'tramo':str})
    e=e.loc[e.escenario.eq('principal') & e.base.eq('tres_semanas') & e.modelo.eq('M0') & e.agrupacion.eq('entidad_fecha')]
    fig,axes=plt.subplots(2,1,figsize=(7.35,4.6),layout='constrained',sharex=True)
    for ax,scale,label in zip(axes,['log1p','niveles'],['Cambio en log(1 + registros)','Registros por municipio y día']):
        for method,color,offset,name in [('emparejada',BLUE,-.10,'1:muchos'),('emparejada_1a1',ACCENT,.10,'1:1')]:
            rows=e.loc[e.muestra.eq(method) & e.escala.eq(scale) & e.tramo.isin([str(h) for h in range(-7,14)])].copy()
            rows['h']=rows.tramo.astype(int);rows=rows.sort_values('h')
            ax.errorbar(rows.h+offset,rows.efecto,yerr=[rows.efecto-rows.ic_inf,rows.ic_sup-rows.efecto],fmt='o-',
                        color=color,markersize=2.8,linewidth=.8,elinewidth=.7,capsize=1.5,label=name)
        ax.axhline(0,color='#555555',linewidth=.6);ax.axvline(-.5,color='#555555',linestyle='--',linewidth=.7)
        ax.set_ylabel(label,fontsize=9);ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False)
    axes[0].legend(frameon=False,ncols=2,fontsize=9)
    axes[0].set_title('Base de tres semanas del mismo día; IC 95 % de dos vías',fontsize=11)
    axes[1].set_xlabel('Día respecto al inicio local');axes[1].set_xticks([-7,-5,-2,0,1,3,6,9,13])
    save(fig,out/'figuras','causal_dinamica')
