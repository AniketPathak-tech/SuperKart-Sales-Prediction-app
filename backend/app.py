import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize the Flask app with a name
superkart_api = Flask("superkart_sales_app")

# Load the trained churn prediction model
model = joblib.load("forecast_superkart_sales_model.joblib")

# Define a route for the home page
@superkart_api.get('/')
def home():
    return "Welcome to SuperKart Sales Prediction API!"

    # Define an endpoint to predict churn for a single customer
@superkart_api.post('/v1/predict')
def predict_sales():

  # Get the JSON data from the request body
      data = request.get_json()

        # Extract relevant product features from the input data.
      sample = {
        'Product_Weight': data['Product_Weight'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_MRP': data['Product_MRP'],
        'Store_Size': data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type': data['Store_Type'],
        'Store_Age_Years': data['Store_Age_Years'],
        'Product_Type_Category': data['Product_Type_Category'],
        'Product_Id_char': data['Product_Id_char']
      }

      # Convert the extracted data into a DataFrame
      input_data = pd.DataFrame([sample])

      # Make a prediction using the trained model
      prediction = model.predict(input_data).tolist()[0]

      # Return the prediction as a JSON response
      return jsonify({'Sales': prediction})

    except KeyError as e:
      return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
      return jsonify({'error': f'Prediction failed: {str(e)}' }), 500

      # Run the Flask app in debug mode
      if __name__ == '__main__':
          superkart_api.run(debug=True)
