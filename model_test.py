import numpy as np
import sys
import pickle
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder # Encode categorical features as an integer array
from sklearn.ensemble import IsolationForest # Isolation Forest algorithm for anomaly detection
import matplotlib.pyplot as plt # Data visualization library
import seaborn as sns # Data visualization library based on matplotlib


def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model


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
    with open('/Volumes/HUNTER/PortiaSoftware/trained_model/encoder_src.sav', 'rb') as file:
        encoder_src = pickle.load(file)
    with open('/Volumes/HUNTER/PortiaSoftware/trained_model/encoder_dest.sav', 'rb') as file:
        encoder_dest = pickle.load(file)


    test_df = pd.read_csv('/Volumes/HUNTER/PortiaSoftware/database/' + test_data_path, encoding='latin1')

    test_df.info()
    test_df.columns = test_df.columns.str.strip()
    print(test_df.columns)

    # Data preprocessing
    test_df['ipv6_encoded'] = encoder_src.transform(test_df[['Source IP']]) #Use just transform so that the encoder is not refitted
    test_df['destip_encoded'] = encoder_dest.transform(test_df[['Destination IP']])

    test_inputs = ['ipv6_encoded', 'Total Fwd Packets', 'Source Port', 'Destination Port', 'destip_encoded']

    # Test the model
    test_df['anomoly_score'] = model.decision_function(test_df[test_inputs])
    #make predictions and add to the dataframe
    test_df['anomoly'] = model.predict(test_df[test_inputs])
    
    print(test_df['anomoly_score'].describe())
    
    #Decode 'ipv6.src' from integer
    test_df['ip_decoded'] = encoder_src.inverse_transform(test_df[['ipv6_encoded']])[:, 0]
    # Display the anomalous packets
    anomalous_packets = test_df[test_df['anomoly'] == -1]
    # Store the Ipv6.src from anomalous  packets
    anomalous_ip = anomalous_packets['ip_decoded']

    ip_set = set()
    with open('anomalous_ip.txt', 'w') as f:
        for item in anomalous_ip:
            ip_set.add(item)
        for item in ip_set:
            f.write("%s\n" % item)

    # Visualize the anomalous packets
    threshold = np.percentile(test_df['anomoly_score'], 10)
    sns.histplot(test_df['anomoly_score'], bins=100, kde=True)
    plt.axvline(threshold, color='r', linestyle='--', label='Anomaly threshold (10%)')
    plt.title("Anomaly Score Distribution")
    plt.xlabel("Anomaly Score")
    plt.ylabel("Count")
    plt.legend()
    plt.show()

    print("Done writing anomalous IPs to file")
main("TFTP.csv")