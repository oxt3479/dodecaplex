import os
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
from scipy.spatial.qhull import QhullError
from itertools import combinations
from scipy.spatial.transform import Rotation as R

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

def plot_center_movements(t4vs, t4vs_disp, scale=3):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for start, end in zip(t4vs, t4vs_disp):
        c = vector_to_rgb(end-start)
        plt.quiver(start[0], start[1], start[2], 
                    end[0]-start[0], end[1]-start[1], end[2]-start[2],color=c, alpha=0.6)
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

def rodrigues(axis, theta):
    axis = axis/np.linalg.norm(axis)
    a = np.cos(theta/2.0)
    b, c, d = -axis * np.sin(theta/2.0)
    
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    
    return np.array([
        [aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
        [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
        [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]
    ])

def solve_primary_neighbor_transforms(d4vs, t4vs):
    set20s = list(yield_dodecahedrons_from_dodecaplex(d4vs, t4vs))

    org_20_set = set20s[0]
    all_transforms = {}

    final_inputs = []
    final_outputs = []

    np.set_printoptions(suppress=True)
    entry = random.randrange(0,20)
    for adj_idx in get_neighbors(t4vs[0], t4vs):
        adj_20_set  = set20s[adj_idx]
        adj_cent    = t4vs[adj_idx]

        rot_axis            = adj_cent[:3]
        rot_mat             = mat_180_around(rot_axis)
        adj_20_arr          = np.array(list(adj_20_set))
        dst_20_arr          = np.array(list(org_20_set))
        org_20_arr          = np.copy(dst_20_arr)
        dst_20_arr[:,:3]    = dst_20_arr[:,:3]@rot_mat

        idx_map = np.zeros((20), np.uint)
        for in_adj_idx, adj_point in enumerate(adj_20_arr):
            for dst_idx, dst_point in enumerate(dst_20_arr):
                if np.all(np.linalg.norm(np.cross(np.array(rot_axis), np.array(adj_point-dst_point)[:3])) < 0.01):
                    idx_map[in_adj_idx] = dst_idx
        adj_20_arr_old = np.copy(adj_20_arr)
        for t,f in enumerate(idx_map):
            adj_20_arr[f, :] = adj_20_arr_old[t, :]
        fourdee = np.linalg.lstsq(adj_20_arr, org_20_arr)
        translated = adj_20_arr@fourdee[0]
        all_transforms[adj_cent] = fourdee[0]
        inv_rot = np.identity(4)
        inv_rot[:3,:3] = np.linalg.inv(rot_mat)
        full_transform = fourdee[0]@inv_rot
        fourdee_friend = fourdee[0].copy()
        for degree in np.arange(0, 2*np.pi-0.1, (2*np.pi)/5):
            rotation_mat = R.from_rotvec((adj_cent[:3]/np.linalg.norm(adj_cent[:3]))*degree)
            final_inputs.append(np.array((*adj_cent, *rotation_mat.as_matrix().flatten())))
            final_outputs.append(fourdee_friend.flatten())
            fourdee_friend=np.dot(fourdee[0], fourdee_friend)
            fourdee_friend=np.dot(fourdee[0], fourdee_friend)

    solution = np.linalg.lstsq(final_inputs, final_outputs)
    print(solution)
    print(np.array(final_inputs).shape)
    return all_transforms

def write_declarations(d4vs, t4vs):

    vertices = '\n'.join([f"{a}, {b}, {c}, {d}," for a,b,c,d in d4vs])

    d4v_arr = np.array(list(d4vs))
    
    indeces = []
    fourdee_mats = solve_primary_neighbor_transforms(d4vs, t4vs)
    #fourdee = fourdee_mats[list(fourdee_mats.keys())[0]] # Arbitrary transform
    penta_indexs = []
    raw_indeces = {}

    def format_indeces(x, super_index, cell_idx, point_array_4d):
        out_str = ''
        raw_indeces[cell_idx] = []
        sets_of_five = []        
        sub_set = set()
        def orderForTextures(set_of_five):
            order = [set_of_five[0]]
            def getOffsets(i):
                origin = point_array_4d[i]
                return [np.linalg.norm( point_array_4d[x]-origin) for x in set_of_five]
            while len(order) < 5:
                offset = getOffsets(order[-1])
                nexts =[set_of_five[a] for a,b in enumerate(offset) if np.isclose(b, 0.7639320225)]
                assert len(nexts) == 2
                for n in nexts:
                    if n not in order:
                        order.append(n)
                        break                
            return order
        for i, (a,b,c) in enumerate(x):
            raw_indeces[cell_idx].append((super_index[a], super_index[b], super_index[c]))
            sub_set.add(a)
            sub_set.add(b)
            sub_set.add(c)
            if (i+1)%3 == 0:
                assert len(sub_set) == 5
                sets_of_five.append(list(sub_set))
                sub_set.clear()
        for i, set_of_five in enumerate(sets_of_five):
            if i%4 == 0:
                out_str+= '\n'
            a,b,c,d,e = orderForTextures(set_of_five)
            penta_indexs.append(set((super_index[x] for x in (a,b,c,d,e))))
            tri_str = f"{super_index[a]}, {super_index[b]}, {super_index[c]}, {super_index[d]}, {super_index[e]},\t\t"
            gap = " "*(15 - len(tri_str))
            out_str += gap+tri_str
        return out_str

    for cell_idx, d in enumerate(yield_indexed_dodecahedrons_from_dodecaplex(d4vs, t4vs)):
        hull=None
        point_array = np.array([list(p[1]) for p in d])        
        while hull == None:
            try:
                hull = ConvexHull(point_array[:,:3])
                assert len(hull.simplices) == 36
            except AssertionError:
                print(len(hull.simplices))
            except QhullError:
                hull=None                
                point_array = point_array@fourdee_mats[random.choice(list(fourdee_mats.keys()))]
                # The current dodecahedron is currently flat in 3D, so we apply a transform to make it 
                # solvable to the hull alg.
        indeces.append(format_indeces(hull.simplices, [p[0] for p in d], cell_idx, point_array))

    np.set_printoptions(suppress=True)

    axiis, mats = [], []

    for key, value in fourdee_mats.items():
        axiis.append(f"glm::vec4({','.join([str(k) for k in list(key)])})")
        mats.append('{'+','.join(['{0:0.8f}'.format(f).rstrip('0').rstrip('.') for f in value.flat])+'}')

    neighbor_data = {}
    
    for key_a, value_a in raw_indeces.items():
        assert len(value_a) == 36
        neighbor_data[key_a] = [None]*36
        for key_b, value_b in raw_indeces.items():
            if key_a == key_b: continue
            all_trips = []
            for b, trip_b in enumerate(value_b):
                all_trips.extend(trip_b)
            for a, trip_a in enumerate(value_a):
                if len(set(trip_a).intersection(set(all_trips))) == 3:
                    assert neighbor_data[key_a][a] == None
                    neighbor_data[key_a][a] = key_b
                    
    points = []

    def characterize_deltas(points, key):
        np_points = np.array([d4vs[y] for y in list(set(points))])
        change = np_points-np_points[key,:]
        lens = [np.linalg.norm(x) for x in change]
        closers = [i for i,x in enumerate(lens) if isclose(x, 0.763932, rel_tol=0.001)]
        futhurs = [i for i,x in enumerate(lens) if isclose(x, 1.236067, rel_tol=0.001)]
        return (closers, futhurs)

    neighbor_indeces = []

    for cell_id in range(120):
        for i, x in enumerate(raw_indeces[cell_id]):
            points.extend(x)
            if (i+1)%3==0:
                csa, fsa = characterize_deltas(points, 0)
                csb, fsb = characterize_deltas(points, fsa[0])

                order = [0, list(set(csa).intersection(set(csb))).pop(), fsa[0], fsa[1], list(set(csa).intersection(set(fsb))).pop()]
                neighbor_indeces.append(order)
                points=[]
    INTERIOR, EXTERIOR, ADJACENT = [],[],[]
    for x, set_a in enumerate(penta_indexs):
        cell = x//12
        neighbors = [(i,o) for i,o in enumerate(penta_indexs) if len(o&set_a) == 2]
        INTERIOR.append([i for i,o in neighbors if i//12 == cell])
        for adj_cells in neighbor_data[cell][::3]:
            adj_pents = penta_indexs[adj_cells*12:adj_cells*12+12]
            shared = [(i,p) for i,p in enumerate(adj_pents) if len(p&set_a)==2]
            if len(shared) == 5:
                ext_cell = adj_cells
                EXTERIOR.append([i+adj_cells*12 for i,_ in shared])
        #print("Int cell: ", len([i for i,o in enumerate(penta_indexs) if len(o & set_a)==2 and i//12 == cell]))
        #print("Ext cell: ", len([i for i,o in enumerate(penta_indexs) if len(o & set_a)==2 and i//12 in neighbor_data[cell]
                                 #and len()]))
        ADJACENT.append([i for i,_ in neighbors if i//12 in neighbor_data[cell] and i//12!=ext_cell])


    with open('dodecaplex.h', 'w') as dph:
        pass        
        dph.write('\n'+'\n'.join([f'//------Cell {i}------{x}'for i, x in enumerate(indeces)]))
        dph.write(',\n'.join([str(nd[::3]).strip('[]') for k, nd  in neighbor_data.items()]))
        dph.write('interior\n'+',\n'.join([str(I).strip('[]') for I in INTERIOR]))
        dph.write('exterior\n'+',\n'.join([str(I).strip('[]') for I in EXTERIOR]))
        dph.write('adjacent\n'+',\n'.join([str(I).strip('[]') for I in ADJACENT]))

        #dph.write(',\n'.join([str(x).strip('[]') for x in neighbor_indeces]))
        #dph.write('\n'+'\n'.join(axiis))
        #dph.write('\n'+'\n'.join(mats))
    
if __name__ == "__main__":   
    normed = lambda x: x/np.linalg.norm(x)
    d4vs, t4vs = gen_dodecaplex_vertices(), gen_tetraplex_vertices()
    #transform_dict = solve_primary_neighbor_transforms(d4vs, t4vs)
    write_declarations(d4vs, t4vs)
