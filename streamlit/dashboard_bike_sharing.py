import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Memuat dataset
day = pd.read_csv('datasetBike-sharing-dataset/day.csv')

# Menambahkan kolom total jumlah sewa
day['total'] = day['casual'] + day['registered']

# Sidebar untuk memilih jenis visualisasi
st.sidebar.title('Bike Sharing Dashboard')
visualization = st.sidebar.selectbox('Pilih Visualisasi:', ['Total Sewa Berdasarkan Musim', 'Pengaruh Suhu', 'Pengaruh Kecepatan Angin', 'Distribusi Sewa Berdasarkan Jenis Pengguna di Setiap Musim'])

# Pengaruh Suhu terhadap Jumlah Sewa
if visualization == 'Pengaruh Suhu':
    st.header('Pengaruh Suhu terhadap Jumlah Sewa')
    
    # Korelasi antara suhu dan total sewa
    correlation_temp_total = day[['temp', 'total']].corr().iloc[0, 1]
    st.write(f'Korelasi antara suhu dan total sewa: {correlation_temp_total:.2f}')
    
    # Visualisasi
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='temp', y='total', data=day)
    plt.title('Pengaruh Suhu terhadap Jumlah Sewa')
    plt.xlabel('Suhu')
    plt.ylabel('Jumlah Sewa')
    st.pyplot(plt)

# Pengaruh Kecepatan Angin terhadap Jumlah Sewa
elif visualization == 'Pengaruh Kecepatan Angin':
    st.header('Pengaruh Kecepatan Angin terhadap Jumlah Sewa')
    
    # Visualisasi
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='windspeed', y='total', data=day)
    plt.title('Pengaruh Kecepatan Angin terhadap Jumlah Sewa')
    plt.xlabel('Kecepatan Angin')
    plt.ylabel('Jumlah Sewa')
    st.pyplot(plt)

# Total Sewa Berdasarkan Musim
elif visualization == 'Total Sewa Berdasarkan Musim':
    st.header('Total Sewa Berdasarkan Musim')
    
    # Total sewa berdasarkan musim
    season_stats = day.groupby('season')['total'].sum().reset_index()
    st.write(season_stats)
    
    # Visualisasi
    plt.figure(figsize=(10, 6))
    sns.barplot(x='season', y='total', data=season_stats)
    plt.title('Jumlah Sewa Berdasarkan Musim')
    plt.xlabel('Musim')
    plt.ylabel('Jumlah Sewa')
    st.pyplot(plt)

# Distribusi Sewa Berdasarkan Jenis Pengguna di Setiap Musim
elif visualization == 'Distribusi Sewa Berdasarkan Jenis Pengguna di Setiap Musim':
    st.header('Distribusi Sewa Berdasarkan Jenis Pengguna di Setiap Musim')
    
    # Distribusi sewa berdasarkan jenis pengguna di setiap musim
    season_user_stats = day.groupby(['season'])[['casual', 'registered']].sum().reset_index()
    st.write(season_user_stats)
    
    # Visualisasi
    plt.figure(figsize=(10, 6))
    season_user_stats_melted = season_user_stats.melt(id_vars=['season'], value_vars=['casual', 'registered'], var_name='user_type', value_name='count')
    sns.barplot(x='season', y='count', hue='user_type', data=season_user_stats_melted)
    plt.title('Distribusi Sewa Berdasarkan Jenis Pengguna di Setiap Musim')
    plt.xlabel('Musim')
    plt.ylabel('Jumlah Sewa')
    st.pyplot(plt)
