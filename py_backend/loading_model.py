# loading_model.py
import open3d as o3d

def launch_gui_with_model(file_path="py_backend/test.ply"):
    # Load your 3D model
    mesh = o3d.io.read_triangle_mesh(file_path)
    mesh.compute_vertex_normals()

    # Visualize it
    o3d.visualization.draw_geometries([mesh], window_name="3D Model Viewer")

# For testing standalone
if __name__ == "__main__":
    launch_gui_with_model()