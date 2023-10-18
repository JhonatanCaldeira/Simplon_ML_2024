from components.mymodule import my_sum, my_concatenate
from components.data_sc import data_load, data_clean_up, data_write_to_csv, DATA_FILE_IN
from components.create_model import preprocessing_model, svc_model, DATA_FILE

# print(my_sum(1,2,3,4,5))

# print(my_concatenate(prenom='Jhonatan',nom='Caldeira'))

df_titanic = data_load(DATA_FILE_IN)
df_titanic = data_clean_up(df_titanic)
data_write_to_csv(df_titanic)

df_titanic = data_load(DATA_FILE)
preprocessing_model(df_titanic)
svc_model()