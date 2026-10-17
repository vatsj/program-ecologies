#!/bin/zsh
# Identity-resistant target cells (notes §1.6, §2.5): Parts I and II, then Part III (800, 8), then (1,600, 8). Resumable.
cd "$(dirname "$0")/../.."
python3 src/identity_resistant_run.py cells --out eps0 --runs 20 --workers 3 --cells \
  ir_ff_L_snon ir_ff_Rm_snon ir_ff_Rp_snon ir_ff_L_spon ir_ff_Rm_spon ir_ff_Rp_spon \
  ir_isl_L_snon_200_64 ir_isl_Rm_snon_200_64 ir_isl_Rp_snon_200_64 ir_isl_L_spon_200_64 ir_isl_Rm_spon_200_64 ir_isl_Rp_spon_200_64 \
  >> runs/identity_resistant/cells_eps0.log 2>&1
python3 src/identity_resistant_run.py cells --out rain800 --runs 40 --workers 3 --cells \
  ir_rain_ann_L_800 ir_rain_ann_Rm_800 ir_rain_ann_Rp_800 ir_rain_const_L_800 ir_rain_const_Rm_800 ir_rain_const_Rp_800 \
  >> runs/identity_resistant/cells_rain800.log 2>&1
python3 src/identity_resistant_run.py cells --out rain1600 --runs 40 --workers 3 --cells \
  ir_rain_ann_L_1600 ir_rain_ann_Rm_1600 ir_rain_const_L_1600 ir_rain_const_Rm_1600 \
  >> runs/identity_resistant/cells_rain1600.log 2>&1
