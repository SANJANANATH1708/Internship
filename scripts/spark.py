# 1. IMPORT LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
from sklearn.preprocessing import LabelEncoder

# 2. LOAD DATA

df = pd.read_excel(r"C:\Users\bhagawathy manju\OneDrive\Desktop\Sales Dataset.xlsx")

df = df.dropna()

# 3. REGRESSION (Predict Profit)

X = df[["Amount", "Quantity"]]
y = df["Profit"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
reg = LinearRegression()
reg.fit(X_train, y_train)

# Prediction
y_pred = reg.predict(X_test)

# Evaluation
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

print("RMSE:", rmse)
print("MAE:", mae)

# Residual Plot
residuals = y_test - y_pred

plt.scatter(y_pred, residuals)
plt.xlabel("Predicted")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.show()


# 4. CLASSIFICATION (Predict Category)

# Encode target
le = LabelEncoder()
df["Category_encoded"] = le.fit_transform(df["Category"])

X = df[["Amount", "Quantity"]]
y = df["Category_encoded"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
clf = LogisticRegression(max_iter=200)
clf.fit(X_train, y_train)

# Prediction
y_pred = clf.predict(X_test)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:\n", cm)

print("\nClassification Report:\n", classification_report(y_test, y_pred))

# 5. ROC CURVE (Binary version)

# Convert to binary (Example: Electronics vs Others)
df["Binary_Category"] = (df["Category"] == "Electronics").astype(int)

X = df[["Amount", "Quantity"]]
y = df["Binary_Category"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf.fit(X_train, y_train)

y_prob = clf.predict_proba(X_test)[:, 1]

fpr, tpr, _ = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.plot(fpr, tpr)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve (AUC = %.2f)" % roc_auc)
plt.show()