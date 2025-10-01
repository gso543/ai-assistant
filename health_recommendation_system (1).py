import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class HealthRecommendationSystem:
    def __init__(self):
        print("Initializing Health Recommendation System...")
        self.model = None
        self.data = None
        self._generate_simulated_data()
        self._train_model()

    def _generate_simulated_data(self):
        """Generates simulated health data for demonstration."""
        np.random.seed(42)
        num_records = 1000

        data = {
            'age': np.random.randint(65, 95, num_records),
            'sleep_hours': np.random.uniform(4, 10, num_records).round(1),
            'daily_activity_level': np.random.choice(['low', 'medium', 'high'], num_records),
            'heart_rate': np.random.randint(60, 100, num_records),
            'medication_adherence': np.random.uniform(0.5, 1.0, num_records).round(2),
            'fall_risk_score': np.random.uniform(0, 1, num_records).round(2),
            'recommended_activity': np.random.choice(['walking', 'stretching', 'reading', 'light_yoga', 'social_games'], num_records)
        }
        self.data = pd.DataFrame(data)

        # Introduce some correlation for fall risk and recommendations
        self.data.loc[self.data['sleep_hours'] < 6, 'fall_risk_score'] += 0.2
        self.data.loc[self.data['daily_activity_level'] == 'low', 'fall_risk_score'] += 0.3
        self.data['fall_risk_score'] = np.clip(self.data['fall_risk_score'], 0, 1).round(2)

        # Adjust recommendations based on fall risk
        high_risk_indices = self.data[self.data["fall_risk_score"] > 0.7].index
        self.data.loc[high_risk_indices, "recommended_activity"] = np.random.choice(["stretching", "reading"], size=len(high_risk_indices))
        
        low_risk_indices = self.data[self.data["fall_risk_score"] < 0.3].index
        self.data.loc[low_risk_indices, "recommended_activity"] = np.random.choice(["walking", "light_yoga", "social_games"], size=len(low_risk_indices))

        print("Simulated health data generated.")

    def _train_model(self):
        """Trains a simple model for activity recommendations."""
        if self.data is None:
            self._generate_simulated_data()

        # Convert categorical features to numerical using one-hot encoding
        X = self.data[['age', 'sleep_hours', 'daily_activity_level', 'heart_rate', 'medication_adherence', 'fall_risk_score']]
        X = pd.get_dummies(X, columns=['daily_activity_level'], drop_first=True)
        y = self.data['recommended_activity']

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a RandomForestClassifier model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Recommendation model trained with accuracy: {accuracy:.2f}")

    def get_recommendations(self, age, sleep_hours, daily_activity_level, heart_rate, medication_adherence, fall_risk_score):
        """Generates personalized health recommendations."""
        input_data = pd.DataFrame([{
            'age': age,
            'sleep_hours': sleep_hours,
            'daily_activity_level': daily_activity_level,
            'heart_rate': heart_rate,
            'medication_adherence': medication_adherence,
            'fall_risk_score': fall_risk_score
        }])

        # Ensure input data has the same columns as training data
        input_data = pd.get_dummies(input_data, columns=['daily_activity_level'], drop_first=True)
        # Add missing columns with 0 if they were present in training data but not in input
        missing_cols = set(self.model.feature_names_in_) - set(input_data.columns)
        for c in missing_cols:
            input_data[c] = 0
        input_data = input_data[self.model.feature_names_in_] # Ensure column order

        recommendation = self.model.predict(input_data)[0]
        return recommendation

    def generate_activity_report_chart(self):
        """Generates a chart of daily activity levels."""
        if self.data is None:
            self._generate_simulated_data()

        activity_counts = self.data['daily_activity_level'].value_counts().sort_index()

        plt.figure(figsize=(8, 6))
        activity_counts.plot(kind='bar', color=['#667eea', '#f093fb', '#a8edea'])
        plt.title('توزيع مستويات النشاط اليومي', fontname='Arial')
        plt.xlabel('مستوى النشاط', fontname='Arial')
        plt.ylabel('عدد الأفراد', fontname='Arial')
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Save chart to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        # Encode to base64
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return image_base64

if __name__ == "__main__":
    recommender = HealthRecommendationSystem()
    
    # Example recommendation
    rec = recommender.get_recommendations(age=70, sleep_hours=6.5, daily_activity_level='low', heart_rate=75, medication_adherence=0.9, fall_risk_score=0.6)
    print(f"Recommended activity: {rec}")

    # Generate and save chart
    chart_base64 = recommender.generate_activity_report_chart()
    # In a real application, this base64 string would be sent to the web dashboard
    print("Activity report chart generated (base64 encoded).")

    # You can decode and save it to a file to view
    # with open("activity_chart.png", "wb") as f:
    #     f.write(base64.b64decode(chart_base64))
    # print("Chart saved as activity_chart.png")

