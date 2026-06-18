#!/bin/zsh
set -eu

workspace='/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Tools history/Claude code Desktop Sonnet 4.6'
output_dir="$workspace/outputs/03Test Outputs"
julia_bin='/Users/vangogh/.julia/juliaup/julia-1.12.6+0.aarch64.apple.darwin14/Julia-1.12.app/Contents/Resources/julia/bin/julia'
script="$workspace/Test3 by sonnet4.6high ae_analysis.jl"

export GKSwstype=100
"$julia_bin" --project="$output_dir" "$script"

expected=(
  '01_ct07_strain_stress.png'
  '02_ct07_normalised_rms.png'
  '03_ct07_normalised_cumulative_rms.png'
  '04_ct07_normalised_ae_energy.png'
  '05_ct07_normalised_cumulative_ae_energy.png'
)

for filename in "${expected[@]}"; do
  test -s "$output_dir/$filename"
done

actual_count=$(find "$output_dir" -maxdepth 1 -type f -name '*.png' | wc -l | tr -d ' ')
test "$actual_count" -eq 5
print "PASS: generated exactly 5 non-empty PNG files."
