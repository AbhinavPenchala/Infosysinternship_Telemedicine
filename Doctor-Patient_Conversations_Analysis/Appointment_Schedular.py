import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class AdvancedDiseaseRiskMapper:
    def __init__(self):
        """
        Comprehensive disease risk mapping with multi-level categorization
        """
        self.disease_categories = {
            'Chronic Conditions': {
                'Diabetes': {
                    'Type 1': 3.5,
                    'Type 2': 3.0,
                    'Prediabetes': 2.0
                },
                'Hypertension': {
                    'Stage 1': 2.5,
                    'Stage 2': 3.0,
                    'Resistant': 3.5
                },
                'Heart Disease': {
                    'Coronary Artery Disease': 4.0,
                    'Heart Failure': 4.5,
                    'Arrhythmia': 3.0
                },
                'Kidney Disease': {
                    'Chronic Kidney Disease': 4.0,
                    'Acute Kidney Injury': 4.5
                },
                'Liver Disease': {
                    'Cirrhosis': 4.0,
                    'Hepatitis B': 3.5,
                    'Hepatitis C': 3.5
                }
            },
            'Respiratory Conditions': {
                'Asthma': {
                    'Intermittent': 1.5,
                    'Mild Persistent': 2.0,
                    'Moderate Persistent': 2.5,
                    'Severe Persistent': 3.0
                },
                'COPD': {
                    'Mild': 2.5,
                    'Moderate': 3.0,
                    'Severe': 3.5
                },
                'Pneumonia': {
                    'Bacterial': 3.5,
                    'Viral': 3.0
                }
            },
            'Neurological Conditions': {
                'Epilepsy': {
                    'Controlled': 2.0,
                    'Uncontrolled': 3.0
                },
                'Multiple Sclerosis': {
                    'Relapsing-Remitting': 2.5,
                    'Secondary Progressive': 3.5
                },
                'Parkinson’s Disease': {
                    'Early Stage': 3.0,
                    'Advanced Stage': 4.0
                }
            },
            'Mental Health': {
                'Depression': {
                    'Mild': 1.5,
                    'Moderate': 2.0,
                    'Severe': 2.5
                },
                'Anxiety Disorders': {
                    'Generalized': 1.5,
                    'Panic Disorder': 2.0
                },
                'Schizophrenia': {
                    'Stable': 3.5,
                    'Unstable': 4.0
                }
            }
        }

    def calculate_disease_risk(self, patient_conditions):
        """
        Calculate comprehensive disease risk

        :param patient_conditions: List of dictionaries with disease details
        :return: Total disease risk score
        """
        total_risk = 0
        detailed_risks = []

        for condition in patient_conditions:
            category = condition.get('category')
            disease = condition.get('disease')
            subtype = condition.get('subtype', 'Default')

            try:
                risk = self.disease_categories[category][disease][subtype]
                total_risk += risk
                detailed_risks.append({
                    'category': category,
                    'disease': disease,
                    'subtype': subtype,
                    'risk': risk
                })
            except KeyError:
                # Default risk if not found
                total_risk += 1.0

        return total_risk, detailed_risks

    def visualize_disease_risk(self, detailed_risks):
        """
        Create advanced risk visualization

        :param detailed_risks: List of detailed risk entries
        :return: Matplotlib figure
        """
        plt.figure(figsize=(12, 6))

        # Extract data for visualization
        categories = [risk['category'] for risk in detailed_risks]
        diseases = [f"{risk['disease']}\n{risk['subtype']}" for risk in detailed_risks]
        risks = [risk['risk'] for risk in detailed_risks]

        # Color palette
        colors = plt.cm.viridis(np.linspace(0, 1, len(detailed_risks)))

        plt.bar(diseases, risks, color=colors)
        plt.title('Detailed Disease Risk Breakdown')
        plt.xlabel('Disease and Subtype')
        plt.ylabel('Risk Score')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        return plt

def main():
    st.set_page_config(layout="wide")
    st.title('Advanced Medical Risk Assessment')

    # Initialize disease risk mapper
    risk_mapper = AdvancedDiseaseRiskMapper()

    # Sidebar for condition input
    with st.sidebar:
        st.header('Patient Condition Details')

        # Dynamic condition input
        num_conditions = st.number_input('Number of Conditions', 1, 5, 1)
        patient_conditions = []

        for i in range(num_conditions):
            st.subheader(f'Condition {i+1}')
            category = st.selectbox(f'Category {i+1}',
                list(risk_mapper.disease_categories.keys()),
                key=f'category_{i}')

            disease = st.selectbox(f'Disease {i+1}',
                list(risk_mapper.disease_categories[category].keys()),
                key=f'disease_{i}')

            subtype = st.selectbox(f'Subtype {i+1}',
                list(risk_mapper.disease_categories[category][disease].keys()),
                key=f'subtype_{i}')

            patient_conditions.append({
                'category': category,
                'disease': disease,
                'subtype': subtype
            })

    # Risk Assessment Button
    if st.sidebar.button('Assess Comprehensive Risk'):
        # Calculate risk
        total_risk, detailed_risks = risk_mapper.calculate_disease_risk(patient_conditions)

        # Results Column
        col1, col2 = st.columns(2)

        with col1:
            st.header('Risk Assessment')
            st.metric('Total Risk Score', f"{total_risk:.2f}")

            # Risk Level Classification
            if total_risk < 2:
                risk_level = 'Low'
                follow_up_weeks = 24
            elif total_risk < 4:
                risk_level = 'Medium'
                follow_up_weeks = 12
            else:
                risk_level = 'High'
                follow_up_weeks = 4

            st.metric('Risk Level', risk_level)
            st.metric('Recommended Follow-Up', f'Every {follow_up_weeks} weeks')

        with col2:
            # Visualization
            plt = risk_mapper.visualize_disease_risk(detailed_risks)
            st.pyplot(plt)

        # Detailed Risks
        st.subheader('Detailed Risk Breakdown')
        risk_df = pd.DataFrame(detailed_risks)
        st.dataframe(risk_df)

if __name__ == '__main__':
    main()
