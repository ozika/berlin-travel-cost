from groo.groo import get_root
root_folder = get_root(".root_berlin_travel")
import streamlit as st
print(root_folder)
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


if "Miles" in options:
    st.sidebar.markdown("**Miles**")
    miles_kmrate = st.sidebar.number_input("Rate per km (in EUR)", value=0.00, step=0.01, help="For example: 0.89")
    miles_unlockfee = 1
    can_refuel_miles = st.sidebar.checkbox("Will refule Miles (5 EUR cashback)", value=False)
    if miles_kmrate != 0.0:
        st.markdown("**Miles cost:** "+str(miles_kmrate*distance + miles_unlockfee + can_refuel_miles*(-5)))

if "ShareNow" in options:
    st.sidebar.markdown("**ShareNow**")
    sharenow_minrate = st.sidebar.number_input("Rate per minute (in EUR)", value=0.00 ,step=0.01, help="For example: 0.29")
    sharenow_unlockfee = 0
    can_refuel_sharenow = st.sidebar.checkbox("Will refule Sharenow (5 EUR cashback)", value=False)
    if sharenow_minrate != 0.00:
        st.markdown("**Sharenow cost:** "+str(sharenow_minrate*estdur + can_refuel_sharenow*(-5)))


st.markdown("---")
