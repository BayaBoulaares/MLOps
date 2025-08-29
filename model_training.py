# model_training.py
# --------------------------------------------
# Import necessary libraries
import pandas as pd
import pickle
import os
import mlflow
import mlflow.sklearn
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split as surprise_train_test_split
from surprise.model_selection import GridSearchCV
from surprise import accuracy

# --------------------------------------------
# Charger le dataset des interactions
interactions_df = pd.read_csv("interactions.csv")

# --------------------------------------------
# Préparer les données pour Surprise
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(interactions_df[['user_id', 'product_id', 'rating']], reader)

# --------------------------------------------
# Hyperparameter tuning avec GridSearchCV
param_grid = {
    'n_factors': [50, 100, 150],
    'n_epochs': [20, 30, 50],
    'lr_all': [0.002, 0.005, 0.01]
}

gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
gs.fit(data)

print("Best RMSE:", gs.best_score['rmse'])
print("Best Params:", gs.best_params['rmse'])

# --------------------------------------------
# MLflow experiment
mlflow.set_experiment("SVD_Recommendation_GridSearch")
with mlflow.start_run():

    best_params = gs.best_params['rmse']

    # Réentraîner le meilleur modèle sur tout le dataset
    best_model = SVD(**best_params)
    trainset = data.build_full_trainset()
    best_model.fit(trainset)

    # Tester le modèle sur un train-test split pour l'évaluation
    trainset_split, testset_split = surprise_train_test_split(data, test_size=0.2)
    predictions = best_model.test(testset_split)

    # Évaluation des performances
    rmse = accuracy.rmse(predictions)
    mae = accuracy.mae(predictions)

    # Log metrics dans MLflow
    mlflow.log_metric("RMSE", rmse)
    mlflow.log_metric("MAE", mae)
    mlflow.log_params(best_params)

    # --------------------------------------------
    # Sauvegarder le modèle dans le dossier 'model'
    os.makedirs('model', exist_ok=True)
    model_filename = os.path.join('model', 'svd_best_model.pkl')
    with open(model_filename, 'wb') as model_file:
        pickle.dump(best_model, model_file)

    # Log du modèle dans MLflow
    mlflow.sklearn.log_model(best_model, "svd_best_model")

    print(f"Best model saved to {model_filename}")

# --------------------------------------------
# Affichage du rapport de performance
performance_report = {'RMSE': rmse, 'MAE': mae}
print("Model Performance Report:")
for metric, score in performance_report.items():
    print(f"{metric}: {score:.4f}")

