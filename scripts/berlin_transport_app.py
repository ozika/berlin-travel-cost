from groo.groo import get_root
root_folder = get_root(".root_berlin_travel")
import streamlit as st
import pandas as pd
import numpy as np
import os

#dispval = False


st.header("Carsharing calculator @ Berlin")
st.text("Calculate how much car rental will cost you.")
st.sidebar.markdown("**1. Input the estimated distance and duration for the ride**")
distance = st.sidebar.number_input("Estimated distance (in km)", value=0.0, step=0.1, help="Distance in km")
estdur = st.sidebar.number_input("Estimated duration (in minutes)", value=0 ,step=1, help="Duration in min")


st.sidebar.markdown("**2. Select comapnies you want to compare**")
options = st.sidebar.multiselect(
     'Select:',
     ['Miles', 'ShareNow'])

#st.text(os.path.join(root_folder, "rates", "miles.csv"))
df_miles = pd.read_csv(os.path.join(root_folder, "rates", "miles.csv"))
df_miles["duration_min"] = df_miles["duration"] * 60

if "Miles" in options:
    st.sidebar.markdown("**Miles**")
    miles_kmrate = st.sidebar.number_input("Rate per km (in EUR)", value=0.00, step=0.01, help="For example: 0.89")
    miles_unlockfee = 1
    can_refuel_miles = st.sidebar.checkbox("Will refule Miles (5 EUR cashback)", value=False)
    if miles_kmrate != 0.0:
        miles_cost = miles_kmrate*distance + miles_unlockfee + can_refuel_miles*(-5)
        st.markdown("**Miles cost:** "+str(miles_cost))
        id = ((df_miles["duration_min"]>estdur) & (df_miles["distance"]>distance) & (df_miles["cost"]<miles_cost))
        if sum(id)>0:
            st.text("You can save money with the following MILES packages:")
            st.dataframe(df_miles.loc[id,:])

if "ShareNow" in options:
    st.sidebar.markdown("**ShareNow**")
    sharenow_minrate = st.sidebar.number_input("Rate per minute (in EUR)", value=0.00 ,step=0.01, help="For example: 0.29")
    sharenow_unlockfee = 0
    can_refuel_sharenow = st.sidebar.checkbox("Will refule Sharenow (5 EUR cashback)", value=False)
    if sharenow_minrate != 0.00:

        st.markdown("**Sharenow cost:** "+str(sharenow_minrate*estdur + can_refuel_sharenow*(-5)))


st.markdown("---")
