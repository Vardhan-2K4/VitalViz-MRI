import os
import nibabel as nib
import numpy as np
from nilearn.image import crop_img
from scipy.ndimage import gaussian_filter, binary_fill_holes
from skimage import measure, morphology
from skimage.filters import threshold_li
from skimage.measure import label, regionprops
import pyvista as pv

def convert_single_nii(input_path, output_dir, output_filename="brain_final.ply"):
    # Load and crop the input NIfTI image
    flair_img = nib.load(input_path)
    flair_data = crop_img(flair_img).get_fdata()

    # Normalize and smooth the intensity values
    p2, p98 = np.percentile(flair_data, (2, 98))
    flair_data = np.clip(flair_data, p2, p98)
    flair_data = (flair_data - p2) / (p98 - p2)
    smoothed = gaussian_filter(flair_data, sigma=1.0)

    # Thresholding to isolate the brain
    threshold_val = threshold_li(smoothed)
    initial_mask = smoothed > threshold_val
    cleaned = morphology.binary_opening(initial_mask, morphology.ball(2))
    cleaned = morphology.binary_closing(cleaned, morphology.ball(3))
    cleaned = binary_fill_holes(cleaned)

    labels = label(cleaned)
    regions = regionprops(labels)
    brain_mask = labels == max(regions, key=lambda x: x.area).label if regions else cleaned

    # Fill inner holes and smooth outer mask
    outer_brain_mask = brain_mask.copy()
    internal_fill = morphology.binary_erosion(brain_mask, morphology.ball(2))
    internal_fill = binary_fill_holes(internal_fill)
    internal_fill = morphology.binary_dilation(internal_fill, morphology.ball(2))
    brain_mask_filled = outer_brain_mask | internal_fill

    # Mesh generation utility
    def get_colored_mesh(mask, color_rgb, smooth_level=15):
        verts, faces, _, _ = measure.marching_cubes(mask.astype(np.float32), level=0.5)
        faces_vtk = np.hstack([np.full((faces.shape[0], 1), 3), faces]).astype(np.int64).flatten()
        mesh = pv.PolyData(verts, faces_vtk)
        mesh = mesh.clean(tolerance=1e-5)
        mesh = mesh.fill_holes(100.0)
        mesh = mesh.smooth(n_iter=smooth_level, relaxation_factor=0.1)
        colors = np.tile(np.array(color_rgb, dtype=np.uint8), (mesh.n_points, 1))
        mesh.point_data['red'] = colors[:, 0]
        mesh.point_data['green'] = colors[:, 1]
        mesh.point_data['blue'] = colors[:, 2]
        return mesh

    # Generate and save mesh
    full_mesh = get_colored_mesh(brain_mask_filled.astype(bool), [255, 255, 255])

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)
    full_mesh.save(output_path)

    return output_path
