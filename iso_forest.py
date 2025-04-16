import pandas as pd # Data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns # Seaborn is a Python data visualization library based on matplotlib
import ipaddress # Library for working with IP addresses
from sklearn.ensemble import IsolationForest # Anomaly detection algorithm
from sklearn.preprocessing import OrdinalEncoder # Encode categorical features as an integer array
import matplotlib.pyplot as plt # Data visualization library
import pickle # Module for serializing and deserializing Python objects
    
def train_isofrst():
    # Load the training data
    
    #df = pd.read_csv('/Volumes/HUNTER/PortiaSoftware/DDoS-HTTP_Flood-.pcap_Flow.csv')
    df1 = pd.read_csv('/Volumes/HUNTER/PortiaSoftware/database/Monday-Benign.csv')
    df1.columns = df1.columns.str.strip()
    df2 = pd.read_csv('/Volumes/HUNTER/PortiaSoftware/database/Wednesday-DDOS.csv')
    df2.columns = df2.columns.str.strip()
    # Concatenate the two dataframes
    combinded_df = pd.concat([df1, df2], ignore_index=True)
   
    # Data preprocessing
    #df = data_preprocessing(df)
    combinded_df.info()
    print(combinded_df.columns)
    print("##############\n")

 #Encode 'ipv6.src' as integer
    encoder_src = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
    encoder_dest = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
    
    combinded_df['ipv6_encoded'] = encoder_src.fit_transform(combinded_df[['Source IP']])
    combinded_df['destip_encoded'] = encoder_dest.fit_transform(combinded_df[['Destination IP']])
    #df['ipv6_encoded'] = encoder.fit_transform(df['Src IP'].astype(str))


    anomoly_inputs = ['ipv6_encoded','Total Fwd Packets','Source Port','Destination Port', 'destip_encoded']
    #anomoly_inputs = ['ipv6_encoded','Total Fwd Packet','Src Port','Dst Port']

    # Train the model
    model_IF = IsolationForest(n_estimators=100, max_samples=0.1, contamination=0.1, random_state=42)
    model_IF.fit(combinded_df[anomoly_inputs])
    combinded_df['anomoly_score'] = model_IF.decision_function(combinded_df[anomoly_inputs])
    combinded_df['anomoly'] = model_IF.predict(combinded_df[anomoly_inputs])
    #df.loc[:, 'ipv6_encoded', 'Total Fwd Packets','Source Port','Destination Port', 'anomoly_score', 'anomoly']

    print ("Model trained")
    print(combinded_df)

    #Save the model
    print("Save the fitted model?(y/n)")
    choice = input().lower()
    if (choice == 'y'):
        with open('./trained_model/isofrst_model.sav', 'wb') as model_file:
            pickle.dump(model_IF, model_file)
        with open('./trained_model/encoder_src.sav', 'wb') as encoder_file:
            pickle.dump(encoder_src, encoder_file)
        with open('./trained_model/encoder_dest.sav', 'wb') as encoder_file:
            pickle.dump(encoder_dest, encoder_file)
        print("Model saved")
    else:
        print("Model not saved")



    #Decode 'ipv6.src' from integer
    combinded_df['ipv6_decoded'] = encoder_src.inverse_transform(combinded_df[['ipv6_encoded']])[:,0] #[:, 0] selects the first column from the returned 2D array and flattens it into a 1D array (a Series), which is what .loc[] or df['col'] = ... expects.
    # Display the anomalous packets
    anomalous_packets = combinded_df[combinded_df['anomoly'] == -1]
    print("Anomalous packets:")
    print(anomalous_packets)

    # Store the Ipv6.src from anomalous  packets
    anomalous_ip = anomalous_packets['ipv6_decoded']

    #with open('anomalous_ip.txt', 'w') as f:
   #     for item in anomalous_ip:
     #       f.write("%s\n" % item)

    # Visualize the anomalous packets
    sizes = [dict(combinded_df['anomoly'].value_counts())[-1], dict(combinded_df['anomoly'].value_counts())[1]]
    lables = ["Anomalous", "Normal"]
    plt.pie(sizes, labels=lables, autopct='%1.1f%%',shadow=True, startangle=90)
    plt.legend(["Malicious", "Benign"])
    plt.title('Percentage of Malicious and Benign packets')
    plt.show() 


train_isofrst()
