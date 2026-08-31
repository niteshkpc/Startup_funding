import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Startup Funding Analysis")

df = pd.read_csv("startup_cleaned.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year


def load_overall_analysis(toatal=None):
    st.title('Overall Analysis')

    #Total investment amount
    total = round(df['amount'].sum())

    # MAx amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    #AVG Ticket Size
    avg_funding = df.groupby('startup')['amount'].sum().mean()

    # Total Funded Startup
    num_startup = df['startup'].nunique()

    col6, col7, col8, col9 = st.columns(4)
    with col6:
        st.metric('Total', str(total) + 'Cr')

    with col7:
        st.metric('max_funding', str(max_funding) + 'Cr')

    with col8:
        st.metric('avg_funding', str(round(avg_funding)) + 'Cr')

    with col9:
        st.metric('num_startup', num_startup)

    st.header('MOM Graph')
    selected_option =  st.selectbox('Selection Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype(str)

    fig7, ax7 = plt.subplots()
    ax7.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig7)


def load_investor_details(investor):
    st.title(investor)
    #load the recent 5 investment of investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        #Biggest Investment
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')

        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Investment')

        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels = vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Round Investment')

        fig3, ax3 = plt.subplots()
        ax3.pie(round_series, labels = round_series.index, autopct="%0.01f%%")
        st.pyplot(fig3)

    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('City Investment')

        fig4, ax4 = plt.subplots()
        ax4.pie(city_series, labels=city_series.index, autopct="%0.01f%%")
        st.pyplot(fig4)

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YOY Investment')

    fig5, ax5 = plt.subplots()
    ax5.plot(year_series.index, year_series.values)
    st.pyplot(fig5)

st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox('Select One', ['Ovarall Analysis', 'Startup', 'Investor'])

if option == 'Ovarall Analysis':
    btn0 = st.sidebar.button('Show Ovarall Analysis')
    load_overall_analysis()
elif option == 'Startup':
    st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title("Startup Funding Analysis")
elif option == 'Investor':
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)