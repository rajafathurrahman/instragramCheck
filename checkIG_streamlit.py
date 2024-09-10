import requests
import streamlit as st
import pandas as pd
from io import StringIO
import time

headers = {
  'accept': '*/*',
  'accept-language': 'id-ID,id;q=0.9',
  'cache-control': 'no-cache',
  'pragma': 'no-cache',
  'priority': 'u=1, i',
  'referer': 'https://www.instagram.com/rajarahman17/',
  'sec-ch-prefers-color-scheme': 'light',
  'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
  'sec-ch-ua-full-version-list': '"Chromium";v="128.0.6613.120", "Not;A=Brand";v="24.0.0.0", "Google Chrome";v="128.0.6613.120"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-model': '""',
  'sec-ch-ua-platform': '"Windows"',
  'sec-ch-ua-platform-version': '"15.0.0"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
  'x-asbd-id': '129477',
  'x-csrftoken': 'F1jFG6_FagqAZuBZAqwKvK',
  'x-ig-app-id': '936619743392459',
  'x-ig-www-claim': '0',
  'x-requested-with': 'XMLHttpRequest'}

def checkusername(username):
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Check for HTTP errors
            dataresponse = response.json()
            return dataresponse  # Return response if successful
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)  # Wait before retrying

    return {'data': {'user': None}, 'status': 'ok'}  # Return empty if all attempts fail

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

def getdataframe(datausername):
    datadf = []
    for i in range(len(datausername)):
        dataresponse = checkusername(datausername[i])
        if dataresponse['data']['user'] != None:
            datadf.append([datausername[i],dataresponse['data']['user']['id'],'active'])
        else:
            datadf.append([datausername[i],'Null','notactive'])
    
        dff = pd.DataFrame(datadf, columns=['username','ID', 'status'])
        dff_clean = dff.drop_duplicates(subset=['username'])

    return dff_clean

col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image("https://akunfb.id/wp-content/uploads/2023/07/Logo2.png")

with col3:
    st.write(' ')
st.markdown("<h2 style='text-align: center; color: black;'>Instagram LIVE Checker </h2>", unsafe_allow_html=True)

centered_headline_with_link = """
<h4 style="text-align: center; color: black;"> Order FB & IG Account :
    <a href="https://akunfb.id/">akunfb.id</a>
</h4>
"""

st.markdown(centered_headline_with_link, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Bulk Checker")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    dataframe = pd.read_csv(uploaded_file)
    datafromcsv = dataframe['username'].tolist()
    st.session_state['usernamelabel'] = True
else:
    st.session_state['usernamelabel'] = False

username = st.text_area('Input IG Username','', height=100, disabled=st.session_state['usernamelabel'])

genre = st.radio(
    "Check Method",
    ["file", "manual"])

but = st.button('Check IG')


if but:
    if genre == 'manual':
        if username != '' :
            datausername = username.split('\n')
            dff = getdataframe(datausername)
            st.write('Active')
            st.write(dff[dff['status']=='active'].reset_index(drop=True))

            st.write('Not Active')
            st.write(dff[dff['status']=='notactive'].reset_index(drop=True))
            
            csv = convert_df(dff)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='resultCheckIG.csv',
                mime='text/csv',
            )
        else:
            st.warning('Please Input username')
    else:
        if uploaded_file is not None:
            dff = getdataframe(datafromcsv)
            st.write('Active')
            st.write(dff[dff['status']=='active'].reset_index(drop=True))

            st.write('Not Active')
            st.write(dff[dff['status']=='notactive'].reset_index(drop=True))

            csv = convert_df(dff)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='resultCheckIG.csv',
                mime='text/csv',
            )
        else:
            st.warning('upload file first')
