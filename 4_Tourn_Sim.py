import streamlit as st
import numpy as np
import pandas as pd

if 't_karter_list_check' not in st.session_state:
    st.session_state.t_karter_list_check = st.session_state.karter_list

if 't_p1' not in st.session_state:
    st.session_state.t_p1 = None
if 't_p2' not in st.session_state:
    st.session_state.t_p2 = None
if 't_p3' not in st.session_state:
    st.session_state.t_p3 = None
if 't_p4' not in st.session_state:
    st.session_state.t_p4 = None
if 't_p5' not in st.session_state:
    st.session_state.t_p5 = None
if 't_p6' not in st.session_state:
    st.session_state.t_p6 = None
if 't_p7' not in st.session_state:
    st.session_state.t_p7 = None
if 't_p8' not in st.session_state:
    st.session_state.t_p8 = None
if 't_p9' not in st.session_state:
    st.session_state.t_p9 = None
if 't_p10' not in st.session_state:
    st.session_state.t_p10 = None
if 't_p11' not in st.session_state:
    st.session_state.t_p11 = None
if 't_p12' not in st.session_state:
    st.session_state.t_p12 = None
if 't_p13' not in st.session_state:
    st.session_state.t_p13 = None
if 't_p14' not in st.session_state:
    st.session_state.t_p14 = None
if 't_p15' not in st.session_state:
    st.session_state.t_p15 = None
if 't_p16' not in st.session_state:
    st.session_state.t_p16 = None

if 't_sims' not in st.session_state:
    st.session_state.t_sims = 500

karter_list = st.session_state.karter_list

disable_input = False
disable_sim = False
data_check = []

if st.session_state.valid_data == False:
    disable_input = True
    disable_sim = True
    data_check.append(True)
    st.error('**:red[There are problems with the selected data. Please change your input on the Select Your Data page.]**')

if (len(karter_list) < 16) & (st.session_state.valid_data == True):
    disable_input = True
    disable_sim = True
    data_check.append(True)
    st.error('**:red[There must be data for at least 16 karters to simulate a tournament. Please change your input on the Select Your Data page.]**')

if any(data_check) == False:

    if 'participants' not in st.session_state:
        st.session_state.participants = np.random.choice(karter_list, 16, replace = False).tolist()

    def reroll_participants():
        st.session_state.participants = np.random.choice(karter_list, 16, replace = False).tolist()

    if set(karter_list) != set(st.session_state.t_karter_list_check):
        reroll_participants()
        st.session_state.t_p1 = None
        st.session_state.t_p2 = None
        st.session_state.t_p3 = None
        st.session_state.t_p4 = None
        st.session_state.t_p5 = None
        st.session_state.t_p6 = None
        st.session_state.t_p7 = None
        st.session_state.t_p8 = None
        st.session_state.t_p9 = None
        st.session_state.t_p10 = None
        st.session_state.t_p11 = None
        st.session_state.t_p12 = None
        st.session_state.t_p13 = None
        st.session_state.t_p14 = None
        st.session_state.t_p15 = None
        st.session_state.t_p16 = None

    st.session_state.tp1key = 't_p1'
    st.session_state.tp2key = 't_p2'
    st.session_state.tp3key = 't_p3'
    st.session_state.tp4key = 't_p4'
    st.session_state.tp5key = 't_p5'
    st.session_state.tp6key = 't_p6'
    st.session_state.tp7key = 't_p7'
    st.session_state.tp8key = 't_p8'
    st.session_state.tp9key = 't_p9'
    st.session_state.tp10key = 't_p10'
    st.session_state.tp11key = 't_p11'
    st.session_state.tp12key = 't_p12'
    st.session_state.tp13key = 't_p13'
    st.session_state.tp14key = 't_p14'
    st.session_state.tp15key = 't_p15'
    st.session_state.tp16key = 't_p16'

    st.session_state.t_karter_list_check = karter_list
    tracks = st.session_state.tracks
    df = st.session_state.df

    if 'tourn_pivot' not in st.session_state:
        st.session_state.tourn_pivot = None

    if 't_sims_completed' not in st.session_state:
        st.session_state.t_sims_completed = None

    st.write('### Tournament Simulator')
    st.write(('Here you may simulate the results of a 16-player Virginia-style tournament. '
            'One tournament consists of a round of 16 (R16), a semifinal round, and a final match.'))
    tourn_explain = st.toggle('Show Detailed Tournament Explanation', value = False)
    if tourn_explain:
        st.write(('In the R16, eight total matches are played with each player playing two matches against non-repeating opponents. '
            'The eight highest scoring players in the R16 (most total points) advance to the semifinals. '
            'There are two semifinal matches with each player playing one match. Semifinals seeding is determined by R16 rank. '
            'The two highest scoring players from each semifinal match advance to the final round. '
            'In the final round, one match is played. The player with the most points in the final match is the tournament winner. '
            'All ties are resolved by a random tiebreak.'))
    st.write(('Use the input options below to choose the players, seeding, and number of simulations. '
            'Then click the Run Simulations button!'))
    st.write(('Please note that a tournament **may take several minutes or longer** to simulate with a high number of simulations set! '
            'Navigating to a different page while a simulation is in progress will cancel the simulation!'))

    player_choice = st.radio('**Select your players!**',
                            ['Choose players myself', 'Choose 16 random players'],
                            key = 't_player_choice', disabled = disable_input)

    if player_choice == 'Choose players myself':
        p_col1, p_col2, p_col3, p_col4 = st.columns(4)

        with p_col1:
            p1 = st.selectbox('Player 1', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp1key, disabled = disable_input)
            p5 = st.selectbox('Player 5', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp5key, disabled = disable_input)
            p9 = st.selectbox('Player 9', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp9key, disabled = disable_input)
            p13 = st.selectbox('Player 13', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp13key, disabled = disable_input)

        with p_col2:
            p2 = st.selectbox('Player 2', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp2key, disabled = disable_input)
            p6 = st.selectbox('Player 6', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp6key, disabled = disable_input)
            p10 = st.selectbox('Player 10', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp10key, disabled = disable_input)
            p14 = st.selectbox('Player 14', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp14key, disabled = disable_input)

        with p_col3:
            p3 = st.selectbox('Player 3', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp3key, disabled = disable_input)
            p7 = st.selectbox('Player 7', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp7key, disabled = disable_input)
            p11 = st.selectbox('Player 11', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp11key, disabled = disable_input)
            p15 = st.selectbox('Player 15', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp15key, disabled = disable_input)

        with p_col4:
            p4 = st.selectbox('Player 4', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp4key, disabled = disable_input)
            p8 = st.selectbox('Player 8', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp8key, disabled = disable_input)
            p12 = st.selectbox('Player 12', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp12key, disabled = disable_input)
            p16 = st.selectbox('Player 16', karter_list, index = None, placeholder = 'Select your player!', key = st.session_state.tp16key, disabled = disable_input)

        participants = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16]

        if (None in participants) | (len(participants) < 16) | (len(set(participants)) != len(participants)):
            disable_sim = True
            st.markdown('**:red[You must select 16 different players. Please change your selections.]**')
    else:
        participants = st.session_state.participants
        p_col1, p_col2, p_col3, p_col4 = st.columns(4)

        with p_col1:
            st.write('Player 1: ', participants[0])
            st.write('Player 5: ', participants[4])
            st.write('Player 9: ', participants[8])
            st.write('Player 13: ', participants[12])

        with p_col2:
            st.write('Player 2: ', participants[1])
            st.write('Player 6: ', participants[5])
            st.write('Player 10: ', participants[9])
            st.write('Player 14: ', participants[13])

        with p_col3:
            st.write('Player 3: ', participants[2])
            st.write('Player 7: ', participants[6])
            st.write('Player 11: ', participants[10])
            st.write('Player 15: ', participants[14])

        with p_col4:
            st.write('Player 4: ', participants[3])
            st.write('Player 8: ', participants[7])
            st.write('Player 12: ', participants[11])
            st.write('Player 16: ', participants[15])

        st.button('Re-Roll', on_click = reroll_participants, disabled = disable_input)

    df = df[df['Karter'].isin(participants)]

    seed_choice_help = ('If "Yes" the R16 matchups will be randomized to be different for each simulation. '
                        'If "No" the R16 matchups will be the same for every simulation, '
                        'and players will be seeded based on placement in the player selection grid. '
                        'Players in the same row will face each other in the first set of matches, '
                        'and players in the same column will face each other in the second set of matches. '
                        'Choosing "No" is only recommended for simulating a specific tournament draw.')
    seed_choice = st.radio('**Randomize R16 seeding?**',
                            ['Yes (Recommended)', 'No'],
                            key = 't_seed_choice', help = seed_choice_help, disabled = disable_input)
    if seed_choice == 'No':
        rand_seed = False
    else:
        rand_seed = True

    sims_help = 'Number of times the tournament will be simulated. A higher number will make the results more consistent but will take longer to run.'
    sims = st.number_input('**Number of Simulations**', min_value = 1, max_value = 10000, help = sims_help, key = 't_sims', disabled = disable_input)

    def simulate_tournament(participants, sims, rand_seed):
        sim_results = {'Sim': [], 'Pools Results': [], 'Pools Pivot': [], 'Semis Results': [], 'Final Results': []}
        tracks_dic = {t: [] for t in tracks}

        def karter_filter(karter):
            df_karter = df[df['Karter'] == karter]
            return df_karter

        def opponent_filter(karter):
            opponents = [opponent for opponent in karters if opponent != karter]
            df_opponents = df[(df['Karter'] == karter) & (df['Karters'].apply(lambda krts: len(set(krts).intersection(set(opponents)))) > 0)]
            return df_opponents

        df_karter_dic = {k: karter_filter(k) for k in participants}

        def draw_finish(karter):
            finishes = df_opponents_dic[karter].loc[:,track].tolist()
            if len(finishes) < 2:
                finishes.append(np.random.choice(df_karter_dic[karter].loc[:,track]))
            return np.random.choice(finishes)

        for sim in range(1, sims + 1):

            if rand_seed:
                participants = np.random.choice(participants, 16, replace = False).tolist()
            pools = [
                [participants[0], participants[1], participants[2], participants[3]],
                [participants[4], participants[5], participants[6], participants[7]],
                [participants[8], participants[9], participants[10], participants[11]],
                [participants[12], participants[13], participants[14], participants[15]],
                [participants[0], participants[4], participants[8], participants[12]],
                [participants[1], participants[5], participants[9], participants[13]],
                [participants[2], participants[6], participants[10], participants[14]],
                [participants[3], participants[7], participants[11], participants[15]],
            ]

            pools_results = {'Pool': [], 'Karter': []}
            pools_results.update(tracks_dic)
            pool_num = 1

            for pool in pools:
                karters = pool
                df_opponents_dic = {k: opponent_filter(k) for k in karters}
                results = {'Pool': [pool_num, pool_num, pool_num, pool_num], 'Karter': karters}

                for track in tracks:
                    track_finishes = [draw_finish(karter) for karter in karters]

                    if len(set(track_finishes)) < 4:
                        track_finishes = np.lexsort((np.random.random(4), track_finishes)).argsort().tolist()
                    else:
                        track_finishes = np.argsort(track_finishes).argsort().tolist()
                    results[track] = [fin + 1 for fin in track_finishes]
                
                pools_results = {k: v + results[k] for k, v in pools_results.items()}
                pool_num += 1

            df_pools = pd.DataFrame(pools_results)
            df_pools['1sts'] = (df_pools[tracks] == 1).sum(axis=1)
            df_pools['2nds'] = (df_pools[tracks] == 2).sum(axis=1)
            df_pools['3rds'] = (df_pools[tracks] == 3).sum(axis=1)
            df_pools['Points'] = (df_pools['1sts']*3) + (df_pools['2nds']*2) + (df_pools['3rds'])
            
            pools_pivot = df_pools.pivot_table(values = 'Points', index = 'Karter', aggfunc = 'sum')
            pools_pivot['TB'] = np.lexsort((np.random.random(16), pools_pivot['Points'])).argsort().tolist()
            pools_pivot = pools_pivot.sort_values(by = 'TB', ascending = False)
            pools_karters_sorted = pools_pivot.index.tolist()

            semis = [
                [pools_karters_sorted[0], pools_karters_sorted[3], pools_karters_sorted[4], pools_karters_sorted[7]],
                [pools_karters_sorted[1], pools_karters_sorted[2], pools_karters_sorted[5], pools_karters_sorted[6]]
            ]

            semis_results = {'Semi': [], 'Karter': []}
            semis_results.update(tracks_dic)
            semi_num = 1

            for semi in semis:
                karters = semi
                df_opponents_dic = {k: opponent_filter(k) for k in karters}
                results = {'Semi': [semi_num, semi_num, semi_num, semi_num], 'Karter': karters}

                for track in tracks:
                    track_finishes = [draw_finish(karter) for karter in karters]

                    if len(set(track_finishes)) < 4:
                        track_finishes = np.lexsort((np.random.random(4), track_finishes)).argsort().tolist()
                    else:
                        track_finishes = np.argsort(track_finishes).argsort().tolist()
                    results[track] = [fin + 1 for fin in track_finishes]
                
                semis_results = {k: v + results[k] for k, v in semis_results.items()}
                semi_num += 1

            df_semis = pd.DataFrame(semis_results)
            df_semis['1sts'] = (df_semis[tracks] == 1).sum(axis=1)
            df_semis['2nds'] = (df_semis[tracks] == 2).sum(axis=1)
            df_semis['3rds'] = (df_semis[tracks] == 3).sum(axis=1)
            df_semis['Points'] = (df_semis['1sts']*3) + (df_semis['2nds']*2) + (df_semis['3rds'])
            df_semis['TB'] = np.random.random(len(df_semis))
            df_semis = df_semis.sort_values(by = ['Semi', 'Points', 'TB'], ascending = [True, False, False])
            df_semis['Place'] = df_semis.groupby(by = 'Semi')['Points'].rank(method = 'first', ascending = False)

            final = df_semis.sort_values(by = 'Place')['Karter'].tolist()[0:4]

            karters = final
            df_opponents_dic = {k: opponent_filter(k) for k in karters}
            results = {'Karter': karters}

            for track in tracks:
                track_finishes = [draw_finish(karter) for karter in karters]

                if len(set(track_finishes)) < 4:
                    track_finishes = np.lexsort((np.random.random(4), track_finishes)).argsort().tolist()
                else:
                    track_finishes = np.argsort(track_finishes).argsort().tolist()
                results[track] = [fin + 1 for fin in track_finishes]
                
            df_final = pd.DataFrame(results)
            df_final['1sts'] = (df_final[tracks] == 1).sum(axis=1)
            df_final['2nds'] = (df_final[tracks] == 2).sum(axis=1)
            df_final['3rds'] = (df_final[tracks] == 3).sum(axis=1)
            df_final['Points'] = (df_final['1sts']*3) + (df_final['2nds']*2) + (df_final['3rds'])
            place = np.lexsort((np.random.random(4), df_final['Points'])).argsort().tolist()
            df_final['Place'] = [4 - p for p in place]

            sim_results['Sim'].append(sim)
            sim_results['Pools Results'].append(df_pools)
            sim_results['Pools Pivot'].append(pools_pivot)
            sim_results['Semis Results'].append(df_semis)
            sim_results['Final Results'].append(df_final)
            tourn_sim_progress.progress(sim / sims, text = f'{sim} of {sims} completed')

        df_sims_final = pd.concat(sim_results['Final Results'], ignore_index = True)
        final_sims_pivot = df_sims_final.groupby('Karter').agg(
            final_apps = ('Points', 'count'),
            final_avg_pts = ('Points', 'mean')
        )
        win_sims_pivot = df_sims_final[df_sims_final['Place'] == 1].groupby('Karter').agg(
            tourn_wins = ('Place', 'count')
        )
        win_sims_pivot['Tourn Win %'] = win_sims_pivot['tourn_wins'] / sims * 100
        final_sims_pivot['Final Reach %'] = final_sims_pivot['final_apps'] / sims * 100
        final_sims_pivot = final_sims_pivot.merge(win_sims_pivot, on = 'Karter', how = 'outer')

        final_sims_pivot = final_sims_pivot.rename(columns = {
            'tourn_wins': 'Tourn Wins',
            'final_avg_pts': 'Avg Points in Final'
        })

        df_pools_pivot = pd.concat(sim_results['Pools Pivot'], ignore_index = False)
        pools_sims_pivot = df_pools_pivot.pivot_table(values = 'Points', index = 'Karter', aggfunc = 'mean')
        pools_sims_pivot = pools_sims_pivot.rename(columns = {'Points': 'Avg R16 Points'})

        sims_matches = [
            pd.concat(sim_results['Pools Results'], ignore_index = True),
            pd.concat(sim_results['Pools Results'], ignore_index = True),
            pd.concat(sim_results['Pools Results'], ignore_index = True)]
        df_sims_matches = pd.concat(sims_matches, ignore_index = True)

        matches_sims_pivot = df_sims_matches.pivot_table(values = 'Points', index = 'Karter', aggfunc = 'mean')
        matches_sims_pivot = matches_sims_pivot.rename(columns = {'Points': 'Avg Points Per Match'})

        df_sims_semis = pd.concat(sim_results['Semis Results'], ignore_index = True)
        semis_sims_pivot = df_sims_semis.pivot_table(values = 'Points', index = 'Karter', aggfunc = 'count')
        semis_sims_pivot['Points'] = semis_sims_pivot['Points'] / sims * 100
        semis_sims_pivot = semis_sims_pivot.rename(columns = {'Points': 'Semis Reach %'})

        tourn_pivot = matches_sims_pivot.merge(pools_sims_pivot, on = 'Karter', how = 'outer')
        tourn_pivot = tourn_pivot.merge(semis_sims_pivot, on = 'Karter', how = 'outer')
        tourn_pivot = tourn_pivot.merge(final_sims_pivot, on = 'Karter', how = 'outer')
        tourn_pivot = tourn_pivot[[
            'Tourn Win %',
            'Tourn Wins',
            'Avg Points Per Match',
            'Avg R16 Points',
            'Semis Reach %',
            'Final Reach %',
            'Avg Points in Final'
            ]].sort_values(by = ['Tourn Win %', 'Avg Points Per Match'], ascending = False).apply(lambda x: np.round(x, decimals = 2))
        tourn_pivot[[
            'Tourn Win %',
            'Tourn Wins',
            'Semis Reach %',
            'Final Reach %',
            ]] = tourn_pivot[[
            'Tourn Win %',
            'Tourn Wins',
            'Semis Reach %',
            'Final Reach %',
            ]].fillna(0)
        tourn_pivot['Tourn Wins'] = tourn_pivot['Tourn Wins'].apply(lambda n: int(n))

        st.session_state.tourn_pivot = tourn_pivot
        st.session_state.t_sims_completed = sims

    st.button('Run Simulations', disabled = disable_sim, on_click = simulate_tournament, args = (participants, sims, rand_seed))

    tourn_sim_progress = st.progress(0.0, text = 'Running Simulations...')
    tourn_sim_progress.empty()

    if st.session_state.tourn_pivot is not None:
        st.write(f'**Results of {st.session_state.t_sims_completed} Simulated Tournaments:**')
        st.dataframe(st.session_state.tourn_pivot)
        results_explain = st.toggle('Show Results Table Explanation')
        if results_explain:
            st.write('**Tourn Win % / Wins:** The percent/number of times the karter won the simulated tournament.')
            st.write('**Avg Points Per Match:** The average points earned per match across all simulated tournament matches.')
            st.write('**Avg R16 Points:** The average number of total points earned in the round of 16 across all simulated tournaments.')
            st.write('**Semis/Final Reach %:** The percent of simulated tournaments in which the karter advanced to the semifinals/final.')
            st.write('**Avg Points in Final:** The average number of points earned in final round matches across all simulated tournaments.')