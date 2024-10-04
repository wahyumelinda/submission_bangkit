import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from datetime import datetime
import gdown

sns.set(style='dark')

# function untuk memvisualisasikan dataset
def get_sales_per_product(df):
    return df.groupby('product_category_name')['price'].count().sort_values(ascending=False)

def get_sales_per_city(df):
    return df.groupby('customer_city')['customer_id'].count().sort_values(ascending=False)

def get_sales_per_product_details(df):
    return df.groupby('product_id').agg(
        total_sales=('order_id', 'count'),
        avg_price=('price', 'mean')
    ).reset_index()

def create_rfm_df(df):
    rfm_df = df.groupby(by="product_category_name", as_index=False).agg({
        "order_purchase_timestamp": "max",  
        "order_id": "nunique", 
        "price": "sum"  
    })
    rfm_df["order_purchase_timestamp"] = pd.to_datetime(rfm_df["order_purchase_timestamp"]).dt.date  
    recent_date = pd.to_datetime(df["order_purchase_timestamp"]).dt.date.max()  
    rfm_df["recency"] = rfm_df["order_purchase_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.rename(columns={"order_id": "frequency", "price": "monetary"}, inplace=True)
    rfm_df.drop("order_purchase_timestamp", axis=1, inplace=True)
    return rfm_df

def visualize_sales_per_product(df):
    sales_per_product = get_sales_per_product(df)
    plt.figure(figsize=(10, 6))
    sales_per_product.head(10).plot(kind='bar', color='pink')
    plt.title('Top 10 Produk dengan Total Penjualan Tertinggi')
    plt.xlabel('Product Name')
    plt.ylabel('Total Unit yang Terjual')
    plt.xticks(rotation=45)
    st.pyplot(plt)

def visualize_sales_per_city(df):
    sales_per_city = get_sales_per_city(df)
    plt.figure(figsize=(10, 6))
    sales_per_city.head(10).plot(kind='bar', color='pink')
    plt.title('Top 10 Kota dengan Total Penjualan Terbanyak')
    plt.xlabel('City')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45)
    st.pyplot(plt)

def visualize_sales_vs_price(df):
    sales_per_product = get_sales_per_product_details(df)
    plt.figure(figsize=(8, 6))
    plt.scatter(sales_per_product['avg_price'], sales_per_product['total_sales'], color='pink')
    plt.title('Hubungan Harga Produk dengan Total Penjualan')
    plt.xlabel('Harga Rata-rata Produk')
    plt.ylabel('Total Units Sold')
    plt.grid(True)
    st.pyplot(plt)

def visualize_rfm(df):
    rfm_df = create_rfm_df(df)
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
    colors = ["#FF69B4"] * 5  
    sns.barplot(y="recency", x="product_category_name", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0], legend=False)
    ax[0].set_title("By Recency (days)", fontsize=18)
    ax[0].tick_params(axis='x', labelsize=9)
    sns.barplot(y="frequency", x="product_category_name", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1], legend=False)
    ax[1].set_title("By Frequency", fontsize=18)
    ax[1].tick_params(axis='x', labelsize=9)
    sns.barplot(y="monetary", x="product_category_name", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2], legend=False)
    ax[2].set_title("By Monetary", fontsize=18)
    ax[2].tick_params(axis='x', labelsize=9)
    plt.suptitle("Best Product Based on RFM Parameters (product_category_name)", fontsize=20)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    st.pyplot(fig)

# URL untuk mengunduh file
file_id = '12_dylVS9CgtuBYLA_stlKJIAdsUAy21l'
gdrive_url = f'https://drive.google.com/uc?id={file_id}'

gdown.download(gdrive_url, 'all_data_new.csv', quiet=False)

all_data = pd.read_csv('all_data_new.csv')


st.title('🛒Brazilian E-Commerce Public Dataset by Olist🛒')

# Definisikan menu utama menggunakan tab
tab1, tab2, tab3 = st.tabs(["MENU UTAMA", "PENJELASAN ANALISIS", "VISUALISASI DATA"])

with tab1:
    st.image("https://raw.githubusercontent.com/wahyumelinda/submission_bangkit/main/dashboard/logo%20tambahan.png")
    st.write(
        """
        Welcome! This is a Brazilian ecommerce public dataset of orders made at Olist Store. The dataset has information of 100k orders from 2016 to 2018 made at multiple marketplaces in Brazil. Its features allows viewing an order from multiple dimensions: from order status, price, payment and freight performance to customer location, product attributes and finally reviews written by customers. We also released a geolocation dataset that relates Brazilian zip codes to lat/lng coordinates. This is real commercial data, it has been anonymised, and references to the companies and partners in the review text have been replaced with the names of Game of Thrones great houses.
        """
    )    
    st.write(
        """
        This dataset was generously provided by Olist, the largest department store in Brazilian marketplaces. Olist connects small businesses from all over Brazil to channels without hassle and with a single contract. Those merchants are able to sell their products through the Olist Store and ship them directly to the customers using Olist logistics partners. See more on our website: www.olist.com After a customer purchases the product from Olist Store a seller gets notified to fulfill that order. Once the customer receives the product, or the estimated delivery date is due, the customer gets a satisfaction survey by email where he can give a note for the purchase experience and write down some comments
        """
    )

with tab2:
    st.image("https://raw.githubusercontent.com/wahyumelinda/submission_bangkit/main/dashboard/logo%20tujuan.png")
    st.write(
        """
        Tujuan analisis yang dilakukan adalah untuk melihat produk manakah yang memiliki total penjualan tertinggi?, lalu kota manakah yang memiliki total penjualan terbanyak?, serta adakah hubungan antara harga produk dan total penjualan?
        """
    )
 
with tab3:
    st.write("Visualisasi ini untuk menjawab apa yang menjadi tujuan analisis")

    # Sidebar untuk memilih visualisasi
    st.sidebar.header('✨OLIST✨')
    st.sidebar.subheader("📊Analisis Data dengan Olist📊")
    st.sidebar.image("https://raw.githubusercontent.com/wahyumelinda/submission_bangkit/main/dashboard/logo%20streamlit.png")
    tab3 = st.sidebar.selectbox("Pilih Visualisasi:", 
                                 ("Pilih Visualisasi",  
                                  "Top 10 Produk Terlaris", 
                                  "Top 10 Kota Penjualan",
                                  "Hubungan Harga dan Penjualan", 
                                  "RFM Analysis"))

    # Menampilkan visualisasi hanya jika pengguna memilih salah satu opsi visualisasi selain "Pilih Visualisasi"
    if tab3 != "Pilih Visualisasi":
        if tab3 == "Top 10 Produk Terlaris":
            st.subheader('Top 10 Produk dengan Total Penjualan Tertinggi')
            visualize_sales_per_product(all_data)
            with st.expander("See explanation"):
                st.write(
                    """Pada visualisasi ini bertujuan untuk melihat 10 produk dengan total penjualan tertinggi.
                    Produk dengan penjualan tertinggi ada pada bagian paling kiri.
                    """
                )

        elif tab3 == "Top 10 Kota Penjualan":
            st.subheader('Top 10 Kota dengan Total Penjualan Terbanyak')
            visualize_sales_per_city(all_data)
            with st.expander("See explanation"):
                st.write(
                    """Pada visualisasi ini bertujuan untuk melihat 10 kota dengan total penjualan terbanyak.
                    Kota dengan penjualan terbanyak ada pada bagian paling kiri.
                    """
                )

        elif tab3 == "Hubungan Harga dan Penjualan":
            st.header('Hubungan Harga Produk dengan Total Penjualan')
            visualize_sales_vs_price(all_data)
            with st.expander("See explanation"):
                st.write(
                    """Pada visualisasi ini bertujuan untuk melihat apakah terdapat hubungan harga dan total penjualan produk
                    """
                )

        elif tab3 == "RFM Analysis":
            st.header('Best Product Based on RFM Parameters')
            visualize_rfm(all_data)
            with st.expander("See explanation"):
                st.write(
                    """Visualisasi ini merupakan visualisasi tambahan yang akan menambah insight dari data
                    """
                )

# Menampilkan nama penulis di bagian bawah halaman
st.caption('wahyu melinda - upnvjt')
