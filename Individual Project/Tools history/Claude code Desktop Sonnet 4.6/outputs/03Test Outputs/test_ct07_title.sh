#!/bin/zsh
set -eu

script='/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Tools history/Claude code Desktop Sonnet 4.6/Test3 by sonnet4.6high ae_analysis.jl'
grep -q 'fig_title = "T07 Commercial Normalised RMS Profile"' "$script"
print 'PASS: Figure 2 title identifies the CT07 dataset.'
