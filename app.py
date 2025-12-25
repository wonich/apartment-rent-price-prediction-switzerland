﻿import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np

IMMOLEX_API_KEY = st.secrets["IMMOLEX_API_KEY"]

# Function to make the API request
def get_rent_prediction(data):
    url = "http://api.immolex.ch:8051/predictCH"  # Your API URL
    #url = "http://127.0.0.1:8000/predictCH"  # Your API URL
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": IMMOLEX_API_KEY  # Add the API key header here
    }
    
    payload = {
        "address": data["address"],
        "data": data["features"]
    }

    try:
        resp = requests.post(url, json=payload, headers=headers)

        # Wichtig: erst Status prüfen, dann JSON "normal" verarbeiten
        if resp.status_code != 200:
            # FastAPI liefert meist {"detail": "..."} zurück
            try:
                err = resp.json()
                detail = err.get("detail", resp.text)
            except ValueError:
                detail = resp.text

            st.error(f"API Error {resp.status_code}: {detail}")
            return None

        # 2xx: OK
        return resp.json()

    except requests.exceptions.RequestException as e:
        st.error(f"Network/API request failed: {e}")
        return None
    
# Function to make the API request
def get_rent_prediction_chronic(data):
    url = "http://api.immolex.ch:8051/predictCHChronic"  # Your API URL
    #url = "http://127.0.0.1:8000/predictCHChronic"  # Your API URL
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": IMMOLEX_API_KEY  # Add the API key header here
    }
    
    payload = {
        "address": data["address"],
        "data": data["features"]
    }
    
    try:
        resp = requests.post(url, json=payload, headers=headers)

        # Wichtig: erst Status prüfen, dann JSON "normal" verarbeiten
        if resp.status_code != 200:
            # FastAPI liefert meist {"detail": "..."} zurück
            try:
                err = resp.json()
                detail = err.get("detail", resp.text)
            except ValueError:
                detail = resp.text

            st.error(f"API Error {resp.status_code}: {detail}")
            return None

        # 2xx: OK
        return resp.json()

    except requests.exceptions.RequestException as e:
        st.error(f"Network/API request failed: {e}")
        return None

    
# Function to make the API request
def get_rent_prediction_ageofbuilding(data):
    url = "http://api.immolex.ch:8051/predictCHAgeOfBuilding"  # Your API URL
    #url = "http://127.0.0.1:8000/predictCHAgeOfBuilding"  # Your API URL
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": IMMOLEX_API_KEY  # Add the API key header here
    }
    
    payload = {
        "address": data["address"],
        "data": data["features"]
    }


    try:
        resp = requests.post(url, json=payload, headers=headers)

        # Wichtig: erst Status prüfen, dann JSON "normal" verarbeiten
        if resp.status_code != 200:
            # FastAPI liefert meist {"detail": "..."} zurück
            try:
                err = resp.json()
                detail = err.get("detail", resp.text)
            except ValueError:
                detail = resp.text

            st.error(f"API Error {resp.status_code}: {detail}")
            return None

        # 2xx: OK
        return resp.json()

    except requests.exceptions.RequestException as e:
        st.error(f"Network/API request failed: {e}")
        return None

# Streamlit App UI
def app():
    st.title("Apartment rent price prediction - switzerland")

    # Input fields for apartment features
    st.header("Apartment details")
    
    address = st.text_input("Where is the appartment located?", "Marktgasse 28, Bülach")

    size_rooms = st.slider("Number of rooms", min_value=1.0, max_value=5.5, value=2.5, step=0.5)
    size_square_meters = st.slider("Size (m²)", min_value=20, max_value=300, value=70)
    app_count_building = st.slider("Number of apartments in the building", min_value=1, max_value=50, value=8)
    floor_numbers = st.slider("Floor of the appartment", min_value=0, max_value=20, value=2)
    age_of_building = st.slider("Age of building (years)", min_value=0, max_value=100, value=5)
    penthouse = st.checkbox("Is it a penthouse?")
    washing_machine = st.checkbox("Has washing machine?")
    elevator = st.checkbox("Has Elevator?")
    garden = st.checkbox("Has garden?")
    is_first_rent = st.checkbox("Is it the first rent?")
    floor_laminate = st.checkbox("Has laminate floor?")
    renovate = st.checkbox("Is it renovated?")
    balcony_terrace = st.checkbox("Has balcony or terrace?")
    

    # Prepare the data payload
    features = {
        "room_class": np.floor(size_rooms),
        "sizeSquareMeters": size_square_meters,
        "AppCountOfBuilding": app_count_building,
        "floornumbers": floor_numbers,
        "penthouse": penthouse,
        "washingmachine": washing_machine,
        "elevator": elevator,
        "garden": garden,
        "isfirstrent": is_first_rent,
        "floorlaminate": floor_laminate,
        "renovate": renovate,
        "balconyterrace": balcony_terrace,
        "ageofbuilding": age_of_building
    }

    data = {
        "address": address,
        "features": features
    }

    # When the user presses the button, fetch the prediction
    if st.button("Predict rent price"):
        prediction_result = get_rent_prediction(data)

        if prediction_result:
            
            # Show the entire JSON response in a pretty format
            #st.subheader("Raw JSON Response:")
            #st.json(prediction_result)  # Streamlit's json method displays the formatted JSON
            
            prediction = prediction_result["prediction"]
            lower_band = prediction_result["interval"]["lower"]
            upper_band = prediction_result["interval"]["upper"]
            confidence = prediction_result["interval"]["confidence"]
            unit = prediction_result["interval"]["unit"]

            # Check if the median (prediction) is outside of the confidence interval
            if prediction < lower_band or prediction > upper_band:
                st.error("This configuration cannot be calculated with the current model. Please contact www.immolex.ch for further assistance in obtaining prices for special configurations")
            else:
                st.subheader(f"Predicted excl. rent: {prediction:.0f} {unit}")
                st.write(f"Confidence interval: {lower_band:.0f} - {upper_band:.0f} {unit} (Confidence: {confidence})")
            
                # Plot the result
                fig, ax = plt.subplots(figsize=(6, 4))

                # Plot bands and prediction
                ax.fill_between([0, 1], lower_band, upper_band, color="cornflowerblue", alpha=0.4, label=f"Confidence interval ({confidence})")
                ax.plot([0, 1], [prediction, prediction], color="black", linewidth=2, label="Predicted excl. rent (median)")

                ax.set_xlim(0, 1)
                ax.set_ylim(min(lower_band, upper_band) - 100, max(lower_band, upper_band) + 100)
                ax.set_xticks([])
                ax.set_yticks([lower_band, upper_band, prediction])
                ax.set_yticklabels([f"{lower_band:.0f}", f"{upper_band:.0f}", f"{prediction:.0f}"])
                ax.set_title("Apartment excl. rent price prediction", fontsize=16, fontweight="bold")
                ax.set_xlabel('Prediction interval', fontsize=14)
                ax.set_ylabel(f'Price ({unit})', fontsize=14)

                # Adding gridlines for clarity
                ax.grid(True, linestyle='--', alpha=0.5)
                ax.legend()

                st.pyplot(fig)
     

        prediction_chronic_result = get_rent_prediction_chronic(data)
        
        if prediction_chronic_result:
            chronical_predictions = prediction_chronic_result["chronical_predictions"]

            # Defensive Check
            if len(chronical_predictions) < 2:
                st.error("Not enough data points to display a time series.")
            else:
                # Extract values
                quarters = [item["quarter"] for item in chronical_predictions]
                predictions = [item["prediction"] for item in chronical_predictions]
                lower = [item["interval"]["lower"] for item in chronical_predictions]
                upper = [item["interval"]["upper"] for item in chronical_predictions]

                # Headline
                st.subheader("Predicted rent development over time")

                # Plot
                fig, ax = plt.subplots(figsize=(10, 4))
                
                ax.plot(
                    quarters,
                    lower,
                    marker="o",
                    linewidth=2,
                    label="Predicted lower excl. rent"
                )
                ax.plot(
                    quarters,
                    predictions,
                    marker="o",
                    linewidth=2,
                    label="Predicted median excl. rent"
                )
                ax.plot(
                    quarters,
                    upper,
                    marker="o",
                    linewidth=2,
                    label="Predicted upper excl. rent"
                )

                ax.set_title(
                    "Apartment excl. rent price prediction (quarterly)",
                    fontsize=16,
                    fontweight="bold"
                )
                ax.set_xlabel("Quarter", fontsize=14)
                ax.set_ylabel("Price (CHF)", fontsize=14)

                ax.set_ylim(
                    min(lower) - 100,
                    max(upper) + 100
                )

                ax.grid(True, linestyle="--", alpha=0.5)
                ax.legend()

                plt.xticks(rotation=45)

                st.pyplot(fig)

        prediction_buildingage_result = get_rent_prediction_ageofbuilding(data)
        
        if prediction_buildingage_result:
            buildingage_predictions = prediction_buildingage_result["ageofbuilding_predictions"]

            # Defensive Check
            if len(buildingage_predictions) < 2:
                st.error("Not enough data points to display a time series.")
            else:
                # Extract values
                ageofbuilding = [item["ageofbuilding"] for item in buildingage_predictions]
                predictions = [item["prediction"] for item in buildingage_predictions]
                lower = [item["interval"]["lower"] for item in buildingage_predictions]
                upper = [item["interval"]["upper"] for item in buildingage_predictions]

                # Headline
                st.subheader("Predicted excl. rent for different building ages")

                # Plot
                fig, ax = plt.subplots(figsize=(10, 4))
                
                ax.plot(
                    ageofbuilding,
                    lower,
                    marker="o",
                    linewidth=2,
                    label="Predicted lower excl. Rent"
                )
                ax.plot(
                    ageofbuilding,
                    predictions,
                    marker="o",
                    linewidth=2,
                    label="Predicted median excl. Rent"
                )
                ax.plot(
                    ageofbuilding,
                    upper,
                    marker="o",
                    linewidth=2,
                    label="Predicted upper excl. Rent"
                )

                ax.set_title(
                    "Apartment excl. rent price prediction (age of building)",
                    fontsize=16,
                    fontweight="bold"
                )
                ax.set_xlabel("Age of building", fontsize=14)
                ax.set_ylabel("Price (CHF)", fontsize=14)

                ax.set_ylim(
                    min(lower) - 100,
                    max(upper) + 100
                )

                ax.grid(True, linestyle="--", alpha=0.5)
                ax.legend()

                plt.xticks(rotation=45)

                st.pyplot(fig)

    # Footer Section
    st.markdown("<hr>", unsafe_allow_html=True)  # Horizontal line
    st.markdown('<p style="text-align: center;">For more informations about the Model have a look at the <a href="https://github.com/wonich/apartment-rent-price-prediction-arount-Bulach">github-Repo</a></p>', unsafe_allow_html=True)    
    st.markdown('<p style="text-align: center;">Data and model are powered by <a href="https://www.immolex.ch"><strong>IMMOLEX</strong></a></p>', unsafe_allow_html=True)
    
# Run the app
if __name__ == "__main__":
    app()