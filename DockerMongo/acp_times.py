"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#


# Was on the right track of getting both functions working, but could not post opening and closing times due to error.
close_hour = 1
speed_dist = [(1300,13.33,26),(1000,11.428,28),(0,15,34),(600,15,30),(400,15,32),(200,15,34)]
max_times = [(1000,75),(600,40),(400,27),(300,20),(200,13.5)]

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    if (control_dist_km)>((brevet_dist_km)*1.2):
        return app.logger.info("Control distance can not be greater")
    if int(control_dist_km)<=(brevet_dist_km*1.2) and int(control_dist_km)>brevet_dist_km:
        control_dist_km = brevet_dist_km
    HOUR = 0
    for dist,MIN,MAX in speed_dist:
        if control_dist_km > dist:
            hours = hours+ (control_dist_km-dist)/MAX
            control_dist_km = dist
    
    return arrow.get(brevet_start_time).shift(hours=HOUR).soformat()


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    cl_time = arrow.get(brevet_start_time)
    if control_dist_km == 0:
        return cl_time.shift(hours=1).isoformat()
    if int(control_dist_km)<=(brevet_dist_km*1.2) and int(control_dist_km)>brevet_dist_km:
        control_dist_km = brevet_dist_km
    for Xdist,Ytime in max_times:
        if int(control_dist_km) == Xdist:
             cl_time = cl_time.shift(minutes=Ytime)
    hours_conv = 0
    for distance,MIN,MAX in speed_dist:
        if control_dist_km > distance:
            hours_conv = hours_conv + (control_dist_km-distance)/MAX
            control_dist_km = distance
    return cl_time.shift(hours=hours_conv).isoformat()
    




