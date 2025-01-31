#!/bin/bash

wallpapers="$HOME/Pictures/wall/"
# monitors="$(hyprctl monitors | grep Monitor | awk '{print $2}')"
monitors="$(xrandr --query | grep " connected" | awk '{print $1}')"

for monitor in $monitors; do
  wallpaper="$(find $wallpapers -type f | shuf -n 1)"
  echo "$monitor, $wallpaper"
  swww img -o "$monitor" --transition-duration 0.1 --transition-type wipe "$wallpaper"
done
