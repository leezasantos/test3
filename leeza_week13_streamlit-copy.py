#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 16:27:09 2020

@author: leeza
"""

import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time
import matplotlib.pyplot as plt
import altair as alt
import seaborn as sns



@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2

#----------Loading Dataset----------  
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()
hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']
inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']
outpatient_ny = df_outpatient_2[df_outpatient_2['provider_state'] == 'NY']

#----------Header----------  

st.title('Analysis of New York Inpatient and Outpatient Facilities 2015 Patient Data')

st.subheader('By: Leeza A. Santos')

st.subheader('Last Updated: 12/20/2020')
 
st.header('This dashboard displays reported patient discharges, patient experience, and payment data of New York inpatient and outpatient hospital facilities utilizing Python programming language and deployed by Streamlit.')


st.subheader("Dataset Directory")
st.markdown("""This dashboard utilzes three types of datasets. The first dataset is NY Hospital Experience. 
             This dataset is derived from a nationwide dataset assessing emergency services, meaningful use of electronic 
             health records,hospital overall rating, safety of care, readmission rates, patient experience, and timeliness of care of
             hospital facilitis across the United States. This dataset compares NY hospital facility scores against nationwide scores.  
             
             The second dataset is a list of inpatient facilities in NY. This dataset includes the diagnosis-related group (drg_group) 
             and payments among NY inpatient facilities.
             
             Lastly, the third dataset is a list of outpatient facilities in NY, their services, and payments. 
             """)

def get_dataset(selectbar):
    if selectbar == 'Hospital Experience':
        st.write(hospitals_ny)
    if selectbar == 'Inpatient Facilities':
        st.write(inpatient_ny)
    if selectbar == 'Outpatient Facilities':
        st.write(outpatient_ny)
    
#----------Overview of NY Hospitals----------        

 
st.subheader('Map of NY Hospital Locations')

hospitals_ny_gps = hospitals_ny['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])

st.map(hospitals_ny_gps)


#----------Scatterplot----------
st.subheader('NY Hospitals by County')
st.markdown('Below is a scatterplot of NY hospitals by county. To view all counties, please enlarge the graph')
circle0 = hospitals_ny[['hospital_name', 'county_name']]

c0 = alt.Chart(circle0).mark_circle().encode(
x='hospital_name', 
y='county_name', 
size='county_name', color='county_name', tooltip=['hospital_name', 'county_name'])

st.altair_chart(c0, use_container_width=True)


#----------Pie Chart----------  
bar4 = hospitals_ny['hospital_type'].value_counts().reset_index()
st.subheader('Pie Chart of NY Hospital Type')
fig = px.pie(bar4, values='hospital_type', names='index')
st.plotly_chart(fig)


#Timeliness of Care
st.subheader('NY Hospitals - Timelieness of Care')
bar5 = hospitals_ny['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar5, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig2)

st.markdown('Based on this above bar chart, we can see the majority of hospitals in the NY area fall below the national\
        average as it relates to timeliness of care')


#----------Hospital Performance---------- 

# NYU Langone
# Northwell Health
# Stony Brook

## finding their row #: df_hospital_2[df_hospital_2['hospital_name'].str.contains('NORTHWELL')]

st.subheader('Hospital Performance New York, Nassau, Suffolk')
st.markdown("""
            We will be examining the hospital performance of three NY counties: New York - Manhattan, Nassau, and Suffolk County.
            For each county, we will be looking at mortality rate, safety of care, and patient experience compared to nationwide data.
            Furthermore, we will examine and compare three hospitals, one from each county, NYU Langone located in Manhattan,
            Northwell Hospital located in Nassau County, and Stony Brook University hospital located in Suffolk County.
             """)

st.markdown("""
            We will be examining the hospital performance of three NY counties: New York - Manhattan, Nassau, and Suffolk County.
            For each county, we will be looking at mortality rate, safety of care, and patient experience compared to nationwide data.
            Furthermore, we will examine and compare three hospitals, one from each county, NYU Langone located in Manhattan,
            Northwell Hospital located in Nassau County, and Stony Brook University hospital located in Suffolk County.
             """)
performance = df_hospital_2.iloc[[3230, 2487, 2139],:]
performance = performance[['hospital_name','county_name','hospital_type','mortality_national_comparison','safety_of_care_national_comparison','patient_experience_national_comparison']]
st.dataframe(performance)


fig3 = px.bar(performance, x='mortality_national_comparison', y='hospital_name')
st.plotly_chart(fig3)


fig4 = px.bar(performance, x='safety_of_care_national_comparison', y='hospital_name')
st.plotly_chart(fig3)
       
fig4 = px.bar(performance, x='patient_experience_national_comparison', y='hospital_name')
st.plotly_chart(fig3)     




#creating dataframes for the counties

ny = hospitals_ny[hospitals_ny['county_name']=='NEW YORK']

nassau = hospitals_ny[hospitals_ny['county_name']=='NASSAU']

suffolk = hospitals_ny[hospitals_ny['county_name']=='SUFFOLK']


st.markdown('<font color=‘blue’>NEW YORK COUNTY MORTALITY</font>', unsafe_allow_html=True)
ny_mortality = ny['mortality_national_comparison'].value_counts().reset_index()
ny_mort_pie = px.pie(ny_mortality, values='mortality_national_comparison', names='index')
st.plotly_chart(ny_mort_pie)


st.markdown('<font color=‘blue’>NEW YORK COUNTY SAFETY OF CARE</font>', unsafe_allow_html=True)
ny_safety = ny['safety_of_care_national_comparison'].value_counts().reset_index()
ny_safety_pie = px.pie(ny_safety, values='safety_of_care_national_comparison', names='index')
st.plotly_chart(ny_safety_pie)


st.markdown('<font color=‘blue’>NEW YORK PATIENT EXPERIENCE</font>', unsafe_allow_html=True)
ny_patient = ny['patient_experience_national_comparison'].value_counts().reset_index()
ny_patient_exp = px.pie(ny_patient, values='patient_experience_national_comparison', names='index')
st.plotly_chart(ny_patient_exp)




#Look at Suffolk County
st.markdown('<font color=‘orange’>SUFFOLK COUNTY MORTALITY</font>', unsafe_allow_html=True)
suffolk_mortality = suffolk['mortality_national_comparison'].value_counts().reset_index()
sfmortality = px.bar(suffolk_mortality, values='mortality_national_comparison', names='index')
st.plotly_chart(sfmortality)


st.markdown('<font color=‘orange’>SUFFOLK COUNTY SAFETY OF CARE</font>', unsafe_allow_html=True)
suffolk_safety = suffolk['safety_of_care_national_comparison'].value_counts().reset_index()
sfsafety = px.bar(suffolk_safety, values='safety_of_care_national_comparison', names='index')
st.plotly_chart(sfsafety)


st.markdown('<font color=‘orange’>SUFFOLK COUNTY PATIENT EXPERIENCE</font>', unsafe_allow_html=True)
suffolk_ptexp = suffolk['patient_experience_national_comparison'].value_counts().reset_index()
sf_ptex = px.bar(suffolk_ptexp , values='patient_experience_national_comparison', names='index')
st.plotly_chart(sf_ptex)






#----------Bar Chart 1---------- 

st.subheader('Top 10 Highest Discharge Rates and Outpatient Services')
st.markdown('The bar charts below displays inpatient hospitals with the highest discharge rates and outpatient facilities with the highest services in NY.')

df_bar1 = inpatient_ny[['provider_name','total_discharges']]
source1 = df_bar1[2077:2087]
 
bar1 = alt.Chart(source1).mark_bar().encode(
    x='provider_name',
    y='total_discharges'
    )
st.altair_chart(bar1, use_container_width=True)

#----------Bar Chart 2---------- 

df_bar2 = outpatient_ny[['provider_name','outpatient_services']]
source2 = df_bar2[321:331]

bar2 = alt.Chart(source2).mark_bar().encode(
    x='provider_name',
    y='outpatient_services'
    )
st.altair_chart(bar2, use_container_width=True)






#----------Inpatient---------- 
st.title('Drill Down into INPATIENT data')


inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']
total_inpatient_count = sum(inpatient_ny['total_discharges'])

st.header('Total Count of Discharges from Inpatient Captured: ' )
st.header( str(total_inpatient_count) )


#Bar Charts of the costs 

costs = inpatient_ny.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_ny.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']


st.title('COSTS')

bar6 = px.bar(costs_sum, x='provider_name', y='average_total_payments')
st.plotly_chart(bar6)
st.header("Hospital - ")
st.dataframe(costs_sum)


#Costs by Condition and Hospital / Average Total Payments
costs_condition_hospital = inpatient_ny.groupby(['provider_name', 'drg_definition'])['average_total_payments'].sum().reset_index()
st.header("Costs by Condition and Hospital - Average Total Payments")
st.dataframe(costs_condition_hospital)


#----------Outpatient---------- 

common_discharges = inpatient_ny.groupby('drg_definition')['total_discharges'].sum().reset_index()


top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)



st.header('DRGs')
st.dataframe(common_discharges)


col1, col2 = st.beta_columns(2)

col1.header('Top 10 DRGs')
col1.dataframe(top10)

col2.header('Bottom 10 DRGs')
col2.dataframe(bottom10)






# hospitals = costs_condition_hospital['provider_name'].drop_duplicates()
# hospital_choice = st.sidebar.selectbox('Select your hospital:', hospitals)
# filtered = costs_sum["provider_name"].loc[costs_sum["provider_name"] == hospital_choice]
# st.dataframe(filtered)