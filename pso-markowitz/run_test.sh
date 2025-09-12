#!/bin/zsh

cargo build

./target/debug/pso-markowitz ./data-files/port1.txt 
