import pandas as pd
import numpy as np
from datetime import timedelta
import re 

def load_main(filename):
	'''Loads main df_main for the charts

	   Params:
	   filename: str, the name of the csv file containing df_main

	   Returns:
	   df_main: df_mainframe
	'''

	# loading df_main
	df_main = pd.read_csv(filename)
	df_main['Time'] = pd.to_datetime(df_main['Time'])
	df_main.sort_values('Time', ascending=True, inplace=True)

	temp_cols = [col for col in df_main.columns if col != 'Time']

	error_values = list(
		set(
			[df_main[col].iloc[i] 
			 for col in temp_cols 
			 for i in range(df_main.shape[0]) 
			 if len(re.findall(r'\d+', str(df_main[col].iloc[i])))==0]
		)
	)

	# for i_error in error_values:
	# 	df_main.replace(i_error, np.nan, inplace=True)
	df_main.replace(error_values, np.nan, inplace=True)
	df_main.fillna(method='ffill', inplace=True)
	# df_main.replace('ERROR', np.nan, inplace=True)
	# df_main.replace('#VALUE!', np.nan, inplace=True)
	# col_names_change_type = [col for col in df_main if col!='Time']
	# df_main = df_main.astype(
	# 	{
	# 		col: int if col=="Frequency; Hz" else float for col in col_names_change_type
	# 	}
	# )
	#df_main = df_main.convert_dtypes()

	for col in df_main.columns:
		if col == 'Time':
			pass
		elif col == "Frequency; Hz":
			df_main[col] = df_main[col].astype(int)
		else:
			df_main[col] = df_main[col].astype(float)

	df_main['Flow error; %'] = 100 * df_main['Flow error; %']
	df_main['Pump efficiency; %'] = 100 * df_main['Pump efficiency; %']
	df_main['Pump efficiency optimal; %'] = 100 * df_main['Pump efficiency optimal; %']
	df_main['Saving potential; %'] = 100 * df_main['Saving potential; %']

	# # specifying some parameters
	# Voltage = 690
	# # Power factor cos φ
	# Power_factor_cos_phi = 0.9

	# # calculating some values for chart 1
	# df_main['Mechanical power - measured; kW'] = df_main['PEN5 A'] * \
	#                                              (1.73 * (Voltage / 1000) * \
	#                                              Power_factor_cos_phi)

	# # calculating some values for chart 3
	# df_main['Head; mH2O'] = ((df_main['PEN5 P2 bar'] - df_main['PEN4 P2 bar']) * \
	#                         101325 / 1000) / (955 * 9.81) *1000

	# # calculating some values for table
	# df_main['Flow error; %'] = 100 * (df_main['Pump flow according to P; m3/h'] - \
	# 	                              df_main['Pump flow according to H; m3/h']) / \
	# 	                       df_main['Pump flow according to P; m3/h']

	# df_main['Pump efficiency; %'] = 100 * df_main['Pump hydraulic power; kW'] / \
	#                                 df_main['Mechanical power - measured; kW']

	# df_main['Specific energy consumption; kW/m3/h'] = df_main['Mechanical power - measured; kW'] / \
	#                                                   df_main['Pump flow according to H; m3/h']

	# df_main['Specific energy consumption - optimum; kW/m3/h'] = df_main['Power mechanical according Head; kW'] / \
	#                                                             df_main['Pump flow according to H; m3/h']

	# df_main['Mechanical power optimum'] = df_main['Power mechanical according Head; kW'].copy()

	# # calculating some values for KPI
	# df_main['Pump efficiency optimal; %'] = 100* df_main['Pump hydraulic power; kW'] / \
	#                                         df_main['Power mechanical according Head; kW']

 # 	# calculating saving potential
	# df_main['Saving potential; %'] = 100 * (df_main['Mechanical power - measured; kW'] - \
	# 	                                    df_main['Power mechanical according Head; kW']) / \
	#                                  df_main['Mechanical power - measured; kW']

	return df_main


def calculate_kpi(df):
	'''Calculates KPI values

	   Params:
	   df: df_mainframe containing the df_main

	   Returns:
	   kpi_dict: dictionary, contains kpi values
	'''
	kpi_dict = {}

	kpi_dict['POWER USAGE AVERAGE; kW'] = df['Mechanical power - measured; kW'].mean()
	temp_average = df['Power mechanical according Head; kW'].mean()
	kpi_dict['POWER USAGE DIFFERENCE; kW'] = 100 * (kpi_dict['POWER USAGE AVERAGE; kW'] - \
	                                                temp_average) / \
	                                         kpi_dict['POWER USAGE AVERAGE; kW']

	kpi_dict['AVERAGE EFFICIENCY'] = df['Pump efficiency; %'].mean()
	temp_opt1 = df['Pump efficiency optimal; %'].mean()
	kpi_dict['PER CENT POINTS BELOW OPTIMUM'] = (temp_opt1 - kpi_dict['AVERAGE EFFICIENCY'])

	kpi_dict['AVERAGE SPECIFIC ENERGY CONSUMPTION'] = df['Specific energy consumption; kW/m3/h'].mean()
	temp_opt2 = df['Specific energy consumption - optimum; kW/m3/h'].mean()
	kpi_dict['PER CENT BELOW OPTIMUM'] = 100 * (temp_opt2 - \
	                                            kpi_dict['AVERAGE SPECIFIC ENERGY CONSUMPTION']) /\
	                                     temp_opt2

	return kpi_dict


def create_summary_table(df_main, df_period):
	'''Creates the summary table

	   Params:
	   df_main: dataframe, contains all available data for the table values' calculation
	   df_period: dataframe, the same as the df_main but for a specified period

	   Returns
	   table_df: dataframe, contains summarized values
	'''
	start_last_24h = df_main['Time'].iloc[-1] - timedelta(days=1)
	start_last_week = df_main['Time'].iloc[-1] - timedelta(days=7)

	average_last_24h = df_main[df_main['Time']>=start_last_24h][['Pump flow according to H; m3/h', 
		                                                         'Head; mH2O',
		                                                         'Mechanical power - measured; kW',
		                                                         'Pump efficiency; %',
		                                                         'Specific energy consumption; kW/m3/h',
		                                                         'Mechanical power optimum',
		                                                         'Specific energy consumption - optimum; kW/m3/h',
		                                                         'Flow error; %']].mean(axis=0)

	average_last_week = df_main[df_main['Time']>=start_last_week][['Pump flow according to H; m3/h', 
		                                                           'Head; mH2O',
		                                                           'Mechanical power - measured; kW',
		                                                           'Pump efficiency; %',
		                                                           'Specific energy consumption; kW/m3/h',
		                                                           'Mechanical power optimum',
		                                                           'Specific energy consumption - optimum; kW/m3/h',
		                                                           'Flow error; %']].mean(axis=0)

	average_last_period = df_period[['Pump flow according to H; m3/h', 
	                                 'Head; mH2O',
	                                 'Mechanical power - measured; kW',
	                                 'Pump efficiency; %',
	                                 'Specific energy consumption; kW/m3/h',
	                                 'Mechanical power optimum',
	                                 'Specific energy consumption - optimum; kW/m3/h',
	                                 'Flow error; %']].mean(axis=0)

	name_index_list = ['Flow', 'Head', 'Mechanical power measured',
	                   'Efficiency measured', 'Specific energy measured',
	                   'Mechanical power optimum', 'Specific energy optimum',
	                   'Flow error']

	measure_index_list = ['m3/h', 'H2O', 'kW', '%', 'kW/m3/h',
	                      'kW', 'kW/m3/h', '%']

	table_df = pd.DataFrame()
	table_df[''] = name_index_list
	table_df[' '] = measure_index_list
	table_df['Average last 24H'] = np.round(average_last_24h.values, 2)
	table_df['Average last week'] = np.round(average_last_week.values, 2)
	table_df['Average last period'] = np.round(average_last_period.values, 2)

	return table_df