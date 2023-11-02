import requests
import streamlit as st
import pandas as pd
# import pickle
# from pathlib import Path
# import streamlit_authenticator as stauth

url = "https://www.instagram.com/api/graphql"
headers = {
  'authority': 'www.instagram.com',
  'accept': '*/*',
  'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
  'content-type': 'application/x-www-form-urlencoded',
  'dpr': '1',
  'origin': 'https://www.instagram.com',
  'referer': 'https://www.instagram.com/rajarahman/',
  'sec-ch-prefers-color-scheme': 'light',
  'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
  'sec-ch-ua-full-version-list': '"Chromium";v="118.0.5993.118", "Google Chrome";v="118.0.5993.118", "Not=A?Brand";v="99.0.0.0"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-model': '""',
  'sec-ch-ua-platform': '"Windows"',
  'sec-ch-ua-platform-version': '"15.0.0"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
  'viewport-width': '1286',
  'x-asbd-id': '129477',
  'x-csrftoken': 'iwyKNIZjMSH8obU4PHB1tRyN1rPF12no',
  'x-fb-friendly-name': 'PolarisBarcelonaProfileBadgeQuery',
  'x-fb-lsd': 'AVpbluxH90g',
  'x-ig-app-id': '936619743392459'
}

def checkusername(username):
    payload = f'lsd=AVpbluxH90g&variables=%7B%22username%22%3A%22{username}%22%7D&doc_id=6887760227926196'
    response = requests.request("POST", url, headers=headers, data=payload)
    dataresponse = response.json()

    return dataresponse

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

    return dff

from io import StringIO

# ## Authentication
# names = ["admin", "raja"]
# usernames = ["admin", "raja"]

# # load hashed passwords
# file_path = Path(__file__).parent / "hashed_pw.pkl"
# with file_path.open("rb") as file:
#     hashed_passwords = pickle.load(file)

# authenticator = stauth.Authenticate(names, usernames, hashed_passwords,"sales_dashboard", "abcdef", cookie_expiry_days=30)

# name, authentication_status, username = authenticator.login("Login", "main")

# if authentication_status == False:
#     st.error("Username/password is incorrect")

# if authentication_status == None:
#     st.warning("Please enter your username and password")

# if authentication_status:
col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image("https://akunfb.id/wp-content/uploads/2023/07/Logo2.png")

with col3:
    st.write(' ')
st.markdown("<h2 style='text-align: center; color: black;'>Instagram LIVE Checker </h2>", unsafe_allow_html=True)

centered_headline_with_link = """
<h3 style="text-align: center; color: black;"> Order FB & IG Account :
    <a href="https://akunfb.id/">akunfb.id</a>
</h3>
"""

st.markdown(centered_headline_with_link, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    dataframe = pd.read_csv(uploaded_file)
    datafromcsv = dataframe['username'].tolist()
    st.session_state['usernamelabel'] = True
else:
    st.session_state['usernamelabel'] = False

username = st.text_area('Username','', height=100, disabled=st.session_state['usernamelabel'])

genre = st.radio(
    "search method",
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
