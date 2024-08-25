import streamlit as st

hide_menu = """
<style>
#MainMenu {
    visibility:hidden;
}
</style>
"""

def intr_page():
    # Hiding the default top-right menu from streamlit
    st.markdown(hide_menu, unsafe_allow_html=True)
    st.title("Ancient Polychromy Database")
    if st.button("Get Started"):
        st.switch_page("main_page.py")
    st.markdown(
"<h5>Introduction</h5><ul><li> Welcome to the interactive database of appearance of ancient polychromy. Here you will find multiangle spectral data and texture images of marble mock-ups painted with different pigments, binders, and ground layers, corresponding to real traces of pigments found in ancient marble sculptures. </li><li>This database is part of the PERCEIVE project, which aims to virtually reconstruct the appearance of ancient marble sculptures. For more information, visit: <a href='https://perceive-horizon.eu'>PERCEIVE</a>.</li></ul>", unsafe_allow_html=True)
    st.markdown("<h5>Mock-up fabrication</h5><ul><li> The mock-ups were fabricated based on analytical results of polychromy traces found on ancient sculptures housed at the MANN museum in Naples. Based on these results, we made different combinations of possible paints. There are two types of <b>marble</b>: <ins>Paros</ins> and <ins>Pentelic</ins>, two types of <b>binder</b>: <ins>Punic wax</ins> and <ins>egg white</ins>, several <b>pigments</b>: <ins>Egyptian blue</ins>, <ins>Cinnabar</ins>, <ins>Red lake</ins>, <ins>Red</ins> and <ins>Yellow ochre</ins>, and <ins>green earth</ins>, different <b>ground layers</b>: <ins>lead white</ins>, <ins>calcite</ins>, <ins>lead white mixed with Egyptian blue</ins>, <ins>no ground</ins>, and multiple combinations of secondary and tertiary mixtures as well as <b>overlapping pigment layers</b>.</li><li>This experimental investigation aims to understand how all these different factors can contribute to the final appearance of the polychrome sculptures.</li><li>The mock-ups were fabricated at the Institute for Heritage Science (ISPC), CNR in Florence.</li></ul>", unsafe_allow_html=True)
    st.image(image="images/mock-up fabrication.png", caption="Mock-up fabrication process")
    st.image(image="images/mock-up examples.png", caption="Examples of Mock-ups")
    st.markdown("<ul><li> The mock-ups were measured using a multi-angle spectrophotometer, MA-T12 from X-Rite. In total there are 12 measurements. At viewing angle 15, illumination angle 60,45, 30, 0, -30, -65. At viewing angle 45, illumination angle 60, 30, 20, 0, -30, -65. The wavelength range is of 400 to 700 nm with a 10 nm step, and the light source is a white LED with blue enhancement.</li><li>The MA-T12 also has a camera for texture images positioned at 15 degrees from the normal, and the size of the texture area is of 0.9 x 1.2 cm.</li></ul>", unsafe_allow_html=True)
    st.image(image="images/MA-T12.png", caption="Scheme of measurements from MA-T12")
    st.markdown("<h5>Naming</h5><ul><li>The mock-ups have been named using the following convention: Marble_Binder_Pigment_Ground_nLayers. For example, the mock-up PEN_PW_EB_CC_2 corresponds to Pentelic marble, Punic wax, Egyptian blue, Calcite ground, 2 layers. </li><li>Explanation of the abbreviation: <ul><li>Marble: PEN = Pentelic, PAR = Paros</li><li>Binder: PW = Punic wax, EW = Egg white</li><li>Pigment: RL = Red lake, CN = Cinnabar, EB = Egyptian blue</li><li>Ground: PB = Lead white, CC = Calcium carbonate, MC = Mixed calcite, NG = No ground</li></ul> </li></ul>", unsafe_allow_html=True)
    st.markdown("<h5 style='color:grey; font-size: 16px'>Credits</h5><ul style='color:grey'><li style='font-size: 13px'> Donata Magrini, Roberta Iannacone (CNR, ISPC), Yoko Arteaga (NTNU): mock-up fabrication. </li><li style='font-size: 13px'>Yoko Arteaga (NTNU): measurements </li><li style='font-size: 13px'>Lu Xu (NTNU):  website </li><li style='font-size: 13px'>Petros Stravoulakis, Sophia Sotiropoulou (FORTH): purchasing marble  </li></ul>", unsafe_allow_html=True)
    st.markdown("<h5 style='color:grey; font-size: 16px'>Funding</h5><span style='color:grey; font-size: 13px'>Funded by the European Union’s under grant agreement Nr. 101061157. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Executive Agency (REA). Neither the European Union nor the granting authority can be held responsible for them.</span>", unsafe_allow_html=True)

st.set_option("client.showErrorDetails", "false")
pg = st.navigation([
    st.Page(intr_page, title="HOME"),
    st.Page("main_page.py", title="Click here to start"),
])
pg.run()