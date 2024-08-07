import os

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import openpyxl
from openpyxl_image_loader import SheetImageLoader

# Define constant
# Website modes
MODES = ("Single pigment", "Comparison", "Show texture images")
COLORMODES = ("Corresponding color mode", "Distinct mode")
MARBLES = ("Pentelic marble", "Paros", None)
BINDERS = ("Punic wax", "Egg white",None)
PIGMENTS = ("Red lake", "Cinnabar", "Egyptian blue", None)
GROUNDS = ("Lead white", "Calcium carbonate", "Mixed calcite", "No ground",None)
NLAYERS = ("1", "2", "3", None)


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
    
    if st.session_state.color_mode == COLORMODES[0]:
        color_file_path = "Data/colors.csv"
        all_cols = pd.read_csv(color_file_path, usecols=[0, 1, 5, 6, 7], header=0)
    

    fig = go.Figure()
    fig.update_layout(
                xaxis_title='Wavelength (in nanometer)',
                yaxis_title='Reflectance',
            )  
    
    if selected_names:
        if st.session_state.mode == MODES[0]:
            name = selected_names.pop()
            selected_names.add(name)
            file_name = name + extension
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_excel(file_path, sheet_name='Spectral Data', usecols="C:AH", skiprows=2, header=0, index_col=0)
            df = df.transpose()
            
            columns = df.columns
            if view_angle == "15":
                columns = df.columns[0:6]
            if view_angle == "45":
                columns = df.columns[6:12]

            for column in columns:
                v_angle = int(column.split('as')[0])
                i_angle = int(column.split('as')[1])-int(column.split('as')[0])
                curve_name = "v: " + str(v_angle) + " i: " + str(i_angle)
               
                if st.session_state.color_mode == COLORMODES[0]:
                    cols = all_cols[all_cols["Name"] == name]
                    r = cols[cols['Geometry'] == column]['r'].values[0]
                    g = cols[cols['Geometry'] == column]['g'].values[0]
                    b = cols[cols['Geometry'] == column]['b'].values[0]
                    col = 'rgb(' + str(r) + ',' + str(g) + ',' + str(b)  + ')'
                    trace = go.Scatter(x=df.index, y=df[column], line=dict(color = col),mode='lines', name=curve_name)
                if st.session_state.color_mode == COLORMODES[1]:
                    trace = go.Scatter(x=df.index, y=df[column], mode='lines', name=curve_name)
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
                if st.session_state.color_mode == COLORMODES[0]:
                    cols = all_cols[all_cols["Name"] == name]
                    r = cols[cols['Geometry'] == "45as45"]['r'].values[0]
                    g = cols[cols['Geometry'] == "45as45"]['g'].values[0]
                    b = cols[cols['Geometry'] == "45as45"]['b'].values[0]
                    col = 'rgb(' + str(r) + ',' + str(g) + ',' + str(b)  + ')'
                    trace = go.Scatter(x=df.index, y=df["45as45"], line=dict(color = col), mode='lines', name=name)
                if st.session_state.color_mode == COLORMODES[1]:
                    trace = go.Scatter(x=df.index, y=df["45as45"], mode='lines', name=name)

                
                fig.add_trace(trace)
        
            fig.update_layout(
                legend_title='Pigment name'
            )
  
    st.plotly_chart(fig)

def show_texture(names):
    name = names.pop()
    names.add(name)
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

def get_download_data(names):
    folder_path = "Data/MA-T12 data/"
    extension = ".xlsx"

    dfs = []
    for name in names:
        file_name = name + extension
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_excel(file_path, sheet_name='Spectral Data', usecols="A,C:AH", skiprows=2, header=0, index_col=None)
        dfs.append(df)
    data = pd.concat(dfs)
    data = data.to_csv(index=False).encode('utf-8')
    return data

def single_selection_list(pigment_list):
    display_list = st.dataframe(pigment_list, on_select="rerun", selection_mode="single-row", hide_index=True, use_container_width=True)
    selected_names = pigment_list.iloc[display_list.selection["rows"]]["Name"].tolist()
    if selected_names:
        st.session_state.selected_names = set(selected_names)
    return display_list

def update_selection():
    st.session_state.p_list_multi.update(st.session_state.display_list_edited)

def sync_selection():
    if "p_list_multi" in st.session_state:
        st.session_state.display_list = st.session_state.p_list_multi.copy()

def clear_selected_names(): 
    if 'display_list' in st.session_state:
        st.session_state.display_list['Select?'] = False
    if 'display_list_edited' in st.session_state:
        st.session_state.display_list_edited['Select?'] = False
    if "p_list_multi" in st.session_state:
        st.session_state.p_list_multi['Select?'] = False
        sync_selection()
    st.session_state.selected_names = set()


def multi_selection_list(pigment_list):
    st.session_state.display_list_edited = st.data_editor(pigment_list, disabled=pigment_list.columns[1:], hide_index=True, use_container_width=True)
    st.session_state.p_list_multi.update(st.session_state.display_list_edited)
    st.session_state.selected_names = set(st.session_state.p_list_multi[st.session_state.p_list_multi['Select?'] == True]['Name'].tolist())

def all_selected():
    st.session_state.display_list = st.session_state.p_list_multi[st.session_state.p_list_multi['Select?'] == True]

def reset_query_conditions():
    st.session_state.marble = MARBLES[-1]
    st.session_state.binder = BINDERS[-1]
    st.session_state.pigment = PIGMENTS[-1]
    st.session_state.ground = GROUNDS[-1]
    st.session_state.nlayers = NLAYERS[-1]


def main():
    list_path = 'Data/pigment_list.csv'
    p_list = pd.read_csv(list_path)
    p_list['Number of Layers'] = p_list['Number of Layers'].astype(str)
   
    if "selected_names" not in st.session_state:
        st.session_state.selected_names = set()
    
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

        if st.session_state.mode is not MODES[2]:
            st.session_state.color_mode = st.radio("Select plot color mode",COLORMODES)

    st.markdown("description")
    plot_area = st.empty()
    st.markdown("description")
    pigment_option1, pigment_option2, pigment_option3, pigment_option4, pigment_option5 = st.columns(5)
    reset_button_area, download_button_area, _ = st.columns([1,2,4])
    reset_button_area.button("reset query", on_click=reset_query_conditions)
    if st.session_state.mode == MODES[1]:
        col1, col2, _= st.columns([2,2,4])
        on_only = col1.toggle("display selected only", on_change=sync_selection)
        if on_only:
            all_selected()
        col2.button("reset slection", on_click=clear_selected_names)
    list_area = st.empty()

    
    with pigment_option1:
        marble_value = st.selectbox(
            "Marble",
            MARBLES,
            index= 2,
            format_func= format_display,
            on_change=sync_selection,
            key="marble",
            placeholder="any"
        )

    with pigment_option2:
        binder_value = st.selectbox(
            "Binder",
            BINDERS,
            index= 2,
            format_func= format_display,
            on_change=sync_selection,
            key="binder",
            placeholder="any"
        )

    with pigment_option3:
        pigment_value = st.selectbox(
            "Pigment",
            PIGMENTS,
            index= 3,
            format_func= format_display,
            on_change=sync_selection,
            key="pigment",
            placeholder="any"
        )

    with pigment_option4:
        ground_value = st.selectbox(
            "Ground",
            GROUNDS,
            index= 4,
            format_func= format_display,
            on_change=sync_selection,
            key="ground",
            placeholder="any"
        )

    with pigment_option5:
        nlayers_value = st.selectbox(
            "Layer numbers",
            NLAYERS,
            index= 3,
            format_func= format_display,
            on_change=sync_selection,
            key="nlayers",
            placeholder="any"
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
        
        if st.session_state.selected_names:
            data = get_download_data(st.session_state.selected_names)
            with download_button_area:
                st.download_button( label='Download spectra as CSV', data=data, file_name='spectra.csv', mime='text/csv')
        
    elif st.session_state.mode == MODES[1]:
        if 'p_list_multi' not in st.session_state:
            st.session_state.p_list_multi = p_list
            st.session_state.p_list_multi.insert(0, 'Select?', False)
            st.session_state.display_list = st.session_state.p_list_multi.copy()
            st.session_state.display_list_edited = st.session_state.p_list_multi.copy()

        with list_area:     
            queried_pigments = query_pigment(st.session_state.display_list, pigment_attributes)
            multi_selection_list(queried_pigments)

        with plot_area:
            plot(st.session_state.selected_names)
        
        if st.session_state.selected_names:
            data = get_download_data(st.session_state.selected_names)
            with download_button_area:
                st.download_button( label='Download spectra as CSV', data=data, file_name='spectra.csv', mime='text/csv')
    
    elif st.session_state.mode == MODES[2]:
        with list_area:
            queried_pigments = query_pigment(p_list, pigment_attributes)
            single_selection_list(queried_pigments) 
        
        if st.session_state.selected_names:
            with plot_area:
                show_texture(st.session_state.selected_names)


if __name__ == "__main__":
    st.set_page_config(
        page_title='Pigment Spectral',
        layout="wide",
        initial_sidebar_state="expanded",
    )
    main()






