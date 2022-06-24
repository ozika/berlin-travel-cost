from groo.groo import get_root
root_folder = get_root(".root_berlin_travel")
import streamlit as st
import pandas as pd
import numpy as np
import os

#dispval = False
sharenow_deals_km_price = 0.19
miles_parking_rate = 0.29

st.header("Carsharing calculator @ Berlin")
st.text("Calculate how much car rental will cost you.")
st.sidebar.markdown("**1. Input the estimated distance and duration for the ride**")
distance = st.sidebar.number_input("Estimated distance (in km)", value=0.0, step=0.1, help="Distance in km")
unit = st.sidebar.selectbox("Select unit", ["min", "hr", "day"])
estdur = st.sidebar.number_input("Estimated duration (in "+unit+")", value=0 ,step=1, help="Duration in "+unit)
if unit == "hr":
    estdur = estdur * 60
elif unit == "day":
    estdur = estdur * 60 * 24

st.sidebar.markdown("Parking is ON TOP if the driving time")
parking = st.sidebar.number_input("Parking time (in "+unit+")", value=0)
if unit == "hr":
    parking = parking * 60
elif unit == "day":
    parking = parking * 60 * 24

st.sidebar.markdown("**2. Select comapnies you want to compare**")
options = st.sidebar.multiselect(
     'Select:',
     ['Miles', 'ShareNow'])


#st.text(os.path.join(root_folder, "rates", "miles.csv"))
df_miles = pd.read_csv(os.path.join(root_folder, "rates", "miles.csv"))
df_miles["duration_min"] = df_miles["duration"] * 60
df_sn = pd.read_csv(os.path.join(root_folder, "rates", "sharenow.csv"))
df_sn["duration_min"] = df_sn["duration hrs"] * 60





if "Miles" in options:

    st.sidebar.markdown("**Miles**")
    miles_kmrate = st.sidebar.number_input("Rate per km (in EUR)", value=0.89, step=0.01, help="For example: 0.89")



    miles_unlockfee = 1
    can_refuel_miles = st.sidebar.checkbox("Will refuel Miles (5 EUR cashback)", value=False)
    if miles_kmrate != 0.0:
        miles_cost = miles_kmrate*distance + miles_unlockfee + can_refuel_miles*(-5) + parking*miles_parking_rate
        st.markdown("**Miles cost:** "+str(miles_cost))
        id = ((df_miles["duration_min"]>estdur) & (df_miles["distance"]>distance) & (df_miles["cost"]<miles_cost))
        if sum(id)>0:
            st.text("You can save money with the following MILES packages:")
            st.dataframe(df_miles.loc[id,:])

if "ShareNow" in options:
    estdur = estdur + parking #in sharenow one pays for the entire time

    st.sidebar.markdown("**ShareNow**")
    sharenow_minrate = st.sidebar.number_input("Rate per minute (in EUR)\nInclude discount.", value=0.00 ,step=0.01, help="For example: 0.29")
    #st.sidebar.markdown()
    sharenow_car = st.sidebar.selectbox("Car type (optional, only necessary if you want to check ShareNow packages)", ["Fiat 500", "BMW 1 Series",	"Peugeot 308",	"Citroen C3",	"Fiat 500X",	"MINI Countryman",	"MINI 3-door",
                                                                 "MINI Convertable",	"MINI 5-door",	"MINI Clubman",	"Peugeot 208",	"Peugeot 3008",	"BMW Convertible",	"BMW Active Tourer",	"BMW X1",	"BMW X2"])
    df_sn["Total cost (with km)"] = df_sn[sharenow_car] + sharenow_deals_km_price * distance
    sharenow_unlockfee = 0
    can_refuel_sharenow = st.sidebar.checkbox("Will refuel Sharenow (5 EUR cashback)", value=False)
    if sharenow_minrate != 0.00:
        sharenow_cost = sharenow_minrate*estdur + can_refuel_sharenow*(-5)
        st.markdown("**Sharenow cost:** "+str(sharenow_cost))
        df_sn_2 = df_sn.loc[:,["duration_min"]+[sharenow_car]]
        id = ((df_sn_2["duration_min"]>estdur) & ( (df_sn_2[sharenow_car] + sharenow_deals_km_price*distance) < sharenow_cost))
        if sum(id)>0:
            st.text("You can save money with the following ShareNow packages:")
            st.dataframe(df_sn.loc[id,["duration"]+[sharenow_car]+["Total cost (with km)"]])


st.markdown("---")
