#!/bin/bash
# Final master encode from the two intact first-level merged files. Re-runnable: skips a language whose final file already exists.
#   final_encode.sh en ta
R=/tmp/claude-0/-home-user/ef44bfcb-cb40-5359-811e-3fd71bd9ae14/scratchpad/ussr; cd $R
for L in "$@"; do
  [ -s out/${L}_full.mp4 ] && { echo "$L: already done"; continue; }
  A=build/tmp_join/${L}_L1_0.mp4; B=build/tmp_join/${L}_L1_8.mp4
  D0=$(python3 -I -c "import subprocess;d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','$A'],capture_output=True,text=True).stdout);print(f'{d-0.5:.3f}')")
  TOT=$(python3 -I -c "import json;sb=json.load(open('build/sb_full_$L.json'));print(f'{sum(s[\"dur\"] for s in sb[\"scenes\"])+0.5:.3f}')")
  FO=$(python3 -I -c "print(f'{$TOT-0.8:.3f}')")
  echo "$(date +%T) $L: d0=$D0 total=$TOT fadeout_at=$FO"
  rm -f out/${L}_full.mp4.part
  ffmpeg -y -loglevel error -stats -i $A -i $B -i audio/${L}_full_mix.wav \
    -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=$D0,fade=t=in:st=0:d=0.6,fade=t=out:st=$FO:d=0.8[v];[2:a]aresample=48000,adelay=500|500,apad[a]" \
    -map "[v]" -map "[a]" -t $TOT -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -f mp4 out/${L}_full.mp4.part \
    && mv out/${L}_full.mp4.part out/${L}_full.mp4 && echo "$(date +%T) $L: DONE $(du -h out/${L}_full.mp4 | cut -f1)" || echo "$(date +%T) $L: FAILED"
done
echo ALLFINISHED
