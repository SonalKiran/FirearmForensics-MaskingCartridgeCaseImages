import streamlit as st
import cv2

# setting up page favicon
st.set_page_config(page_title="About", page_icon=":performing_arts:")

# adding project's Github link to the sidebar
with st.sidebar:
    st.markdown(
        "[Link to Github](https://github.com/SonalKiran/FirearmForensics-MaskingCartridgeCaseImages)"
    )

# title
st.markdown("## <span style='color: #0781f2'>About The Project</span>", unsafe_allow_html=True)

# adding bullet casing images
# creating columns
col1, col_, col2 = st.columns((2, 0.6, 2))

# adding original bullet casing image
# original = cv2.imread("./resources/o_1.jpg")
col1.markdown("<h5 style='text-align: center'>Original Casing Image</h2>", unsafe_allow_html=True)
col1.image("./resources/o_1.jpg", use_column_width=True)

# adding masked bullet casing image
# masked = cv2.imread("./resources/masked_o_1.jpg")
col2.markdown("<h5 style='text-align: center'>Masked Casing Image</h2>", unsafe_allow_html=True)
col2.image("./resources/masked_o_1.jpg", use_column_width=True)

# project information
st.write(
    "This project employs computer vision algorithms and creates a tool to build masks on top of fired cartridge \
case images identifying regions of interest to aid in forensic investigations. These masks are used to compare the \
impressions on the cartridge case with the breech face and firing pin impressions of the firearm."
)

st.write("This tool masks the following regions of interest -")

st.write("\n")

st.markdown("- **Breech face impression**\n- **Firing pin impression**\n- **Firing pin drag**")

st.markdown(
    "For this algorithm to work as required it is important to use properly lit images focused on the firing \
pin and the breech face regions, including the grooves around the breech face but *excluding the head stamp region* of \
the case. Below is an image to illustrate the anatomy of a fired cartridge case -\n"
)

st.markdown(
    "**<span style='color: #0781f2'>Fired Cartridge Case Image</span>**", unsafe_allow_html=True
)
st.image("./resources/bullet_casing.jpg")

st.markdown(
    "1. **Head stamp region** (should not be a part of the image)\n2. **Breech face impression**\n3. **Firing pin impression**\n4. **Firing pin drag**"
)
