from groo.groo import get_root
root_folder = get_root(".root_berlin_travel")
import streamlit as st
import pandas as pd
import numpy as np
import os

#dispval = False
sharenow_deals_km_price = 0.19
miles_parking_rate = 0.29

st.header("Carsharing price calculator @ Berlin")
st.markdown("This site compares mobility sharing companies (MILES, SHARE NOW) for better deal given your estimated distance, duration, parking etc.")
st.markdown("It also checks for any packages/deals that one can take. Enjoy! :heart:")
st.sidebar.markdown("**1. Input the estimated distance and duration for the ride (google estimates will do)**")
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

st.sidebar.markdown("**2. Select companies you want to compare**")
options = st.sidebar.multiselect(
     'Select:',
     ['Miles', 'ShareNow'])


#st.text(os.path.join(root_folder, "rates", "miles.csv"))
df_miles = pd.read_csv(os.path.join(root_folder, "rates", "miles.csv"))
df_miles["duration_min"] = df_miles["duration"] * 60
df_sn = pd.read_csv(os.path.join(root_folder, "rates", "sharenow.csv"))
df_sn["duration_min"] = df_sn["duration hrs"] * 60

donate_string = '''<form action="https://www.paypal.com/donate" method="post" target="_top">
<input type="hidden" name="hosted_button_id" value="3X5CKVFVU723L" />
<input type="image" src="https://www.paypalobjects.com/en_GB/i/btn/btn_donate_LG.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
<img alt="" border="0" src="https://www.paypal.com/en_GB/i/scr/pixel.gif" width="1" height="1" />
</form>'''




if "Miles" in options:

    st.sidebar.markdown("**Miles**")
    miles_kmrate = st.sidebar.number_input("Rate per km (in EUR)", value=0.89, step=0.01, help="For example: 0.89")



    miles_unlockfee = 1
    can_refuel_miles = st.sidebar.checkbox("Will refuel Miles (5 EUR cashback)", value=False)
    if miles_kmrate != 0.0:
        miles_cost = miles_kmrate*distance + miles_unlockfee + can_refuel_miles*(-5) + parking*miles_parking_rate
        st.markdown("**MILES cost:** "+str(miles_cost))
        st.markdown("Breakdown: "+str(miles_kmrate)+"EUR/km * "+str(distance) +"km + "+str(miles_unlockfee)+" (unlock fee) - "+str(can_refuel_miles*(5))  + " (refuel) + "+str(miles_parking_rate) + "EUR/min * "+str(parking)+" (parking)"  )

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
        st.markdown("**SHARE NOW cost:** "+str(sharenow_cost))
        st.markdown("Breakdown: "+str(sharenow_minrate)+"EUR/min * "+str(estdur)+" - " +str(can_refuel_sharenow*(5))+"(refuel)" )
        df_sn_2 = df_sn.loc[:,["duration_min"]+[sharenow_car]]
        id = ((df_sn_2["duration_min"]>estdur) & ( (df_sn_2[sharenow_car] + sharenow_deals_km_price*distance) < sharenow_cost))
        if sum(id)>0:
            st.text("You can save money with the following ShareNow packages:")
            st.dataframe(df_sn.loc[id,["duration"]+[sharenow_car]+["Total cost (with km)"]])


st.markdown("---")
st.markdown('For improvements, suggestions and any errors you can [write me here](https://github.com/ozika/berlin-travel-cost/issues) (just click "open issue")')
st.markdown("If this saved you some money, please tip me. I love working on this but it also takes some of my time (and a lot of B-lin coffee :coffee:) Berlin :heart:")
st.markdown(donate_string, unsafe_allow_html=True)
#twitter_string = '''<a href="https://twitter.com/OndrejZika"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Twitter-logo.svg/2491px-Twitter-logo.svg.png" width="40px"></a>'''
#st.markdown(twitter_string, unsafe_allow_html=True)
