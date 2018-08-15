from typing import List, Callable
import math
import numpy as np


class Point:
    x: float
    y: float

    def __init__(self, x, y):
        self.x = x
        self.y = y


def segment_len(p0: Point, p1: Point) -> float:
    return math.sqrt((p0.x - p1.x) * (p0.x - p1.x) + (p0.y - p1.y) * (p0.y - p1.y))


def sampling(fx: Callable[[float], float], fy: Callable[[float], float], t0: float, t_max: float, step: float) -> \
        List[Point]:
    """
    Transform your function f(t) to array of values.

    :param fy: y=f(t)
    :param fx: x=f(t)
    :param t0: start param value
    :param t_max: max param value
    :param step: function parameter increment
    :return: list of points
    """
    samples: List[Point] = []
    for t in np.linspace(t0, t_max, math.trunc((t_max - t0) / step)):
        try:
            samples.append(Point(fx(t), fy(t)))
        except ZeroDivisionError:
            pass
    return samples


def get_point(p0: Point, p1: Point, l0: float, l1: float, dl: float) -> Point:
    k = (dl - l0) / (l1 - l0)
    x = k * (p1.x - p0.x) + p0.x
    y = k * (p1.y - p0.y) + p0.y
    return Point(x, y)


def length(points: List[Point]) -> List[float]:
    count = len(points)
    lengths = [0]
    for i in range(0, count - 1):
        lengths.append(segment_len(points[i], points[i + 1]) + lengths[i])
    lengths.pop(0)
    return lengths


def prepare_seg_values(max_value: float, seg_len: float, ) -> List[float]:
    size = math.trunc(max_value / seg_len)
    values = []
    current_sum = 0
    for i in range(size):
        current_sum += seg_len
        values.append(current_sum)
    return values


def fast_len_interpolation(fx: Callable[[float], float], fy: Callable[[float], float], t0: float, t_max: float,
                           segment_length: float, interpolation_step: float, output_size: int) -> List[Point]:
    points = sampling(fx, fy, t0, t_max, interpolation_step)
    lengths = length(points)
    seg_len = prepare_seg_values(lengths[len(lengths) - 1] if lengths[len(lengths) - 1] < output_size else output_size,
                                 segment_length)
    int_points = [Point(fx(t0), fy(t0))]
    seg_id = 0
    len_id = 0
    while seg_id < len(seg_len):
        if lengths[len_id - 1] <= seg_len[seg_id] < lengths[len_id]:
            int_points.append(
                get_point(
                    points[len_id],
                    points[len_id + 1],
                    0 if len_id - 1 < 0 else lengths[len_id - 1],
                    lengths[len_id],
                    seg_len[seg_id]
                )
            )
            seg_id += 1
            if seg_id >= len(seg_len):
                break
        if seg_len[seg_id] >= lengths[len_id]:
            len_id += 1
    return int_points


def interpolation_bspline_xform(x: float, y: List[float]) -> float:
    # 4 - point, 3rd - orderB - spline(x - form)
    ym1py1 = y[0] + y[2]
    c0 = 1 / 6.0 * ym1py1 + 2 / 3.0 * y[1]
    c1 = 1 / 2.0 * (y[2] - y[0])
    c2 = 1 / 2.0 * ym1py1 - y[1]
    c3 = 1 / 2.0 * (y[1] - y[2]) + 1 / 6.0 * (y[3] - y[0])
    return ((c3 * x + c2) * x + c1) * x + c0


def interpolation_spline(samples: List[Point], multiplication_kof: int) -> List[Point]:
    out = []
    matrix_size = 4
    for p in range(len(samples)):
        x = []
        y = []
        for i in range(matrix_size if p + matrix_size < len(samples) else math.trunc(
                len(samples) - len(out) / multiplication_kof)):
            x.append(samples[i + p].x)
            y.append(samples[i + p].y)
        while (len(x) < matrix_size):
            x.append(0)
            y.append(0)
        for t in np.linspace(0, 1, multiplication_kof):
            out.append(
                Point(
                    interpolation_bspline_xform(t, x),
                    interpolation_bspline_xform(t, y)
                )
            )
    return out
