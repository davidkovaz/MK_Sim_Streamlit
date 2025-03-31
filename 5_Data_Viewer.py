import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style = 'ticks', rc = {'font.family': 'Franklin Gothic Medium'})

disable_input = False
data_check = False

if st.session_state.valid_data == False:
    disable_input = True
    data_check = True
    st.error('**:red[There are problems with the selected data. Please change your input on the Select Your Data page.]**')

if data_check == False:

    if 'dv_karter_list_check' not in st.session_state:
        st.session_state.dv_karter_list_check = st.session_state.karter_list

    if 'karterchoice' not in st.session_state:
        st.session_state.karterchoice = None

    if 'showrecordschoice' not in st.session_state:
        st.session_state.showrecordschoice = None

    if 'trackscomparechoice' not in st.session_state:
        st.session_state.trackscomparechoice = False

    if 'comparedkarterchoice' not in st.session_state:
        st.session_state.comparedkarterchoice = None

    if 'matchupkarters' not in st.session_state:
        st.session_state.matchupkarters = []

    if 'matchupshowrecordschoice' not in st.session_state:
        st.session_state.matchupshowrecordschoice = None

    karter_list = st.session_state.karter_list

    if set(karter_list) != set(st.session_state.dv_karter_list_check):
        st.session_state.karterchoice = None
        st.session_state.showrecordschoice = None
        st.session_state.trackscomparechoice = False
        st.session_state.comparedkarterchoice = None
        st.session_state.matchupkarters = []
        st.session_state.matchupshowrecordschoice = None

    st.session_state.karterchoicekey = 'karterchoice'
    st.session_state.showrecordschoicekey = 'showrecordschoice'
    st.session_state.trackscomparechoicekey = 'trackscomparechoice'
    st.session_state.comparedkarterchoicekey = 'comparedkarterchoice'
    st.session_state.matchupkarterskey = 'matchupkarters'
    st.session_state.matchupshowrecordschoicekey = 'matchupshowrecordschoice'

    st.session_state.dv_karter_list_check = karter_list
    tracks = st.session_state.tracks
    df = st.session_state.df.copy()
    track_data_cols = df.columns.tolist()
    df['1sts'] = (df[tracks] == 1).sum(axis=1)
    df['2nds'] = (df[tracks] == 2).sum(axis=1)
    df['3rds'] = (df[tracks] == 3).sum(axis=1)
    df['4ths'] = (df[tracks] == 4).sum(axis=1)
    df['Points'] = (df['1sts']*3) + (df['2nds']*2) + (df['3rds'])
    stat_cols = [col for col in track_data_cols if col not in tracks] + ['Points', '1sts', '2nds', '3rds', '4ths']
    df = df[track_data_cols + ['Points', '1sts', '2nds', '3rds', '4ths']]
    df_tracks = df[track_data_cols]
    df_stats = df[stat_cols]

    matches_pivot = df.pivot_table(values = ['Points'], index = 'Karter', aggfunc = 'count')
    matches_pivot = matches_pivot.rename(columns = {'Points': 'Matches'})
    stats_pivot = df.pivot_table(values = ['Points', '1sts'], index = 'Karter', aggfunc = 'mean')
    stats_pivot = stats_pivot.rename(columns = {'Points': 'Avg Points Per Match', '1sts': 'Avg 1sts Per Match'})
    stats_pivot = stats_pivot.merge(matches_pivot, on = 'Karter', how = 'outer')

    df_track_points = df.copy()
    df_track_points[tracks] = df_track_points[tracks].apply(lambda f: 4 - f)
    track_points_pivot = df_track_points.pivot_table(values = tracks, index = 'Karter', aggfunc = 'mean')
    track_points_pivot = track_points_pivot[tracks]

    disable_input = False

    if st.session_state.valid_data == False:
        disable_input = True
        st.error('**:red[There are problems with the selected data. Please change your input on the Select Your Data page.]**')

    st.write('### Data Viewer')
    st.write(('Here you may view match records and statistics for karters in the selected dataset. '
            'Please note that any filters you have applied on the Select Your Data page will also be appiled to the data you view here. '))

    def clear_comparisons():
        del st.session_state.comparedkarterchoice
        del st.session_state.matchupkarters

    karter = st.selectbox('**View data for:**',
                            karter_list,
                            index = None, placeholder = 'Select your karter!', key = st.session_state.karterchoicekey, disabled = disable_input, on_change = clear_comparisons)

    if karter is not None:
        st.write(f'#### {karter}\'s Overview')

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        num_matches = np.round(stats_pivot.loc[karter, 'Matches'], decimals = 2)
        metric_col1.metric(label = 'Number of Matches', value = num_matches, delta = None)

        avg_ppm = np.round(stats_pivot.loc[karter, 'Avg Points Per Match'], decimals = 2)
        metric_col2.metric(label = 'Average Points Per Match', value = avg_ppm, delta = None)

        avg_1sts = np.round(stats_pivot.loc[karter, 'Avg 1sts Per Match'], decimals = 2)
        metric_col3.metric(label = 'Average 1sts Per Match', value = avg_1sts, delta = None)

        show_records = st.segmented_control(f'**Show {karter}\'s match records:**',
                                            options = ['All Stats', 'Track Stats Only', 'Match Stats Only'],
                                            default = None,
                                            selection_mode = 'single',
                                            key = st.session_state.showrecordschoicekey)

        dfs_dictionary = {'All Stats': df, 'Track Stats Only': df_tracks, 'Match Stats Only': df_stats}

        if show_records is not None:
            df_show = dfs_dictionary[show_records]
            st.dataframe(df_show[df_show['Karter'] == karter], hide_index = True)

        st.write(f'#### {karter}\'s Track Breakdown')

        tracks_compare_choice = st.checkbox('Compare to another karter', key = st.session_state.trackscomparechoicekey)

        compared_karter_list = karter_list.copy()
        compared_karter_list.remove(karter)
        compared_karter = None

        if tracks_compare_choice:
            compared_karter = st.selectbox('Compare to:',
                                                compared_karter_list,
                                                index = None, placeholder = 'Select your karter!', key = st.session_state.comparedkarterchoicekey, disabled = disable_input)

            if compared_karter is not None:
                compare_track_points = track_points_pivot[track_points_pivot.index.isin([karter, compared_karter])]
                compare_track_points = compare_track_points.transpose()
                compare_track_points['Difference'] = compare_track_points[karter] - compare_track_points[compared_karter]
                largest_value = max(compare_track_points[karter].max(), compare_track_points[compared_karter].max())
                if round(largest_value) < largest_value:
                    min_max_limit = round(largest_value) + 0.5
                else:
                    min_max_limit = round(largest_value)
                
                fig, ax = plt.subplots()
                sns.barplot(
                    data = compare_track_points,
                    y = compare_track_points.index,
                    x = 'Difference',
                    ax = ax,
                    hue = 'Difference',
                    palette = 'crest',
                    legend = False
                    )
                plt.title(f'Average Points on Each Track ({karter} vs. {compared_karter})')
                plt.xlim(min_max_limit * -1, min_max_limit)
                plt.ylabel('')
                plt.xlabel(f'Difference in Average Points ({karter} minus {compared_karter})')
                plt.tight_layout()
                st.pyplot(fig)
                figure_explain = st.toggle('Show Figure Explanation')
                if figure_explain:
                    st.write('The above figure shows the difference between the karters in average points on each track. '
                            f'Bars extending to the right of zero favor {karter}, and bars extending to the left of zero favor {compared_karter}.')
        else:
            karter_track_points = track_points_pivot[track_points_pivot.index == karter].transpose()

            fig, ax = plt.subplots()
            sns.barplot(
                data = karter_track_points,
                y = karter_track_points.index,
                x = karter,
                ax = ax,
                hue = karter,
                palette = 'crest',
                legend = False
                )
            plt.title(f'{karter}\'s Average Points on Each Track')
            plt.xlim(0, 3)
            plt.ylabel('')
            plt.xlabel('Average Points')
            plt.tight_layout()
            st.pyplot(fig)
        
        st.write(f'#### {karter}\'s Matchup Stats')

        matchup_karters = st.multiselect(f'**View records for {karter}\'s matches that involve any of the following karters:**',
                                        compared_karter_list,
                                        max_selections = 3,
                                        placeholder = 'Select your karters!',
                                        key = st.session_state.matchupkarterskey)
        
        if len(matchup_karters) > 0:
            df_matchup = df[df['Karters'].apply(lambda x: any(y in matchup_karters for y in x))]
            matchup_karters_text = ' or '.join(matchup_karters)
            if len(df_matchup[df_matchup['Karter'] == karter]) == 0:
                st.write(f'No matches against {matchup_karters_text} were found!')
            else:
                df_matchup_tracks = df_matchup[track_data_cols]
                df_matchup_stats = df_matchup[stat_cols]

                matchup_matches_pivot = df_matchup.pivot_table(values = ['Points'], index = 'Karter', aggfunc = 'count')
                matchup_matches_pivot = matchup_matches_pivot.rename(columns = {'Points': 'Matches'})
                matchup_stats_pivot = df_matchup.pivot_table(values = ['Points', '1sts'], index = 'Karter', aggfunc = 'mean')
                matchup_stats_pivot = matchup_stats_pivot.rename(columns = {'Points': 'Avg Points Per Match', '1sts': 'Avg 1sts Per Match'})
                matchup_stats_pivot = matchup_stats_pivot.merge(matchup_matches_pivot, on = 'Karter', how = 'outer')

                df_matchup_track_points = df_track_points[df_track_points['Karters'].apply(lambda x: any(y in matchup_karters for y in x))]
                matchup_track_points_pivot = df_matchup_track_points.pivot_table(values = tracks, index = 'Karter', aggfunc = 'mean')
                matchup_track_points_pivot = matchup_track_points_pivot[tracks]

                matchup_metric_col1, matchup_metric_col2, matchup_metric_col3 = st.columns(3)

                matchup_num_matches = np.round(matchup_stats_pivot.loc[karter, 'Matches'], decimals = 2)
                matchup_metric_col1.metric(label = 'Number of Matches', value = matchup_num_matches, delta = None)

                matchup_avg_ppm = np.round(matchup_stats_pivot.loc[karter, 'Avg Points Per Match'], decimals = 2)
                matchup_metric_col2.metric(label = 'Average Points Per Match', value = matchup_avg_ppm, delta = np.round(matchup_avg_ppm - avg_ppm, decimals = 2))

                matchup_avg_1sts = np.round(matchup_stats_pivot.loc[karter, 'Avg 1sts Per Match'], decimals = 2)
                matchup_metric_col3.metric(label = 'Average 1sts Per Match', value = matchup_avg_1sts, delta = np.round(matchup_avg_1sts - avg_1sts, decimals = 2))

                matchup_show_records = st.segmented_control(f'**Show {karter}\'s matchup records:**',
                                                    options = ['All Stats', 'Track Stats Only', 'Match Stats Only'],
                                                    default = None,
                                                    selection_mode = 'single',
                                                    key = st.session_state.matchupshowrecordschoicekey)

                matchup_dfs_dictionary = {'All Stats': df_matchup, 'Track Stats Only': df_matchup_tracks, 'Match Stats Only': df_matchup_stats}

                if matchup_show_records is not None:
                    df_matchup_show = matchup_dfs_dictionary[matchup_show_records]
                    st.dataframe(df_matchup_show[df_matchup_show['Karter'] == karter], hide_index = True)
                
                matchup_karter_track_points = matchup_track_points_pivot[matchup_track_points_pivot.index == karter].transpose()

                matchup_fig, matchup_ax = plt.subplots()
                sns.barplot(
                    data = matchup_karter_track_points,
                    y = matchup_karter_track_points.index,
                    x = karter,
                    ax = matchup_ax,
                    hue = karter,
                    palette = 'crest',
                    legend = False
                    )
                plt.title(f'{karter}\'s Average Points in Matches with {matchup_karters_text}')
                plt.xlim(0, 3)
                plt.ylabel('')
                plt.xlabel('Average Points')
                plt.tight_layout()
                st.pyplot(matchup_fig)