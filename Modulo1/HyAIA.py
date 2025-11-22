import pandas as pd
import numpy as np
import string

class HyAIA:
    def __init__(self, df):
        self.data = df
        self.columns = df.columns
        
        self.data_binarios, self.binarios_columns = self.get_binarios()
        self.data_cuantitativos, self.cuantitativos_columns = self.get_cuantitativos()
        self.data_categoricos, self.categoricos_columns = self.get_categoricos()

        self.df_dqr = self.get_dqr()

    # --------- Identificación de variables ---------
    def get_binarios(self):
        col_bin = [col for col in self.data.columns if self.data[col].nunique() == 2]
        return self.data[col_bin], col_bin

    def get_cuantitativos(self):
        col_cuant = self.data.select_dtypes(include='number').columns
        return self.data[col_cuant], col_cuant

    def get_categoricos(self):
        col_cat = []
        cols = self.data.select_dtypes(exclude='number').columns
        for col in cols:
            if self.data[col].nunique() > 2:
                col_cat.append(col)
        return self.data[col_cat], col_cat

    # ---------------- REPORTE DQR ----------------
    def get_dqr(self):

    columns = pd.DataFrame(list(self.data.columns.values),
                           columns=['Columns_Names'],
                           index=list(self.data.columns.values))

    data_dtypes = pd.DataFrame(self.data.dtypes, columns=['Dtypes'])

    present_values = pd.DataFrame(self.data.count(), columns=['Present_values'])

    missing_values = pd.DataFrame(self.data.isnull().sum(), columns=['Missing_values'])

    unique_values = pd.DataFrame(columns=['Unique_values'])
    for col in list(self.data.columns.values):
        unique_values.loc[col] = [self.data[col].nunique()]

    # Columna booleana Is_Categorical
    is_categorical = pd.DataFrame(columns=['Is_Categorical'])
    for col in self.data.columns:
        is_categorical.loc[col] = [self.data[col].dtype == 'object']

    # Columna Categories
    categories = pd.DataFrame(columns=['Categories'])
    for col in self.data.columns:
        if is_categorical.loc[col].values[0] == True:  # solo categóricas
            if unique_values.loc[col].values[0] <= 10:  # solo si <= 10 categorías
                categories.loc[col] = [list(self.data[col].dropna().unique())]
            else:
                categories.loc[col] = ['>10 categorías']
        else:
            categories.loc[col] = ['N/A']

    # Máximos
    max_values = pd.DataFrame(columns=['Max_Values'])
    for col in self.data.columns:
        try:
            max_values.loc[col] = [self.data[col].max()]
        except:
            max_values.loc[col] = ['N/A']

    # Mínimos
    min_values = pd.DataFrame(columns=['Min_Values'])
    for col in self.data.columns:
        try:
            min_values.loc[col] = [self.data[col].min()]
        except:
            min_values.loc[col] = ['N/A']

    # Desviación estándar
    std_values = pd.DataFrame(self.data.std(numeric_only=True), columns=['Std'])

    # Media
    mean_values = pd.DataFrame(self.data.mean(numeric_only=True), columns=['Mean'])

    # Percentiles
    percentiles = self.data.quantile([0.25, 0.5, 0.75], numeric_only=True).transpose()
    percentiles.columns = ['P25', 'P50', 'P75']

    return (columns
            .join(data_dtypes)
            .join(present_values)
            .join(missing_values)
            .join(unique_values)
            .join(is_categorical)
            .join(categories)
            .join(max_values)
            .join(min_values)
            .join(std_values)
            .join(mean_values)
            .join(percentiles))