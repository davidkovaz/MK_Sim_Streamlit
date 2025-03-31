import streamlit as st

st.markdown('### Instructions for Uploading Data')
st.markdown(('To upload and use your own data for simulation, your data file must first be formatted correctly. '
             'This page explains the required format your data file should be in before you attempt to upload it to the app. '))

st.markdown('#### Requirements')
st.markdown(('An uploaded data file should contain complete track finish results for 4-player matches. '
             'A "match" consists of 16 races (one race on each of the 16 tracks). Each row in your data file should contain the results of one match for one karter/player. '
             'Your data file must meet the formatting requirements explained below BEFORE it is uploaded to the app...'))

st.markdown(('1. The file must be in comma separated values (.csv) format.'))

st.image('images\example_data_full.PNG')

st.markdown(('2. The first row of the data file must contain column names (i.e., the header row) as shown above. '))

st.markdown(('3. There should be no columns named "Points" "1sts" "2nds" "3rds" or "4ths". '
             'Points, number of 1sts, etc. are not needed for simulation, and these are computed automatically on the Data Viewer page!'))

st.markdown(('4. The following columns **MUST BE in the data file**...'))

col1row1, col2row1 = st.columns(2)
with col1row1:
    st.markdown(('* A column named "Karter" that contains the name of the karter that each row of data corresponds to. '
                'Make sure to use consistent naming and spelling for each karter. '
                'For example, the app will treat "Ngamer" and "N Gamer" as different karters!'))
with col2row1:
    st.image('images\example_data_karter.png')

col1row2, col2row2 = st.columns(2)
with col1row2:
    st.markdown(('* Four (4) columns named "K1" "K2" "K3" and "K4" respectively. '
                'These columns should contain the names of the karters who were involved in the match for the corresponding row of data (one name per column).'))
with col2row2:
    st.image('images\example_data_karters.png')

col1row3, col2row3 = st.columns(2)
with col1row3:
    st.markdown(('* Sixteen (16) columns that contain the karters\' finishes on the 16 tracks (Luigi Raceway, Moo Moo Farm, etc.). '
                'You may name these columns however you want (e.g., "Luigi Raceway" or "LR" will work) and they do not have to be in any particular order. '
                'HOWEVER, these track results columns **MUST BE THE LAST 16 COLUMNS IN THE DATA FILE**. '
                'There should be no additional columns to the right of the track results columns. '
                'Each value in the track results columns should be a 1, 2, 3, or 4 to indicate the karter\'s finish on that track (1st, 2nd, 3rd, and 4th respectively).'))
with col2row3:
    st.image('images\example_data_tracks.png')

st.markdown('#### Optional Columns')
st.markdown(('Any other columns you wish to have are allowed as long as they appear to the LEFT of the track results columns in the data file. '
            'Additional columns are purely optional, but recommended for more advanced functionality (e.g., applying filters). '
            'Here are some examples of optional columns you may wish to include...'))

col1row4, col2row4 = st.columns(2)
with col1row4:
    st.markdown(('* A column named "Event" that specifies where the match took place (e.g., "Virginia 2018").'))
    st.markdown(('* A column named "Match" that contains a descriptive identifier for the type of match ("Practice" "Playin" "Semifinal" etc.).'))
with col2row4:
    st.image('images\example_data_optional.png')

st.markdown('#### Additional Things to Note')
st.markdown(('There should be no missing/blank values for any columns. Any rows with missing values will automatically be dropped when you upload your file. '))
st.markdown(('To simulate a match, there must be data for at least 4 different karters in your data file. '
             'To simulate a tournament, you must have data for at least 16 different karters. '
             'I recommend that each karter have at least 2 matches worth of data, but more data will produce better results.'))

st.markdown('#### Is there an example I may follow?')
st.markdown('Yes! You may download the default data file [here](va_2014_18.csv) to see an example of a correctly formatted data file.')

