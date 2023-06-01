import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

# Defining the keywords to monitor for telecom fraud
keywords = ['telecoms scam', 'phone fraud', 'billing fraud', 'identity theft']

# Fetching real-time posts from Pushshift API
posts = []
for keyword in keywords:
  url = f"https://api.pushshift.io/reddit/search/submission/?q={keyword}&size=20&sort=new"
  response = requests.get(url)
  data = response.json()
  for post in data['data']:
    posts.append({
      'post_text': post['title'],
      'user_name': post['author'],
      'subreddit': post['subreddit'],
      'date': pd.to_datetime(post['created_utc'], unit='s'),
    })

# Creating a DataFrame from the fetched posts
data = pd.DataFrame(posts)

# Setting the title and description of your Streamlit application
st.title('Telecom Fraud Detection Dashboard')
st.markdown('Real-time data visualization of telecom fraud mentions on Reddit')

# Displaying the data table
st.subheader('Data Table')
st.dataframe(data)

# Creating a bar chart showing the number of fraud mentions by subreddit
st.subheader('Fraud Mentions by Subreddit')
chart_data = data['subreddit'].value_counts()
st.bar_chart(chart_data)

# Creating a line chart showing the frequency of fraud mentions over time
st.subheader('Fraud Mentions Over Time')
chart_data = data['date'].value_counts().sort_index()
st.line_chart(chart_data)

# Creating a pie chart showing the distribution of fraud mentions by user
st.subheader('Fraud Mentions by User')
chart_data = data['user_name'].value_counts()
fig = px.pie(chart_data, values=chart_data.values, names=chart_data.index)

# Updating the layout to make the pie chart bigger
fig.update_layout(width=800, height=600)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.plotly_chart(fig)

# Creating a line chart showing the relationship between date and the number of fraud mentions by subreddit
st.subheader('Relationship between Date and Subreddit')
chart_data = data.groupby(['date', 'subreddit']).size().unstack()
st.line_chart(chart_data)

# Additional visualizations and analysis
st.subheader('Top Users')
top_users = data['user_name'].value_counts().head(10)
st.bar_chart(top_users)

st.subheader('Posts by Hour')
data['hour'] = data['date'].dt.hour
posts_by_hour = data['hour'].value_counts().sort_index()
st.line_chart(posts_by_hour)

plt.axis('off')
st.pyplot()
