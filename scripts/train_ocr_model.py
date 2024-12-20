import cv2
import numpy as np
import pandas as pd
import os
from skimage.feature import hog
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report
import joblib

# Define paths
data_dir = '/home/harshavardhan/Documents/OCR_Project'
model_path = 'models/ocr_model.pkl'

# Function to extract HOG features
def extract_features(img_path):
    img = cv2.imread(img_path)
    img_res = cv2.resize(img, (64, 128), interpolation=cv2.INTER_AREA)
    img_gray = cv2.cvtColor(img_res, cv2.COLOR_BGR2GRAY)
    features = hog(img_gray, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(1, 1))
    return features

# Prepare dataset
features = []
labels = []

for label in os.listdir(data_dir):
    label_dir = os.path.join(data_dir, label)
    for img_name in os.listdir(label_dir):
        img_path = os.path.join(label_dir, img_name)
        features.append(extract_features(img_path))
        labels.append(label)

# Convert to DataFrame
df = pd.DataFrame(features)
df['target'] = labels

# Balance the dataset
x = np.array(df.iloc[:, :-1])
y = np.array(df['target'])
sm = SMOTE(random_state=0)
x_bal, y_bal = sm.fit_resample(x, y)

# Split into train and test sets
x_train, x_test, y_train, y_test = train_test_split(x_bal, y_bal, test_size=0.20, random_state=42)

# Train logistic regression model
clf = LogisticRegression(max_iter=1000)
clf.fit(x_train, y_train)

# Evaluate the model
y_pred = clf.predict(x_test)
print('Classification Report:')
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(clf, model_path)
print(f'Model saved to {model_path}')
