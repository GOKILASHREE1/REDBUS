import streamlit as st
import mysql.connector
import pandas as pd

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="redbus"
)

# Create a cursor object
mycursor = mydb.cursor()

# Sidebar components
st.sidebar.image('C:/REDBUS_PROJECT/envi/redbus.png')
st.sidebar.video("https://youtu.be/eyAAUGhvZu8")

st.title("REDBUS BOOKINGS")
st.header("India's No. 1 Online Bus Ticket Booking")

# Transport selection
transport_options = ["Select Transport"] + ["ASTC", "BSRTC", "CTU", "JKSRTC", "KAAC", "KSRTC", "KTCL", "NBSTC", "PEPSU", "WBTC"]
selected_transport = st.selectbox("**CHOOSE TRANSPORT**", transport_options, index=0)

st.write(f"You have selected: {selected_transport}")

# Route selection based on selected transport
if selected_transport != "Select Transport":
    query = f"SELECT DISTINCT route_name, busname FROM redbus_data WHERE transport='{selected_transport}'"
    mycursor.execute(query)
    routes = mycursor.fetchall()
    route_options = ["Select Route"] + [f"{route[0]} ({route[1]})" for route in routes]
    selected_route = st.selectbox("**CHOOSE ROUTE NAME**", route_options, index=0)
    st.write(f"You have selected: Route - {selected_route}")
else:
    selected_route = None

# Bus type selection (Multi-select)
if selected_transport != "Select Transport" and selected_route and selected_route != "Select Route":
    query = f"""
    SELECT DISTINCT bustype 
    FROM redbus_data 
    WHERE transport='{selected_transport}' 
    AND route_name='{selected_route.split(' (')[0]}'
    """
    mycursor.execute(query)
    bus_types = mycursor.fetchall()
    bus_type_options = [bus_type[0] for bus_type in bus_types]
    selected_bustype = st.multiselect("**CHOOSE BUSTYPE**", bus_type_options)
    st.write(f"You have selected: Bus Type - {selected_bustype}")
else:
    selected_bustype = None

# Star rating selection
star_rating_options = ["1.1 to 3.3", "3.4 to 5.0"]
selected_starrating = st.multiselect("**STAR RATING**", star_rating_options)
st.write(f"You have selected: Star Rating - {selected_starrating}")

# Price selection
price_options = ["100 - 2500", "2501 - 5000"]
selected_price = st.multiselect("**PRICE**", price_options)
st.write(f"You have selected: Price - {selected_price}")

# Departing time selection
departing_time = ["03:00 to 12:00", "12:01 to 18:00", "18:01 to 23:59"]
selected_departingtime = st.multiselect("**DEPARTING TIME**", departing_time)
st.write(f"You have selected: Departing Time - {selected_departingtime}")

# Parse selected star rating, price, and departing time ranges
def parse_range(selected_options):
    ranges = []
    for option in selected_options:
        range_values = option.split(" to " if " to " in option else "-")
        ranges.append((range_values[0].strip(), range_values[1].strip()))
    return ranges

star_rating_ranges = parse_range(selected_starrating)
price_ranges = parse_range(selected_price)
departing_time_ranges = parse_range(selected_departingtime)

# Checkbox for acceptance
if st.checkbox('Accepted'):
    st.write('THANK YOU!!! SELECT YOUR BUS BELOW!!! VISIT US AGAIN')

st.markdown("[**CLICK HERE FOR PAYMENT DETAILS AND CUSTOMER CARE**](https://www.redbus.in/)")

# Fetch filtered data from redbus_data table based on selected filters
if all([selected_transport != "Select Transport", selected_route != "Select Route", selected_bustype, 
        star_rating_ranges, price_ranges, departing_time_ranges]):
    
    query_conditions = [
        f"transport='{selected_transport}'",
        f"route_name='{selected_route.split(' (')[0]}'",
        f"busname='{selected_route.split(' (')[1][:-1]}'",
    ]
    
    if selected_bustype:
        bustype_conditions = " OR ".join([f"bustype='{bustype}'" for bustype in selected_bustype])
        query_conditions.append(f"({bustype_conditions})")
    
    star_rating_conditions = " OR ".join([f"(star_rating BETWEEN {r[0]} AND {r[1]})" for r in star_rating_ranges])
    query_conditions.append(f"({star_rating_conditions})")
    
    price_conditions = " OR ".join([f"(price BETWEEN {r[0]} AND {r[1]})" for r in price_ranges])
    query_conditions.append(f"({price_conditions})")
    
    departing_time_conditions = " OR ".join([f"(departing_time BETWEEN '{r[0]}' AND '{r[1]}')" for r in departing_time_ranges])
    query_conditions.append(f"({departing_time_conditions})")
    
    query = f"SELECT * FROM redbus_data WHERE {' AND '.join(query_conditions)}"
    #st.write(f"Generated Query: {query}")  
    
    mycursor.execute(query)
    data = mycursor.fetchall()
    columns = [desc[0] for desc in mycursor.description]

    # Check if data is fetched
    if data:
        # Create a DataFrame from the fetched data
        df = pd.DataFrame(data, columns=columns)
        # Display the DataFrame in Streamlit
        st.write("**Redbus Data**")
        st.dataframe(df)
    else:
        st.write("No data found for the selected filters.")

# Close the cursor and connection
mycursor.close()
mydb.close()
