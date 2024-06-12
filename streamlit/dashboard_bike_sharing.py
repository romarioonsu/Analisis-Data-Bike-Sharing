# Memuat dataset
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Memuat dataset
day_url = "https://raw.githubusercontent.com/romarioonsu/Analisis-Data-Bike-Sharing/main/datasetBike-sharing-dataset/day.csv"
day = pd.read_csv(day_url)

# Menambahkan kolom total jumlah sewa
day['total'] = day['casual'] + day['registered']

# Mengubah format tanggal dan menambahkan kolom tahun
day['dteday'] = pd.to_datetime(day['dteday'])
day['yr'] = day['dteday'].dt.year

# Menambah kolom musim
day['season'] = day['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

# Sidebar untuk memilih jenis visualisasi
st.sidebar.title('Bike Sharing Dashboard')
visualization = st.sidebar.selectbox('Pilih Visualisasi:', [
    'Tren Pengaruh Faktor Cuaca pada Setiap Musim', 
    'Total Sewa Berdasarkan Musim', 
    'Distribusi Sewa Berdasarkan Jenis Pengguna di Setiap Musim', 
    'Perbedaan Pola Penggunaan Sepeda Berbagi'
])

# Membuat layout aplikasi Streamlit
st.title('Bike Sharing Analysis')
st.subheader('By Romario Onsu')

# Suhu
if visualization == 'Tren Pengaruh Faktor Cuaca pada Setiap Musim':
    st.write("""
        ## Tren Pengaruh Faktor Cuaca pada Setiap Musim (2011 dan 2012)
        Grafik di bawah ini menunjukkan bagaimana suhu, kelembaban, dan kecepatan angin mempengaruhi jumlah penyewaan sepeda selama musim yang berbeda pada tahun 2011 dan 2012.
    """)

    # Suhu
    st.subheader('Pengaruh Suhu')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='dteday', y='temp', hue='season', data=day, marker='o', ax=ax)
    ax.set_title('Tren Pengaruh Suhu pada Setiap Musim (2011 dan 2012)')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Suhu')
    st.pyplot(fig)

    # Kelembaban
    st.subheader('Pengaruh Kelembaban')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='dteday', y='hum', hue='season', data=day, marker='o', ax=ax)
    ax.set_title('Tren Pengaruh Kelembaban pada Setiap Musim (2011 dan 2012)')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Kelembaban')
    st.pyplot(fig)

    # Kecepatan Angin
    st.subheader('Pengaruh Kecepatan Angin')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='dteday', y='windspeed', hue='season', data=day, marker='o', ax=ax)
    ax.set_title('Tren Pengaruh Kecepatan Angin pada Setiap Musim (2011 dan 2012)')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Kecepatan Angin')
    st.pyplot(fig)

# Total Sewa Berdasarkan Musim
elif visualization == 'Total Sewa Berdasarkan Musim':
    st.header('Total Sewa Berdasarkan Musim')
    
    # Total sewa berdasarkan musim
    season_stats = day.groupby('season')['total'].sum().reset_index()
    st.write(season_stats)
    
    # Visualisasi
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season', y='total', data=season_stats, ax=ax)
    ax.set_title('Jumlah Sewa Berdasarkan Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Sewa')
    st.pyplot(fig)

# Distribusi Sewa Berdasarkan Jenis Pengguna di Setiap Musim
elif visualization == 'Distribusi Sewa Berdasarkan Jenis Pengguna di Setiap Musim':
    st.header('Distribusi Sewa Berdasarkan Jenis Pengguna di Setiap Musim')
    
    # Distribusi sewa berdasarkan jenis pengguna di setiap musim
    season_user_stats = day.groupby(['season'])[['casual', 'registered']].sum().reset_index()
    st.write(season_user_stats)
    
    # Visualisasi
    fig, ax = plt.subplots(figsize=(10, 6))
    season_user_stats_melted = season_user_stats.melt(id_vars=['season'], value_vars=['casual', 'registered'], var_name='user_type', value_name='count')
    sns.barplot(x='season', y='count', hue='user_type', data=season_user_stats_melted, ax=ax)
    ax.set_title('Distribusi Sewa Berdasarkan Jenis Pengguna di Setiap Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Sewa')
    st.pyplot(fig)

# Perbedaan Pola Penggunaan Sepeda Berbagi
elif visualization == 'Perbedaan Pola Penggunaan Sepeda Berbagi':
    st.header('Perbedaan Pola Penggunaan Sepeda Berbagi antara Hari Kerja dan Hari Libur selama Musim Panas dan Musim Dingin (2011-2012)')
    
    # Filter data untuk tahun 2011 dan 2012, dan hanya musim panas dan musim dingin
    filtered_day = day[((day['yr'] == 2011) | (day['yr'] == 2012)) & ((day['season'] == 'Summer') | (day['season'] == 'Winter'))]

    # Distribusi sewa berdasarkan hari kerja/hari libur di musim panas dan musim dingin
    season_workingday_stats = filtered_day.groupby(['season', 'workingday'])[['casual', 'registered']].sum().reset_index()
    season_workingday_stats['total'] = season_workingday_stats['casual'] + season_workingday_stats['registered']
    season_workingday_stats['day_type'] = season_workingday_stats['workingday'].map({1: 'Hari Kerja', 0: 'Hari Libur'})
    
    # Memeriksa data setelah filter
    st.write("Distribusi sewa berdasarkan hari kerja/hari libur di musim panas dan musim dingin (2011-2012):")
    st.write(season_workingday_stats)
    
    # Visualisasi
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='season', y='total', hue='day_type', data=season_workingday_stats, palette='muted', ax=ax)
    ax.set_title('Perbedaan Pola Penggunaan Sepeda Berbagi antara Hari Kerja dan Hari Libur selama Musim Panas dan Musim Dingin (2011-2012)')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Sewa')
    ax.legend(title='Tipe Hari')
    st.pyplot(fig)
