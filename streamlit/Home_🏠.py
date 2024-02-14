import pathlib
import sys

# This adds the path of the …/src folder to the PYTHONPATH variable
# This code assumed that streamlit is being called from the parent
# (FirearmForensics-MaskingCartridgeCaseImages) folder [streamlit run streamlit/home.py]
sys.path.append(str(pathlib.Path().absolute()) + "/services")

import streamlit as st

# setting up page favicon
st.set_page_config(page_title="Home", page_icon=":house:")

# adding project's Github link to the sidebar
with st.sidebar:
    st.markdown(
        "[Link to Github](https://github.com/SonalKiran/FirearmForensics-MaskingCartridgeCaseImages)"
    )

# title
st.markdown("## <span style='color: #0781f2'>Firearm Forensics</span>", unsafe_allow_html=True)
# landing page image
st.image("./resources/forensic_firearms_header.jpg")
# general introduction
st.markdown("#### What is firearm forensics?")
st.markdown(
    "Forensic firearm examination is a fascinating field, where experts meticulously **<span style='color: #0781f2'>analyze \
    the intricate details of firearms and bullets to aid criminal investigations</span>**.",
    unsafe_allow_html=True,
)
st.markdown(
    "The ability to link a bullet or a bullet casing to a specific weapon through striations left on the \
    bullet's surface or the impressions on a bullet casing is akin to matching \
    fingerprints or DNA evidence in terms of its significance. This process not only helps identify the weapon used in a crime but \
    can also provide crucial evidence in linking suspects to the scene."
)
