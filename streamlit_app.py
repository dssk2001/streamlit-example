import streamlit as st
import pandas as pd
import seaborn as sns

#configs

st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    global df
    st.title("EDA for Dataset with streamlit")
    st.header("Start by Uploading your file and selecting various options to explore data")
    st.sidebar.subheader("File Uploading Options")

    data = st.sidebar.file_uploader(label="Upload only csv files",type=['csv'])
    if(data) is not None:
        df = pd.read_csv(data)
        
    # Viewing Rows
    st.subheader("See rows of data")
    if(st.checkbox('See Rows')):
        st.header("Data Rows")
        rows = st.number_input("Number of rows to view from head:",value=5)
        st.dataframe(df.head(rows))

    # Viewing Columns
    st.subheader("View Columns")
    cols = st.checkbox("Column Names")
    if(cols):
        st.header("Columns Data")
        st.write(df.columns)

    # Viewing Dimensions
    st.subheader("View Dimensions")
    dims = st.checkbox("Show Dimensions")
    if(dims):
        st.write("Dimensions")
        st.write(f"Rows:{df.shape[0]},Columns:{df.shape[1]}")

    st.subheader("Columns show")
    if st.checkbox("Select Columns To Show"):
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect("Select", all_columns)
        new_df = df[selected_columns]
        st.dataframe(new_df)

        # Show Values
    st.subheader("Counts of classes")
    if st.button("Value Counts"):
        st.text("Value Counts By Target/Class")
        st.write(df.iloc[:, -1].value_counts())

        # Show Datatypes
    st.subheader("See Data Types")
    if st.button("Data Types"):
        st.write(df.dtypes)

        # Show Summary
    st.subheader("Summary of Dataset")
    summary_box = st.checkbox("Summary")
    if summary_box:
        st.write(df.describe())

    st.sidebar.subheader("Data Visualization")
    # Correlation Seaborn Plot
    if st.sidebar.checkbox("Correlation Plot[Seaborn]"):
        st.write(sns.heatmap(df.corr(), annot=True))
        st.pyplot()

    # Pie Chart
    if st.sidebar.checkbox("Pie Plot"):
        all_columns_names = df.columns.tolist()
        if st.sidebar.button("Generate Pie Plot"):
            st.success("Generating A Pie Plot")
            st.write(df.iloc[:, -1].value_counts().plot.pie(autopct="%1.1f%%"))
            st.pyplot()

    # Count Plot
    if st.sidebar.checkbox("Plot of Value Counts"):
        st.text("Value Counts By Target")
        all_columns_names = df.columns.tolist()
        primary_col = st.selectbox("Primary Columm to GroupBy", all_columns_names)
        selected_columns_names = st.multiselect("Select Columns", all_columns_names)
        if st.sidebar.button("Plot"):
            st.text("Generate Plot")
            if selected_columns_names:
                vc_plot = df.groupby(primary_col)[selected_columns_names].count()
            else:
                vc_plot = df.iloc[:, -1].value_counts()
            st.write(vc_plot.plot(kind="bar"))
            st.pyplot()
    
    #own Customizable Plots
    st.subheader("Customizable Plot")
    try:
        all_columns_names = df.columns.tolist()
        type_of_plot = st.selectbox("Select Type of Plot", ["area", "bar", "line", "hist", "box", "kde","scatter"])
        selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names)
        if st.button("Generate Plot"):
            st.success("Generating Plot of {} for {}".format(type_of_plot, selected_columns_names))
            cust_plot = df[selected_columns_names].plot(kind=type_of_plot)
            st.write(cust_plot)
            st.pyplot()
    except:
        pass
if __name__ == '__main__':
    main()
