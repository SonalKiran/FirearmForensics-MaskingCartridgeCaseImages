# mypy throws errors
# related Github issue tracked here - https://github.com/opencv/opencv/issues/24803

# imports
from helper import *
import cv2
import math
import os
from typing import Any, Sequence
import numpy as np
import numpy.typing as npt


# image masking algorithm
# function to find contours
def finding_contours(im_path: str, size: tuple[int, int] = (150, 150)) -> Any:
    # loading the image
    imgray = load_image_grayscale(im_path, size)
    # applying median blur
    imgray_mb = cv2.medianBlur(imgray, 5)
    # thresholding to find contours
    ret, thresh = cv2.threshold(imgray_mb, np.mean(imgray_mb), 255, 0)
    # applying canny edge-detection
    thresh_canny = cv2.Canny(thresh, 100, 200, 3)
    # finding contours
    contours, hierarchy = cv2.findContours(thresh_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return imgray, contours


# function to prepare contours by find bounding ellipses and triangles
def preparing_contours(imgray: npt.NDArray[Any], contours: npt.NDArray[Any]) -> Any:
    # looping over each contour to find bounding ellipses and triangles meet criteria set by thresholds
    # setting thresholds to differentiate useful contours from noise
    x, y = imgray.shape
    im_center = (int(x / 2), int(y / 2))
    thresh_dist = 25
    thresh_radius = 12
    thresh_arc = 2 * np.pi * 80
    thresh_arc_min = 0.2 * thresh_arc
    selected_ellipses = []
    selected_triangles = []
    selected_triangles_centroid = []
    for cnt in contours:
        arc_length = cv2.arcLength(cnt, True)
        if thresh_arc_min < arc_length:
            # fitting ellipse
            # there should be at least 5 points to fit the ellipse
            if len(cnt) > 4:
                (e_x, e_y), (a, b), rot = cv2.fitEllipse(cnt)
                el_center = (int(e_x), int(e_y))
                dist = calculate_distance(im_center, el_center)
                if dist < thresh_dist and a > thresh_radius and b > thresh_radius:
                    # cv2.ellipse(img, ((e_x,e_y), (a,b), rot), (0, 255, 0), 2)
                    selected_ellipses.append([int(e_x), int(e_y), a, b, rot])
            # fitting triangles
            d, tri = cv2.minEnclosingTriangle(cnt)
            if len(tri) == 3:
                tri = tri.astype(int)
                # calculating centroid
                num_points = tri.shape[0]
                p_x, p_y = 0, 0
                for i in range(num_points):
                    p_x += tri[i][0][0]
                    p_y += tri[i][0][1]
                p_x /= num_points
                p_y /= num_points
                centroid = (int(p_x), int(p_y))
                # calculating distance from center
                dist = calculate_distance(im_center, centroid)
                # drawing contour
                if dist < thresh_dist:
                    # cv2.drawContours(img, [tri], -1, (255, 0, 0), 2)
                    selected_triangles.append([tri])
                    selected_triangles_centroid.append(centroid)
    return selected_ellipses, selected_triangles, selected_triangles_centroid


# function to refine selected contours by removing redundant / overlapping contours
def refining_contours(
    imgray: npt.NDArray[Any],
    selected_ellipses: Sequence[list[Any]],
    selected_triangles: Sequence[list[Any]],
    selected_triangles_centroid: Sequence[list[Any]],
    pix_diff: int = 3,
    rad_diff: int = 3,
    prop_diff: float = 0.05,
) -> Any:
    # refining ellipses
    # instantiating list of indexes to be removed
    ind_to_pop = []
    # looping over all ellipses to find the index of the ellipses to be removed from the list
    for i in range(0, len(selected_ellipses) - 1):
        for j in range(i + 1, len(selected_ellipses)):
            # checking if the difference in corresponding points of the ellipses are withing specified pixels/radians
            if (
                sum(
                    np.array(selected_ellipses[i]) - np.array(selected_ellipses[j])
                    > np.array([pix_diff, pix_diff, pix_diff, pix_diff, rad_diff])
                )
                == 0
            ):
                ind_to_pop.append(j)
    # removing overlapping ellipses
    selected_ellipses = [
        selected_ellipses[i] for i in range(len(selected_ellipses)) if i not in set(ind_to_pop)
    ]

    # refining triangles
    # instantiating list of indexes to be removed
    ind_to_pop = []
    # looping over all triangles to find the index of the triangles to be removed from the list
    for i in range(0, len(selected_triangles) - 1):
        for j in range(i + 1, len(selected_triangles)):
            # calculating the difference in overlapping area by plotting the triangles
            temp_img = np.zeros(imgray.shape[:2])
            cv2.drawContours(temp_img, selected_triangles[i], 0, 255.0, -1)
            # calculating area with one triangle
            old_area = sum(temp_img[temp_img > 0])
            cv2.drawContours(temp_img, selected_triangles[j], 0, 255, -1)
            # calculating plotted area of both triangles
            new_area = sum(temp_img[temp_img > 0])
            # calculating the proportion of pixels that do NOT overlap
            # if this proportion is less than 5% of the old area, that means more than 95% of the triangle areas overlap
            # and hence can be considered as duplicates
            if new_area - old_area < prop_diff * old_area:
                ind_to_pop.append(j)
    # removing overlapping triangles
    selected_triangles = [
        selected_triangles[i] for i in range(len(selected_triangles)) if i not in set(ind_to_pop)
    ]
    selected_triangles_centroid = [
        selected_triangles_centroid[i]
        for i in range(len(selected_triangles_centroid))
        if i not in set(ind_to_pop)
    ]
    # sorting smallest to largest by area
    selected_ellipses = sorted(selected_ellipses, key=lambda x: x[2] * x[3])
    selected_triangles_ind = sorted(
        range(len(selected_triangles)),
        key=lambda x: cv2.contourArea(selected_triangles[x][0]),
    )
    selected_triangles = [selected_triangles[i] for i in selected_triangles_ind]
    selected_triangles_centroid = [selected_triangles_centroid[i] for i in selected_triangles_ind]
    # returning selected contours
    return selected_ellipses, selected_triangles, selected_triangles_centroid


# function to generate masks and write masked image
def building_masks(
    selected_ellipses: Sequence[list[Any]],
    selected_triangles: Sequence[list[Any]],
    selected_triangles_centroid: Sequence[list[Any]],
    imgray: npt.NDArray[Any],
) -> npt.NDArray[Any]:
    # converting image from grayscale to BGR to be able to add colored masks
    img = cv2.cvtColor(imgray, cv2.COLOR_GRAY2BGR)
    # verifying that we have contours that can be used to build the mask
    if len(selected_triangles) == 0 or len(selected_ellipses) == 0:
        raise AssertionError("Sorry, unable to build masks! Please try with another image.")
    # selecting the smallest ellipse since based on our criteria for shortlisting,
    # this is the ellipse that encloses the firing pin impression
    elip = selected_ellipses[0]
    # due to the shape of the impression left by the firing pin, the vertex of the triangle enclosing
    # firing pin area which is farthest from the remaining vertices points in the direction of the firing pin
    # we use this to our advantage to identify points of interest (poi_polygons)
    poi_tri = []
    for i, tri in enumerate(selected_triangles):
        # checking that the area of the triangle is greater than that of the ellipse/circle since
        # we are trying to find the triangle that encloses the ellipse
        if cv2.contourArea(tri[0]) < (np.pi * elip[2] * elip[3]) / 4:
            continue
        vert_a = np.squeeze(tri[0][0]).tolist()
        vert_b = np.squeeze(tri[0][1]).tolist()
        vert_c = np.squeeze(tri[0][2]).tolist()
        # calculating distance between vertices
        dist_ab = calculate_distance(vert_a, vert_b)
        dist_ac = calculate_distance(vert_a, vert_c)
        dist_bc = calculate_distance(vert_c, vert_b)
        # calculating the sum of the distance of each vertex from the other 2 vertices
        # the vertex which is farthest would have the highest sum of distances
        dist_a = dist_ab + dist_ac
        dist_b = dist_ab + dist_bc
        dist_c = dist_ac + dist_bc
        # finding the vertex which is farthest from the other vertices
        if dist_a > dist_b:
            if dist_a > dist_c:
                poi_tri.append(vert_a)
        elif dist_b > dist_c:
            poi_tri.append(vert_b)
        else:
            poi_tri.append(vert_c)
        poi_tri.append(selected_triangles_centroid[i])
        break
    # verifying that we were able to determine the direction of the firing pin (farthest vertex)
    # without it, we cannot build the mask
    if len(poi_tri) != 2:
        raise AssertionError("Sorry, unable to build masks! Please try with another image.")
    # finding coordinates of the endpoints of the minor and major axis of the ellipse
    # this will help us determine the end point of the major axis of ellipse closest to the farthest triangle vertex
    xc = elip[0]
    yc = elip[1]
    rminor = elip[2] / 2
    rmajor = elip[3] / 2
    angle = elip[4]
    minor_1 = (
        int(xc + math.cos(math.radians(angle)) * rminor),
        int(yc + math.sin(math.radians(angle)) * rminor),
    )
    minor_2 = (
        int(xc - math.cos(math.radians(angle)) * rminor),
        int(yc - math.sin(math.radians(angle)) * rminor),
    )
    major_1 = (
        int(xc + math.sin(math.radians(angle)) * rmajor),
        int(yc - math.cos(math.radians(angle)) * rmajor),
    )
    major_2 = (
        int(xc - math.sin(math.radians(angle)) * rmajor),
        int(yc + math.cos(math.radians(angle)) * rmajor),
    )
    # finding point on major axis of ellipse closest to the triangle vertex pointing in the direction of the firing pin
    if calculate_distance(major_1, poi_tri[0]) < calculate_distance(major_2, poi_tri[0]):
        arrow_head = major_1
    else:
        arrow_head = major_2
    # the centroid of the triangle is a better measure of where the center of the masking figures should be
    arrow_tail = poi_tri[1]
    # building the masks
    # 1. breech face
    new_img = np.zeros(img.shape)
    # finding the right contour for breech face by thresholding based on expected image
    for el in selected_ellipses[1:]:
        if el[3] < 0.4 * img.shape[0]:
            continue
        else:
            center = (int(el[0]), int(el[1]))
            radius = min(int(el[3] / 2), 70)
            cv2.circle(new_img, center, radius, (0, 0, 255), -1)
            break
    # ensuring that the breech face does not overlap with the firing pin impression
    cv2.ellipse(new_img, (arrow_tail, (2 * rminor + 10, 2 * rmajor + 5), angle), (0, 0, 0), -1)
    # adding breech face on to the original image
    final_img = np.zeros(img.shape)
    final_img[:, :, 0] = np.where(new_img[:, :, 2] == 0, img[:, :, 0], new_img[:, :, 0])
    final_img[:, :, 1] = np.where(new_img[:, :, 2] == 0, img[:, :, 1], new_img[:, :, 1])
    final_img[:, :, 2] = np.where(new_img[:, :, 2] > 0, new_img[:, :, 2], img[:, :, 2])
    # 2. firing pin drag
    new_ellipse_center = (
        int((arrow_head[0] + arrow_tail[0]) / 2),
        int((arrow_head[1] + arrow_tail[1]) / 2),
    )
    cv2.ellipse(
        final_img,
        (new_ellipse_center, (rminor, 1.2 * rmajor), elip[-1]),
        (143, 159, 8),
        -1,
    )
    # 3. firing pin impression
    cv2.circle(final_img, arrow_tail, int(0.9 * rminor), (120, 75, 100), -1)
    # 4. direction of the firing pin drag
    cv2.arrowedLine(final_img, arrow_tail, arrow_head, (186, 36, 7), 2, tipLength=0.2)
    # returning masked image
    return final_img


if __name__ == "__main__":
    image_path = input(
        "Please provide the entire path to the JPEG/PNG formatted image \nof a fired 9mm calibre cartridge case or the folder containing these images: "
    )
    image_path = image_path.strip()
    if not os.path.isdir(image_path):
        img_path = [image_path]
    else:
        img_path = [os.path.join(image_path, im) for im in os.listdir(image_path)]

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
            selected_ellipses, selected_triangles, selected_triangles_centroid = preparing_contours(
                imgray, contours
            )
        except Exception as e:
            print(f"An exception occurred while preparing contours:\n{e}")
            continue
        # refining contours
        try:
            selected_ellipses, selected_triangles, selected_triangles_centroid = refining_contours(
                imgray,
                selected_ellipses,
                selected_triangles,
                selected_triangles_centroid,
                pix_diff=3,
                rad_diff=3,
                prop_diff=0.05,
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
        im_path_split = im_path.split("/")
        im_name = im_path_split[-1]
        im_path_o = im_path_split[:-1]
        out_dir = os.path.join("/".join(im_path_o), "masked_images")
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        # writing masked image
        im_out_path = os.path.join(out_dir, f"masked_{im_name}")
        write_masked_image(im_out_path, masked_image)
