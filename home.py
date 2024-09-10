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
    st.markdown("<h5>Mock-up fabrication</h5><ul><li> The mock-ups were fabricated based on analytical results of polychromy traces found on ancient sculptures housed at the MANN museum in Naples. Based on these results, we made different combinations of possible paints. There are two types of <b>marble</b>: Paros and Pentelic, two types of <b>binder</b>: Punic wax and egg white, several <b>pigments</b>: Egyptian blue, Cinnabar, Red lake, Red and Yellow ochre, and green earth, different <b>ground layers</b>: lead white, calcite, lead white mixed with Egyptian blue, no ground, and multiple combinations of secondary and tertiary mixtures as well as <b>overlapping pigment layers</b>.</li><li>This experimental investigation aims to understand how all these different factors can contribute to the final appearance of the polychrome sculptures.</li><li>The mock-ups were fabricated at the Institute for Heritage Science (ISPC), CNR in Florence.</li></ul>", unsafe_allow_html=True)
    st.image(image="images/mock-up fabrication.png", caption="Mock-up fabrication process")
    st.image(image="images/mock-up examples.png", caption="Examples of Mock-ups")
    st.markdown("<ul><li> The mock-ups were measured using a multi-angle spectrophotometer, MA-T12 from X-Rite. In total there are 12 measurements. At viewing angle 15, illumination angle 60,45, 30, 0, -30, -65. At viewing angle 45, illumination angle 60, 30, 20, 0, -30, -65. The wavelength range is of 400 to 700 nm with a 10 nm step, and the light source is a white LED with blue enhancement.</li><li>The MA-T12 also has a camera for texture images positioned at 15 degrees from the normal, and the size of the texture area is of 0.9 x 1.2 cm.</li></ul>", unsafe_allow_html=True)
    st.image(image="images/MA-T12.png", caption="Scheme of measurements from MA-T12")
    st.markdown("<h5>Naming</h5><ul><li>The mock-ups have been named using the following convention: Marble_Binder_Pigment_Ground_nLayers. For example, the mock-up PEN_PW_EB_CC_2 corresponds to Pentelic marble, Punic wax, Egyptian blue, Calcite ground, 2 layers. </li><li>Explanation of the abbreviation: <ul><li>Marble: <b>PEN</b> = Pentelic, <b>PAR</b> = Paros</li><li>Binder: <b>PW</b> = Punic wax, <b>EW</b> = Egg white</li><li>Pigment: <b>EB</b> = Egyptian blue, <b>CN</b> = Cinnabar, <b>GE</b> = green earth, <b>GEz</b> = green earth with gypsum (Zecchi), <b>RO</b> = red ochre, <b>ROsi</b> = red ochre with sinopia (Zecchi), <b>ROz</b> = red ochre with gypsum (Zecchi), <b>YO</b> = yellow ochre, <b>YO</b> = yellow ochre with gypsum (Zecchi), <b>RL</b> = red lake, <b>RLk</b> = red lake Carminic (Kremer), <b>CB</b> = carbon black, <b>CN+</b> = Cinnabar + carbon black line, <b>PUR</b> = mixture dark purple, <b>lightPUR</b> = mixture light purple, <b>raspberry</b> = mixture raspberry, <b>RL+CC</b> = red lake mixed with calcium carbonate, <b>RL+EB+CC</b> = red lake mixed with Egyptian blue and calcium carbonate, <b>RO-EB</b> = red ochre over Egyptian blue, <b>RO+YO</b> = red ochre mixed with yellow ochre, <b>YO-RO</b> = yellow ochre over red ochre, <b>salmon</b> = mixture salmon, <b>STI</b> = mixture skin tone I, <b>STII</b> = mixture skin tone II, <b>YO+EB</b> = yellow ochre mixed with Egyptian blue, <b>GE+EB</b> = green earth mixed with Egyptian blue </li><li>Ground: <b>PB</b> = Lead white, <b>CC</b> = Calcium carbonate, <b>MC</b> = Mixed with calcite, <b>EB+CC</b> = Egyptian blue with calcite, <b>NG</b> = No ground</li></ul> </li></ul>", unsafe_allow_html=True)
    st.markdown("<h5 style='color:grey; font-size: 16px'>Credits</h5><ul style='color:grey'><li style='font-size: 13px'> Donata Magrini, Roberta Iannacone (CNR, ISPC), Yoko Arteaga (NTNU): mock-up fabrication. </li><li style='font-size: 13px'>Yoko Arteaga (NTNU): measurements </li><li style='font-size: 13px'>Lu Xu (NTNU):  website </li><li style='font-size: 13px'>Petros Stravoulakis, Sophia Sotiropoulou (FORTH): purchasing marble  </li></ul>", unsafe_allow_html=True)
    st.markdown("<h5 style='color:grey; font-size: 16px'>Funding</h5><span style='color:grey; font-size: 13px'>Funded by the European Union’s under grant agreement Nr. 101061157. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Executive Agency (REA). Neither the European Union nor the granting authority can be held responsible for them.</span>", unsafe_allow_html=True)

st.set_option("client.showErrorDetails", "false")
pg = st.navigation([
    st.Page(intr_page, title="HOME"),
    st.Page("main_page.py", title="Click here to start"),
])
pg.run()