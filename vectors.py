import math
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'NO_UNIQUE_PARALLEL_COMPONENT_MSG'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)
        except ValueError:
            raise ValueError("The coordinates must be nonempty")
        except TypeError:
            raise TypeError("The coordinates must be an iterable")

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates
    def plus(self, v):
        newCoordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(newCoordinates)
    def minus(self, v):
        newCoordinates = [float(x)-float(y) for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(newCoordinates)
    def multiply(self, c):
        newCoordinates = [c*x for x in self.coordinates]
        return Vector(newCoordinates)
    def magnitude(self):
        squared_coordinates = [x ** 2 for x in self.coordinates]
        return math.sqrt(sum(squared_coordinates))
    def normalized(self):
        try:
            one_over_vector = 1./ self.magnitude()
            return self.multiply(one_over_vector)
        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')
    def dot(self, v):
         return sum([x*y for x,y in zip(self.coordinates, v.coordinates)])

    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radians = math.acos(round(u1.dot(u2),4))
            if in_degrees:
                degrees_per_radian = 180 / math.pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)
            else:
                raise e
    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def is_parallel_to(self, v):
        return (self.is_zero() or
                v.is_zero() or
                self.angle_with(v) == 0 or
                self.angle_with(v) == math.pi)

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.multiply(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e
    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e
    def cross(self, v):
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = [
                y_1*z_2 - y_2*z_1,
                -(x_1*z_2 - x_2*z_1),
                x_1*y_2 - x_2*y_1
            ]
            return Vector(new_coordinates)
        except ValueError as e:
            msg = str(e)
            if msg == "need more than 2 values to unpack":
                self_embeded_in_R3 = Vector(self.coordinates + ('0',))
                v_embeded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embeded_in_R3.cross(v_embeded_in_R3)
            elif(msg == 'too many values to unpack' or
                msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e
    def area_of_parallelogram_with(self, v):
        cross_product = self.cross(v)
        return cross_product.magnitude()
    def area_of_triangle_with(self, v):
        return Decimal(self.area_of_parallelogram_with(v)) / Decimal(2)


# v = Vector([8.462, 7.893, -8.187])
# w = Vector([6.984, -5.975, 4.778])
# print('#1: ', v.cross(w))
#
# v = Vector([-8.987,-9.838,5.031])
# w = Vector([-4.268,-1.861,-8.866])
# print('#2: ', v.area_of_parallelogram_with(w))
#
#
# v = Vector([1.5,9.547,3.691])
# w = Vector([-6.007,0.124,5.772])
# print('#3: ', v.area_of_triangle_with(w))

