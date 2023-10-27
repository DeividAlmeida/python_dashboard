import streamlit as st
import pandas as pd
import plotly.express as px
import re
st.set_page_config(layout="wide")
uploaded_file = st.file_uploader("Selecione um arquivo .xlsx", type="xlsx",)

def clean_string(string):
	if type(string) == str:
		string = re.sub(r"[^0-9]", "", string)
	return string

def data_cleaning(df):
	for i in range(0, len(df[df.columns[0]])):
		if type(df[df.columns[1]][i]) == str and re.search('[a-zA-Z]', df[df.columns[1]][i]) or type(df[df.columns[0]][i]) == str  and"Total" in  df[df.columns[0]][i]:
			df.loc[i, df.columns[0]] = ""
			df.loc[i, df.columns[1]] = 0
	df[df.columns[1]] = pd.to_datetime(df[df.columns[1]], format="mixed").dt.time
	df[df.columns[1]] = df[df.columns[1]].apply(lambda x: (x.hour * 3600 + x.minute * 60 + x.second) / 3600)
	return df

if uploaded_file is not None:
	df = pd.read_excel(uploaded_file, sheet_name=None, parse_dates=[1])
	selected_tab = st.sidebar.selectbox("Selecione um colaborador", df.keys())

	total_person = {}
	total_tasks = {}

	for person in df.keys():
		df[person] = data_cleaning(df[person])
		total = df[person][df[person].columns[1]].sum()
		dedicated = float(clean_string(df[person][df[person].columns[5]][1]))
		total_person[person] = [total, dedicated, dedicated - total]
		print()
		for i in range(len(df[person][df[person].columns[1]])):
			if df[person][df[person].columns[1]][i] not in total_tasks.keys():
				total_tasks[df[person][df[person].columns[0]][i]] = df[person][df[person].columns[1]][i]
			else:
				total_tasks[df[person][df[person].columns[0]][i]] += df[person][df[person].columns[1]][i]
	total_person = pd.DataFrame(total_person, index=["Horas Trabalhadas", "Horas Dedicadas", "Horas Livres"])
	total_person = total_person.sort_values(by=["Horas Livres"], axis=1, ascending=False)
	total_person
	total_tasks = pd.DataFrame.from_dict(total_tasks, orient="index", columns=["Tempo"])
	total_tasks = total_tasks.sort_values(by=[total_tasks.columns[0]], ascending=False)

	df[selected_tab] = df[selected_tab].sort_values(by=[df[selected_tab].columns[1]], ascending=False)
	col1, col2 = st.columns(2)

	total_person_tasks = px.bar(df[selected_tab], x=df[selected_tab].columns[0], y=df[selected_tab].columns[1], title="Atividade / Tempo - " + selected_tab)
	total_tasks = px.bar(total_tasks, x=total_tasks.index, y=total_tasks["Tempo"], title="Atividade / Tempo - Equipe")

	col2.plotly_chart(total_tasks, use_container_width=True)
	col1.plotly_chart(total_person_tasks, use_container_width=True)