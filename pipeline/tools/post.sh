#!/bin/bash
# Extras cut from a finished master.   post.sh <en|ta> <teaser|p720|parts>
R=/tmp/claude-0/-home-user/ef44bfcb-cb40-5359-811e-3fd71bd9ae14/scratchpad/ussr; cd $R; L=$1; M=out/${L}_full.mp4
case "$2" in
 teaser)   # first 65 s (the prologue), wide and vertical (blurred-background) versions, CRF 23
   ffmpeg -y -loglevel error -i $M -t 65 -vf "fade=t=out:st=64:d=1" -af "afade=t=out:st=63.5:d=1.5" -c:v libx264 -crf 23 -preset medium -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart out/${L}/teaser_wide_${L}.mp4
   ffmpeg -y -loglevel error -i $M -t 65 -filter_complex "[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:6[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,fade=t=out:st=64:d=1[v]" -map "[v]" -map 0:a -af "afade=t=out:st=63.5:d=1.5" -c:v libx264 -crf 23 -preset medium -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart out/${L}/teaser_vertical_${L}.mp4 ;;
 p720)     ffmpeg -y -loglevel error -i $M -vf scale=1280:720:flags=lanczos -c:v libx264 -crf 23 -preset medium -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart out/${L}/video_${L}_720p.mp4 ;;
 p1080)    # chat-sized 1080p copy (under the 500 MiB send limit): same picture size, CRF 21
   ffmpeg -y -loglevel error -i $M -c:v libx264 -crf 21 -preset medium -pix_fmt yuv420p -c:a copy -movflags +faststart -f mp4 out/${L}/video_${L}_1080p_light.mp4.part && mv out/${L}/video_${L}_1080p_light.mp4.part out/${L}/video_${L}_1080p_light.mp4 ;;
 parts)    mkdir -p out/${L}/parts; rm -f out/${L}/parts/*; split -b 94371840 -d -a 2 $M out/${L}/parts/the_fall_of_the_soviet_union_${L}.mp4.part-
           (cd out/${L}/parts && sha256sum the_fall_of_the_soviet_union_${L}.mp4.part-* > SHA256SUMS.txt && echo "$(sha256sum ../../${L}_full.mp4 | cut -d' ' -f1)  the_fall_of_the_soviet_union_${L}.mp4 (all parts joined)" >> SHA256SUMS.txt) ;;
esac
