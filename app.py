import streamlit as st
import requests
import re
import pandas as pd
from streamlit_folium import st_folium
import folium
import socket

# Function to validate IP address
def is_valid_ip(ip):
    pattern = re.compile(
        r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    )
    return pattern.match(ip)

# Function to store IP lookup history
def add_to_history(ip, details):
    if 'history' not in st.session_state:
        st.session_state.history = []
    if ip not in [record[0] for record in st.session_state.history]:
        st.session_state.history.append((ip, details))

def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "N/A"

def export_to_csv(ip, details):
    df = pd.DataFrame([details])
    df.to_csv(f"{ip}_info.csv", index=False)
    return df

def main():
    # Sidebar
    st.sidebar.title("About")
    st.sidebar.info("""
        This app allows you to check detailed information about an IP address using the 
        [IPinfo](https://ipinfo.io/) API. Enter an IP address in the input field and get information such as the location, ISP, and more.
    """)

    st.sidebar.title("How to Use")
    st.sidebar.info("""
    1. Enter a valid IP address in the input field.
    2. Click enter or return to see the results.
    3. A map will display the location of the IP address if available.
    """)

    st.sidebar.title("Author")
    st.sidebar.info("""
    **Author:** Jacolon Walker
    - [GitHub](https://github.com/jwalker)
    - [X](https://x.com/call_eax)
    - [LinkedIn](https://www.linkedin.com/in/jacolonwalker/)
    """)

    # Title of the app
    st.title("IP Information Checker")

    # Tabs for IP Lookup, History, and Comparison
    tabs = st.tabs(["IP Lookup", "Lookup History", "IP Comparison"])

    # Input IP address in IP Lookup tab
    with tabs[0]:
        st.subheader("IP Lookup")
        ip_address = st.text_input("Enter IP address to check")

        if ip_address:
            if is_valid_ip(ip_address):
                # Display loading message
                with st.spinner("Checking IP information..."):
                    # Call the IPinfo API
                    access_token = 'YOUR_ACCESS_TOKEN'  # Replace with your actual access token
                    response = requests.get(f"https://ipinfo.io/{ip_address}?token={access_token}")

                    if response.status_code == 200:
                        result = response.json()
                        add_to_history(ip_address, result)
                        st.write(f"**IP Address:** {ip_address}")
                        st.write(f"**Hostname:** {result.get('hostname', 'N/A')}")
                        st.write(f"**City:** {result.get('city', 'N/A')}")
                        st.write(f"**Region:** {result.get('region', 'N/A')}")
                        st.write(f"**Country:** {result.get('country', 'N/A')}")
                        st.write(f"**Location:** {result.get('loc', 'N/A')}")
                        st.write(f"**Organization:** {result.get('org', 'N/A')}")
                        st.write(f"**Postal:** {result.get('postal', 'N/A')}")
                        st.write(f"**Timezone:** {result.get('timezone', 'N/A')}")
                        st.write(f"**ASN:** {result.get('asn', {}).get('asn', 'N/A')} - {result.get('asn', {}).get('name', 'N/A')}")
                        st.write(f"**Reverse DNS:** {reverse_dns(ip_address)}")

                        # Display ISP and organization logos if available
                        if result.get('org') and result['org'] != 'N/A':
                            org_logo = f"https://logo.clearbit.com/{result['org'].split()[-1]}.com"
                            st.image(org_logo, caption=f"Organization: {result['org']}", use_column_width=True)

                        # Map to show the location
                        location = result.get('loc', 'N/A').split(',')
                        if len(location) == 2:
                            lat, lon = map(float, location)
                            m = folium.Map(location=[lat, lon], zoom_start=10)
                            folium.Marker([lat, lon], popup=f"IP: {ip_address}").add_to(m)
                            st_folium(m, width=700, height=500)
                        
                        # Export to CSV button
                        if st.button("Export to CSV"):
                            df = export_to_csv(ip_address, result)
                            st.success("CSV exported successfully!")
                            st.dataframe(df)
                    else:
                        st.error("Failed to retrieve information for the given IP address.")
            else:
                st.error("Please enter a valid IP address.")

    # Display IP lookup history in Lookup History tab
    with tabs[1]:
        st.subheader("Lookup History")
        if 'history' in st.session_state:
            for ip, details in st.session_state.history[::-1]:  # Show the history in reverse order
                st.write(f"**IP:** {ip}")
                st.write(f"**City:** {details.get('city', 'N/A')}, **Region:** {details.get('region', 'N/A')}")
                st.write("---")
        else:
            st.write("No history available.")

    # IP Comparison tab
    with tabs[2]:
        st.subheader("IP Comparison")
        col1, col2 = st.columns(2)
        
        with col1:
            ip1 = st.text_input("Enter first IP address")
        
        with col2:
            ip2 = st.text_input("Enter second IP address")

        if ip1 and ip2:
            if is_valid_ip(ip1) and is_valid_ip(ip2):
                with st.spinner("Comparing IP information..."):
                    response1 = requests.get(f"https://ipinfo.io/{ip1}?token={access_token}")
                    response2 = requests.get(f"https://ipinfo.io/{ip2}?token={access_token}")

                    if response1.status_code == 200 and response2.status_code == 200:
                        result1 = response1.json()
                        result2 = response2.json()
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**IP Address:** {ip1}")
                            st.write(f"**Hostname:** {result1.get('hostname', 'N/A')}")
                            st.write(f"**City:** {result1.get('city', 'N/A')}")
                            st.write(f"**Region:** {result1.get('region', 'N/A')}")
                            st.write(f"**Country:** {result1.get('country', 'N/A')}")
                            st.write(f"**Location:** {result1.get('loc', 'N/A')}")
                            st.write(f"**Organization:** {result1.get('org', 'N/A')}")
                            st.write(f"**Postal:** {result1.get('postal', 'N/A')}")
                            st.write(f"**Timezone:** {result1.get('timezone', 'N/A')}")
                            st.write(f"**ASN:** {result1.get('asn', {}).get('asn', 'N/A')} - {result1.get('asn', {}).get('name', 'N/A')}")
                            st.write(f"**Reverse DNS:** {reverse_dns(ip1)}")

                        with col2:
                            st.write(f"**IP Address:** {ip2}")
                            st.write(f"**Hostname:** {result2.get('hostname', 'N/A')}")
                            st.write(f"**City:** {result2.get('city', 'N/A')}")
                            st.write(f"**Region:** {result2.get('region', 'N/A')}")
                            st.write(f"**Country:** {result2.get('country', 'N/A')}")
                            st.write(f"**Location:** {result2.get('loc', 'N/A')}")
                            st.write(f"**Organization:** {result2.get('org', 'N/A')}")
                            st.write(f"**Postal:** {result2.get('postal', 'N/A')}")
                            st.write(f"**Timezone:** {result2.get('timezone', 'N/A')}")
                            st.write(f"**ASN:** {result2.get('asn', {}).get('asn', 'N/A')} - {result2.get('asn', {}).get('name', 'N/A')}")
                            st.write(f"**Reverse DNS:** {reverse_dns(ip2)}")
                    else:
                        st.error("Failed to retrieve information for one or both IP addresses.")
            else:
                st.error("Please enter valid IP addresses.")

    # Footer
    st.markdown("""
        This app uses the IPinfo API to check detailed information about an IP address. 
        Replace `YOUR_ACCESS_TOKEN` with your actual access token from [IPinfo](https://ipinfo.io/).
    """)

if __name__ == "__main__":
    main()
