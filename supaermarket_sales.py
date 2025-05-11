
import pandas as pd
import plotly.express as px
import streamlit as st

df_supermarket = pd.read_csv('supermarket_sales - Sheet1.csv')
df_supermarket.drop_duplicates()
df_supermarket['Date'] = pd.to_datetime(df_supermarket['Date'])

st.set_page_config(layout= 'wide', page_title= 'Supermarket sales EDA', page_icon= '🛒')
st.markdown("""<h1 style="color:Black;text-align:center;">🛒 Supermarket sales EDA(Exploratory Data Analysis) </h1>""", unsafe_allow_html= True)

st.image('https://miro.medium.com/v2/resize:fit:1100/format:webp/0*8HaV1Eoqz_8DuO1X')

categorical_columns = ['City', 'Gender', 'Product line', 'Payment', 'Customer type'	]
numerical_columns = ['Total', 'cogs', 'gross income', 'Rating']

page = st.sidebar.radio('Navigation', ['Univariate Analysis', 'Bivariate Analysis', 'Multivariate Analysis', 'Filter by Date and City'])

if(page == 'Univariate Analysis'):
  st.header('📊 Univariate Analysis')
  types_col = st.selectbox('Select Type', ['Categorical', 'Numerical'])
  if(types_col == 'Numerical'):
    col = st.selectbox('Select Column', numerical_columns)
    chart = st.selectbox('Select Chart', ['Histogram', 'Box'])
    if(chart == 'Histogram'):
      st.plotly_chart(px.histogram(data_frame = df_supermarket, x = col, title = col))
    else:
      st.plotly_chart(px.box(data_frame = df_supermarket, x = col, title = col))
  else:
    col = st.selectbox('Select Column', categorical_columns)
    chart = st.selectbox('Select Chart', ['Histogram', 'Pie'])
    if(chart == 'Histogram'):
      st.plotly_chart(px.histogram(data_frame = df_supermarket, x = col, title = col))
    else:
      st.plotly_chart(px.pie(data_frame = df_supermarket, names = col, title = col))
elif(page == 'Bivariate Analysis'):
  st.header('📊 Bivariate Analysis')
  st.header('Total sales per city')
  sales_per_city =df_supermarket.groupby('City')['Total'].sum().sort_values(ascending= False).reset_index()
  st.plotly_chart(px.bar(data_frame = sales_per_city, x = 'City', y = 'Total', text_auto= True))

  st.header('Average rating per city')
  rating_per_city =df_supermarket.groupby('City')['Rating'].mean().round(2).sort_values(ascending= False).reset_index()
  st.plotly_chart(px.bar(data_frame = rating_per_city, x = 'City', y = 'Rating', text_auto= True))

  st.header('Total sales per gender')
  st.plotly_chart(px.box(data_frame = df_supermarket, x = 'Gender', y = 'Total'))

  st.header('Average rating per branch')
  rating_per_branch = df_supermarket.groupby('Branch')['Rating'].mean().round(2).sort_values(ascending = False).reset_index()
  st.plotly_chart(px.bar(data_frame = rating_per_branch, x = 'Branch', y = 'Rating', text_auto = True))

  st.header('Total sales for each product line')
  sales_per_product = df_supermarket.groupby('Product line')['Total'].sum().sort_values(ascending = False).reset_index()
  st.plotly_chart(px.bar(data_frame = sales_per_product, x = 'Product line', y = 'Total', text_auto = True))

  st.header('Rating for each product line')
  rating_per_product = df_supermarket.groupby('Product line')['Rating'].mean().round(2).sort_values(ascending = False).reset_index()
  st.plotly_chart(px.bar(data_frame = rating_per_product, x = 'Product line', y = 'Rating', text_auto = True))

  st.header('Total sales per Month')
  sales_per_month = df_supermarket.groupby(df_supermarket["Date"].dt.month_name())['Total'].sum().reset_index()
  st.plotly_chart(px.bar(data_frame = sales_per_month, x = 'Date', y = 'Total', category_orders = {'Date' : ['January', 'February', 'March']}))

  cities = st.selectbox('Select City', list(df_supermarket.City.unique()))
  df_supermarket_per_city = df_supermarket[df_supermarket['City'] == cities]
  sales_per_month = df_supermarket_per_city.groupby(df_supermarket_per_city["Date"].dt.month_name())['Total'].sum().reset_index()
  st.plotly_chart(px.bar(data_frame = sales_per_month, x = 'Date', y = 'Total', title = 'Sales per month for '+ cities, category_orders = {'Date' : ['January', 'February', 'March']}))



elif(page == 'Multivariate Analysis'):
  st.header('📊 Multivariate Analysis')
  st.header('Sales for each Branch and Gender')
  sales_per_branch_gender = df_supermarket.groupby(['Branch', 'Gender'])['Total'].sum().reset_index()
  st.plotly_chart(px.bar(data_frame = sales_per_branch_gender, x = 'Branch', y = 'Total',color = 'Gender',barmode= 'group', text_auto = True))

  st.header('Rating for each Branch and Gender')
  rating_per_branch_gender = df_supermarket.groupby(['Branch', 'Gender'])['Rating'].mean().round(2).reset_index()
  st.plotly_chart(px.bar(data_frame = rating_per_branch_gender, x = 'Branch', y = 'Rating',color = 'Gender',barmode= 'group', text_auto = True))

  st.header('Sales for each month per city')
  sales_per_month_city = df_supermarket.groupby([df_supermarket['Date'].dt.month_name(), 'City'])['Total'].sum().reset_index()
  st.plotly_chart(px.bar(data_frame = sales_per_month_city, x = 'Date', y = 'Total',color = 'City',barmode= 'group', text_auto = True, category_orders = {'Date' : ['January', 'February', 'March']}))

elif(page == 'Filter by Date and City'):
  st.header('📅 Filter by Date and City')
  df_supermarket = df_supermarket.sort_values(by = 'Date')
  start_date = st.date_input('Start Date', value= df_supermarket.Date.min(), min_value= df_supermarket.Date.min(), max_value= df_supermarket.Date.max())
  end_date = st.date_input('End Date', value= df_supermarket.Date.max(), min_value= df_supermarket.Date.min(), max_value= df_supermarket.Date.max())
  city = st.multiselect('City', df_supermarket.City.unique())
  df_filtered = df_supermarket[(df_supermarket.Date >= str(start_date)) & (df_supermarket.Date <= str(end_date))]
  df_filtered =  df_filtered[(df_filtered.City.isin(city))]
  st.dataframe(df_filtered)


