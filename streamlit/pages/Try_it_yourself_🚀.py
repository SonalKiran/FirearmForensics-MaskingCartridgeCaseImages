import streamlit as st
import pathlib
import time
from cartridge_masking import *

# setting up page favicon
st.set_page_config(page_title="Try", page_icon=":rocket:")

# adding project's Github link to the sidebar
with st.sidebar:
    st.markdown(
        "[Link to Github](https://github.com/SonalKiran/FirearmForensics-MaskingCartridgeCaseImages)"
    )

# title
st.markdown(
    "## <span style='color: #0781f2'>Masking Cartridge Case Images</span>", unsafe_allow_html=True
)

# creating a list of the images in the resources directory
raw_images_path = str(pathlib.Path().absolute()) + "/data"
raw_images = []
for p in pathlib.Path(raw_images_path).iterdir():
    if str(p).endswith((".jpg", ".jpeg", ".png")):
        raw_images.append(str(p).split("/")[-1])

# creating a dropdown to select image for masking
st.markdown("Please select a bullet casing image to proceed.")
option = st.selectbox(
    "",
    tuple(raw_images),
    index=None,
    placeholder="Select an image...",
)

# proceed if an image has been selected from the dropdown
if option:
    st.markdown("You have selected the following image -")
    # defining path to the selected image
    im_path = raw_images_path + "/" + option
    st.image(im_path, width=200)
    st.markdown("Let's go ahead and build the mask!")
    # adding a button to initiate mask creation
    if st.button("Build Mask", type="primary"):
        # adding a spinner for effect
        with st.spinner("Building the masked image..."):
            time.sleep(2)
        image_path = pathlib.Path(im_path.strip())
        if not image_path.is_dir():
            img_path = [str(image_path)]
        else:
            img_path = [str(p) for p in pathlib.Path(image_path).iterdir()]
        # processing each image in img_path
        for im_path in img_path:
            im_name = im_path.split("/")[-1]
            print(f"\nProcessing {im_name}")
            # finding contours
            try:
                imgray, contours = finding_contours(im_path, (150, 150))
            except Exception as e:
                print(f"An exception occurred while finding contours:\n{e}")
                continue
            # preparing contours
            try:
                selected_ellipses, selected_triangles, selected_triangles_centroid = (
                    preparing_contours(imgray, contours)
                )
            except Exception as e:
                print(f"An exception occurred while preparing contours:\n{e}")
                continue
            # refining contours
            try:
                selected_ellipses, selected_triangles, selected_triangles_centroid = (
                    refining_contours(
                        imgray,
                        selected_ellipses,
                        selected_triangles,
                        selected_triangles_centroid,
                        pix_diff=3,
                        rad_diff=3,
                        prop_diff=0.05,
                    )
                )
            except Exception as e:
                print(f"An exception occurred while refining contours:\n{e}")
                continue
            # building masks
            try:
                masked_image = building_masks(
                    selected_ellipses,
                    selected_triangles,
                    selected_triangles_centroid,
                    imgray,
                )
            except Exception as e:
                print(f"An exception occurred while building masks:\n{e}")
                continue
            # creating 'masked_images' directory
            # creating 'masked_images' directory
            im_path_split = im_path.split("/")
            im_name = im_path_split[-1]
            im_path_o = im_path_split[:-1]
            out_dir = "/".join(["/".join(im_path_o), "masked_images"])
            if not pathlib.Path(out_dir).exists():
                pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
            # writing masked image
            im_out_path = "/".join([out_dir, f"masked_{im_name}"])
            # write_masked_image(im_out_path, masked_image)
            st.markdown("Please find the masked image below -")
            st.image(im_out_path, width=200)
