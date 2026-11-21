import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from choques.causal import baseline_offsets, contrasts, transform, select_pre, jackknife, predicted_coverage, calendar_flags
from choques.modelos import Matrix, caliber_mask
from choques.persistente import territorial_donors
from choques.seleccion import match, one_to_one


class FinalDesign(unittest.TestCase):
    def test_official_calendar_distinguishes_labor_school_and_weekends(self):
        root=Path(__file__).resolve().parents[1]
        flags=calendar_flags(root,pd.to_datetime(['2023-01-05','2025-04-23','2025-07-26','2024-10-01','2025-10-01','2025-02-03','2025-09-28'])).set_index('fecha')
        for date in ['2023-01-05','2025-04-23','2025-07-26']:
            self.assertTrue(flags.loc[date,'escolar'])
            self.assertFalse(flags.loc[date,'laboral'])
        self.assertTrue(flags.loc['2024-10-01','laboral'])
        self.assertFalse(flags.loc['2025-10-01','laboral'])
        self.assertTrue(flags.loc['2025-02-03','laboral'])
        self.assertFalse(flags.loc['2025-09-28','escolar'])

    def test_weekday_reference_and_clean_limits(self):
        for h in range(-28, 29):
            refs = baseline_offsets(h)
            self.assertEqual(len(set(refs)), 3)
            self.assertTrue(all(-28 <= b <= -8 and (h-b) % 7 == 0 for b in refs))
        self.assertEqual(baseline_offsets(1), (-27, -20, -13))
        self.assertEqual(baseline_offsets(13), (-22, -15, -8))
        # Datos de los mismos lunes en tres semanas, más un lunes tratado.
        t = pd.Timestamp('2023-06-05')
        dates = pd.date_range(t-pd.Timedelta(days=28), t+pd.Timedelta(days=13))
        panel = pd.DataFrame(dict(clave='01001', fecha=dates, accidentes=0., continuidad=True))
        panel.loc[panel.fecha.isin([t-pd.Timedelta(days=b) for b in (28,21,14)]), 'accidentes'] = [0,3,8]
        panel.loc[panel.fecha.eq(t), 'accidentes'] = 3
        sample = pd.DataFrame(dict(clave=['01001'], indice=[t]))
        actual = contrasts(Matrix(panel), sample, 'log1p', spans={'d0':(0,)})[0,0]
        self.assertAlmostEqual(actual, np.log(4) - (np.log(1)+np.log(4)+np.log(9))/3)

    def test_log_zero_and_invalid(self):
        np.testing.assert_allclose(transform([0,1,3], 'log1p'), [0,np.log(2),np.log(4)])
        for invalid in ([np.nan], [-1], [np.inf]):
            with self.assertRaises(ValueError): transform(invalid, 'log1p')

    def test_heterogeneous_treated_caliber_and_matching(self):
        rows = [('09001',1,1),('09002',1,25)]
        rows += [(f'{s:02}001',0,1) for s in (1,2)] + [(f'{s:02}001',0,25) for s in (3,4)]
        sample = pd.DataFrame(rows, columns=['clave','tratado','pre_nivel']).assign(
            indice=pd.Timestamp('2023-01-20'), id_episodio='x', peso=1., poblacion=100., empleo_mil=10., autos_mil=20.)
        sample['estado'] = sample.clave.str[:2]
        matched, diagnostic, edges = match(sample, {'individual_caliber':True,'min_controls':2,'min_control_states':2})
        pairs = edges.groupby('tratado_clave').control_clave.apply(set).to_dict()
        self.assertEqual(pairs, {'09001':{'01001','02001'},'09002':{'03001','04001'}})
        paired, chosen = one_to_one(matched, edges)
        self.assertEqual(set(paired.loc[paired.tratado.eq(1),'clave']), {'09001','09002'})
        self.assertEqual(chosen.control_clave.tolist(), ['01001','03001'])
        np.testing.assert_array_equal(caliber_mask([1,25], 1), [True,False])
        np.testing.assert_allclose(matched.groupby('tratado').peso.sum(), [2,2])

    def test_eligibility_invariant_to_future(self):
        dates=pd.date_range('2020-12-01','2021-08-31')
        keys=['01001','02001','03001']
        p=pd.MultiIndex.from_product([keys,dates],names=['clave','fecha']).to_frame(index=False)
        p=p.assign(accidentes=1.,continuidad=True)
        t=pd.Timestamp('2021-06-15')
        reported=p[['clave','fecha']].copy()
        invalid=pd.DataFrame({'clave':pd.Series(dtype=str),'anio':pd.Series(dtype=int),'mes':pd.Series(dtype=float)})
        events=pd.DataFrame([('A','01001','01',t,t,'confirmado','extensa')],columns=['id_episodio','clave','cve_ent','inicio','fin','estado','clase_final'])
        changes=pd.DataFrame({'origen':pd.Series(dtype=str),'destino':pd.Series(dtype=str),'fecha':pd.to_datetime([]),'codigo':pd.Series(dtype=str)})
        args=(events,reported,invalid,changes,{})
        initial,di=select_pre(Matrix(p),Matrix(p),*args)
        altered=p.copy()
        altered.loc[altered.fecha.ge(t), ['accidentes','continuidad']]=[np.nan,False]
        future=events.iloc[[0]].assign(id_episodio='B',clave='02001',cve_ent='02',inicio=t+pd.Timedelta(days=1),fin=t+pd.Timedelta(days=1))
        later_invalid=pd.DataFrame({'clave':['02001'],'anio':[2021],'mes':[7]})
        later,da=select_pre(Matrix(altered),Matrix(p),pd.concat([events,future]),reported.loc[reported.fecha.lt(t)],later_invalid,changes,{})
        # Comparar la cohorte original: un nuevo episodio futuro crea su propia cohorte.
        pd.testing.assert_frame_equal(initial.reset_index(drop=True),later.loc[later.indice.eq(t)].reset_index(drop=True))
        self.assertTrue(initial.tratado.sum()==1)
        selected,_=select_pre(Matrix(altered),Matrix(p),*args,persistence=True)
        self.assertTrue(selected.empty)
        old=predicted_coverage(pd.Index(keys),reported,invalid,t)
        new=predicted_coverage(pd.Index(keys),reported.loc[reported.fecha.lt(t)],later_invalid,t)
        np.testing.assert_array_equal(old,new)
        # Un filtro posterior no debe habilitar un antecedente del mismo id.
        clue=events.iloc[[0]].assign(clave='',inicio=t-pd.Timedelta(days=1),fin=t-pd.Timedelta(days=1),estado='pendiente',clase_final='incierta')
        catalog=pd.concat([events,clue],ignore_index=True)
        before,_=select_pre(Matrix(p),Matrix(p),catalog,reported,invalid,changes,{})
        after,_=select_pre(Matrix(p),Matrix(p),catalog,reported,invalid,changes,{},persistence=True)
        self.assertTrue(before.empty and after.empty)
        # Tampoco permite como donante una expansión posterior del episodio focal.
        donor=events.iloc[[0]].assign(clave='02001',cve_ent='02',inicio=t+pd.Timedelta(days=1),fin=t+pd.Timedelta(days=1),estado='pendiente',clase_final='incierta')
        isolated,_=select_pre(Matrix(p),Matrix(p),pd.concat([events,donor]),reported,invalid,changes,{},persistence=True)
        self.assertNotIn('02001',set(isolated.clave))
        self.assertIn('03001',set(isolated.clave))

    def test_villa_de_pozos_week_and_boundaries(self):
        keys=pd.Index(['24028','24059','01001','31094'])
        changes=pd.DataFrame({'origen':['24028','31094'],'destino':['24059','31094'],
                              'fecha':pd.to_datetime(['2024-08-30','2024-08-30']),'codigo':['M','W']})
        np.testing.assert_array_equal(territorial_donors(keys,changes,pd.Timestamp('2024-08-26'),pd.Timestamp('2024-09-01')),[False,False,True,True])
        self.assertTrue(territorial_donors(keys,changes,pd.Timestamp('2024-09-02'),pd.Timestamp('2024-09-08')).all())
        self.assertFalse(territorial_donors(keys,changes,pd.Timestamp('2024-08-30'),pd.Timestamp('2024-08-30'))[0])

    def test_synthetic_known_effect_and_jackknife_refits(self):
        from choques.estadistica import estimate
        rng=np.random.default_rng(15)
        frame=pd.DataFrame([(d,str(g),int(g<2),1.) for d in range(7) for g in range(6) for _ in range(3)],columns=['indice','estado','tratado','peso'])
        frame['peso']=1+frame.estado.astype(int)*.3+frame.indice*.07
        y=(frame.indice + 2*frame.tratado + rng.normal(0,.01,len(frame))).to_numpy()[:,None]
        b,_,_=estimate(frame,['tratado'],y,{})
        self.assertAlmostEqual(b[0,0],2,places=2)
        v,states,replicas=jackknife(frame,['tratado'],y,{})
        oracle=[]
        for g in states:
            keep=frame.estado.ne(g).to_numpy(); sub=frame.loc[keep]
            X=np.column_stack([sub.tratado,pd.get_dummies(sub.indice,dtype=float)])
            w=np.sqrt(sub.peso.to_numpy())[:,None]
            oracle.append(np.linalg.lstsq(X*w,y[keep]*w,rcond=None)[0][0,0])
        np.testing.assert_allclose(replicas[:,0,0],oracle,atol=1e-12)
        self.assertAlmostEqual(v[0,0],5/6*np.square(np.asarray(oracle)-b[0,0]).sum())

    def test_synthetic_full_design_recovers_immediate_effect(self):
        from choques.estadistica import estimate
        t=pd.Timestamp('2021-06-15')
        dates=pd.date_range('2020-12-01','2021-08-31')
        keys=['09001','01001','02001','03001']
        panel=pd.MultiIndex.from_product([keys,dates],names=['clave','fecha']).to_frame(index=False)
        panel=panel.assign(accidentes=1.,continuidad=True)
        panel.loc[panel.clave.eq('09001') & panel.fecha.isin([t,t+pd.Timedelta(days=1)]),'accidentes']=3.
        events=pd.DataFrame([('A','09001','09',t,t,'confirmado','extensa')],columns=['id_episodio','clave','cve_ent','inicio','fin','estado','clase_final'])
        invalid=pd.DataFrame({'clave':pd.Series(dtype=str),'anio':pd.Series(dtype=int),'mes':pd.Series(dtype=float)})
        changes=pd.DataFrame({'origen':pd.Series(dtype=str),'destino':pd.Series(dtype=str),'fecha':pd.to_datetime([]),'codigo':pd.Series(dtype=str)})
        matrix=Matrix(panel)
        candidates,_=select_pre(matrix,matrix,events,panel[['clave','fecha']],invalid,changes,{})
        candidates=candidates.assign(poblacion=100.,empleo_mil=10.,autos_mil=20.)
        sample,_,edges=match(candidates,{'individual_caliber':True,'min_controls':2,'min_control_states':2})
        self.assertEqual(len(edges),3)
        y=contrasts(matrix,sample,'niveles',spans={'inmediato':(0,1),'posterior':tuple(range(2,7))})
        b,_,_=estimate(sample,['tratado'],y,{})
        np.testing.assert_allclose(b[:,0],[2,0],atol=1e-12)
        y=contrasts(matrix,sample,'log1p',spans={'inmediato':(0,1)})
        b,_,_=estimate(sample,['tratado'],y,{})
        self.assertAlmostEqual(b[0,0],np.log(2))


if __name__=='__main__': unittest.main()
