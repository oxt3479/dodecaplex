import pprint
import random
import matplotlib.animation
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as a3
import matplotlib.colors as colors
import matplotlib
from fourdsolids import *
from scipy.spatial import ConvexHull

def plot_2d_projection(vertices):
    vertices = np.array(vertices)
    plt.figure(figsize=(8, 8))
    plt.scatter(vertices[:, 0], vertices[:, 2])
    for v in vertices:
        neighbors = np.array([vx-v for vx in vertices if np.linalg.norm(np.array(v)-np.array(vx)) < .765])
        plt.quiver([v[0] for x in range(len(neighbors))], 
                   [v[1] for y in range(len(neighbors))], neighbors[:,0], neighbors[:,1], 
                   color=['red' for c in range(len(neighbors))], angles='xy', scale_units='xy', scale=1,
                   headwidth=4, headlength=3, width=0.002)

    plt.title(f'2D Projection of vertices')
    plt.show()

def plot_3d_projection(vertices, EDGE=EDGE_120CELL, scale=3):
    vertices = np.array(vertices)
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')
    ax.scatter3D(vertices[:, 0], vertices[:, 1], vertices[:, 2], s=0.1)
    for ov,osv in zip(vertices, vertices):
        neighbors = np.array([sv-osv for v, sv in zip(vertices, vertices) if ((EDGE-0.01) < np.linalg.norm(np.array(ov)-np.array(v)) < (EDGE+0.01))]) 
        color_new = random.choice(['red', 'green', 'blue', 'yellow', 'purple', 'cyan'])
        if len(neighbors) < 3: 
            continue
        plt.quiver([osv[0] for x in range(len(neighbors))], 
                   [osv[1] for y in range(len(neighbors))], 
                   [osv[2] for z in range(len(neighbors))], neighbors[:,0], neighbors[:,1], neighbors[:,2],
                   color=[color_new for c in range(len(neighbors))], alpha=0.4)

    ax.set_xlim(-scale, scale)
    ax.set_ylim(-scale, scale)
    ax.set_zlim(-scale, scale)

    plt.title(f'3D Projection of vertices')
    plt.show()

def animate_projection(vertices_groups, EDGE=EDGE_120CELL, scale=3):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')        
    ax.scatter3D(vertices_groups[0][:, 0], vertices_groups[0][:, 1], vertices_groups[0][:, 2], s=0.1)
    quiver = plt.quiver([])

    def update_graph(idx):
        vertices = np.array(vertices_groups[idx])
        
        for ov,osv in zip(vertices, vertices):
            neighbors = np.array([sv-osv for v, sv in zip(vertices, vertices) if ((EDGE-0.01) < np.linalg.norm(np.array(ov)-np.array(v)) < (EDGE+0.01))]) 
            color_new = random.choice(['red', 'green', 'blue', 'yellow', 'purple', 'cyan'])
            if len(neighbors) < 3: 
                continue
            plt.quiver([osv[0] for x in range(len(neighbors))], 
                    [osv[1] for y in range(len(neighbors))], 
                    [osv[2] for z in range(len(neighbors))], neighbors[:,0], neighbors[:,1], neighbors[:,2],
                    color=[color_new for c in range(len(neighbors))], alpha=0.4)

    ax.set_xlim(-scale, scale)
    ax.set_ylim(-scale, scale)
    ax.set_zlim(-scale, scale)
    ani = matplotlib.animation.FuncAnimation(fig, update_graph, 2, interval=10, blit=False)

    plt.show()

def plot_3d_hulls(hulls, scale = 3):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    color_params = ['y-', 'b-']
    for i, pts in enumerate(hulls):
        hull = ConvexHull(pts[:,:3])
        #ax.plot(pts.T[0], pts.T[1], pts.T[2], 'ko')
        for s in hull.simplices:
            s = np.append(s, s[0])
            ax.plot(pts[s, 0], pts[s, 1], pts[s, 2], color_params[i%len(color_params)])
    
    for start, end in zip(hulls[0], hulls[1]):
        plt.quiver(start[0], start[1], start[2], 
                   end[0]-start[0], end[1]-start[1], end[2]-start[2],
                   color='red')

    ax.set_xlim(-scale, scale)
    ax.set_ylim(-scale, scale)
    ax.set_zlim(-scale, scale)
    plt.show()

def plot_isolated_cells(dodecaplex_4d_verts, tetraplex_4d_verts, transformation=None):

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')
    count = 0
    all_d_verts = yield_dodecahedrons_from_dodecaplex(dodecaplex_4d_verts, tetraplex_4d_verts)

    color_dict = {}
    origin = np.array(random.choice(tetraplex_4d_verts))

    the_colors = ['black', 'orange', 'purple', 'magenta', 'green', 'red', 'black', 'yellow', 'grey', 'magenta', 'orange']

    np20sOff, os, svs, numpyDisps = [],[],[],[]

    for set20verts, center in zip(all_d_verts, tetraplex_4d_verts):
        np20verts = np.array(list(set20verts))
        if transformation is not None: np20verts = np20verts@transformation
        np20sOff.append(np20verts-origin[np.newaxis,:])
        disp =  np.linalg.norm(np.array(center)-origin)
        numpyDisps.append(disp)

    minDisp = min(list(numpyDisps))
    avrgDisp = sum(set(list(numpyDisps)))/len(set(list(numpyDisps)))

    for np20off, disp in zip(np20sOff, numpyDisps):
        
        if disp > avrgDisp: continue
        
        color_new = color_dict.get(disp, the_colors[len(color_dict.keys())%len(the_colors)])
        color_dict[disp] = color_new
        
        for ov in np20off:
            quiverArrows = np.array([v-ov for v in np20off if isclose(get_seperation(ov, v), EDGE_120CELL)])
            plt.quiver([ov[0] for x in range(len(quiverArrows))], 
                    [ov[1] for y in range(len(quiverArrows))], 
                    [ov[2] for z in range(len(quiverArrows))], quiverArrows[:,0], quiverArrows[:,1], quiverArrows[:,2],
                    color=[color_new for c in range(len(quiverArrows))], alpha=(1./(disp*2)**4) if disp!=minDisp else 1)
        count += 1

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-3, 3)

    plt.title(f'3D Projection of vertices with {count} primitives')
    plt.show()
        
def characterize_displacements(d4vs, t4vs, neighbor_map):    
    all20sets = list(yield_dodecahedrons_from_dodecaplex(d4vs, t4vs))
    isolated_sides = {i :
        { n: 
            {'points' : sub20set & all20sets[n],
            'displacement' : tuple(t-c for c,t in zip(center,t4vs[n]))}
            for n in neighbor_map[i]
        } for (i, sub20set), center in zip(enumerate(all20sets), t4vs)
    }
    unique_displacements = []
    all_displacements = []

    for _, cell_data in isolated_sides.items():
        for _, side_data in cell_data.items():
            if not any( [are_close(other_disp, side_data['displacement']) for other_disp in unique_displacements] ):
                unique_displacements.append(side_data['displacement'])
            all_displacements.append(side_data['displacement'])

                    
    # there are 120 unique relative displacements....
    # while there are 1440 total displacements

    print(len(unique_displacements))
    print(len(all_displacements))

def plot_translated_neighbor_maps(t4vs):        
    neighbor_map = get_neighbor_map(t4vs)

    for o_idx in range(len(t4vs)):

        starting_origins = []
        neighbor_origins = []
        for n_idx in neighbor_map[o_idx]:
            starting_origins.append(t4vs[n_idx])
            neighbor_origins.append(np.array([t4vs[nn_idx] for nn_idx in neighbor_map[n_idx]]))
        starting_origins = np.array(starting_origins)
        
        for n_idx, (nPoints, oPoint) in enumerate(zip(neighbor_origins, starting_origins)):
            nMean = np.mean(nPoints, axis=0)
            assert are_close((nMean)*(2/PHI), oPoint)
            fPoints = (nPoints-nMean[np.newaxis, :])*(2/PHI)
            print(f"origin: {o_idx}, neighbor: {n_idx}")
            plot_3d_projection(fPoints, scale = 0.66)

def solve_primary_neighbor_transforms(d4vs, t4vs):
    set20s = list(yield_dodecahedrons_from_dodecaplex(d4vs, t4vs))

    org_20_set = set20s[0]
    
    core_transforms = {}
    
    for adj_idx in get_neighbors(t4vs[0], t4vs):
        adj_20_set  = set20s[adj_idx]
        adj_cent    = t4vs[adj_idx]

        rot_axis            = adj_cent[:3]
        rot_mat             = mat_180_around(rot_axis)
        adj_20_arr          = np.array(list(adj_20_set))
        dst_20_arr          = np.array(list(org_20_set))
        dst_20_arr[:,:3]    = dst_20_arr[:,:3]@rot_mat

        idx_map = np.zeros((20), np.uint)
        for in_adj_idx, adj_point in enumerate(adj_20_arr):
            for dst_idx, dst_point in enumerate(dst_20_arr):
                if np.all(np.linalg.norm(np.cross(np.array(rot_axis), np.array(adj_point-dst_point)[:3])) < 0.01):
                    idx_map[in_adj_idx] = dst_idx
        adj_20_arr_old = np.copy(adj_20_arr)
        for t,f in enumerate(idx_map):
            adj_20_arr[f, :] = adj_20_arr_old[t, :]

        fourdee = np.linalg.lstsq(adj_20_arr, dst_20_arr)
        translated = adj_20_arr@fourdee[0]
        
        #translated[:,:3] =translated[:,:3]@np.linalg.inv(rot_mat)
        plot_3d_hulls([adj_20_arr, translated])
        core_transforms[rot_axis] = tuple(rot_mat, fourdee)

if __name__ == "__main__":   
    d4vs, t4vs = gen_dodecaplex_vertices(), gen_tetraplex_vertices()
    solve_primary_neighbor_transforms(d4vs, t4vs)
    #nmap = get_neighbor_map(t4vs)
    #neighbor_arr = np.array([t4vs[ni] for ni in nmap[x]])
