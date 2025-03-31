import streamlit as st
import pandas as pd

path = 'va_12_19.csv'

@st.cache_data
def load_default_data(link):
    df_default = pd.read_csv(link)
    return df_default

@st.cache_data
def create_karter_list():
    karter_list = list(set(df_default['Karter'].values))
    karter_list.sort()
    return karter_list

@st.cache_data
def create_track_list():
    tracks = df_default.columns[-16:].tolist()
    return tracks

@st.cache_data
def clean_default_data():
    df = df_default.copy()
    df['Karters'] = df[['K1', 'K2', 'K3', 'K4']].values.tolist()
    df = df.drop(['K1', 'K2', 'K3', 'K4'], axis = 1)
    data_cols = df.columns.tolist()
    data_cols = [col for col in data_cols if col not in tracks] + tracks
    df = df[data_cols]
    return df

df_default = load_default_data(path)
karter_list = create_karter_list()
tracks = create_track_list()
df = clean_default_data()

if 'df_default' not in st.session_state:
    st.session_state.df_default = df_default

if 'karter_list' not in st.session_state:
    st.session_state.karter_list = karter_list

if 'tracks' not in st.session_state:
    st.session_state.tracks = tracks

if 'df' not in st.session_state:
    st.session_state.df = df

if 'valid_data' not in st.session_state:
    st.session_state.valid_data = True


if 'udatakey' in st.session_state:
    st.session_state.udatakey = st.session_state.udatakey

if 'apply_filters' in st.session_state:
    st.session_state.apply_filters = st.session_state.apply_filters

if 'm_player_choice' in st.session_state:
    st.session_state.m_player_choice = st.session_state.m_player_choice

if 'm_p1' in st.session_state:
    st.session_state.m_p1 = st.session_state.m_p1
if 'm_p2' in st.session_state:
    st.session_state.m_p2 = st.session_state.m_p2
if 'm_p3' in st.session_state:
    st.session_state.m_p3 = st.session_state.m_p3
if 'm_p4' in st.session_state:
    st.session_state.m_p4 = st.session_state.m_p4

if 'm_sims' in st.session_state:
    st.session_state.m_sims = st.session_state.m_sims

if 't_player_choice' in st.session_state:
    st.session_state.t_player_choice = st.session_state.t_player_choice

if 't_p1' in st.session_state:
    st.session_state.t_p1 = st.session_state.t_p1
if 't_p2' in st.session_state:
    st.session_state.t_p2 = st.session_state.t_p2
if 't_p3' in st.session_state:
    st.session_state.t_p3 = st.session_state.t_p3
if 't_p4' in st.session_state:
    st.session_state.t_p4 = st.session_state.t_p4
if 't_p5' in st.session_state:
    st.session_state.t_p5 = st.session_state.t_p5
if 't_p6' in st.session_state:
    st.session_state.t_p6 = st.session_state.t_p6
if 't_p7' in st.session_state:
    st.session_state.t_p7 = st.session_state.t_p7
if 't_p8' in st.session_state:
    st.session_state.t_p8 = st.session_state.t_p8
if 't_p9' in st.session_state:
    st.session_state.t_p9 = st.session_state.t_p9
if 't_p10' in st.session_state:
    st.session_state.t_p10 = st.session_state.t_p10
if 't_p11' in st.session_state:
    st.session_state.t_p11 = st.session_state.t_p11
if 't_p12' in st.session_state:
    st.session_state.t_p12 = st.session_state.t_p12
if 't_p13' in st.session_state:
    st.session_state.t_p13 = st.session_state.t_p13
if 't_p14' in st.session_state:
    st.session_state.t_p14 = st.session_state.t_p14
if 't_p15' in st.session_state:
    st.session_state.t_p15 = st.session_state.t_p15
if 't_p16' in st.session_state:
    st.session_state.t_p16 = st.session_state.t_p16

if 't_sims' in st.session_state:
    st.session_state.t_sims = st.session_state.t_sims
if 't_seed_choice' in st.session_state:
    st.session_state.t_seed_choice = st.session_state.t_seed_choice

if 'karterchoice' in st.session_state:
    st.session_state.karterchoice = st.session_state.karterchoice
if 'showrecordschoice' in st.session_state:
    st.session_state.showrecordschoice = st.session_state.showrecordschoice
if 'trackscomparechoice' in st.session_state:
    st.session_state.trackscomparechoice = st.session_state.trackscomparechoice
if 'comparedkarterchoice' in st.session_state:
    st.session_state.comparedkarterchoice = st.session_state.comparedkarterchoice
if 'matchupkarters' in st.session_state:
    st.session_state.matchupkarters = st.session_state.matchupkarters
if 'matchupshowrecordschoice' in st.session_state:
    st.session_state.matchupshowrecordschoice = st.session_state.matchupshowrecordschoice

pg = st.navigation([
    st.Page('0_Intro.py', title = 'Welcome to Mario Kart (Simulator)!'),
    st.Page('1_Upload_Instructions.py', title = 'Upload Instructions'),
    st.Page('2_Data.py', title = 'Select Your Data'),
    st.Page('3_Match_Sim.py', title = 'Simulate a Match'),
    st.Page('4_Tourn_Sim.py', title = 'Simulate a Tournament'),
    st.Page('5_Data_Viewer.py', title = 'Data Viewer')
])
pg.run()