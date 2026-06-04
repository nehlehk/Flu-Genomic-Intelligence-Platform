import mlflow

def log_experiment(subtype, prior_mean, prior_sd, mae, rmse, coverage, anomaly_count):
    
    run_name = f"{subtype}_Bayesian_Gaussian_Model"
    with mlflow.start_run(run_name=run_name):
        mlflow.log_param( "model_type", "bayesian_gaussian" )

        mlflow.log_param("subtype",subtype)    

        mlflow.log_param("prior_mean",prior_mean)

        mlflow.log_param( "prior_sd", prior_sd)

        mlflow.log_metric("MAE", mae)

        mlflow.log_metric("RMSE", rmse)

        mlflow.log_metric("Coverage", coverage)

        mlflow.log_metric( "Anomaly_Count", anomaly_count)