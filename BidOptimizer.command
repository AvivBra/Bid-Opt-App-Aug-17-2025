#!/bin/bash
cd "/Applications/My Apps/Bid Opt App Aug 17, 2025"
pkill -f streamlit
sleep 1
streamlit run app/main.py
