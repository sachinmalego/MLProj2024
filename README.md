# MLProj2024
Air Quality Index Prediction ML2024 Project



# recent update Nov 13
* added model_valid notebook under .devcontainer/notebook/Models
* added model in model folder 
* added source code under src imputer and preprocessing

* for prepocessing each file will be read and cleaned (use the object for further feature Engineering)
* for feature engineering merging , temporal, weather, rain, traffic , misc features are added
* for imputation we have prophet model, knn imputer, mice iterable imputer from sklearn, then basic imputaion like exponential smoothning, bfill, ffill
* Current model is xgbm note that model could overfit if you can try to test on your sample
* current version does not take care of classes for extreme AQI 



# recent updates
*  added two notebooks under eda crawl.ipynb, vis_traffic.pynb
*  added two scripts file one under experiment in .devcontiner spacial_temporal_permutaion
*  another is to perform preprocssing i.e getting traffic and fire data from traffic_process.py

#do not need to run traff_parse.py file as it needed once only
#for traffic_process.py you need run for your locations and merge everything at vis_traffic.py



