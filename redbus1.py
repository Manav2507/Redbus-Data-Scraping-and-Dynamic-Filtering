import pandas as pd
import numpy as np
import mysql.connector
import sqlite3
import streamlit as slt
from streamlit_option_menu import option_menu
import plotly.express as px
import time

#ASRTC

list_ASRTC = []
df_ASRTC = pd.read_csv("./CSV files/ASRTC_bus_details.csv") 
for i, r in df_ASRTC.iterrows():
    route_name = r["Route_Name"]
    if route_name not in list_ASRTC:  # Ensure only unique values are added
        list_ASRTC.append(route_name)

# JKRTC

list_JKRTC = []
df_JKRTC = pd.read_csv("./CSV files/JKRTC_bus_details.csv")
for i, r in df_JKRTC.iterrows():
    route_name = r["Route_Name"]
    if route_name not in list_JKRTC:  # Ensure only unique values are added
        list_JKRTC.append(route_name)

#GSRTC

list_GSRTC = []
df_GSRTC = pd.read_csv("./CSV files/GSRTC_bus_details.csv")
for i, r in df_GSRTC.iterrows():
    route_name = r["Route_Name"]
    if route_name not in list_GSRTC:  # Ensure only unique values are added
        list_GSRTC.append(route_name)

#KTCL

list_KTCL = []
df_KTCL = pd.read_csv("./CSV files/KTCL_bus_details.csv")
for i, r in df_KTCL.iterrows():
    route_name = r["Route_Name"]
    if route_name not in list_KTCL:  # Ensure only unique values are added
        list_KTCL.append(route_name)

#NBSTC

list_NBSTC = []
df_NBSTC = pd.read_csv("./CSV files/NBSTC_bus_details.csv")
for i, r in df_NBSTC.iterrows():
    route_name = r["Route_Name"]
    if route_name not in list_NBSTC:  # Ensure only unique values are added
        list_NBSTC.append(route_name)

#PEPSU

list_PEPSU = []
df_PEPSU = pd.read_csv("./CSV files/PEPSU_bus_details.csv")
for i, r in df_PEPSU.iterrows():
    route_name = r["Route_Name"]
    if route_name not in list_PEPSU:  # Ensure only unique values are added
        list_PEPSU.append(route_name)

#RSRTC

list_RSRTC = []
df_RSRTC = pd.read_csv("./CSV files/RSRTC_bus_details.csv")
for i, r in df_RSRTC.iterrows():
    route_name = r["Route_Name"]
    if route_name not in list_RSRTC:  # Ensure only unique values are added
        list_RSRTC.append(route_name)

#SNT

list_SNT = []
df_SNT = pd.read_csv("./CSV files/SNT_bus_details.csv")
for i, r in df_SNT.iterrows():
    route_name = r["Route_Name"]
    if route_name not in list_SNT:  # Ensure only unique values are added
        list_SNT.append(route_name)

# WBSTC

list_WBSTC = []
df_WBSTC = pd.read_csv("./CSV files/WBSTC_bus_details.csv")
for i, r in df_WBSTC.iterrows():
    route_name = r["Route_Name"]
    if route_name not in list_WBSTC:  # Ensure only unique values are added
        list_WBSTC.append(route_name)

# WBTC

list_WBTC = []
df_WBTC = pd.read_csv("./CSV files/WBTC_bus_details.csv")
for i, r in df_WBTC.iterrows():
    route_name = r["Route_Name"]
    if route_name not in list_WBTC:  # Ensure only unique values are added
        list_WBTC.append(route_name)

slt.set_page_config(layout="wide")

col1, col2 = slt.columns([1, 3])  # Adjust column widths as needed

# Left-hand side: Menu
with col1:
    menu_option = option_menu(
        "Main Menu",
        options=["Home", "Bus Details"],
        icons=["house","train-front"],
        menu_icon="cast",  # Optional: Icon for the menu
        default_index=0
    )

# Right-hand side: Output
with col2:
    if menu_option == "Home":
        # st.write("Welcome to the Home Page")
        slt.title("Redbus Data Scraping and Dynamic Filtering")
        slt.subheader("Streamlined Bus Travel Data at Your Fingertips")
        slt.markdown("""
        Welcome to the **Redbus Data Scraping and Filtering Application**, your one-stop solution 
        for analyzing and visualizing bus travel data. Explore real-time bus schedules, prices, and availability with ease.

        ### Features
        - **Real-time Data Scraping**: Automated extraction of bus schedules and seat availability.
        - **Dynamic Filtering**: Refine results by route, type, price, and more.
        - **User-friendly Interface**: Simplified travel insights through an interactive app.

        ### Business Use Cases
        - Travel Aggregators, Market Analysis, Customer Service, Competitor Analysis

        ### Technology Stack
        - **Web Scraping**: Selenium
        - **Data Management**: SQL
        - **Frontend**: Streamlit
        - **Programming Language**: Python - Numpy, Pandas

        Navigate through the menu to explore more!
        """)
    elif menu_option == "Bus Details":
        col1, col2 = slt.columns(2)
        col1_1, col2_2 = slt.columns(2)
        with col1:
            S = slt.selectbox(
                "List of States",
                ["Gujarat", "Assam", "Jammu & Kashmir", "Kadamba", 
                "NORTH BENGAL", "Punjab", "Rajasthan", "Sikkim", 
                "West Bengal", "WBTC (CTC)"]
            )
        
        with col2:
            select_fare = slt.selectbox(
                "Choose Bus Fare Range",
                ["50-1000", "1000-2500", "2500 and above"]
            )
 
        star_rating_ranges = {
            "4.0 - 5.0": (4.0, 5.0),
            "3.0 - 3.9": (3.0, 3.9),
            "2.0 - 2.9": (2.0, 2.9),
            "1.0 - 1.9": (1.0, 1.9),
            "0.0 - 0.9": (0.0, 0.9),
        }

# Add a select box for choosing the range
        selected_range = slt.selectbox("Select Star Rating Range", list(star_rating_ranges.keys()), key="global_rating")

# Get the min and max star rating for the selected range
        min_rating, max_rating = star_rating_ranges[selected_range]
# 1. Assam
        if S == "Assam":
            K = slt.selectbox("List of Routes", list_ASRTC)

            if select_fare == "50-1000":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query with the star rating range filter
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price BETWEEN ? AND ? 
                        AND Route_name = ? 
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                    ''', (50, 1000, K, min_rating, max_rating))

                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output for debugging
                    if not out:
                        slt.warning("No data retrieved from the database.")
                    else:
                        print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                # Convert to DataFrame
                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])

                # Display the data in Streamlit as a table
                slt.write(df)


            elif select_fare == "1000-2500":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                            SELECT * FROM bus_details
                            WHERE Price BETWEEN ? AND ? AND Route_name=?
                            AND Star_Rating BETWEEN ? AND ?
                            ORDER BY Price DESC
                            ''', (1000, 2500, K, min_rating, max_rating)) 
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    print(f"Database error: {e}")

                finally:
                    conn.close()
                df = pd.DataFrame(out,columns=["Route_Name","Route_Link","Bus_Name","Bus_Type","Departing_Time","Duration","Reaching_Time","Star_Rating","Price","Seat_Availability"])
                slt.write(df)

            elif select_fare == '2500 and above':
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price >= ? AND Route_name = ?
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                        ''', (2500, K, min_rating, max_rating))
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    print(f"Database error: {e}")

                finally:
                    conn.close()
                df = pd.DataFrame(out,columns=["Route_Name","Route_Link","Bus_Name","Bus_Type","Departing_Time","Duration","Reaching_Time","Star_Rating","Price","Seat_Availability"])
                slt.write(df)

#2. Jammu & Kasmir
        if S == "Jammu & Kashmir":
            J_K = slt.selectbox("List of Routes", list_JKRTC)

            if select_fare == "50-1000":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query with the star rating range filter
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price BETWEEN ? AND ? 
                        AND Route_name = ? 
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                    ''', (50, 1000, J_K, min_rating, max_rating))

                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output for debugging
                    if not out:
                        slt.warning("No data retrieved from the database.")
                    else:
                        print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                # Convert to DataFrame
                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])

                # Display the data in Streamlit as a table
                slt.write(df)

            elif select_fare == "1000-2500":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                            SELECT * FROM bus_details
                            WHERE Price BETWEEN ? AND ? AND Route_name=?
                            AND Star_Rating BETWEEN ? AND ?
                            ORDER BY Price DESC
                            ''', (1000, 2500, J_K, min_rating, max_rating)) 
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)

            elif select_fare == '2500 and above':
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price >= ? AND Route_name = ?
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                        ''', (2500, J_K, min_rating, max_rating))
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)
#3. Kadamba
        if S == "Kadamba":
            Kadamba_Route = slt.selectbox("List of Routes", list_KTCL)

            if select_fare == "50-1000":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query with the star rating range filter
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price BETWEEN ? AND ? 
                        AND Route_name = ? 
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                    ''', (50, 1000, Kadamba_Route, min_rating, max_rating))

                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output for debugging
                    if not out:
                        slt.warning("No data retrieved from the database.")
                    else:
                        print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                # Convert to DataFrame
                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])

                # Display the data in Streamlit as a table
                slt.write(df)

            elif select_fare == "1000-2500":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                            SELECT * FROM bus_details
                            WHERE Price BETWEEN ? AND ? AND Route_name=?
                            AND Star_Rating BETWEEN ? AND ?
                            ORDER BY Price DESC
                            ''', (1000, 2500, Kadamba_Route, min_rating, max_rating)) 
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)

            elif select_fare == '2500 and above':
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price >= ? AND Route_name = ?
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                        ''', (2500, Kadamba_Route, min_rating, max_rating))
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)
#4. North Bengal
        if S == "NORTH BENGAL":
            NorthBengal_Route = slt.selectbox("List of Routes", list_NBSTC)

            if select_fare == "50-1000":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query with the star rating range filter
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price BETWEEN ? AND ? 
                        AND Route_name = ? 
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                    ''', (50, 1000, NorthBengal_Route, min_rating, max_rating))

                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output for debugging
                    if not out:
                        slt.warning("No data retrieved from the database.")
                    else:
                        print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                # Convert to DataFrame
                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])

                # Display the data in Streamlit as a table
                slt.write(df)

            elif select_fare == "1000-2500":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                            SELECT * FROM bus_details
                            WHERE Price BETWEEN ? AND ? AND Route_name=?
                            AND Star_Rating BETWEEN ? AND ?
                            ORDER BY Price DESC
                            ''', (1000, 2500, NorthBengal_Route, min_rating, max_rating)) 
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)

            elif select_fare == '2500 and above':
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price >= ? AND Route_name = ?
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                        ''', (2500, NorthBengal_Route, min_rating, max_rating))
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)

#5. Punjab
        if S == "Punjab":
            Punjab_Route = slt.selectbox("List of Routes", list_PEPSU)

            if select_fare == "50-1000":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query with the star rating range filter
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price BETWEEN ? AND ? 
                        AND Route_name = ? 
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                    ''', (50, 1000, Punjab_Route, min_rating, max_rating))

                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output for debugging
                    if not out:
                        slt.warning("No data retrieved from the database.")
                    else:
                        print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                # Convert to DataFrame
                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])

                # Display the data in Streamlit as a table
                slt.write(df)

            elif select_fare == "1000-2500":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                            SELECT * FROM bus_details
                            WHERE Price BETWEEN ? AND ? AND Route_name=?
                            AND Star_Rating BETWEEN ? AND ?
                            ORDER BY Price DESC
                            ''', (1000, 2500, Punjab_Route, min_rating, max_rating)) 
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)

            elif select_fare == '2500 and above':
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price >= ? AND Route_name = ?
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                        ''', (2500, Punjab_Route, min_rating, max_rating))
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)
#6. Rajasthan
        if S == "Rajasthan":
            Rajasthan_Route = slt.selectbox("List of Routes", list_RSRTC)

            if select_fare == "50-1000":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query with the star rating range filter
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price BETWEEN ? AND ? 
                        AND Route_name = ? 
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                    ''', (50, 1000, Rajasthan_Route, min_rating, max_rating))

                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output for debugging
                    if not out:
                        slt.warning("No data retrieved from the database.")
                    else:
                        print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                # Convert to DataFrame
                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])

                # Display the data in Streamlit as a table
                slt.write(df)

            elif select_fare == "1000-2500":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                            SELECT * FROM bus_details
                            WHERE Price BETWEEN ? AND ? AND Route_name=?
                            AND Star_Rating BETWEEN ? AND ?
                            ORDER BY Price DESC
                            ''', (1000, 2500, Rajasthan_Route, min_rating, max_rating)) 
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)

            elif select_fare == '2500 and above':
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price >= ? AND Route_name = ?
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                        ''', (2500, Rajasthan_Route, min_rating, max_rating))
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)
#7. Sikkim
        if S == "Sikkim":
            Sikkim_Route = slt.selectbox("List of Routes", list_SNT)

            if select_fare == "50-1000":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query with the star rating range filter
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price BETWEEN ? AND ? 
                        AND Route_name = ? 
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                    ''', (50, 1000, Sikkim_Route, min_rating, max_rating))

                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output for debugging
                    if not out:
                        slt.warning("No data retrieved from the database.")
                    else:
                        print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                # Convert to DataFrame
                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])

                # Display the data in Streamlit as a table
                slt.write(df)

            elif select_fare == "1000-2500":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                            SELECT * FROM bus_details
                            WHERE Price BETWEEN ? AND ? AND Route_name=?
                            AND Star_Rating BETWEEN ? AND ?
                            ORDER BY Price DESC
                            ''', (1000, 2500, Sikkim_Route, min_rating, max_rating)) 
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)

            elif select_fare == '2500 and above':
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price >= ? AND Route_name = ?
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                        ''', (2500, Sikkim_Route, min_rating, max_rating))
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)
#8. West Bengal
        if S == "West Bengal":
            West_Bengal_Route = slt.selectbox("List of Routes", list_WBSTC)

            if select_fare == "50-1000":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query with the star rating range filter
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price BETWEEN ? AND ? 
                        AND Route_name = ? 
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                    ''', (50, 1000, West_Bengal_Route, min_rating, max_rating))

                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output for debugging
                    if not out:
                        slt.warning("No data retrieved from the database.")
                    else:
                        print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                # Convert to DataFrame
                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])

                # Display the data in Streamlit as a table
                slt.write(df)

            elif select_fare == "1000-2500":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                            SELECT * FROM bus_details
                            WHERE Price BETWEEN ? AND ? AND Route_name=?
                            AND Star_Rating BETWEEN ? AND ?
                            ORDER BY Price DESC
                            ''', (1000, 2500, West_Bengal_Route, min_rating, max_rating)) 
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)

            elif select_fare == '2500 and above':
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price >= ? AND Route_name = ?
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                        ''', (2500, West_Bengal_Route, min_rating, max_rating))
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)
#9. WBTC (CTC)
        if S == "WBTC (CTC)":
            WBTC_Route = slt.selectbox("List of Routes", list_WBTC)

            if select_fare == "50-1000":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query with the star rating range filter
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price BETWEEN ? AND ? 
                        AND Route_name = ? 
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                    ''', (50, 1000, WBTC_Route, min_rating, max_rating))

                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output for debugging
                    if not out:
                        slt.warning("No data retrieved from the database.")
                    else:
                        print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                # Convert to DataFrame
                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])

                # Display the data in Streamlit as a table
                slt.write(df)

            elif select_fare == "1000-2500":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                            SELECT * FROM bus_details
                            WHERE Price BETWEEN ? AND ? AND Route_name=?
                            AND Star_Rating BETWEEN ? AND ?
                            ORDER BY Price DESC
                            ''', (1000, 2500, WBTC_Route, min_rating, max_rating)) 
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)

            elif select_fare == '2500 and above':
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price >= ? AND Route_name = ?
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                        ''', (2500, WBTC_Route, min_rating, max_rating))
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)

#10. Gujarat

        if S == "Gujarat":
            Gujarat_Route = slt.selectbox("List of Routes", list_GSRTC)

            if select_fare == "50-1000":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query with the star rating range filter
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price BETWEEN ? AND ? 
                        AND Route_name = ? 
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                    ''', (50, 1000, Gujarat_Route, min_rating, max_rating))

                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output for debugging
                    if not out:
                        slt.warning("No data retrieved from the database.")
                    else:
                        print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                # Convert to DataFrame
                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])

                # Display the data in Streamlit as a table
                slt.write(df)

            elif select_fare == "1000-2500":
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                            SELECT * FROM bus_details
                            WHERE Price BETWEEN ? AND ? AND Route_name=?
                            AND Star_Rating BETWEEN ? AND ?
                            ORDER BY Price DESC
                            ''', (1000, 2500, Gujarat_Route, min_rating, max_rating)) 
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)

            elif select_fare == '2500 and above':
                conn = sqlite3.connect('redbus_database.db')  # Replace with your database file

                try:
                    # Create a cursor object
                    cursor = conn.cursor()

                    # Execute a query
                    cursor.execute('''
                        SELECT * FROM bus_details
                        WHERE Price >= ? AND Route_name = ?
                        AND Star_Rating BETWEEN ? AND ?
                        ORDER BY Price DESC
                        ''', (2500, Gujarat_Route, min_rating, max_rating))
                    # Fetch all rows from the executed query
                    out = cursor.fetchall()

                    # Print the output
                    print(out)

                except sqlite3.Error as e:
                    slt.error(f"Database error: {e}")

                finally:
                    conn.close()

                df = pd.DataFrame(out, columns=[
                    "Route_Name", "Route_Link", "Bus_Name", "Bus_Type", "Departing_Time",
                    "Duration", "Reaching_Time", "Star_Rating", "Price", "Seat_Availability"
                ])
                slt.write(df)

