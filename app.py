import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
st.title('My first web app')
image = Image.open("C:/Users/xaver/OneDrive/Imágenes/Logo-KDT-JU.jpg")
st.image(image)
st.write(chart_data)
option = st.selectbox('Select an option:', ['a','b','c'])
st.bar_chart(chart_data['a'])
