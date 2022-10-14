import streamlit as st
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pickle
import numpy as np
import openpyxl
import string
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
import string
from nltk import PorterStemmer
from io import BytesIO
ps =PorterStemmer()
from Girnar_Keywords_code import dotask

# df = pd.read_excel(r'Z:\DATA SCIENCE(RCR)\Rahul Agarwal\data_labeling_for_bhim\bhim_all_with_nps_final1.xlsx')
#
# print(df)

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

st.title('Girnar Automation')
st.header('You can upload free text column with "Remarks" name')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df =pd.read_excel(uploaded_file)
    df= df.astype(str)
    col = ['Sr No:', 'Product', 'SMS', 'Rating', 'Remarks','Type of lead','Mode','Cleaned_Remarks', 'Categories', 'Sub Categories','NPS CAT', 'Total Nps Score']
    df_final =pd.DataFrame(columns=col)

if st.button('transformed_data'):
    df['transformed_text']=df['Remarks'].apply(transform_text)
    df['transformed_text']=df['transformed_text'].replace('',np.NaN)
    df.dropna(subset =['transformed_text'],how ='any',inplace=True)
    st.write(df)

else:
    pass

if st.button('CATEGORIZATION and NPS_cal'):
    a = dotask(df)
    df_xlsx = to_excel(a)
    st.download_button(
        label="Download data as CSV",
        data=df_xlsx,
        file_name='large_df.csv',
        mime='text/csv',
    )


# elif st.button('NPS graph data'):
#     a = dotask(df)
#     b = quad(a)
#     df_xlsx1 = to_excel(b)
#     st.download_button(
#         label="Download excel sheet for Quadrant graph",
#         data=df_xlsx1,
#         file_name='Quadrant graph.csv',
#         mime='text/csv',
#     )








