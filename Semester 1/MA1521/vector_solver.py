#!/usr/bin/env python
from vpython import vector as v
from vpython import *
from typing import Union, Type
import sympy as sym
from fractions import Fraction

def man():
    print("""
    origin = v(0,0,0)

    To create a vector:
    A = vector(0,0,0)
    B = v(1,1,1)

    k * A: scalar constant k multiplied to A
    mag(A): magnitude of A
    dot(A,B): dot product of A and B
    cross(A,B): cross product of A and B
    diff_angle(A,B): angle between A and B (in radians)
    proj(A,B): vector projection of A onto B
    A.equals(B): check if A and B have the same magnitude and direction

    same_direction(A,B): check if A and B have the same direction
    midpoint(A,B): midpoint of A and B
    unit(A): unit vector in direction of A

    Line(position_v, direction_v): Create a Line object 
    Line.point(t): Find a point on the Line using the given scalar t
    Line.is_on(position_v): Check if point is on the line
    Line.shortest_distance(position_v): Calculate the shortest distance from point to Line
    Line.line_intersection(line): Calculate the point of intersection between both Lines
    Line.is_same_line(line): Check if both Line are equivalent

    Plane(position_v, normal_v, d=0, use_d=False): Create a Plane Object. If no d is given, you can just supply position_v and normal_v. If equation is in the form of ax + by + cz = d, set the d argument and set use_d to True and put origin/v(0,0,0) as the position_v.
    Plane.is_on(position_v): Check if point is on the plane
    Plane.shortest_distance(position_v): Calculate the shortest distance from point to Plane
    Plane.line_intersection(line): Calculate the point of intersection between Line and Plane
    Plane.plane_intersection(plane): Calculate the Line of intersection between both Planes
    """)

origin = v(0,0,0)

def midpoint(position_v1: vector, position_v2:vector) -> vector:
    """
    Calculates the position vector of the midpoint of the given 2 points

    :param position_v1: position vector of the first point
    :param position_v2: position vector of the second point
    :return: returns position vector of the midpoint
    """
    print("Midpoint: ({}/2, {}/2, {}/2)".format(position_v1.x + position_v2.x, position_v1.y + position_v2.y, position_v1.z + position_v2.z ))

    return vector((position_v1.x + position_v2.x)/2, (position_v1.y + position_v2.y)/2, (position_v1.z + position_v2.z)/2 )

def unit(direction_v: vector) -> vector:
    """
    Calculates the unit vector of the given direction vector

    :param direction_v: given direction vector
    :return: returns unit vector
    """
    magn_square = direction_v.x**2 + direction_v.y**2 + direction_v.z**2
    print("{}/sqrt({})i + {}/sqrt({})j + {}/sqrt({})k".format(direction_v.x, magn_square, direction_v.y, magn_square, direction_v.z, magn_square))
 
    return norm(direction_v)

def same_direction(direction_v1: vector,direction_v2:vector) -> bool:
    """
    Checks if the two given vectors are in the scalar multiples of each other

    :param direction_v1: first vector
    :param direction_v2: second vector
    :return: returns True if vectors are in the same direction
    """

    k = sym.symbols('k')
    x_eqn = sym.Eq(direction_v1.x, direction_v2.x * k)
    y_eqn = sym.Eq(direction_v1.y, direction_v2.y * k)
    z_eqn = sym.Eq(direction_v1.z, direction_v2.z * k)
    result = sym.solve([x_eqn, y_eqn, z_eqn], [k])
    print(result)
    
    return result != []

class Line:
    def __init__(self, position_v: vector, direction_v: vector) -> None:
        """
        Construct a new vector equation of a Line.

        :param position_v: a position vector of a point on the line
        :param direction_v: the direction vector
        :return: returns nothing
        """

        self.position_v = position_v
        self.direction_v = direction_v
        print(self.__str__())

    def point(self, t: Union[int, float]) -> vector:
        """
        Calculate a new point on the Line.

        :param t: the scalar to be multipled to the direction vector of the line
        :return: returns the calculated position vector
        """

        return self.position_v + t * self.direction_v
    
    def is_on(self, position_v: vector) -> bool:
        """
        Checks if a given point lies on this Line.

        :param position_v: the position vector of the point to be checked
        :return: returns True if the given point lies on this Line, False otherwise
        """
        t = sym.symbols("t")
        eqn_x = sym.Eq(self.direction_v.x * t, position_v.x - self.position_v.x)
        eqn_y = sym.Eq(self.direction_v.y * t, position_v.y - self.position_v.y)
        eqn_z = sym.Eq(self.direction_v.z * t, position_v.z - self.position_v.z)

        result = sym.solve([eqn_x, eqn_y, eqn_z], [t])
        print(result)

        return result != []

        # return (position_v.x - self.position_v.x) / self.direction_v.x == \
        #     (position_v.y - self.position_v.y) / self.direction_v.y == \
        #     (position_v.z - self.position_v.z) / self.direction_v.z 
    
    def shortest_distance(self, position_v: vector) -> Union[sym.core.mul.Mul, float] :
        """
        Calculate the shortest/perpendicular distance of a given point to this Line. 

        :param position_v: the position vector of the given point
        :return: returns the shortest/perpendicular distance
        """

        temp = cross(position_v - self.position_v, self.direction_v)
        num = temp.x**2 + temp.y**2 + temp.z**2
        den = self.direction_v.x**2 + self.direction_v.y**2 +self.direction_v.z**2
    
        print("Shortest distance: sqrt({})/sqrt({}) or sqrt({})".format(num, den, Fraction(num/den).limit_denominator()))

        return mag(cross(position_v - self.position_v, self.direction_v)/mag(self.direction_v))
    
    def line_intersection(self, line: Type["Line"]) -> vector:
        """
        Calculates the position vector of the point at which the given Line and this Line intersects.

        :param line: the given Line to check with
        :return: returns the position vector of the intersection point
        """

        t,s = sym.symbols('t, s')
        x_eqn = sym.Eq(self.position_v.x + t * self.direction_v.x, line.position_v.x + s * line.direction_v.x)
        y_eqn = sym.Eq(self.position_v.y + t * self.direction_v.y, line.position_v.y + s * line.direction_v.y)
        z_eqn = sym.Eq(self.position_v.z + t * self.direction_v.z, line.position_v.z + s * line.direction_v.z)
        result = sym.solve([x_eqn, y_eqn, z_eqn],(t,s))
        print(result)

        if result == []:
            raise AssertionError("Both Lines do not intersect!")

        return self.position_v + float(result[t]) * self.direction_v

    def is_same_line(self, line: Type["Line"]) -> bool:
        """
        Checks if the given Line is equivalent to this Line

        :param line: the given Line to check with
        :return: returns True if both Lines are equivalent
        """

        return same_direction(self.direction_v, line.direction_v) and self.is_on(line.position_v) and line.is_on(self.position_v)

    def __str__(self) -> str:
        """
        String representation of the Line 

        :return: returns the string representation
        """

        return """
            [{}i]     [{}i]
        r = [{}j] + t [{}j]
            [{}k]     [{}k]

        x = {} + {}t , y = {} + {}t, z = {} + {}t
        """.format(
            self.position_v.x, self.direction_v.x,
            self.position_v.y, self.direction_v.y,
            self.position_v.z, self.direction_v.z,
            self.position_v.x, self.direction_v.x,
            self.position_v.y, self.direction_v.y,
            self.position_v.z, self.direction_v.z,
            )

    def __repr__(self) -> str:
        """
        Objection representation of the Line 

        :return: returns the object representation
        """

        return "<Line position_v={} direction_v={} >".format(repr(self.position_v), repr(self.direction_v))


class Plane:
    def __init__(self, position_v: vector, normal_v: vector, d: Union[int, float] = 0, use_d: bool = False) -> None:
        """
        Construct a new vector equation of a Plane.

        :param position_v: a position vector of a point on the plane
        :param normal_v: the vector normal to the plane
        :param d: the d value of ax + by + cz = d
        :param use_d: True if you are using the d parameter
        :return: returns nothing
        """

        self.normal_v = normal_v

        if use_d:
            self.d = d 
        else:
            self.d = dot(self.normal_v, position_v)
        
        print(self.__str__())

    def is_on(self, position_v: vector) -> bool:
        """
        Checks if a given point lies on the Plane.

        :param position_v: the position vector of the point to be checked
        :return: returns True if the given point lies on the plane, False otherwise
        """

        return dot(position_v, self.normal_v) == self.d

    def shortest_distance(self, position_v: vector) -> Union[int, float]:
        """
        Calculate the shortest/perpendicular distance of a given point to the Plane. 

        :param position_v: the position vector of the given point
        :return: returns the shortest/perpendicular distance
        """

        num = abs(dot(position_v, self.normal_v) - self.d )
        den = self.normal_v.x**2 + self.normal_v.y**2 + self.normal_v.z**2
        distance = num/sqrt(den)

        print("Shortest distance: {}/sqrt({}) or {}".format(num, den, Fraction(distance).limit_denominator()))

        return distance
    
    def line_intersection(self, line: Line) -> vector:
        """
        Calculate the intersection point of a given Line intersects with this Plane

        :param line: the given Line to check with
        :return: returns the position vector of the intersection point
        """
        
        t = sym.symbols('t')
        x = (line.position_v.x + t * line.direction_v.x) * self.normal_v.x
        y = (line.position_v.y + t * line.direction_v.y) * self.normal_v.y
        z = (line.position_v.z + t * line.direction_v.z) * self.normal_v.z

        eqn = sym.Eq(x + y + z, self.d)
        result = sym.solve([eqn],[t])

        print(result)

        if result == []:
            raise AssertionError("The Line does not intersect this Plane")
        
        return line.position_v + float(result[t]) * line.direction_v

    def plane_intersection(self, plane: Type["Plane"]) -> Line:
        """
        Calculate the equation of Line at the intersection of the given Plane and this Plane

        :param line: the given Plane to check with
        :return: returns the Line at the intersection
        """
        
        x, y, z = sym.symbols('x, y, z')

        p1_eqn = self.normal_v.x * x + self.normal_v.y * y + self.normal_v.z * z - self.d
        p2_eqn = plane.normal_v.x * x + plane.normal_v.y * y + plane.normal_v.z * z - plane.d 

        # eqn1 = sym.Eq(p1_eqn, p2_eqn)
        eqn2 = sym.Eq(p1_eqn, 0)
        eqn3 = sym.Eq(p2_eqn, 0)
        result = sym.solve([eqn2, eqn3], (x,y,z))

        if result == []:
            raise AssertionError("These 2 Planes do not intersect")

        results = {
            "x": sym.solve([eqn2, eqn3, sym.Eq(x, 0)], (x,y,z)),
            "y": sym.solve([eqn2, eqn3, sym.Eq(y, 0)], (x,y,z)),
            "z": sym.solve([eqn2, eqn3, sym.Eq(z, 0)], (x,y,z))
        }    
    
        print("If x = 0, then {}".format(results["x"]))
        print("If y = 0, then {}".format(results["y"]))
        print("If z = 0, then {}".format(results["z"]))

        choice = input("Choose [x/y/z] to be 0: ")

        position_v = v(results[choice][x], results[choice][y], results[choice][z])
        direction_v = cross(self.normal_v, plane.normal_v)

        return Line(position_v, direction_v)

    def __str__(self) -> str:
        return """
            [{}i]     
        r . [{}j] = {}      or      {}x + {}y + {}z = {}
            [{}k]    
        """.format(
            self.normal_v.x,
            self.normal_v.y,
            self.d,
            self.normal_v.x,
            self.normal_v.y,
            self.normal_v.z,
            self.d,
            self.normal_v.z,
            )

    def __repr__(self) -> str:
        return "<Plane normal_v={} d={} >".format(repr(self.normal_v), self.d)


def test():
    l1 = Line(v(1,2,3), v(4,5,6))
    assert l1.point(0) == v(1,2,3)
    assert l1.point(5) == v(21, 27, 33)
    assert l1.point(0.54) == v(3.16, 4.7, 6.24)
    
    l2 = Line(v(1,2,4), v(4,5,7))
    assert l1.line_intersection(l2) == v(-3,-3,-3)
    assert l2.shortest_distance(v(-3,-3,-3)) == 0

    l3 = Line(v(2,3,4),v(-1,1,1))
    assert l3.shortest_distance(v(7,4,2)) == 3 * sqrt(2) 
    
    p1 = Plane(v(1,2,3), v(-20,16,-4))
    assert p1.d == 0
    assert p1.is_on(v(1,2,3))
    assert p1.is_on(v(3,4,1))
    assert p1.is_on(v(-1,-2,-3))

    assert Plane(v(0,0,0), v(2,1,-4), 4).line_intersection(Line(v(0,2,0),v(1,3,1))) == v(2,8,2)
    
# test()