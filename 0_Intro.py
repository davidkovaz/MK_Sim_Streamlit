import streamlit as st

st.markdown('### Welcome to Mario Kart (Simulator)!')

st.markdown('#### What is this?')
st.markdown(('This app allows users to simulate the results of 4-player Mario Kart 64 matches based on data from real matches. '
             'Results are simulated at the track level by drawing random results from the data for the karters involved in the match. '
             'Using this app, you can simulate a full 4-player match or an entire 16-player tournament! '
             'You may use the default data built into the app (Virginia tournament matches from 2012 to 2019) or upload your own data to use as the basis for the simulations.'))

st.markdown('#### How do I use this?')
st.markdown(('If you want to just use the default data and get right to simulating, you may immediately navigate to the Simulate a Match/Tournament pages. '
             'Then just follow the instructions on those pages. If you want to use your own data, first please CAREFULLY review the Upload Instructions page. '
             'Then upload your formatted data file on the Select Your Data page.'))

st.markdown('#### Want to know more?')
st.markdown(('If you would like to know more about how the simulator works and how it was developed, '
             'I encourage you to read the [documentation](https://github.com/davidkovaz/MK_Sim_Streamlit/blob/80be8d254b44912b3e2ec74c30696ceda283b6cd/README.md) '
             'in the [GitHub repository](https://github.com/davidkovaz/MK_Sim_Streamlit) I created for the app. '
             'This app was written in Python and the source code is freely available for anyone to view, use, and modify.'))

st.markdown('#### DISCLAIMER:')
st.markdown(('Simulation results produced by this app are NOT meant to be an indicator of individual skill in Mario Kart. '
             'This app simply provides a method of estimating win percentages for hypothetical matchups purely based on the data it is given. '
             'This method is not guaranteed to produce realistic results. '
             'I did not create and share this app with any intention of causing arguments, hurt feelings, etc. '
             'So please do not take the results too seriously and have fun with it!'))