"""Reproduce rolling one-month-ahead forecasting on a frozen WFP snapshot.
No interpolation, future fill, shuffled split, or tuning on test targets.
"""
from pathlib import Path
import json, hashlib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'prices_raw.csv'
NAMES={'Rice (coarse)':('rice','চাল','Rice · coarse','KG'),'Lentils (masur)':('lentils','মসুর ডাল','Lentils · masur','KG'),'Wheat flour':('flour','আটা','Wheat flour','KG'),'Oil (palm)':('oil','পাম তেল','Palm oil','L')}
FEATURES=['lag1','ratio2','ratio3','ratio6','ratio12','month_sin','month_cos']
def features(s):
 d=pd.DataFrame({'price':s})
 for k in [1,2,3,6,12]:d[f'lag{k}']=s.shift(k)
 for k in [2,3,6,12]:d[f'ratio{k}']=d[f'lag{k}']/d.lag1
 d['month_sin']=np.sin(d.index.month*2*np.pi/12);d['month_cos']=np.cos(d.index.month*2*np.pi/12)
 return d

def models():
 return {'Random Forest':RandomForestRegressor(n_estimators=160,min_samples_leaf=8,max_depth=10,random_state=42,n_jobs=2), 'XGBoost':XGBRegressor(n_estimators=160,max_depth=3,learning_rate=.035,subsample=.9,colsample_bytree=1,objective='reg:squarederror',random_state=42,n_jobs=2)}

def run():
 raw=pd.read_csv(RAW);p=raw[raw.commodity.isin(NAMES)&raw.pricetype.eq('Retail')&raw.currency.eq('BDT')&~raw.market.str.contains('Division',na=False)].copy()
 p=p[((p.commodity.eq('Oil (palm)'))&p.unit.eq('L'))|((~p.commodity.eq('Oil (palm)'))&p.unit.eq('KG'))]
 p=p[p.priceflag.isin(['actual','aggregate','actual,aggregate']) & pd.to_numeric(p.price,errors='coerce').gt(0)]
 p['date']=pd.to_datetime(p.date).dt.to_period('M').dt.to_timestamp();assert not p.duplicated(['date','market_id','commodity']).any()
 p=p.sort_values(['commodity','market_id','date']);p.to_csv(ROOT/'data/selected_prices.csv',index=False)
 allseries=[];allmetrics=[];predictions=[]
 for cname,(cid,bn,label,unit) in NAMES.items():
  cp=p[p.commodity.eq(cname)];frames=[];series=[]
  for mid,g in cp.groupby('market_id'):
   s=g.set_index('date').price.sort_index();s=s.reindex(pd.date_range(s.index.min(),s.index.max(),freq='MS'))
   d=features(s);d['market_id']=int(mid);frames.append(d.dropna(subset=FEATURES+['price']).reset_index(names='date'))
   series.append((int(mid),g,s))
  d=pd.concat(frames,ignore_index=True);end=cp.date.max();valstart=end-pd.DateOffset(months=17);teststart=end-pd.DateOffset(months=11)
  train=d[d.date<valstart];val=d[(d.date>=valstart)&(d.date<teststart)];test=d[d.date>=teststart]
  assert train.date.max()<val.date.min() and val.date.max()<test.date.min()
  def baseline(z,n):return z.lag1.to_numpy() if n=='Persistence' else z.lag12.to_numpy()
  vp={n:baseline(val,n) for n in ['Persistence','Seasonal naive']}
  for n,m in models().items():m.fit(train[FEATURES],train.price/train.lag1);vp[n]=m.predict(val[FEATURES])*val.lag1.to_numpy()
  selected=min(vp,key=lambda n:mean_absolute_error(val.price,vp[n]))
  dev=pd.concat([train,val]);tp={n:baseline(test,n) for n in ['Persistence','Seasonal naive']}
  fitted=models()
  for n,m in fitted.items():m.fit(dev[FEATURES],dev.price/dev.lag1);tp[n]=m.predict(test[FEATURES])*test.lag1.to_numpy()
  metrics=[]
  for n,ys in tp.items():
   r={'commodity':cid,'model':n,'validation_mae':round(float(mean_absolute_error(val.price,vp[n])),4),'test_mae':round(float(mean_absolute_error(test.price,ys)),4),'test_rmse':round(float(np.sqrt(mean_squared_error(test.price,ys))),4),'test_smape':round(float(np.mean(200*np.abs(ys-test.price)/(np.abs(ys)+np.abs(test.price)))),2),'train_rows':len(train),'validation_rows':len(val),'test_rows':len(test),'train_end':str(train.date.max().date()),'validation_start':str(val.date.min().date()),'validation_end':str(val.date.max().date()),'test_start':str(test.date.min().date()),'test_end':str(test.date.max().date()),'selected_on_validation':n==selected}
   metrics.append(r);allmetrics.append(r)
   for date,mid,y,yp in zip(test.date,test.market_id,test.price,ys):predictions.append({'commodity':cid,'model':n,'date':str(date.date()),'market_id':int(mid),'actual':float(y),'prediction':float(yp)})
  finals=models()
  for n,m in finals.items():m.fit(d[FEATURES],d.price/d.lag1)
  import joblib
  for n,m in finals.items():joblib.dump(m,ROOT/'ml'/f'{cid}_{n.replace(" ","_")}.joblib',compress=3)
  for mid,g,s in series:
   nextdate=s.index.max()+pd.offsets.MonthBegin(1);future=s.reindex(pd.date_range(s.index.min(),nextdate,freq='MS'));row=features(future).iloc[[-1]]
   eligible=(s.index.max()==end) and not row[FEATURES].isna().any(axis=None);forecasts={}
   if eligible:
    forecasts={'Persistence':float(row.lag1.iloc[0]),'Seasonal naive':float(row.lag12.iloc[0])}
    forecasts.update({n:float(m.predict(row[FEATURES])[0]*row.lag1.iloc[0]) for n,m in finals.items()})
   hist=[{'date':str(r.date.date())[:7],'price':round(float(r.price),2),'flag':r.priceflag} for r in g.itertuples()]
   allseries.append({'id':f'{cid}-{mid}','commodity':cid,'bn':bn,'label':label,'unit':unit,'market_id':mid,'market':g.market.iloc[0],'division':g.admin1.iloc[0],'history':hist,'forecast_date':str(nextdate.date())[:7],'forecasts':{n:round(v,2) for n,v in forecasts.items()},'forecast_reason':('Available' if eligible else 'Older market history or missing exact monthly lag values; no forecast is issued.'),'selected_model':selected,'metrics':metrics,'feature_importance':{n:{f:round(float(v),4) for f,v in zip(FEATURES,m.feature_importances_)} for n,m in finals.items()}})
  print(label,len(d),'selected',selected,[(r['model'],r['test_mae']) for r in metrics])
 pd.DataFrame(allmetrics).to_csv(ROOT/'evidence/model_metrics.csv',index=False);pd.DataFrame(predictions).to_csv(ROOT/'evidence/holdout_predictions.csv',index=False)
 meta={'source':'World Food Programme via HDX','url':'https://data.humdata.org/dataset/wfp-food-prices-for-bangladesh','license':'CC BY-IGO','retrieved':'2026-10-16','raw_sha256':hashlib.sha256(RAW.read_bytes()).hexdigest(),'raw_rows':len(raw),'selected_rows':len(p),'series':len(allseries),'last_month':str(p.date.max().date())[:7],'first_month':str(p.date.min().date())[:7],'flags':p.priceflag.value_counts().to_dict(),'method':'Monthly Retail BDT, four named commodities; exclude Division pseudo-markets; exact KG/L units. Keep actual and aggregate flags, no invented observations. Missing months stay missing. Seven lag/season features; target next-month price / last-month price. Fixed chronological train/6-month validation/12-month test per commodity. Select by validation MAE only; fit once before test; rolling test uses preceding observed lags. Refit on all data for next-month snapshot forecasts. Historical snapshot may include revisions; this is not vintage-safe operational backtesting. Markets share one commodity model; MAE is pooled, not guaranteed per market.'}
 (ROOT/'data/dashboard.json').write_text(json.dumps({'meta':meta,'series':allseries},ensure_ascii=False,separators=(',',':')),encoding='utf-8')
 (ROOT/'evidence/provenance.json').write_text(json.dumps(meta,indent=2))
if __name__=='__main__':run()
