import os

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import openpyxl
from openpyxl_image_loader import SheetImageLoader

# Define constant
# Website modes
MODES = ("Single mock-up", "Comparison", "Texture images")
COLORMODES = ("Corresponding color mode", "Distinct mode")
MOCKUP_ATTRIBUTES = (
('Pentelic', 'Paros', None), # MARBLES
 ('Egg white', 'Pentelic', 'Punic wax',None), # BINDERS
 ('Cinnabar',
 'Cinnabar + carbon black line',
 'Egyptian blue',
 'carbon black',
 'green earth',
 'green earth mixed with Egyptian blue',
 'green earth with gypsum (Zecchi)',
 'mixture dark purple',
 'mixture purple',
 'mixture light purple',
 'mixture raspberry',
 'mixture salmon',
 'mixture skin tone I',
 'mixture skin tone II',
 'red lake',
 'red lake Carminic (Kremer)',
 'red lake mixed with Egyptian blue and calcium carbonate',
 'red lake mixed with calcium carbonate',
 'red ochre',
 'red ochre mixed with yellow ochre',
 'red ochre over Egyptian blue',
 'red ochre with gypsum (Zecchi)',
 'red ochre with sinopia (Zecchi)',
 'yellow ochre',
 'yellow ochre mixed with Egyptian blue',
 'yellow ochre over red ochre',
 'yellow ochre with gypsum (Zecchi)', None), # PIGMENTS
 ('Calcium carbonate',
 'Egyptian blue with calcite',
 'Lead white',
 'Mixed with calcite',
 'No ground',None), # GROUNDS
 ("1", "2", "3","many", None) # NLAYERS
 ) 
hide_menu = """
<style>
#MainMenu {
    visibility:hidden;
}
</style>
"""

# Use Mockup_attribute object to wrap mock-up attribute names and values for querying
class Mockup_attribute():
    def __init__(self, column_name, value) -> None:
        self.column_name = column_name
        self.value = value

def query_mockup(df, mockup_attributes):
    res = df
    for attribute in mockup_attributes:
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
    folder_path = 'Data new/MA-T12 data/'
    extension = '.xlsx'
    
    if st.session_state.color_mode == COLORMODES[0]:
        color_file_path = 'Data new/colors.csv'
        all_cols = pd.read_csv(color_file_path, usecols=[0, 1, 5, 6, 7], header=0)
    

    fig = go.Figure()
    fig.update_layout(
                xaxis_title='Wavelength (nm)',
                yaxis_title='Reflectance',
            )
    fig.update_yaxes(range=[-.01, 1.01])  
    
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
                legend_title='Illumination & viewing angle',
                title= f'Mock-up: {name}'
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
                legend_title='Mock-up',
                showlegend = True
            )
  
    st.plotly_chart(fig)

def show_texture(name):
    folder_path = "Data new/MA-T12 data/"
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
    folder_path = "Data new/MA-T12 data/"
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

def single_selection_list(mockup_list):
    display_list = st.dataframe(mockup_list, on_select="rerun", selection_mode="single-row", hide_index=True, use_container_width=True)
    selected_names = mockup_list.iloc[display_list.selection["rows"]]["Name"].tolist()
    if selected_names:
        st.session_state.selected_names = set(selected_names)
    return display_list

def multi_selection_list(mockup_list):
    st.session_state.display_list_edited = st.data_editor(mockup_list, disabled=mockup_list.columns[1:], hide_index=True, use_container_width=True)
    st.session_state.all_mockup_list_multi.update(st.session_state.display_list_edited)
    st.session_state.selected_names = set(st.session_state.all_mockup_list_multi[st.session_state.all_mockup_list_multi['Select?'] == True]['Name'].tolist())

def update_selection():
    st.session_state.all_mockup_list_multi.update(st.session_state.display_list_edited)

def sync_selection():
    if "all_mockup_list_multi" in st.session_state:
        st.session_state.display_list = st.session_state.all_mockup_list_multi.copy()

def clear_selected_names(): 
    if "all_mockup_list_multi" in st.session_state:
        st.session_state.display_list_edited['Select?'] = False
        st.session_state.all_mockup_list_multi['Select?'] = False
        sync_selection()
        sync_all_selection()
    st.session_state.selected_names = set()

def all_selected():
    st.session_state.display_list = st.session_state.all_mockup_list_multi[st.session_state.all_mockup_list_multi['Select?'] == True].copy()

def on_select_only_change():
    sync_selection()
    sync_all_selection()

def reset_query_conditions():
    st.session_state.marble = MOCKUP_ATTRIBUTES[0][-1]
    st.session_state.binder = MOCKUP_ATTRIBUTES[1][-1]
    st.session_state.pigment = MOCKUP_ATTRIBUTES[2][-1]
    st.session_state.ground = MOCKUP_ATTRIBUTES[3][-1]
    st.session_state.nlayers = MOCKUP_ATTRIBUTES[4][-1]
    sync_selection()
    sync_all_selection()

def sync_all_selection():
    if "on_only" in st.session_state:
        if st.session_state.on_only:
            all_selected()

def on_query_change():
    sync_selection()
    sync_all_selection()

def main():
    # Hiding the default top-right menu from streamlit
    st.markdown(hide_menu, unsafe_allow_html=True)
    # Read pigment list file
    @st.cache_data
    def read_mockup_list():
        list_path = 'Data new/pigment_list.csv'
        list = pd.read_csv(list_path)
        list['Number of layers'] = list['Number of layers'].astype(str)
        return list
    
    st.session_state.all_mockup_list = read_mockup_list()
    # Initialize session stste
    if "selected_names" not in st.session_state:
        st.session_state.selected_names = set()
    
    # Layout
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
                                                   captions=["Use the corresponding mock-up color for each curve", "Use distinct colors for curves"])

    
    # layout of the main part
    title_area = st.empty()
    description_area = st.empty()
    if st.session_state.mode == MODES[2]:
        current_name_area = st.empty()
    plot_area = st.empty()
    st.markdown("<span style='color:grey'> You can query the mock-ups with the corresponding attribute combinations through the following select boxes</span>", unsafe_allow_html=True)
    mockup_options = st.columns(5)
    reset_button_area, download_button_area, _ = st.columns([1,2,4])
    reset_button_area.button("reset query", on_click=reset_query_conditions)
    if st.session_state.mode == MODES[1]:
        col1, col2, _= st.columns([2,2,4])
        on_only = col1.toggle("display selected only", on_change=on_select_only_change, key="on_only")
        if on_only:
            col2.button("clear selection", on_click=clear_selected_names)
    list_area = st.empty()

    # Set mock-up query checkboxes
    with mockup_options[0]:
        # Only set defualt value at the first time the widget is initiated
        if "marble" in st.session_state:
            marble_value = st.selectbox(
                "Marble",
                MOCKUP_ATTRIBUTES[0],
                format_func= format_display,
                on_change=on_query_change,
                key="marble",
                placeholder="any"
            )
        else:
            marble_value = st.selectbox(
                "Marble",
                MOCKUP_ATTRIBUTES[0],
                index= len(MOCKUP_ATTRIBUTES[0])-1,
                format_func= format_display,
                on_change=on_query_change,
                key="marble",
                placeholder="any"
            )

        with mockup_options[1]:
            # Only set defualt value at the first time the widget is initiated
            if "binder" in st.session_state:
                binder_value = st.selectbox(
                    "Binder",
                    MOCKUP_ATTRIBUTES[1],
                    format_func= format_display,
                    on_change=on_query_change,
                    key="binder",
                    placeholder="any"
                )
            else:
                binder_value = st.selectbox(
                    "Binder",
                    MOCKUP_ATTRIBUTES[1],
                    index= len(MOCKUP_ATTRIBUTES[1])-1,
                    format_func= format_display,
                    on_change=on_query_change,
                    key="binder",
                    placeholder="any"
                )

    with mockup_options[2]:
        # Only set defualt value at the first time the widget is initiated
        if "pigment" in st.session_state:
             pigment_value = st.selectbox(
                "Pigment",
                MOCKUP_ATTRIBUTES[2],
                format_func= format_display,
                on_change=on_query_change,
                key="pigment",
                placeholder="any"
            )
        else:
            pigment_value = st.selectbox(
                "Pigment",
                MOCKUP_ATTRIBUTES[2],
                index= len(MOCKUP_ATTRIBUTES[2])-1,
                format_func= format_display,
                on_change=on_query_change,
                key="pigment",
                placeholder="any"
            )

    with mockup_options[3]:
        # Only set defualt value at the first time the widget is initiated
        if "ground" in st.session_state:
            ground_value = st.selectbox(
                "Ground",
                MOCKUP_ATTRIBUTES[3],
                format_func= format_display,
                on_change=on_query_change,
                key="ground",
                placeholder="any"
            )
        else:
            ground_value = st.selectbox(
                "Ground",
                MOCKUP_ATTRIBUTES[3],
                index= len(MOCKUP_ATTRIBUTES[3])-1,
                format_func= format_display,
                on_change=on_query_change,
                key="ground",
                placeholder="any"
            )

    with mockup_options[4]:
        # Only set defualt value at the first time the widget is initiated
        if "nlayers" in st.session_state:
            nlayers_value = st.selectbox(
                "Numbers of layers",
                MOCKUP_ATTRIBUTES[4],
                format_func= format_display,
                on_change=on_query_change,
                key="nlayers",
                placeholder="any"
            )
        else:
            nlayers_value = st.selectbox(
                "Numbers of layers",
                MOCKUP_ATTRIBUTES[4],
                index= len(MOCKUP_ATTRIBUTES[4])-1,
                format_func= format_display,
                on_change=on_query_change,
                key="nlayers",
                placeholder="any"
            )

    marble = Mockup_attribute("Marble", marble_value)
    binder = Mockup_attribute("Binder", binder_value)
    pigment = Mockup_attribute("Pigment", pigment_value)
    ground = Mockup_attribute("Ground", ground_value)
    nlayers = Mockup_attribute("Number of layers", nlayers_value)
    mockup_attributes = [marble, binder, pigment, ground, nlayers]
    
    if st.session_state.mode == MODES[0]:
        with title_area:
            st.title("Single mock-up multiangle reflectance")
        
        with description_area:
            st.markdown("<span> Reflectance spectra of single mock-up.</span><span> The mock-ups have been named using the following convention: Marble_Binder_Pigment_Ground_nLayers. More information in the Home page. </span>", unsafe_allow_html=True)

        with mode_intro_area:
            st.markdown("<span style='color:grey'> Select one mock-up from the table (by clicking the box at the front of each row) to show its reflectance spectra in the interactive plot,where you can also download the plot.</span>" ,unsafe_allow_html=True)
        
        with list_area:
            queried_mockups = query_mockup(st.session_state.all_mockup_list, mockup_attributes)
            single_selection_list(queried_mockups)
        
        with plot_area:
            plot(st.session_state.selected_names, st.session_state.view_angle)
        
        if st.session_state.selected_names:
            data = get_download_data(st.session_state.selected_names)
            with download_button_area:
                st.download_button( label='Download spectral data as CSV', data=data, file_name='spectra.csv', mime='text/csv')
        
    elif st.session_state.mode == MODES[1]:
        with title_area:
            st.title("Comparison of mock-up reflectance")

        with description_area:
            st.markdown("<span> Reflectance spectra of selected mock-ups. The mock-ups have been named using the following convention: Marble_Binder_Pigment_Ground_nLayers. More information in the Home page. </span>", unsafe_allow_html=True)

        with mode_intro_area:
            st.markdown("<span style = 'color:grey'> Select mock-ups from the table (by clicking the box at the front of each row) to show their reflectance spectra in the interactive plot, where you can also download the plot. In this mode the plotted curve for each mock-up is the reflectance spectrum at 0/45 geometry</span>", unsafe_allow_html=True )
            
        if 'all_mockup_list_multi' not in st.session_state:
            st.session_state.all_mockup_list_multi = st.session_state.all_mockup_list
            st.session_state.all_mockup_list_multi.insert(0, 'Select?', False)
            st.session_state.display_list = st.session_state.all_mockup_list_multi.copy()
            st.session_state.display_list_edited = st.session_state.all_mockup_list_multi.copy()

        with list_area:     
            st.session_state.display_list = query_mockup(st.session_state.display_list, mockup_attributes)
            multi_selection_list(st.session_state.display_list)

        with plot_area:
            plot(st.session_state.selected_names)
        
        if st.session_state.selected_names:
            data = get_download_data(st.session_state.selected_names)
            with download_button_area:
                st.download_button( label='Download spectral Data as CSV', data=data, file_name='spectra.csv', mime='text/csv')
    
    elif st.session_state.mode == MODES[2]:
        with title_area:
            st.title("Texture images")

        with description_area:
            st.markdown("<span> Texture images of mock-up. The mock-ups have been named using the following convention: Marble_Binder_Pigment_Ground_nLayers. More information in the Home page. </span>", unsafe_allow_html=True)

        with mode_intro_area:
            st.markdown("<span style='color:grey'>Select one mock-up from the table (by clicking the box at the front of each row) to show its texture photos.</span>", unsafe_allow_html=True)
            
        with list_area:
            queried_mockups = query_mockup(st.session_state.all_mockup_list, mockup_attributes)
            single_selection_list(queried_mockups) 
        
        if st.session_state.selected_names:
            name = st.session_state.selected_names.pop()
            st.session_state.selected_names.add(name)
            with current_name_area:
                st.write(f"**Mock-up: {name}**")
            with plot_area:
                show_texture(name)

# page_config
st.set_page_config(
    page_title='Pigment Spectral',
    layout="wide",
    initial_sidebar_state="expanded",
)
st.set_option("client.showErrorDetails", "false")
main()






