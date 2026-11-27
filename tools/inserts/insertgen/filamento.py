"""Estimativa de filamento como um fatiador faz: casca maciça + preenchimento só no miolo.

A peça é rasterizada em voxels (fatias do STL), e a distância de cada voxel até a superfície separa a
casca (paredes/topo/fundo, 100% plástico) do miolo (preenchido a `preenchimento`). Resultado em gramas.
"""
import numpy as np
from scipy import ndimage
from matplotlib.path import Path
import manifold3d as m3


def gramas(vertices, faces, paredes=3, linha=0.42, camada=0.2, topo_fundo=4, preenchimento=0.15,
           densidade=1.24, passo=0.4):
    sol = m3.Manifold(m3.Mesh(vert_properties=np.asarray(vertices, np.float32),
                              tri_verts=np.asarray(faces, np.uint32)))
    b = sol.bounding_box()
    xs = np.arange(b[0] + passo / 2, b[3], passo)
    ys = np.arange(b[1] + passo / 2, b[4], passo)
    zs = np.arange(b[2] + passo / 2, b[5], passo)
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    pts = np.c_[X.ravel(), Y.ravel()]
    vox = np.zeros((len(xs), len(ys), len(zs)), bool)
    for k, z in enumerate(zs):
        dentro = np.zeros(len(pts), bool)
        for pol in sol.slice(float(z)).to_polygons():
            dentro ^= Path(np.asarray(pol)).contains_points(pts)
        vox[:, :, k] = dentro.reshape(X.shape)
    total = vox.sum()
    if total == 0:
        return 0.0
    # distância à superfície, em mm, separada em horizontal (paredes) e vertical (topo/fundo)
    d_h = ndimage.distance_transform_edt(np.pad(vox, ((1, 1), (1, 1), (0, 0)))[:, :, :], sampling=(passo, passo, 1e6))[1:-1, 1:-1, :]
    d_v = ndimage.distance_transform_edt(np.pad(vox, ((0, 0), (0, 0), (1, 1))), sampling=(1e6, 1e6, passo))[:, :, 1:-1]
    casca = vox & ((d_h <= paredes * linha) | (d_v <= topo_fundo * camada))
    miolo = vox & ~casca
    vol = (casca.sum() + preenchimento * miolo.sum()) * passo ** 3 / 1000.0  # cm3
    return vol * densidade
