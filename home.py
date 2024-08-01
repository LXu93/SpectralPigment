import os

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import openpyxl
from openpyxl_image_loader import SheetImageLoader

# Define constant
# Website modes
MODES = ('Single pigment', 'Comparison', 'Show texture images')

class Pigment_attribute():
    def __init__(self, column_name, value) -> None:
        self.column_name = column_name
        self.value = value

def query_pigment(df, pigment_attributes):
    res = df
    for attribute in pigment_attributes:
        if attribute.value is not None:
            res = res[res[attribute.column_name] == attribute.value]
    return res

def format_display(label):
    if label == None:
        return "any"
    else:
        return label
    
def plot(selected_names, view_angle="45"):
    folder_path = "Data/MA-T12 data/"
    extension = ".xlsx"
    
    color_file_path = "Data/colors.csv"
    all_cols = pd.read_csv(color_file_path, usecols=[0, 1, 5, 6, 7], header=0)
    

    fig = go.Figure()
    fig.update_layout(
                xaxis_title='Wavelength (in nanometer)',
                yaxis_title='Reflectance',
            )  
    
    if selected_names:
        if st.session_state.mode == MODES[0]:
            name = selected_names[-1]
            file_name = name + extension
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_excel(file_path, sheet_name='Spectral Data', usecols="C:AH", skiprows=2, header=0, index_col=0)
            df = df.transpose()
            
            columns = df.columns
            if view_angle == "15":
                columns = df.columns[0:6]
            if view_angle == "45":
                columns = df.columns[6:12]

            cols = all_cols[all_cols["Name"] == name]

            for column in columns:
                v_angle = int(column.split('as')[0])
                i_angle = int(column.split('as')[1])-int(column.split('as')[0])
                curve_name = "v: " + str(v_angle) + " i: " + str(i_angle)
                r = cols[cols['Geometry'] == column]['r'].values[0]
                g = cols[cols['Geometry'] == column]['g'].values[0]
                b = cols[cols['Geometry'] == column]['b'].values[0]
                col = 'rgb(' + str(r) + ',' + str(g) + ',' + str(b)  + ')'
                trace = go.Scatter(x=df.index, y=df[column], line=dict(color = col),mode='lines', name=curve_name)
                fig.add_trace(trace)
        
            fig.update_layout(
                legend_title='Illumination & view angles',
                title= f'Pigament: {name}'
            )

        if st.session_state.mode == MODES[1]:
            for name in selected_names:
                file_name = name + extension
                file_path = os.path.join(folder_path, file_name)
                df = pd.read_excel(file_path, sheet_name='Spectral Data', usecols="C:AH", skiprows=2, header=0, index_col=0)
                df = df.transpose()
            
                cols = all_cols[all_cols["Name"] == name]
                r = cols[cols['Geometry'] == "45as45"]['r'].values[0]
                g = cols[cols['Geometry'] == "45as45"]['g'].values[0]
                b = cols[cols['Geometry'] == "45as45"]['b'].values[0]
                col = 'rgb(' + str(r) + ',' + str(g) + ',' + str(b)  + ')'

                trace = go.Scatter(x=df.index, y=df["45as45"], line=dict(color = col), mode='lines', name=name)
                fig.add_trace(trace)
        
            fig.update_layout(
                legend_title='Pigment name'
            )
  
    st.plotly_chart(fig)

def show_texture(name):
    folder_path = "Data/MA-T12 data/"
    extension = ".xlsx"
    file_name = name + extension
    file_path = os.path.join(folder_path, file_name)

    cells = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']  
    sheet_name = "Texture Images"

    pxl_doc = openpyxl.load_workbook(file_path)
    sheet = pxl_doc[sheet_name]

    image_loader = SheetImageLoader(sheet)
    images = []
    caption_cells = sheet['A2:A7']
    captions = []
    for cell in caption_cells:
        captions.append(cell[0].value)

    for cell in cells:
        image = image_loader.get(cell)
        image = np.asarray(image)
        images.append(image)

    cols = st.columns(3)
    for i in range(0,3):
        cols[i].image(image=images[i],caption=captions[i])
        cols[i].image(image=images[i+3],caption=captions[i+3])

def clear_selected_names():
    if "p_list_multi" in st.session_state:
        st.session_state.p_list_multi['Select?'] = False
    st.session_state.selected_names = []

def single_selection_list(pigment_list):
    display_list = st.dataframe(pigment_list, on_select="rerun", selection_mode="single-row", hide_index=True, use_container_width=True)
    selected_names = pigment_list.iloc[display_list.selection["rows"]]["Name"].tolist()
    if selected_names:
        st.session_state.selected_names = selected_names
    return display_list

def multi_selection_list(pigment_list):
    display_list = st.data_editor(pigment_list, disabled=pigment_list.columns[1:], hide_index=True, use_container_width=True)
    st.session_state.p_list_multi.update(display_list)
    st.session_state.selected_names = st.session_state.p_list_multi[st.session_state.p_list_multi['Select?'] == True]['Name'].tolist() 
    return display_list  

def main():
    list_path = 'Data/pigment_list.csv'
    p_list = pd.read_csv(list_path)
    p_list['Number of Layers'] = p_list['Number of Layers'].astype(str)
   
    if "selected_names" not in st.session_state:
        st.session_state.selected_names = list()
    
    st.title("Spectral Pigment (This is title)")
    with st.sidebar:
        st.header("Configuration")
        st.session_state.mode = st.sidebar.selectbox('Choose mode:', MODES, on_change=clear_selected_names)
        if st.session_state.mode == MODES[0]:
            st.session_state.view_angle = st.sidebar.selectbox(
                "View angle",
                ("15", "45",None),
                index= 0,
                format_func= format_display,                
            )
            
        if st.session_state.mode == MODES[1]:
            st.button("reset slection", on_click=clear_selected_names)
    
    st.markdown("description")
    plot_area = st.empty()
    st.markdown("description")
    pigment_option1, pigment_option2, pigment_option3, pigment_option4, pigment_option5 = st.columns(5)
    list_area = st.empty()

    
    with pigment_option1:
        marble_value = st.selectbox(
            "Marble",
            ("Pentelic marble", "Paros", None),
            index= 2,
            format_func= format_display,
        )

    with pigment_option2:
        binder_value = st.selectbox(
            "Binder",
            ("Punic wax", "Egg white",None),
            index= 2,
            format_func= format_display,
        )

    with pigment_option3:
        pigment_value = st.selectbox(
            "Pigment",
            ("Red lake", "Cinnabar", "Egyptian blue", None),
            index= 3,
            format_func= format_display,
        )

    with pigment_option4:
        ground_value = st.selectbox(
            "Ground",
            ("Lead white", "Calcium carbonate", "Mixed calcite", "No ground",None),
            index= 3,
            format_func= format_display,
        )

    with pigment_option5:
        nlayers_value = st.selectbox(
            "Layer numbers",
            ("1", "2", "3", None),
            index= 3,
            format_func= format_display,
        )

    marble = Pigment_attribute("Marble", marble_value)
    binder = Pigment_attribute("Binder", binder_value)
    pigment = Pigment_attribute("Pigment", pigment_value)
    ground = Pigment_attribute("Ground", ground_value)
    nlayers = Pigment_attribute("Number of Layers", nlayers_value)
    pigment_attributes = [marble, binder, pigment, ground, nlayers]
    
    if st.session_state.mode == MODES[0]:
        with list_area:
            queried_pigments = query_pigment(p_list, pigment_attributes)
            single_selection_list(queried_pigments)
        
        with plot_area:
            plot(st.session_state.selected_names, st.session_state.view_angle)
        
    elif st.session_state.mode == MODES[1]:
        if 'p_list_multi' not in st.session_state:
            st.session_state.p_list_multi = p_list
            st.session_state.p_list_multi.insert(0, 'Select?', False)
        
        with list_area:
            queried_pigments = query_pigment(st.session_state.p_list_multi, pigment_attributes)
            multi_selection_list(queried_pigments)
    
        with plot_area:
            plot(st.session_state.selected_names)
        st.session_state.selected_names
    

    elif st.session_state.mode == MODES[2]:
        with list_area:
            queried_pigments = query_pigment(p_list, pigment_attributes)
            single_selection_list(queried_pigments) 
        
        if st.session_state.selected_names:
            with plot_area:
                show_texture(st.session_state.selected_names[-1])


if __name__ == "__main__":
    st.set_page_config(
        page_title='Pigment Spectral',
        layout="wide",
        initial_sidebar_state="expanded",
    )
    main()






