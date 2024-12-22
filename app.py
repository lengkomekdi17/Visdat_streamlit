import pandas as pd
import pickle
from PIL import Image
import streamlit as st
import plotly.express as px

px.defaults.template ='plotly_dark'
px.defaults.color_continuous_scale = 'reds'


img = Image.open('assets/Youtube.png')
st.sidebar.image(img)

with open("data_input/used_data.pickle", 'rb') as f:
    data = pickle.load(f)

#Input Tanggal
min_date = data['trending_date'].min()
max_date = data['trending_date'].max()
start_date, end_date = st.sidebar.date_input(label='Rentang Waktu',
                                             min_value=min_date,
                                             max_value=max_date,
                                             value=[min_date, max_date]
                                             )

#Input kategori
categories = ["All Categories"] + list(data['category'].value_counts().keys().sort_values())
category = st.sidebar.selectbox(label='Kategori Video', options=categories)

#Filter Data by Input
outputs = data[(data['trending_date'] >= start_date) &
               (data['trending_date'] <= end_date)]
if category != "All Categories":
    outputs = outputs[outputs['category'] == category]

#Visualisasi Bar Chart
st.header(':video_camera: Channel')
bar_data = outputs['channel_name'].value_counts().nlargest(10).sort_values()
fig = px.bar(bar_data, color=bar_data, orientation='h', title=f'Channel Terpopuler dari kategori {category}')
st.plotly_chart(fig)

#visualisasi dengan scatter plot
st.header(':bulb: Engagement')
col1, col2 = st.columns(2)
metrics_choice = ['like', 'dislike', 'comment']
choice_1 = col1.selectbox('Horizontal', options=metrics_choice)
choice_2 = col2.selectbox('Vertical', options=metrics_choice)
fig = px.scatter(outputs,
                 x=choice_1,
                 y=choice_2,
                 size='view',
                 hover_name='channel_name',
                 hover_data=['title'],
                 title=f'Engagement of {choice_1.title()} and {choice_2.title()}')
st.plotly_chart(fig)