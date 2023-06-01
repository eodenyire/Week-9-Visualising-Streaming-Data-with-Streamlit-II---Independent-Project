import streamlit as st
import praw
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Set up authentication with Reddit API
reddit = praw.Reddit(
client_id='IYiJ0yRchydJPN19ToFjmw',
    client_secret='qb6NiPlYhaqVpG_Ce3_ovCD4rqMUhA',
    user_agent='akemboi',
)

# Define the keywords to monitor for telecom fraud
keywords = ['telecoms scam', 'phone fraud', 'billing fraud', 'identity theft']

# Fetch real-time posts from Reddit API
posts = []
for keyword in keywords:
    subreddit = reddit.subreddit('all')
    for post in subreddit.search(keyword, limit=20, sort='new'):
        posts.append({
            'post_text': post.title,
            'user_name': post.author.name,
            'subreddit': post.subreddit.display_name,
            'date': pd.to_datetime(post.created_utc, unit='s'),
        })

# Create a DataFrame from the fetched posts
data = pd.DataFrame(posts)

# Set the title and description of your Streamlit application
st.title('Telecom Fraud Detection Dashboard')
st.markdown('Real-time data visualization of telecom fraud mentions on Reddit')

# Display the data table
st.subheader('Data Table')
st.dataframe(data)

# Create a bar chart showing the number of fraud mentions by subreddit
st.subheader('Fraud Mentions by Subreddit')
chart_data = data['subreddit'].value_counts()
st.bar_chart(chart_data)

# Create a line chart showing the frequency of fraud mentions over time
st.subheader('Fraud Mentions Over Time')
chart_data = data['date'].value_counts().sort_index()
st.line_chart(chart_data)

# Additional visualizations and analysis
st.subheader('Top Users')
top_users = data['user_name'].value_counts().head(10)
st.bar_chart(top_users)

st.subheader('Posts by Hour')
data['hour'] = data['date'].dt.hour
posts_by_hour = data['hour'].value_counts().sort_index()
st.line_chart(posts_by_hour)

st.subheader('Word Cloud')
st.set_option('deprecation.showPyplotGlobalUse', False)
from wordcloud import WordCloud
text = ' '.join(data['post_text'])
wordcloud = WordCloud(width=800, height=400).generate(text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot()
