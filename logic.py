import pandas as pd

FILE_PATH = "test.xlsx"
FIELDS_ORDER = ("s_code", "i_doctor", "i_med_entity", "s_pin_patient", "i_icd", "i_generic", "d_start")

def read_data():
    try:
        df = pd.read_excel(FILE_PATH, dtype=str)
        df['d_start'] = df['d_start'].str.strip('"').str.strip()
        df['d_start'] = pd.to_datetime(df['d_start'], errors='coerce')
        df = df.dropna(subset=['d_start'])
        return df
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return pd.DataFrame(columns=FIELDS_ORDER)

def static_pharm():
    df = read_data()
    if df.empty:
        return []

    grouped = df.groupby('i_med_entity').agg(
        total_prescriptions=pd.NamedAgg(column='s_code', aggfunc='count'),
        unique_patients=pd.NamedAgg(column='s_pin_patient', aggfunc=pd.Series.nunique)
    )
    grouped['Среднее рецептов на пациента'] = (grouped['total_prescriptions'] / grouped['unique_patients']).round(1)
    result = grouped.reset_index()
    return result[['i_med_entity', 'total_prescriptions', 'unique_patients', 'Среднее рецептов на пациента']].values.tolist()

def static_doc():
    df = read_data()
    if df.empty:
        return [], []

    suspicious = []
    suspicious_doctors = {}
    repeat_counter = {}

    grouped = df.groupby(['i_doctor', 'i_icd', 'i_generic'])

    for (doctor, icd, generic), group in grouped:
        group = group.sort_values('d_start')
        dates = group['d_start'].tolist()
        indices = group.index.tolist()
        repeat_count_for_this_group = 0

        for i in range(len(dates) - 1):
            delta_seconds = (dates[i + 1] - dates[i]).total_seconds()
            if 0 < delta_seconds <= 3600:
                suspicious.append(df.loc[indices[i], list(FIELDS_ORDER)].tolist())
                suspicious.append(df.loc[indices[i + 1], list(FIELDS_ORDER)].tolist())

                if doctor not in suspicious_doctors:
                    suspicious_doctors[doctor] = set()
                suspicious_doctors[doctor].add(generic)
                repeat_count_for_this_group += 1

        if repeat_count_for_this_group > 0:
            if (doctor, generic) not in repeat_counter:
                repeat_counter[(doctor, generic)] = 0
            repeat_counter[(doctor, generic)] += repeat_count_for_this_group

    seen = set()
    unique_suspicious = []
    for row in suspicious:
        row_tuple = tuple(row)
        if row_tuple not in seen:
            seen.add(row_tuple)
            unique_suspicious.append(row)

    suspicious_summary = []
    for doctor, drugs_set in suspicious_doctors.items():
        count_drugs = len(drugs_set)
        count_prescriptions = sum(1 for row in unique_suspicious if row[1] == doctor)
        total_repeats = sum(repeat_counter.get((doctor, drug), 0) for drug in drugs_set)
        suspicious_summary.append([doctor, count_drugs, count_prescriptions, total_repeats])

    suspicious_summary.sort(key=lambda x: x[3], reverse=True)
    return unique_suspicious, suspicious_summary

def doc():
    df = read_data()
    if df.empty:
        return []

    top_drugs = df.groupby('i_generic').size().reset_index(name='Количество назначений')
    top_drugs = top_drugs.sort_values('Количество назначений', ascending=False).head(20)
    return top_drugs.values.tolist()

def diagnosis_analysis():
    df = read_data()
    if df.empty:
        return []

    diagnosis_count = df.groupby('i_icd').size().reset_index(name='Количество')
    diagnosis_count = diagnosis_count.sort_values('Количество', ascending=False).head(20)
    return diagnosis_count.values.tolist()

def overall_dynamics():
    df = read_data()
    if df.empty:
        return []

    df['date'] = df['d_start'].dt.date
    daily_counts = df.groupby('date').size().reset_index(name='Количество рецептов')
    daily_counts = daily_counts.sort_values('date')
    return daily_counts.values.tolist()

def generate_report():
    print("Отчет успешно создан!") # тут пока что типа заглушка
