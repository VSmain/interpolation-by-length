import time

import matplotlib.pyplot as plt
import numpy as np
from input import fx, fy, t_max, segment_length, t0, interpolation_step, limits, \
    output_size, create_csv
import algorithm as alg
import naive as naive_alg


def __init__():
    plt.xticks(np.arange(limits[0], limits[2], 1))
    plt.yticks(np.arange(limits[1], limits[3], 1))
    plt.figure(1)

    start_time = time.time()
    int_points = alg.fast_len_interpolation(fx, fy, t0, t_max, segment_length, interpolation_step, output_size)
    total_time = int(round((time.time() - start_time) * 1000))
    points = alg.sampling(fx, fy, t0, t_max, interpolation_step)

    print('interpolation by curve length:')
    print('1) count of point after sampling: ', len(points))
    print('2) count of points after interpolation by length: ', len(int_points))
    print('3) evaluation time milis: ', total_time, ' ms')

    ax1 = plt.subplot(221)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid()
    ax1.set_title('{x(t),y(t)}')
    plt.plot([p.x for p in points], [p.y for p in points], '-')
    ax2 = plt.subplot(222)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid()
    ax2.set_title('interpolated by len')
    plt.plot([p.x for p in int_points], [p.y for p in int_points], '*')
    ax3 = plt.subplot(223)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid()
    ax3.set_title('interpolation by curve length')
    plt.plot([p.x for p in points], [p.y for p in points], '-')
    plt.plot([p.x for p in int_points], [p.y for p in int_points], '*')

    if create_csv:
        file = open('out.csv', 'w')
        file.write('x, y\n')
        for p in int_points:
            file.write(str(p.x) + ', ' + str(p.y) + '\n')
        print('csv created')
        file.close()

    # TODO: comment this code if you setup function, which can't be interpolated using this method (infinity evaluation)
    ax4 = plt.subplot(224)
    plt.grid()
    ax4.set_title('line interpolation using step calibration (naive approach)')
    print('\n naive approach -> \n')

    start_time = time.time()
    interpolated = naive_alg.interpolate_by_length()
    total_time = int(round((time.time() - start_time) * 1000))

    print('evaluation time for accurate line interpolation with const segment length: ', total_time)
    plt.plot([p.x for p in points], [p.y for p in points], '-')
    plt.plot(interpolated['x'], interpolated['y'], '*-')
    
    # TODO: do not comment this lines
    plt.show()
    print('done')


__init__()

'''
alg description:
1) interpolation by t with minimal shift of t
2) line or spline interpolation 
3) shift by length using 
'''
