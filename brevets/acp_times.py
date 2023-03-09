"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

def find_time_val(control_sum):
   hours_value = int(control_sum)
   mins_value = (control_sum - hours_value) * 60 # Multiplying resulting fractional part by 60
   mins_value = round(mins_value)

   return (hours_value, mins_value)
   
def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
   """
   Args:
   control_dist_km:  number, control distance in kilometers
   brevet_dist_km: number, nominal distance of the brevet
      in kilometers, which must be one of 200, 300, 400, 600,
      or 1000 (the only official ACP brevet distances)
   brevet_start_time:  An arrow object
   Returns:
   An arrow object indicating the control open time.
   This will be in the same time zone as the brevet start time.
   """
   # To calculate opening times, use the maximum speed from table
   # Based on the control dist, will determine max speed
   # Then, once have that speed, use the control_dist and speed to calculate hours and mins
   # Then shift the brevet start time with those hour and min values
   max_speed = 1
   max_check = control_dist_km * 1.2

   if(control_dist_km > max_check):
      print("ERROR: Control distance can not be larger than the distance of the overall brevet")
      return 0
   else:
      if(control_dist_km > 200):
         #print(f"control dist: {control_dist_km} is greater than 200 so doing fancy stuff")
         hours_value = 0
         mins_value = 0
         # If control distance is beyond 200km, do the following calculations
         dist_traveled = 0
         dist_remaining = control_dist_km
         
         travel_level = 0
         control_sum = 0
         subt_amnt = 0
            
         while((dist_remaining > 200) and ((dist_remaining-subt_amnt) > 0)):
            #print(hours_mins_dict)
            # If control is beyond 200km, have to use a different speed value for that part and for the first 200 use 34 for speed
            # Ex for 350, have 200/34 + 150/32 = 10.56985... -> 10H34
   
            if dist_traveled < 200: # Going to define each block as a certain distance level, this is distance level 1
               control_sum += (200/34)
               travel_level = 1
               dist_traveled += 200
               dist_remaining -= 200
               subt_amnt = 200
   
            elif 200 <= dist_traveled < 400: # distance level 2
               control_sum += (200/32)
               travel_level = 2
               dist_traveled += 200
               dist_remaining -= 200
               subt_amnt = 200
   
            elif 400 <= dist_traveled < 600: # distance level 3
               control_sum += (200/30)
               travel_level = 3
               dist_traveled += 200
               dist_remaining -= 200
               subt_amnt = 400 # 400 for the next control location range
   
            elif 600 <= dist_traveled < 1000: # distance level 4, the final level
               control_sum += (200/28)
               travel_level = 4
    
         # Now have to deal with the remaining amount of distance that is less than 200, and based on how much have traveled
         # will decide the max speed to divide by
         # Based on the travel_level, will look in the dict to determine the right speed to use for the remaining time
         
         travel_level_dict = {0: 34, 1: 32, 2:30, 3:28, 4:26}
   
         speed_to_use = travel_level_dict[travel_level]
         control_sum += (dist_remaining/speed_to_use)
         hours_value, mins_value = find_time_val(control_sum)
    
      else: # control dist is <= 200
         if(control_dist_km == 0): # For the brevet, the first open time is just the start of the race, so don't shift the start time
            hours_value = 0
            mins_value = 0
         else:
            control_sum = control_dist_km/34
            hours_value, mins_value = find_time_val(control_sum) # For 200 and below, use 34 for speed
      
      while(mins_value >= 60):
               mins_value -= 60
               hours_value += 1
    
      return brevet_start_time.shift(hours=hours_value, minutes=mins_value)


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
   """
   Args:
      control_dist_km:  number, control distance in kilometers
         brevet_dist_km: number, nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600, or 1000
         (the only official ACP brevet distances)
      brevet_start_time:  An arrow object
   Returns:
      An arrow object indicating the control close time.
      This will be in the same time zone as the brevet start time.
   """
   # To calculate closing times, use the maximum speed from table
   # Based on the control dist, will determine min speed
   # Then, once have that speed, use the control_dist and speed to calculate hours and mins
   # Then shift the brevet start time with those hour and min values
   max_speed = 1
   hours_value = 0
   mins_value = 0
   
   max_check = control_dist_km * 1.2
   final_cp_times = {200: (13, 30), 300: (20,0), 400: (27,0), 600: (40,0), 1000: (75,0)}
   
   if(control_dist_km > max_check):
       print("ERROR control_dist exceeds the allowed distance amount")
   else:
      if(control_dist_km >= brevet_dist_km):
         # This is the last control, so check the data vals from Wiki
         # Still find the overall time if control dist is within 20km, 
         # so for 400km if control is 420km find time for 400km
         if(control_dist_km > 1000):
            control_dist_km = 1000
         elif(600 < control_dist_km < 1000):
            control_dist_km = 600
         elif(400 < control_dist_km < 600):
            control_dist_km = 400
         elif(300 < control_dist_km < 400):
            control_dist_km = 300
         elif(200 < control_dist_km < 300):
            control_dist_km = 200

         hours_last, mins_last = final_cp_times[control_dist_km]
         #print(hours)
         #print(mins)
         hours_last = int(hours_last)
         mins_last = int(mins_last)

         return brevet_start_time.shift(hours=hours_last, minutes=mins_last)

      if(control_dist_km < 60):
          #print(f"near 60km, control dist is: {control_dist_km}")
          
          # Within 60km, use cont_dist/20 + 1 hr instead of regular calcs
          hours_near = (control_dist_km // 20)
          mins_near = ((control_dist_km / 20) - hours_near) * 60
          round(mins_near)
          mins_near = int(mins_near)
          #print(f"hours_near: {hours_near} minsn: {mins_near}")
          
          hours_near += 1
          hours_near = int(hours_near)
          mins_near = int(mins_near)
          
          return brevet_start_time.shift(hours=hours_near, minutes=mins_near)
   
      elif(control_dist_km > 200):
         #print(f"control dist: {control_dist_km} is greater than 200 so doing fancy stuff")
         #Think need to add code for the wiki closing times in this elif block, if the checkpoint is the final checkpoint refer to wiki vals
         
         # If control distance is beyond 200km, do the following calculations
         dist_traveled = 0
         dist_remaining = control_dist_km
         
         travel_level = 0
         subt_amnt = 0
         control_sum = 0
            
         while((dist_remaining > 200) and ((dist_remaining-subt_amnt) > 0)):
            #print(hours_mins_dict)
            # If control is beyond 600km, have to use a different speed value for that part and for the first 600 use 15 for the speed
            # Ex for 890, have 600/15 + 290/11.428 -> 65H23
   
            if dist_traveled < 200: # Going to define each block as a certain distance level, this is distance level 1
               control_sum += (200/15)
               travel_level = 1
               dist_traveled += 200
               dist_remaining -= 200
               subt_amnt = 200
   
            elif 200 <= dist_traveled < 400: # distance level 2
               control_sum += (200/15)
               travel_level = 2
               dist_traveled += 200
               dist_remaining -= 200
               subt_amnt = 200
   
            elif 400 <= dist_traveled < 600: # distance level 3
               control_sum += (200/15)
               travel_level = 3
               dist_traveled += 200
               dist_remaining -= 200
               subt_amnt = 400 # 400 for the next control location range, 600-1000
   
            elif 600 <= dist_traveled < 1000: # distance level 4, the final level
               control_sum += (200/11.428)
               travel_level = 4
               dist_traveled += 400
               dist_remaining -= 400
               subt_amnt = 300
         
         # Now have to deal with the remaining amount of distance that is less than 200, and based on how much have traveled
         # will decide the max speed to divide by
         # Based on the travel_level, will look in the dict to determine the right speed to use
         # Max length of ACP brevet is 1000km, so for travel_level 5 just set speed to a large number, brevets with distance
         # from 1000 to 1300 use different calculator, so doesn't really apply here
         
         travel_level_dict = {0: 15, 1: 15, 2: 15, 3: 11.428, 4: 13.333}
   
         speed_to_use = travel_level_dict[travel_level]
         control_sum += (dist_remaining/speed_to_use)
         hours_value, mins_value = find_time_val(control_sum)
 
      else: # control dist is <= 200 but not within first 60km
         if(control_dist_km == 0): # For the brevet, the first close time is one hour ahead
            hours_value = 1
            mins_value = 0
         else:
            control_sum = control_dist_km/15
            hours_value, mins_value = find_time_val(control_sum) # For 200 and below, use 15 for speed
            
      while(mins_value >= 60):
        mins_value -= 60
        hours_value += 1

      hours_value = int(hours_value)
      mins_value = int(mins_value)
      
      return brevet_start_time.shift(hours=hours_value, minutes=mins_value)