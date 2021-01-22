from vpython import *
#GlowScript 3.0 VPython

# ---animation settings---
time_for_a_loop = 1.0 / 30.0;
max_frame = 10000;
time = 0

# ---environment settings---
drag_coefficient = 0.4
air_density = 1.225
gravity = 9.8

# ---box1 status---
length_1 = 2
width_1 = 2
height_1 = 1

mass_1 = 10
speed_1 = 0
position_1 = vector(0, 0, 0)

# ---box2 status---
length_2 = 1
width_2 = 1
height_2 = 1

mass_2 = 10
speed_2 = 0
position_2 = vector(5, 0, 0)

# ---free-fall ball status---
mass_3 = 10
speed_3 = 0
position_3 =vector(10, 0, 0)

# --- small def---
def drag_force(current_speed, affected_area, drag_coefficient = 0.4, air_density = 1.225):
    '''cal the air drag force'''
    #print("drag_force:", drag_coefficient * air_density * affected_area * current_speed * current_speed / 2)
    try:
        return drag_coefficient * air_density * affected_area * current_speed * current_speed / 2
    except ZeroDivisionError:
        return 0
    
def gravity_force(mass, gravity = 9.8):
    '''cal the gravity affected on the item'''
    #print("gravity_force:", mass * gravity)
    return mass * gravity

def final_acceleration(gravity_force, drag_force, mass):
    '''cal the acceleration with g force and drag force and mass effected'''
    #print("final_acceleration:", (gravity_force - drag_force) / mass)
    return (gravity_force - drag_force) / mass

def delta_time_move(acceleration, min_time, current_speed):
    '''cal the delta time movement'''
    #print("delta_time_move:", current_speed * min_time + acceleration * min_time * min_time / 2)
    return current_speed * min_time + acceleration * min_time * min_time / 2

def delta_time_speed(acceleration, min_time, current_speed):
    '''cal the delta time speed (final speed)'''
    #print("delta_time_speed:", current_speed + acceleration * min_time)
    return current_speed + acceleration * min_time

# --- main def ---
def cal_speed(mass, gravity, current_speed, affected_area, drag_coefficient, air_density, min_time):
    return delta_time_speed(final_acceleration(gravity_force(mass, gravity), drag_force(current_speed, affected_area, drag_coefficient, air_density), mass), min_time, current_speed)

def cal_position(now_position, mass, gravity, current_speed, affected_area, drag_coefficient, air_density, min_time):
    change_vector = vector(0, -1 * delta_time_move(final_acceleration(gravity_force(mass, gravity), drag_force(current_speed, affected_area, drag_coefficient, air_density), mass), min_time, current_speed), 0)
    return now_position + change_vector
    
# make boxes
box1 = box(pos=position_1, length=length_1, width=width_1, height=height_1, make_trail=True, trail_type="points", color=color.red)
box2 = box(pos=position_2, length=length_2, width=width_2, height=height_2, make_trail=True, trail_type="points", color=color.blue)
sphere3 = sphere(pos=position_3, color=color.yellow, make_trail=True, trail_type="points", color=color.yellow)
# make speed graph window
speed_graph = graph(xtitle="Time", ytitle="speed")
speed_curve_1 = gcurve(color=color.red, label="Area = " + str(width_1 * length_1))
speed_curve_2 = gcurve(color=color.blue, label="Area = " + str(width_2 * length_2))
speed_curve_3 = gcurve(color=color.yellow, label="Free-fall")

# make position graph window
pos_graph = graph(xtitle="Time", ytitle="position")
pos_curve_1 = gcurve(color=color.red, label="Area = " + str(width_1 * length_1))
pos_curve_2 = gcurve(color=color.blue, label="Area = " + str(width_2 * length_2))
pos_curve_3 = gcurve(color=color.yellow, label="Free-fall")

for i in range(max_frame):
    rate(1.0 / time_for_a_loop)
    # cal time
    time = time + time_for_a_loop
    # cal speed
    speed_1 = cal_speed(mass_1, gravity, speed_1, length_1 * width_1, drag_coefficient, air_density, time_for_a_loop)
    speed_2 = cal_speed(mass_2, gravity, speed_2, length_2 * width_2, drag_coefficient, air_density, time_for_a_loop)
    speed_3 = cal_speed(mass_3, gravity, speed_3, 0, drag_coefficient, air_density, time_for_a_loop)
    speed_curve_1.plot(time, speed_1)
    speed_curve_2.plot(time, speed_2)
    speed_curve_3.plot(time, speed_3)
    # cal pos
    box1.pos = cal_position(box1.pos, mass_1, gravity, speed_1, length_1 * width_1, drag_coefficient, air_density, time_for_a_loop)
    box2.pos = cal_position(box2.pos, mass_2, gravity, speed_2, length_2 * width_2, drag_coefficient, air_density, time_for_a_loop)
    sphere3.pos = cal_position(sphere3.pos, mass_3, gravity, speed_3, 0, drag_coefficient, air_density, time_for_a_loop)
    pos_curve_1.plot(time, box1.pos.y * -1.0)
    pos_curve_2.plot(time, box2.pos.y * -1.0)
    pos_curve_3.plot(time, sphere3.pos.y * -1.0)
    
