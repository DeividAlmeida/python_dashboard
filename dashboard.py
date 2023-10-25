import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide")

uploaded_file = st.file_uploader("Selecione um arquivo .xlsx", type="xlsx")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name=None, parse_dates=['Tempo'], date_parser=lambda x: pd.to_timedelta(x) )
    selected_tab = st.sidebar.selectbox("Selecione um colaborador", df.keys())

    total_person = {}
    total_tasks = {}

    for person in df.keys():
        df[person]['Tempo'] = df[person]['Tempo'].apply(lambda x: x.total_seconds() / 3600)
        total = df[person]['Tempo'].sum()
        dedicated = df[person]["Unnamed: 5"][1]
        total_person[person] = [total, dedicated, dedicated - total]
        for i in range(len(df[person]['Tarefas'])):
            if df[person]['Tarefas'][i] not in total_tasks.keys():
                total_tasks[df[person]['Tarefas'][i]] = df[person]['Tempo'][i]
            else:
                total_tasks[df[person]['Tarefas'][i]] += df[person]['Tempo'][i]
    total_person = pd.DataFrame(total_person, index=['Horas Trabalhadas', 'Horas Dedicadas', 'Horas Livres'])
    total_person = total_person.sort_values(by=['Horas Trabalhadas'], axis=1, ascending=False)
    total_person

    total_tasks = pd.DataFrame.from_dict(total_tasks, orient='index', columns=['Tempo'])
    total_tasks = total_tasks.sort_values(by=['Tempo'], ascending=False)

    df[selected_tab] = df[selected_tab].sort_values(by=['Tempo'], ascending=False)

    col1, col2 = st.columns(2)

    total_person_tasks = px.bar(df[selected_tab], x="Tarefas", y="Tempo", title="Atividade / Tempo - " + selected_tab)
    total_tasks = px.bar(total_tasks, x=total_tasks.index, y=total_tasks['Tempo'], title="Atividade / Tempo - Equipe")

    col2.plotly_chart(total_tasks, use_container_width=True)
    col1.plotly_chart(total_person_tasks, use_container_width=True)