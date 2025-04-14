import numpy as np
import sys
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

def test_model(model, test_data):
    predictions = model.predict(test_data)
    return predictions


def main(test_data_path):
    # Check if the test data path is provided
    if len(sys.argv) != 2:
        print("No test data path provided")
        test_data_path = 'TFTP.csv'
    else:
        test_data_path = sys.argv[1]
    # Load the model
    model_path = '/Volumes/HUNTER/PortiaSoftware/trained_model/isofrst_model.sav'
    model = load_model(model_path)

    # Load the encoder
    with open('/Volumes/HUNTER/PortiaSoftware/trained_model/encoder.sav', 'rb') as file:
        encoder = pickle.load(file)


    test_df = pd.read_csv('/Volumes/HUNTER/PortiaSoftware/database/' + test_data_path, encoding='latin1')

    test_df.info()
    test_df.columns = test_df.columns.str.strip()
    print(test_df.columns)
    test_df['ipv6_encoded'] = encoder.fit_transform(test_df['Source IP'].astype(str))

    test_inputs = ['ipv6_encoded', 'Total Fwd Packets', 'Source Port', 'Destination Port']
    test_df = test_df[test_inputs]
    print(test_df)

    # Test the model
    test_df['anomoly_score'] = model.decision_function(test_df[test_inputs])
    #make predictions and add to the dataframe
    test_df['anomoly'] = model.predict(test_df[test_inputs])
    

    
    #Decode 'ipv6.src' from integer
    test_df['ip_decoded'] = encoder.inverse_transform(test_df['ipv6_encoded'])
    # Display the anomalous packets
    anomalous_packets = test_df[test_df['anomoly'] == -1]

    # Store the Ipv6.src from anomalous  packets
    anomalous_ip = anomalous_packets['ip_decoded']

    with open('anomalous_ip.txt', 'w') as f:
        for item in anomalous_ip:
            f.write("%s\n" % item)

    print("Done writing anomalous IPs to file")
main()