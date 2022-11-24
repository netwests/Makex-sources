import math
def mps_to_rpm(mps):
    return 60*mps/(2 * (3.1452 * 0.029))

def angle_to_distance(angle,blength) : #for the wheels
    return ( angle / 180 ) * math.pi * blength

def distance_and_time_to_speed(x,t) : 
    return x / t

print(distance_and_time_to_speed(0.20,60))
print((distance_and_time_to_speed(0.20,60)))
print(mps_to_rpm(distance_and_time_to_speed(angle_to_distance(90,0.36),60)))

def AutoController(Angle, Time, Distance, Motor, inverse=True):
    localdistance = Distance
    if Angle:
        if not Angle == 0:
            localdistance = (Angle / 180) * math.pi * 0.5

    localspeed = localdistance / Time
    localrpm = (60 * localspeed) / (2 * (3.1452 * 0.029))
    if Motor == 1:
        EM1.set_speed(localrpm)

    if Motor == 2:
        if inverse:
            EM2.set_speed(localrpm * -1)

        else:
            EM2.set_speed(localrpm)

    if Motor == 12:
        EM1.set_speed(localrpm)
        EM2.set_speed(localrpm * -1)

    time.sleep(float(Time))
    EM1.set_speed(0)
    EM2.set_speed(0)
