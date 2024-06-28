I created this app as a scaffold template to use for deploying Streamlit apps to AWS Elastic Beanstalk.
Important files/folders:

 - .ebextensions/
 - Procfile
 - requirements.txt

All the above needed for a successful deploy. Also make sure you add the `PORT` key and `8501` value to envionment variables for AWS EB configuration.


# IP Information Checker

This app allows you to check detailed information about an IP address using the [IPinfo](https://ipinfo.io/) API. You can get information such as the location, ISP, and more.

## Features

- IP Lookup: Enter an IP address to get detailed information. (with map viz)
- Lookup History: View the history of IP lookups performed during the session.
- IP Comparison: Compare information between two IP addresses side-by-side.
- CSV Export: Download the lookup results as a CSV file.

## How to Use

1. Enter a valid IP address in the input field.
2. Click enter or return to see the results.
3. A map will display the location of the IP address if available.

## Requirements

- Python 3.7+
- [Streamlit](https://streamlit.io/)
- [Requests](https://pypi.org/project/requests/)
- [Streamlit-Folium](https://pypi.org/project/streamlit-folium/)
- [Folium](https://pypi.org/project/folium/)
- [Pandas](https://pypi.org/project/pandas/)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/jwalker/ip-info-checker.git
    cd ip-info-checker
    ```

2. Install the required packages:

    ```bash
    uv venv
    souce venv/bin/activate
    uv pip install -r requirements.txt
    ```

3. Replace `YOUR_ACCESS_TOKEN` in `app.py` with your actual IPinfo access token.

4. Run the app:

    ```bash
    streamlit run app.py
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This app uses the [IPinfo](https://ipinfo.io/) API for IP address information.
- Folium and Streamlit-Folium are used for map visualizations.

