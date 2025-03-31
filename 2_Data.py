import streamlit as st
import pandas as pd

if 'uploaded_data_name' not in st.session_state:
    st.session_state.uploaded_data_name = None

if 'df_uploaded' not in st.session_state:
    st.session_state.df_uploaded = None

if 'df_filtered' not in st.session_state:
    st.session_state.df_filtered = None

if 'apply_filters' not in st.session_state:
    st.session_state.apply_filters = 'No'

if 'active_filters' not in st.session_state:
    st.session_state.active_filters = []

if 'disable_filter_submit' not in st.session_state:
    st.session_state.disable_filter_submit = False

if 'disable_clear_filter' not in st.session_state:
    st.session_state.disable_clear_filter = True

def data_choice_clear_filters():
    st.session_state.disable_filter_submit = False
    st.session_state.df_filtered = None
    st.session_state.active_filters = []
    st.session_state.disable_clear_filter = True

df_default = st.session_state.df_default
df_raw = df_default
uploaded_data = None

st.write('### Select Your Data!')
st.write(('Here you may select the data to use as the basis for simulation. '
          'You may use the built-in (default) data or upload your own dataset. '
          'The default data are Virginia tournament match results from 2012 to 2019 (complete 4-player matches only). '
          'If you want to use your own data, first please review the instructions for formatting your data file on the Upload Instructions page.'))

data_choice = st.radio('**Select your data!**',
                       options = ['Use default data (Virginia Tournaments 2012-2019)', 'Upload and use my own data'],
                       key = 'udatakey', on_change = data_choice_clear_filters)

if data_choice == 'Upload and use my own data':
    uploaded_data = st.file_uploader('Choose file (MUST BE A .CSV FILE)', type = 'csv', accept_multiple_files = False)

if uploaded_data is not None:
    st.session_state.uploaded_data_name = uploaded_data.name
    st.session_state.df_uploaded = pd.read_csv(uploaded_data)

if (st.session_state.df_uploaded is not None) & (data_choice == 'Upload and use my own data'):
    df_raw = st.session_state.df_uploaded

df_raw = df_raw.dropna()

st.session_state.valid_data = True

if (st.session_state.df_uploaded is not None) & (data_choice == 'Upload and use my own data'):
    problem_list = []

    for col in ['Karter', 'K1', 'K2', 'K3', 'K4']:
        if col not in df_raw.columns:
            problem = f'**:red[Dataset does not have a {col} column.]**'
            problem_list.append(problem)

    if len(df_raw.columns) < 21:
        problem = '**:red[Dataset does not have enough columns. There must be 16 track columns in addition to the Karter and K1-K4 columns.]**'
        problem_list.append(problem)

    track_values = set().union(*[set(df_raw[track]) for track in df_raw.columns[-16:].tolist()])
    if track_values.issubset({1, 2, 3, 4}) == False:
        problem = '**:red[There are invalid values in track columns. Track columns must contain numerical values 1, 2, 3, or 4 only.]**'
        problem_list.append(problem)

    df_raw_cols = df_raw.columns.tolist()
    if any(x in df_raw_cols for x in ['Points', '1sts', '2nds', '3rds', '4ths']):
        problem = '**:red[There are invalid column names. There should be no columns named "Points" "1sts" "2nds" "3rds" or "4ths".]**'
        problem_list.append(problem)

    if problem_list:
        st.session_state.valid_data = False
        st.error(('**:red[There are problems with the uploaded dataset.] '
                    ':red[Please review the Upload Instructions, resolve the problems below, and then reupload your dataset.]**'))
        for problem in problem_list:
            st.markdown(problem)

if st.session_state.valid_data:
    karter_list = list(set(df_raw['Karter'].values))
    karter_list.sort()
    st.session_state.karter_list = karter_list

    tracks = df_raw.columns[-16:].tolist()
    st.session_state.tracks = tracks

    df = df_raw.copy()
    df['Karters'] = df[['K1', 'K2', 'K3', 'K4']].values.tolist()
    df = df.drop(['K1', 'K2', 'K3', 'K4'], axis = 1)
    data_cols = df.columns.tolist()
    data_cols = [col for col in data_cols if col not in tracks] + tracks
    df = df[data_cols]

    if (st.session_state.df_uploaded is not None) & (data_choice == 'Upload and use my own data'):
        st.write(f'**Selected Data: {st.session_state.uploaded_data_name}**')
    else:
        st.write('**Selected Data: Default**')

    apply_filters = st.radio('**Apply additional filters?**',
                            ['No', 'Yes'],
                            key = 'apply_filters')

    def disable_submission():
        st.session_state.disable_filter_submit = True

    def clear_filters():
        st.session_state.disable_filter_submit = False
        st.session_state.df_filtered = None
        st.session_state.df = df
        st.session_state.active_filters = []
        st.session_state.disable_clear_filter = True

    if apply_filters == 'Yes':
        if st.session_state.df_filtered is None:
            df_filtered = df.copy()
            filter_cols = [col for col in df.columns.tolist() if col not in (['Karter', 'Karters'] + tracks)]
            st.write('**Choose filters to apply:**')
            with st.form(key = 'filter_form', clear_on_submit = True, enter_to_submit = False):
                if 'Karter_filter' not in st.session_state:
                    st.session_state.Karter_filter = None
                st.session_state.Karter_filter = st.multiselect('REMOVE match records for the following Karters:', karter_list)
                if 'Karters_filter' not in st.session_state:
                    st.session_state.Karters_filter = None
                st.session_state.Karters_filter = st.multiselect('REMOVE records for matches that involve any of the following Karters:', karter_list)
                for col in filter_cols:
                    removals_key = f'{col}_filter'
                    if removals_key not in st.session_state:
                        st.session_state[removals_key] = None
                    st.session_state[removals_key] = st.multiselect(f'Select values of **{col}** to REMOVE:', sorted(set(df[col].values)))
                submit_filters = st.form_submit_button('Apply Filters', on_click = disable_submission, disabled = st.session_state.disable_filter_submit)
            if submit_filters:
                st.session_state.active_filters = []
                st.session_state.disable_clear_filter = False
                if len(st.session_state.Karter_filter) > 0:
                        df_filtered = df_filtered[df_filtered['Karter'].apply(lambda x: x not in st.session_state.Karter_filter)]
                        st.session_state.active_filters.append('Removed match records for Karters: ' + ', '.join(st.session_state.Karter_filter))
                if len(st.session_state.Karters_filter) > 0:
                        df_filtered = df_filtered[df_filtered['Karters'].apply(lambda x: not any(y in st.session_state.Karters_filter for y in x))]
                        st.session_state.active_filters.append('Removed records for matches involving: ' + ', '.join(st.session_state.Karters_filter))
                for filter in (filter_cols):
                    if len(st.session_state[f'{filter}_filter']) > 0:
                        df_filtered = df_filtered[df_filtered[filter].apply(lambda x: x not in st.session_state[f'{filter}_filter'])]
                        st.session_state.active_filters.append(f'Removed match records for {filter}: ' + ', '.join(st.session_state[f'{filter}_filter']))
                
                if len(st.session_state.active_filters) > 0:
                    st.session_state.df_filtered = df_filtered
    
        if len(st.session_state.active_filters) > 0:
            st.session_state.df = st.session_state.df_filtered
            karter_list = list(set(st.session_state.df['Karter'].values))
            karter_list.sort()
            st.session_state.karter_list = karter_list
            st.write('**Currently Applied Filters:**')
            for filter in st.session_state.active_filters:
                st.write(filter)
        else:
            st.session_state.df = df
        
        st.button('Clear Filters', on_click = clear_filters, disabled = st.session_state.disable_clear_filter)

    else:
        st.session_state.df = df

    st.write(f'**{len(karter_list)} Karters in the dataset:**')
    st.write(', '.join(karter_list))
    st.write(f'**{len(st.session_state.df)} records in the dataset**')

    st.write('**Data Preview (First 10 Records):**')
    st.dataframe(st.session_state.df.head(10), hide_index = True)
