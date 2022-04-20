import streamlit as st
import pandas as pd
import numpy as np

st.title('My first web app')
st.image("C:/Users/xaver/OneDrive/Imágenes/Logo-KDT-JU.jpg")

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
st.write(chart_data)
option = st.selectbox(['a', 'b', 'c'])
st.bar_chart(chart_data[option])
