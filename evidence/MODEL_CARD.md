# Model card — frozen WFP snapshot

## Intended use

Educational exploration of monthly Bangladesh retail food prices. Forecasts are point estimates for one month after the commodity's last source month, only when a market reaches that cutoff and all exact lags exist. Not current daily prices, trade signals, official policy evidence or guaranteed future prices.

## Selection and feature construction

Four exact commodities: Rice (coarse), Lentils (masur), Wheat flour, Oil (palm). Retail/BDT only. KG for the first three and L for palm oil. Exclude market names containing `Division`; retain actual and aggregate flags. Preserve positive source prices without manual outlier editing. Convert monthly reporting dates to month-start labels. No forward filling, interpolation or smoothing is applied.

Each market is reindexed to a monthly calendar before generating lags. Required lag months: 1, 2, 3, 6, 12. Features: lag1, lag2/lag1, lag3/lag1, lag6/lag1, lag12/lag1, calendar-month sine/cosine. Target: price / lag1. A single model is pooled across eligible markets for each commodity; market ID is not a numerical model feature. All features at time t use observations strictly earlier than t.

## Fixed models

- Persistence: previous month's price.
- Seasonal naive: same month one year earlier.
- Random Forest: 160 trees, max depth 10, min leaf 8, random seed 42.
- XGBoost: 160 trees, max depth 3, learning rate .035, subsample .9, seed 42, squared-error objective.

Parameters were fixed for this project. There is no hyperparameter search, external covariate feed or causal economic model.

## Evaluation procedure

Relative to the latest source month **per commodity**, reserve the preceding 18 calendar months: first 6 validation, last 12 test. Train first on earlier rows; choose the model using validation MAE alone. Refit each ML method on train+validation before a fixed rolling one-step test. Test row features use preceding observed prices, including earlier observations inside the test window. The model weights are not retrained at each test month. This tests monthly updates with newly observed lags, not a single twelve-month-ahead path. A single-month target is never included in its own features.

Rows missing any required lag are dropped from train/validation/test; therefore some calendar months and many markets are not represented. `model_metrics.csv` gives the actual eligible row counts and actual first/last target dates. Pooled errors may be dominated by better-covered markets and do not establish reliable performance for every named market. We have not quantified independent confidence intervals or statistical significance.

The raw dataset snapshot may include retrospective revisions and aggregated measurements. Time splitting prevents direct target leakage in the constructed features but does not reconstruct data vintages that would have been available historically. This is **not** a vintage-safe operational backtest. There is no independent field validation.

## Results and choice

See `model_metrics.csv` for all four methods, validation MAE, test MAE/RMSE/sMAPE, dates and counts. `holdout_predictions.csv` includes every test actual/prediction pair. Persistence achieved the lowest validation and test MAE for every commodity; it is the default. Tree models do not demonstrate added predictive value here.

Wheat flour has noticeably larger RMSE than MAE, indicating sensitivity to larger errors. Source anomalies were not silently repaired. Test errors are in BDT/unit and must not be compared across commodities as if their scales were identical. sMAPE is a descriptive error measure, not an accuracy probability.

## Final snapshot and unavailable forecasts

After evaluation, RF and XGBoost are fitted on all eligible history for each commodity, with their parameters unchanged. Final snapshots are generated only for market series at the commodity's last source month, with all five exact lag months present for the next target. Models are not applied to an older market cutoff using later pooled training information. Older/incomplete series return unavailable. For this snapshot, 132 of 361 series have all four forecast methods available.

The website only displays these precomputed values. It does not load serialized models or accept arbitrary forecast inputs. Run `ml/train.py` and `build_demo.py` to reproduce or deliberately refresh the snapshot. Model feature importances are included in the JSON, but are associations, not price-driver explanations.

## Before operational use

Obtain current, well-defined market observations; evaluate source quality and vintage availability; test multiple rolling origins and shock periods; examine per-market errors and subgroup coverage; benchmark simpler methods; quantify uncertainty using an appropriate temporal protocol; seek independent domain review. No such operational validation is claimed by this release.
