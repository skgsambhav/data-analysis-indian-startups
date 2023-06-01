import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(layout='wide', page_title='Startup Analysis')

df = pd.read_csv('startup_data_cleaned.csv')

df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month


def load_overall_analysis():
    Total_funded = round(df['amount(cr)'].sum())
    max_funded =  df.groupby('startup')['amount(cr)'].sum().sort_values(ascending=False)
    avg_funded = df.groupby('startup')['amount(cr)'].sum().mean()
    no_of_funded_startups = df['startup'].nunique()

    col21,col22,col23,col24 = st.columns(4)
    with col21:
        st.metric('Total Funded Amount',str(Total_funded) + " Cr")

    with col22:
        st.metric('Maximum Funded Amount',str(round(max_funded[1])) + " Cr")

    with col23:
        st.metric('Average Funded Amount',str(round(avg_funded)) + " Cr")

    with col24:
        st.metric('No of Funded Startups',no_of_funded_startups)

    #MoM Graph

    


def load_investor_details(investor):
# Assuming 'date' is a column in your DataFrame
    df['date'] = pd.to_datetime(df['date'])
# Now you can access the year component
    df['year'] = df['date'].dt.year

    st.title('Investor Details: ')
    st.header(investor_selected)
    #recent investment
    top5investment = df[df['investors'].str.contains(investor)][['date','startup','vertical','city','investors','rounds','amount(cr)','year']].head(5)
    st.subheader('Most recent Investments')
    st.dataframe(top5investment)

    st.subheader('Biggest Investments')
    col1, col2 = st.columns(2)
    with col1 :
        #top 5 big investments
        st.subheader('Biggest Investments')
        big_investment = df.groupby('startup')['amount(cr)'].sum().sort_values(ascending=False).head(10)

        # Create a figure and axis
        fig, ax = plt.subplots()

        # Plot the bar chart
        ax.bar(big_investment.index, big_investment.values)

        # Customize the chart
        ax.set_xlabel('Companies')
        ax.set_ylabel('Amount (in Cr)')
        ax.set_title('Big Investments')

        # Display the chart in Streamlit
        st.pyplot(fig)

    with col2:
        st.subheader('Sector Investments')
        sector_investments = df.groupby('vertical').size().sort_values(ascending=False).head(10)
        # Create a figure and axis
        fig1, ax1 = plt.subplots(figsize=(4.5,4.5))

        # Plot the pie chart
        ax1.pie(sector_investments.values, labels=sector_investments.index, autopct='%1.1f%%')

        # Display the chart in Streamlit
        st.pyplot(fig1)

    col11, col12 = st.columns(2)
    with col11:
        st.subheader('Rounds')
        rounds1 = df.groupby('rounds').size().sort_values(ascending=False)
        # Create a figure and axis
        fig2, ax2 = plt.subplots(figsize=(4.5,4.5))

        # Plot the pie chart
        ax2.pie(rounds1.values, labels=rounds1.index, autopct='%1.1f%%')

        # Display the chart in Streamlit
        st.pyplot(fig2)

    with col12:
        st.subheader('City')
        city = df.groupby('city').size().sort_values(ascending=False).head(10)
        # Create a figure and axis
        fig3, ax3 = plt.subplots(figsize=(4.5,4.5))

        # Plot the pie chart
        ax3.pie(city.values, labels=city.index, autopct='%1.0f%%')

        # Display the chart in Streamlit
        st.pyplot(fig3)
    
   #YOY INVESTMENTS
    st.subheader('Year of investment')
    YOY = df.groupby('year')['amount(cr)'].sum()
    # Create a figure and axis
    fig4, ax4 = plt.subplots()

    # Plot the line chart
    ax4.plot(YOY.index, YOY.values)

    # Customize the chart
    ax4.set_xlabel('Year of investment')
    ax4.set_ylabel('Total amount (in cr)')
    ax4.set_title('Year of investment')

    # Set the x-axis tick formatter to display integers
    ax4.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Display the chart in Streamlit
    st.pyplot(fig4)       
    
 
st.sidebar.title('Startup Funding Analysis')

options = st.sidebar.selectbox('Select One',['Overall analysis','Startup','Investors'])

if options=='Overall analysis':
    st.title('Overall Analysis')
    clicked_btn = st.sidebar.button('Show Overall Analysis')
    if clicked_btn:
        load_overall_analysis()


elif options=='Startup':
    st.sidebar.selectbox('Select one',sorted(df['startup'].unique().tolist()))
    st.sidebar.button('Show Startup Details')
    st.title('Startup')
else: 
    investor_selected = st.sidebar.selectbox('Select one',sorted(set(df['investors'].str.split(',').sum())))
    btn1 = st.sidebar.button('Show Investors Details')

    if btn1:
        load_investor_details(investor_selected)



