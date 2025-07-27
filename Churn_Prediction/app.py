from flask import Flask, request, render_template
import pickle
import numpy as np
app = Flask(__name__)
with open ('model.pkl', 'rb') as file:
 model = pickle.load(file)
@app.route('/')
def home():
 return render_template('index.html')

# @app.route('/predict',methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Binary Inputs
        binary_fields = ['gender', 'SeniorCitizen', 'Partner', 'Dependents',
                         'PhoneService', 'MultipleLines', 'OnlineSecurity',
                         'OnlineBackup', 'DeviceProtection', 'TechSupport',
                         'StreamingTV', 'StreamingMovies', 'PaperlessBilling']

        input_data = []
        for field in binary_fields:
            input_data.append(int(request.form[field]))

        # Numeric Inputs
        tenure = float(request.form['tenure'])
        monthly = float(request.form['MonthlyCharges'])
        total = float(request.form['TotalCharges'])

        input_data += [tenure, monthly, total]

        # One-Hot Encoded Inputs
        one_hot_features = [
            'Payment_Bank transfer (automatic)',
            'Payment_Credit card (automatic)',
            'Payment_Electronic check',
            'Payment_Mailed check',
            'Contract_Month-to-month',
            'Contract_One year',
            'Contract_Two year',
            'Service_DSL',
            'Service_Fiber optic',
            'Service_No'
        ]

        # Initialize all to 0
        one_hot_values = [0] * len(one_hot_features)

        # Set selected payment method
        payment_method = request.form['PaymentMethod']
        if payment_method in one_hot_features:
            one_hot_values[one_hot_features.index(payment_method)] = 1

        # Set selected contract type
        contract_type = request.form['ContractType']
        if contract_type in one_hot_features:
            one_hot_values[one_hot_features.index(contract_type)] = 1

        # Set selected service type
        service_type = request.form['ServiceType']
        if service_type in one_hot_features:
            one_hot_values[one_hot_features.index(service_type)] = 1

        input_data += one_hot_values

        # Convert to NumPy and predict
        final_input = np.array(input_data).reshape(1, -1)
        prediction = model.predict(final_input)

        return render_template('index.html', prediction_text=f'Churn Prediction: {prediction[0]}')

    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

# # def predict():
#  try:
#   inputFeature = [float(x) for x in request.form.values()]
#   input_array = np.array(inputFeature).reshape(1, -1)
#   prediction = model.predict(input_array)
#   return render_template('index.html', prediction_text=f'Predicted Output: {prediction[0]}')
#  except Exception as e:
#   return render_template('index.html', prediction_text=f'Error: {str(e)}')
if __name__ == '__main__':
 app.run(debug=True)