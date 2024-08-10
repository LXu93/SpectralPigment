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
PIGMENT_ATTRIBUTES = (
("Pentelic marble", "Paros", None), # MARBLES
 ("Punic wax", "Egg white",None), # BINDERS
 ("Red lake", "Cinnabar", "Egyptian blue", None), # PIGMENTS
 ("Lead white", "Calcium carbonate", "Mixed calcite", "No ground",None), # GROUNDS
 ("1", "2", "3", None) # NLAYERS
 ) 

# Use Pigment_attribute object to wrap pigment attribute names and values for querying
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

# Customize display format for select lists 
def format_display(label):
    if label == None:
        return "any"
    else:
        return label
    
def plot(selected_names, view_angle='45'):
    folder_path = 'Data/MA-T12 data/'
    extension = '.xlsx'
    
    if st.session_state.color_mode == COLORMODES[0]:
        color_file_path = 'Data/colors.csv'
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
            df = pd.read_excel(file_path, sheet_name='Spectral Data', usecols='C:AH', skiprows=2, header=0, index_col=0)
            df = df.transpose()
            
            columns = df.columns
            if view_angle == '15':
                columns = df.columns[0:6]
            if view_angle == '45':
                columns = df.columns[6:12]

            for column in columns:
                v_angle = int(column.split('as')[0])
                i_angle = int(column.split('as')[1])-int(column.split('as')[0])
                curve_name = 'i: ' + str(i_angle) + ' v: ' + str(v_angle)
               
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
                title= f'Pigment: {name}'
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
        text = cell[0].value
        v_angle = int(text.split('as')[0])
        i_angle = int(text.split('as')[1])-int(text.split('as')[0])
        caption = 'illumination angle: ' + str(i_angle) + ' viewing angle: ' + str(v_angle)
        captions.append(caption)

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

def multi_selection_list(pigment_list):
    st.session_state.display_list_edited = st.data_editor(pigment_list, disabled=pigment_list.columns[1:], hide_index=True, use_container_width=True)
    st.session_state.p_list_multi.update(st.session_state.display_list_edited)
    st.session_state.selected_names = set(st.session_state.p_list_multi[st.session_state.p_list_multi['Select?'] == True]['Name'].tolist())

def update_selection():
    st.session_state.p_list_multi.update(st.session_state.display_list_edited)

def sync_selection():
    if "p_list_multi" in st.session_state:
        st.session_state.display_list = st.session_state.p_list_multi.copy()

def clear_selected_names(): 
    if "p_list_multi" in st.session_state:
        st.session_state.display_list_edited['Select?'] = False
        st.session_state.p_list_multi['Select?'] = False
        sync_selection()
    st.session_state.selected_names = set()

def all_selected():
    st.session_state.display_list = st.session_state.p_list_multi[st.session_state.p_list_multi['Select?'] == True].copy()

def reset_query_conditions():
    st.session_state.marble = PIGMENT_ATTRIBUTES[0][-1]
    st.session_state.binder = PIGMENT_ATTRIBUTES[1][-1]
    st.session_state.pigment = PIGMENT_ATTRIBUTES[2][-1]
    st.session_state.ground = PIGMENT_ATTRIBUTES[3][-1]
    st.session_state.nlayers = PIGMENT_ATTRIBUTES[4][-1]
    if 'p_list_multi' in st.session_state:
        sync_selection()


def main():
    # Read pigment list file
    list_path = 'Data/pigment_list.csv'
    p_list = pd.read_csv(list_path)
    p_list['Number of Layers'] = p_list['Number of Layers'].astype(str)
   
    # Initialize session stste
    if "selected_names" not in st.session_state:
        st.session_state.selected_names = set()
    
    # Layout
    st.title("Spectral Pigment (This is title)")
    # Layout of the sidebar
    with st.sidebar:
        st.header("Configuration")
        st.session_state.mode = st.sidebar.selectbox('Choose mode:', MODES, on_change=clear_selected_names)
        mode_intro_area = st.empty()
        if st.session_state.mode == MODES[0]:
            st.session_state.view_angle = st.sidebar.selectbox(
                "View angle",
                ("15", "45",None),
                index= 0,
                format_func= format_display,                
            )
        if st.session_state.mode is not MODES[2]:
            st.session_state.color_mode = st.radio("Color mode of curves",
                                                   COLORMODES,
                                                   captions=["Use the corresponding pigment color for each curve", "Use distinct colors for curves"])

    # layout of the main part
    st.markdown("description")
    plot_area = st.empty()
    st.markdown(
"<span style='color:grey'> You can query the pigments with the corresponding attributes through the following select boxes</span>", unsafe_allow_html=True)
    pigment_options = st.columns(5)
    reset_button_area, download_button_area, _ = st.columns([1,2,4])
    reset_button_area.button("reset query", on_click=reset_query_conditions)
    if st.session_state.mode == MODES[1]:
        col1, col2, _= st.columns([2,2,4])
        on_only = col1.toggle("display selected only", on_change=sync_selection)
        if on_only:
            all_selected()
        col2.button("reset slection", on_click=clear_selected_names)
    list_area = st.empty()

    # Set pigment query checkboxes
    with pigment_options[0]:
        marble_value = st.selectbox(
            "Marble",
            PIGMENT_ATTRIBUTES[0],
            index= 2,
            format_func= format_display,
            on_change=sync_selection,
            key="marble",
            placeholder="any"
        )

    with pigment_options[1]:
        binder_value = st.selectbox(
            "Binder",
            PIGMENT_ATTRIBUTES[1],
            index= 2,
            format_func= format_display,
            on_change=sync_selection,
            key="binder",
            placeholder="any"
        )

    with pigment_options[2]:
        pigment_value = st.selectbox(
            "Pigment",
            PIGMENT_ATTRIBUTES[2],
            index= 3,
            format_func= format_display,
            on_change=sync_selection,
            key="pigment",
            placeholder="any"
        )

    with pigment_options[3]:
        ground_value = st.selectbox(
            "Ground",
            PIGMENT_ATTRIBUTES[3],
            index= 4,
            format_func= format_display,
            on_change=sync_selection,
            key="ground",
            placeholder="any"
        )

    with pigment_options[4]:
        nlayers_value = st.selectbox(
            "Layer numbers",
            PIGMENT_ATTRIBUTES[4],
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
        with mode_intro_area:
            st.markdown("<span style='color:grey'> Select one pigment from the table (by clicking the box at the front of each row) to show its reflectance spectra in the interactive plot, where you would also be able to download the plot.</span>" ,unsafe_allow_html=True)
        
        with list_area:
            queried_pigments = query_pigment(p_list, pigment_attributes)
            single_selection_list(queried_pigments)
        
        with plot_area:
            plot(st.session_state.selected_names, st.session_state.view_angle)
        
        if st.session_state.selected_names:
            data = get_download_data(st.session_state.selected_names)
            with download_button_area:
                st.download_button( label='Download spectral data as CSV', data=data, file_name='spectra.csv', mime='text/csv')
        
    elif st.session_state.mode == MODES[1]:
        with mode_intro_area:
            st.markdown("<span style = 'color:grey'> Select pigments from the table (by clicking the box at the front of each row) to show their reflectance spectra in the interactive plot, where you would also be able to download the plot. In this mode, the plotted curve for each pigment is the reflectance spetra of 0/45 geometry.</span>", unsafe_allow_html=True )
            
        if 'p_list_multi' not in st.session_state:
            st.session_state.p_list_multi = p_list
            st.session_state.p_list_multi.insert(0, 'Select?', False)
            st.session_state.display_list = st.session_state.p_list_multi.copy()
            st.session_state.display_list_edited = st.session_state.p_list_multi.copy()

        with list_area:     
            st.session_state.display_list = query_pigment(st.session_state.display_list, pigment_attributes)
            multi_selection_list(st.session_state.display_list)

        with plot_area:
            plot(st.session_state.selected_names)
        
        if st.session_state.selected_names:
            data = get_download_data(st.session_state.selected_names)
            with download_button_area:
                st.download_button( label='Download spectral Data as CSV', data=data, file_name='spectra.csv', mime='text/csv')
    
    elif st.session_state.mode == MODES[2]:
        with mode_intro_area:
            st.markdown("<span style='color:grey'>Select one pigment from the table (by clicking the box at the front of each row) to show its texture photos.</span>", unsafe_allow_html=True)
            
        with list_area:
            queried_pigments = query_pigment(p_list, pigment_attributes)
            single_selection_list(queried_pigments) 
        
        if st.session_state.selected_names:
            with plot_area:
                show_texture(st.session_state.selected_names)



st.set_page_config(
    page_title='Pigment Spectral',
    layout="wide",
    initial_sidebar_state="expanded",
)
main()






