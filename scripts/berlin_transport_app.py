from groo.groo import get_root
root_folder = get_root(".root_berlin_travel")
import streamlit as st
import pandas as pd
import numpy as np
import os
#import pathlib
#from bs4 import BeautifulSoup
#import logging
#import shutil

#dispval = False
sharenow_deals_km_price = 0.19
miles_parking_rate = 0.29
weshare_parking_rate= 0.29

df_miles = pd.read_csv(os.path.join(root_folder, "rates", "miles.csv"))
df_miles["duration_min"] = df_miles["duration"] * 60
df_sn = pd.read_csv(os.path.join(root_folder, "rates", "sharenow.csv"))
df_sn["duration_min"] = df_sn["duration hrs"] * 60
df_ws = pd.read_csv(os.path.join(root_folder, "rates", "weshare.csv"))
df_ws["duration_min"] = df_ws["duration"] * 60



st.header("Carsharing price calculator @ Berlin")
st.markdown("This site compares mobility sharing companies (MILES, SHARE NOW, WESHARE) for better deal given your estimated distance, duration, parking etc. Enjoy! :heart:")
#st.markdown("**Quick version**: You just need to type in distance and duration, all else is optional.")
#st.markdown("**Extensive version**: Needs more input, but also checks for packages/deals specific to a given car type.")
#st.markdown("---")
showresults = True#st.button("Show me!")

st.sidebar.markdown("## 1. Choose comparison type")
scope = st.sidebar.radio("Quick = based on time, distance and parking only\nExtensive = also deals, car type, better for long-term", ["Quick", "Extensive"], horizontal=True)

if scope=="Quick":
    st.sidebar.markdown("## 2. Type in distance, duration and parking time")
    distance = st.sidebar.number_input("Estimated distance (in km)", value=0, step=1, help="Distance in km")
    unit = "min"
    estdur = st.sidebar.number_input("Estimated duration (in "+unit+")", value=0 ,step=1, help="Duration in "+unit)
    parking = st.sidebar.number_input("Parking time (in "+unit+")", value=0)

    if (distance != 0.0) & (estdur != 0):
         st.sidebar.markdown("## 3. Select companies you want to compare")
         options = st.sidebar.multiselect(
              'You can specify the rates below if you need to.',
              ['MILES', 'SHARENOW', 'WESHARE'], default=['MILES', 'SHARENOW', 'WESHARE'])
         if "MILES" in options:
             st.sidebar.markdown("### **Miles**")
             miles_kmrate = st.sidebar.number_input("Rate per km (in EUR)", value=0.89, step=0.01, help="For example: 0.89")
             miles_unlockfee = 1
             can_refuel_miles = st.sidebar.checkbox("Will refuel Miles (5 EUR cashback)", key="refuel1", value=False)
             miles_cost = round(miles_kmrate*distance + miles_unlockfee + can_refuel_miles*(-5) + parking*miles_parking_rate,2)
             #st.markdown("**MILES cost:** "+str(miles_cost))
             st.metric(label="", value="MILES: "+str(miles_cost)+" EUR")

             st.markdown("Breakdown: "+str(miles_kmrate)+" EUR/km * "+str(distance) +" km + "+str(miles_unlockfee)+" (unlock fee) - "+str(can_refuel_miles*(5))  + " (refuel) + "+str(miles_parking_rate) + " EUR/min * "+str(parking)+" (parking)"  )

         if "SHARENOW" in options:
             estdur = estdur + parking #in sharenow one pays for the entire time
             st.sidebar.markdown("### **ShareNow**")
             sharenow_minrate = st.sidebar.number_input("Rate per minute (in EUR)\nInclude discount.", key="sn_minrate_1", value=0.26 ,step=0.01, help="For example: 0.26")
             sharenow_unlockfee = 0
             can_refuel_sharenow = st.sidebar.checkbox("Will refuel Sharenow (5 EUR cashback)", key="refuelsn1", value=False)
             if (sharenow_minrate != 0.00) & showresults:
                 sharenow_cost = round(sharenow_minrate*estdur + can_refuel_sharenow*(-5),2)
                 #st.markdown("**SHARE NOW cost:** "+str(sharenow_cost))
                 st.metric(label="", value="SHARE NOW: "+str(sharenow_cost)+" EUR")
                 st.markdown("Breakdown: "+str(sharenow_minrate)+" EUR/min * "+str(estdur)+" min - " +str(can_refuel_sharenow*(5))+" (refuel)" )
                 #st.markdown("> **NOTE:** *The `Quick` option doesn't check for packages/deals! Use the `Extensive` version for that.*")

         if "WESHARE" in options:
              s=1
              st.sidebar.markdown("### **WeShare**")
              weshare_unlockfee = 1
              weshare_minrate = st.sidebar.number_input("Rate per minute (in EUR)\nInclude discount.", key="ws_minrate_1", value=0.29 ,step=0.01, help="For example: 0.29")
              can_refuel_weshare = st.sidebar.checkbox("Will recharge WeShare (5 EUR cashback)", key="refuel1", value=False)
              if (weshare_minrate != 0.00) & showresults:
                  weshare_cost = round(weshare_minrate*estdur + parking*weshare_parking_rate + weshare_unlockfee + can_refuel_weshare*(-5),2)
                  st.metric(label="", value="WESHARE: "+str(weshare_cost)+" EUR")
                  st.markdown("Breakdown: "+str(weshare_minrate)+" EUR/min * "+str(estdur)+" min + "+str(weshare_parking_rate)+" EUR/min * "+str(parking)+" min (parking) + " +str(weshare_unlockfee)+" (unlock fee) - " +str(can_refuel_weshare*(5))+" (refuel)" )



         st.markdown("> **NOTE:** *The `Quick` option doesn't check for packages/deals! Use the `Extensive` version for that.*")


elif scope=="Extensive":
    st.sidebar.markdown("## 2. Type in distance, duration and parking time")
    st.sidebar.markdown("(google estimates will do)")
    distance = st.sidebar.number_input("Estimated distance (in km)", value=0, step=1, help="Distance in km")
    unit = st.sidebar.selectbox("Select unit", ["min", "hr", "day"])
    estdur = st.sidebar.number_input("Estimated duration (in "+unit+")", value=0 ,step=1, help="Duration in "+unit)
    if unit == "hr":
        estdur = estdur * 60
    elif unit == "day":
        estdur = estdur * 60 * 24

    #st.sidebar.markdown("")
    parking = st.sidebar.number_input("Parking time (in "+unit+")", value=0, help="Parking is on top of the driving time")
    if unit == "hr":
        parking = parking * 60
    elif unit == "day":
        parking = parking * 60 * 24

    st.sidebar.markdown("**2. Select companies you want to compare**")
    options = st.sidebar.multiselect(
         'Select:',
         ['MILES', 'SHARENOW', 'WESHARE'], default=['MILES', 'SHARENOW', 'WESHARE'])

    if ("MILES" in options) & (distance != 0) & (estdur != 0):
        st.sidebar.markdown("### **Miles**")
        miles_unlockfee = 1
        miles_car = st.sidebar.selectbox("Car type", ["S", "M",	"L", "Premium"])
        miles_dicounted = st.sidebar.checkbox("Discounted car", key="m_disc_1", value=False)
        if miles_dicounted:
            miles_kmrate = df_miles["discounted_price"].loc[df_miles["cartype"].isin([miles_car])].unique()[0] # t.sidebar.number_input("Rate per km (in EUR)", value=0.89, step=0.01, help="For example: 0.89")
        else:
            miles_kmrate = df_miles["base_price"].loc[df_miles["cartype"].isin([miles_car])].unique()[0] # t.sidebar.number_input("Rate per km (in EUR)", value=0.89, step=0.01, help="For example: 0.89")
        st.sidebar.markdown("Rate per km: **"+str(miles_kmrate)+"**")
        can_refuel_miles = st.sidebar.checkbox("Will refuel Miles (5 EUR cashback)", key="refuel2", value=False)
        if (miles_kmrate != 0.0) & showresults:
            miles_cost = round(miles_kmrate*distance + miles_unlockfee + can_refuel_miles*(-5) + parking*miles_parking_rate,2)
            #st.markdown("**MILES cost:** "+str(miles_cost))
            st.metric(label="", value="MILES: "+str(miles_cost)+" EUR")
            st.markdown("Breakdown: "+str(miles_kmrate)+" EUR/km * "+str(distance) +" km + "+str(miles_unlockfee)+" (unlock fee) - "+str(can_refuel_miles*(5))  + " (refuel) + "+str(miles_parking_rate) + " EUR/min * "+str(parking)+" (parking)"  )

            id = ((df_miles["duration_min"]>estdur) & (df_miles["distance"]>distance) & (df_miles["cost"]<miles_cost))
            if sum(id)>0:
                st.markdown("You can save money with the following MILES packages:")
                st.dataframe(df_miles.loc[id,["Rental duration", "distance", "cost", "cartype"]])

    if ("SHARENOW" in options) & (distance != 0) & (estdur != 0):
        estdur = estdur + parking #in sharenow one pays for the entire time

        st.sidebar.markdown("### **ShareNow**")
        sharenow_minrate = st.sidebar.number_input("Rate per minute (in EUR)\nInclude discount.", key="sn_minrate_2", value=0.26 ,step=0.01, help="For example: 0.29")
        sharenow_car = st.sidebar.selectbox("Car type", ["Fiat 500", "BMW 1 Series",	"Peugeot 308",	"Citroen C3",	"Fiat 500X",	"MINI Countryman",	"MINI 3-door",
                                                                     "MINI Convertable",	"MINI 5-door",	"MINI Clubman",	"Peugeot 208",	"Peugeot 3008",	"BMW Convertible",	"BMW Active Tourer",	"BMW X1",	"BMW X2"])
        df_sn["Total cost (with km)"] = df_sn[sharenow_car] + sharenow_deals_km_price * distance
        sharenow_unlockfee = 0
        can_refuel_sharenow = st.sidebar.checkbox("Will refuel Sharenow (5 EUR cashback)", value=False)
        if (sharenow_minrate != 0.00) & showresults:
            sharenow_cost = round(sharenow_minrate*estdur + can_refuel_sharenow*(-5),2)
            #st.markdown("**SHARE NOW cost:** "+str(sharenow_cost))
            st.metric(label="", value="SHARE NOW: "+str(sharenow_cost)+" EUR")
            st.markdown("Breakdown: "+str(sharenow_minrate)+" EUR/min * "+str(estdur)+" min - " +str(can_refuel_sharenow*(5))+" (refuel)" )
            df_sn_2 = df_sn.loc[:,["duration_min"]+[sharenow_car]]
            id = ((df_sn_2["duration_min"]>estdur) & ( (df_sn_2[sharenow_car] + sharenow_deals_km_price*distance) < sharenow_cost))
            if sum(id)>0:
                st.markdown("You can save money with the following ShareNow packages:")
                st.dataframe(df_sn.loc[id,["duration"]+[sharenow_car]+["Total cost (with km)"]])

    if ("WESHARE" in options) & (distance != 0) & (estdur != 0): # add paring!
        s=1
        st.sidebar.markdown("### **WeShare**")
        weshare_unlockfee = 1
        weshare_car = st.sidebar.selectbox("Car type", ["ID.3", "ID.4"])
        weshare_member = st.sidebar.checkbox("I have WeSHARE membership", key="ws_memb_1", value=False)
        if weshare_member:
            weshare_parking_rate = 0.09
            weshare_minrate = df_ws["membership_price"].loc[df_ws["cartype"].isin([weshare_car])].unique()[0] # t.sidebar.number_input("Rate per km (in EUR)", value=0.89, step=0.01, help="For example: 0.89")
        else:
            weshare_minrate = df_ws["base_price"].loc[df_ws["cartype"].isin([weshare_car])].unique()[0] # t.sidebar.number_input("Rate per km (in EUR)", value=0.89, step=0.01, help="For example: 0.89")
        st.sidebar.markdown("Rate per min: **"+str(weshare_minrate)+"**")
        #weshare_minrate = st.sidebar.number_input("Rate per minute (in EUR)\nInclude discount.", key="ws_minrate_1", value=0.29 ,step=0.01, help="For example: 0.29")
        can_refuel_weshare = st.sidebar.checkbox("Will recharge WeShare (5 EUR cashback)", key="refuel1", value=False)


        if (weshare_minrate != 0.00) & showresults:
            weshare_cost = round(weshare_minrate*estdur + parking*weshare_parking_rate + weshare_unlockfee + can_refuel_weshare*(-5),2)
            st.metric(label="", value="WESHARE: "+str(weshare_cost)+" EUR")
            st.markdown("Breakdown: "+str(weshare_minrate)+" EUR/min * "+str(estdur)+" min + "+str(weshare_parking_rate)+" EUR/min * "+str(parking)+" min (parking) + " +str(weshare_unlockfee)+" (unlock fee) - " +str(can_refuel_weshare*(5))+" (refuel)" )

            id = (weshare_cost > df_ws["cost"]) & (df_ws["cartype"].isin([weshare_car])) & (distance<df_ws["distance"]) & (estdur<df_ws["duration_min"])
            if sum(id)>0:
                st.markdown("You can save money with the following WeSHARE packages:")
                st.dataframe(df_ws.loc[id,["Rental duration", "distance", "cartype", "cost"]])



donate_string = '''<a href="https://www.paypal.com/donate/?hosted_button_id=3X5CKVFVU723L">
<img src="https://github.com/ozika/berlin-travel-cost/blob/main/img/donate.png?raw=true" width="60px">
</a>
'''
st.markdown("---")
st.markdown('For improvements, suggestions and any errors you can [write me here](https://github.com/ozika/berlin-travel-cost/issues) (just click "open issue")')
st.markdown("If this saved you some money, please tip me. I love working on this but it also takes some of my time (and a lot of B-lin coffee :coffee:) Berlin :heart:")
st.markdown(donate_string, unsafe_allow_html=True)
#twitter_string = '''<a href="https://twitter.com/OndrejZika"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Twitter-logo.svg/2491px-Twitter-logo.svg.png" width="40px"></a>'''
#st.markdown(twitter_string, unsafe_allow_html=True)


#inject_ga()
