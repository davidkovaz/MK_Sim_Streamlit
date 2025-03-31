import streamlit as st
import numpy as np
import pandas as pd

if 'm_karter_list_check' not in st.session_state:
    st.session_state.m_karter_list_check = st.session_state.karter_list

if 'm_p1' not in st.session_state:
    st.session_state.m_p1 = None
if 'm_p2' not in st.session_state:
    st.session_state.m_p2 = None
if 'm_p3' not in st.session_state:
    st.session_state.m_p3 = None
if 'm_p4' not in st.session_state:
    st.session_state.m_p4 = None

if 'm_sims' not in st.session_state:
    st.session_state.m_sims = 500

karter_list = st.session_state.karter_list

disable_input = False
disable_sim = False
data_check = []

if st.session_state.valid_data == False:
    disable_input = True
    disable_sim = True
    data_check.append(True)
    st.error('**:red[There are problems with the selected data. Please change your input on the Select Your Data page.]**')

if (len(karter_list) < 4) & (st.session_state.valid_data == True):
    disable_input = True
    disable_sim = True
    data_check.append(True)
    st.error('**:red[There must be data for at least 4 karters to simulate a match. Please change your input on the Select Your Data page.]**')

if any(data_check) == False:

    if 'karters' not in st.session_state:
        st.session_state.karters = np.random.choice(karter_list, 4, replace = False).tolist()

    def reroll_ktrs():
        st.session_state.karters = np.random.choice(karter_list, 4, replace = False).tolist()

    if set(karter_list) != set(st.session_state.m_karter_list_check):
        reroll_ktrs()
        st.session_state.m_p1 = None
        st.session_state.m_p2 = None
        st.session_state.m_p3 = None
        st.session_state.m_p4 = None

    st.session_state.mp1key = 'm_p1'
    st.session_state.mp2key = 'm_p2'
    st.session_state.mp3key = 'm_p3'
    st.session_state.mp4key = 'm_p4'

    st.session_state.m_karter_list_check = karter_list
    tracks = st.session_state.tracks
    df = st.session_state.df

    if 'match_pivot' not in st.session_state:
        st.session_state.match_pivot = None

    if 'm_sims_completed' not in st.session_state:
        st.session_state.m_sims_completed = None

    st.write('### Match Simulator')
    st.write(('Here you may simulate the results of a 4-player match. '
            'One match consists of 16 races (one race on each track). '
            'Players earn points based on their finish in each race, '
            'with 1st place = 3 points, 2nd place = 2 points, and 3rd place = 1 point. '
            'The winner is the player with the most points after 16 races. '
            'If there is a tie for most points, the match winner is decided by a random tiebreak.'))
    st.write(('Use the input options below to choose the players and number of simulations. '
            'Then click the Run Simulations button!'))
    st.write(('Please note that navigating to a different page while a simulation is in progress will cancel the simulation!'))

    player_choice = st.radio('**Select your players!**',
                            ['Choose players myself', 'Choose 4 random players'],
                            key = 'm_player_choice', disabled = disable_input)

    if player_choice == 'Choose players myself':
        p1 = st.selectbox('Player 1', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.mp1key, disabled = disable_input)
        p2 = st.selectbox('Player 2', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.mp2key, disabled = disable_input)
        p3 = st.selectbox('Player 3', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.mp3key, disabled = disable_input)
        p4 = st.selectbox('Player 4', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.mp4key, disabled = disable_input)

        karters = [p1, p2, p3, p4]

        if (None in karters) | (len(karters) < 4) | (len(set(karters)) != len(karters)):
            disable_sim = True
            st.markdown('**:red[You must select 4 different players. Please change your selections.]**')
    else:
        karters = st.session_state.karters
        st.write('Player 1: ', karters[0])
        st.write('Player 2: ', karters[1])
        st.write('Player 3: ', karters[2])
        st.write('Player 4: ', karters[3])
        st.button('Re-Roll', on_click = reroll_ktrs, disabled = disable_input)

    df = df[df['Karter'].isin(karters)]

    sims_help = 'Number of times the match will be simulated. A higher number will make the results more consistent but will take longer to run.'
    sims = st.number_input('**Number of Simulations**', min_value = 1, max_value = 10000, help = sims_help, key = 'm_sims', disabled = disable_input)

    def simulate_match(karters, sims):
        sim_results = {'Sim': [], 'Karter': []}
        tracks_dic = {t: [] for t in tracks}
        sim_results.update(tracks_dic)

        def karter_filter(karter):
            df_karter = df[df['Karter'] == karter]
            return df_karter

        def opponent_filter(karter):
            opponents = [opponent for opponent in karters if opponent != karter]
            df_opponents = df[(df['Karter'] == karter) & (df['Karters'].apply(lambda krts: len(set(krts).intersection(set(opponents)))) > 0)]
            return df_opponents

        df_karter_dic = {k: karter_filter(k) for k in karters}
        df_opponents_dic = {k: opponent_filter(k) for k in karters}

        def draw_finish(karter):
            finishes = df_opponents_dic[karter].loc[:,track].tolist()
            if len(finishes) < 2:
                finishes.append(np.random.choice(df_karter_dic[karter].loc[:,track]))
            return np.random.choice(finishes)
        
        for sim in range(1, sims + 1):
            results = {'Sim': [sim, sim, sim, sim], 'Karter': karters}

            for track in tracks:
                track_finishes = [draw_finish(karter) for karter in karters]

                if len(set(track_finishes)) < 4:
                    track_finishes = np.lexsort((np.random.random(4), track_finishes)).argsort().tolist()
                else:
                    track_finishes = np.argsort(track_finishes).argsort().tolist()
                results[track] = [fin + 1 for fin in track_finishes]
            
            sim_results = {k: v + results[k] for k, v in sim_results.items()}
            match_sim_progress.progress(sim / sims, text = f'{sim} of {sims} completed')
        
        df_results = pd.DataFrame(sim_results)
        df_results['1sts'] = (df_results[tracks] == 1).sum(axis=1)
        df_results['2nds'] = (df_results[tracks] == 2).sum(axis=1)
        df_results['3rds'] = (df_results[tracks] == 3).sum(axis=1)
        df_results['4ths'] = (df_results[tracks] == 4).sum(axis=1)
        df_results['Points'] = (df_results['1sts']*3) + (df_results['2nds']*2) + (df_results['3rds'])
        df_results['TB'] = np.random.random(len(df_results))
        df_results = df_results.sort_values(by = ['Sim', 'Points', 'TB'], ascending = [True, False, False])
        df_results['Place'] = df_results.groupby(by = 'Sim')['Points'].rank(method = 'first', ascending = False)

        match_pivot = df_results.pivot_table(values = ['Points', '1sts', '2nds', '3rds', '4ths'], index = 'Karter', aggfunc = 'mean')
        match_pivot = match_pivot.rename(columns = {
            'Points': 'Avg Points',
            '1sts': 'Avg # of 1sts',
            '2nds': 'Avg # of 2nds',
            '3rds': 'Avg # of 3rds',
            '4ths': 'Avg # of 4ths'
        })
        place_pivot = df_results[df_results['Place'] == 1].pivot_table(values = 'Place', index = 'Karter', aggfunc = 'count')
        place_pivot = place_pivot.rename(columns = {'Place': 'Wins'})
        place_pivot['Win %'] = place_pivot['Wins'] / sims * 100
        match_pivot = match_pivot.merge(place_pivot, on = 'Karter', how = 'outer')
        match_pivot[['Win %', 'Avg Points', 'Avg # of 1sts', 'Avg # of 2nds', 'Avg # of 3rds', 'Avg # of 4ths']] = match_pivot[[
            'Win %', 'Avg Points', 'Avg # of 1sts', 'Avg # of 2nds', 'Avg # of 3rds', 'Avg # of 4ths'
            ]].apply(lambda x: np.round(x, decimals = 2))
        match_pivot = match_pivot[[
            'Win %', 'Wins', 'Avg Points', 'Avg # of 1sts', 'Avg # of 2nds', 'Avg # of 3rds', 'Avg # of 4ths'
            ]].fillna(0).sort_values(by = ['Win %', 'Avg Points'], ascending = False)

        st.session_state.match_pivot = match_pivot
        st.session_state.m_sims_completed = sims

    st.button('Run Simulations', disabled = disable_sim, on_click = simulate_match, args = (karters, sims))

    match_sim_progress = st.progress(0.0, text = 'Running Simulations...')
    match_sim_progress.empty()

    if st.session_state.match_pivot is not None:
        st.write(f'**Results of {st.session_state.m_sims_completed} Simulated Matches:**')
        st.dataframe(st.session_state.match_pivot)
        results_explain = st.toggle('Show Results Table Explanation')
        if results_explain:
            st.write('**Win % / Wins:** The percent/number of times the karter won the simulated match.')
            st.write('**Avg Points:** The average points earned across all simulated matches.')
            st.write('**Avg # of 1sts/2nds/3rds/4ths:** The average number of 1st/2nd/3rd/4th place race finishes across all simulated matches.')