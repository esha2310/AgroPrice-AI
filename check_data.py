"""Verify provenance, chronology, forecasts and reported holdout error."""
from pathlib import Path
import json,hashlib
import pandas as pd
import numpy as np
from ml.train import features,FEATURES
R=Path(__file__).resolve().parent
d=json.loads((R/'data/dashboard.json').read_text());m=pd.read_csv(R/'evidence/model_metrics.csv');p=pd.read_csv(R/'evidence/holdout_predictions.csv')
assert hashlib.sha256((R/'prices_raw.csv').read_bytes()).hexdigest()==d['meta']['raw_sha256']
assert len({s['id'] for s in d['series']})==len(d['series'])
assert not p.duplicated(['commodity','model','date','market_id']).any()
for r in m.itertuples():
 assert r.train_end<r.validation_start<=r.validation_end<r.test_start<=r.test_end
 q=p[(p.commodity==r.commodity)&(p.model==r.model)]
 assert len(q)==r.test_rows
 assert abs(np.abs(q.actual-q.prediction).mean()-r.test_mae)<.0001
for s in d['series']:
 h=s['history'];assert [x['date'] for x in h]==sorted(set(x['date'] for x in h));assert all(x['price']>0 for x in h)
 assert s['forecast_date']>h[-1]['date'];assert all(np.isfinite(v) and v>0 for v in s['forecasts'].values())
 assert s['selected_model']==min(s['metrics'],key=lambda x:x['validation_mae'])['model']
# Alter a target at t: its lag features must remain identical at t.
series=pd.Series(np.arange(1,26,dtype=float),index=pd.date_range('2020-01-01',periods=25,freq='MS'))
a=features(series);series.iloc[18]=10000;b=features(series);assert np.allclose(a.iloc[18][FEATURES].to_numpy(float),b.iloc[18][FEATURES].to_numpy(float))
# A missing exact lag remains missing, rather than shifting an older observation forward.
series.iloc[17]=np.nan;assert pd.isna(features(series).iloc[18].lag1)
print('PASS: checksum, unique rows, temporal split, lag causality, missing-month handling, predictions and recomputed MAE.',len(d['series']),'series;',len(p),'held-out model predictions.')
