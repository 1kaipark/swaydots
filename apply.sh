#!/bin/bash 

rm ~/.config/fabric ~/.config/ghostty ~/.config/hypr ~/.config/nvim ~/.config/rofi ~/.config/sway ~/.config/waybar
for dir in $(ls); do 
  stow $dir 
done

rm ~/Pictures/wall 
ln -s ~/Pictures/catppuccin_frappe_tokyo ~/Pictures/wall
wpswitch

