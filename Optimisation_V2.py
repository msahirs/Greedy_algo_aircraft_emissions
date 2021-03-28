'''Greedy algorithm to select from a pool of aircraft on emission vs passenger & payload efficiency, 
given a maximum payload or fuel quota. Note that not all class variables are used for simplicity, 
but can be for a dynamic optimisation problem! Round trips are also used to integrate 
Landing-Taxi-Operation (LTO) exhausts whilst in multiple airports'''

class aircraft: #Aircraft data structure instantiator for ease of data input from [multiple] sources
    '''LTO cycle is a list of contributions from individual airports '''
    def __init__(self, model_name, mtow, PAX, pay_weight, sound_level, dep_arr_locations, ETA, 
    flight_distance, fuel_consumption,engines, NOx_ex, CO_ex, LTO_fuel, LTO_NOx, LTO_CO, cruise_ratio):
        '''Categorically passing arguments to instance variables'''
        self.aircraft_info= [model_name, mtow, PAX, pay_weight, dep_arr_locations, ETA, flight_distance, cruise_ratio]
        self.aircraft_comp=[sound_level, fuel_consumption, engines, NOx_ex, CO_ex, LTO_fuel, LTO_NOx, LTO_CO]
        self.cruise_time = self.aircraft_info[-1]*self.aircraft_info[-3] 
        ''' weight function (payload quota uncommented, fuel quota commented)'''
        self.weight = self.aircraft_info[3]
        # self.weight = 2*self.aircraft_comp[1]*self.cruise_time*self.aircraft_comp[2] + sum(self.aircraft_comp[-3])
        '''Value assigner based on [un]favourable characteristics. Note the value itself is of no physical meaning '''
        total_NOx_rt_per_km = (2*self.aircraft_comp[2]*self.cruise_time*self.aircraft_comp[3] 
        + sum(self.aircraft_comp[-2]))/self.aircraft_info[-2]
        total_CO_rt_per_km = (2*self.aircraft_comp[4]*self.cruise_time*self.aircraft_comp[2] 
        + sum(self.aircraft_comp[-1]))/self.aircraft_info[-2]
        passengers = self.aircraft_info[2]
        payload = self.aircraft_info[3]
        self.val = (passengers*payload)/(total_CO_rt_per_km*total_NOx_rt_per_km)

def maximisor(aircraft_list, cap): #Greedy function to find 'optimal' combo from a pool of type 
    #"aircraft" - given a threshold
    weights = []
    values = []
    
    for i in aircraft_list: #fill up lists with ranking arguments to perform comparisons upon
        weights.append(i.weight)
        values.append(i.val)
    '''house-keeping data'''
    storage = []
    Weight = 0
    val=0

    while(Weight <= cap and values): #Comparator function
        i = values.index(max(values)) # Find best value in values at that instant
        if weights[i] <= cap - Weight: #Check if cap is being exceeded. If not, then sum up current value with ex
            storage.append(aircraft_list[i].aircraft_info[0])
            val+=values[i]
            Weight += weights[i]
        '''Remove from pool'''
        del aircraft_list[i]
        del values[i]
        del weights[i]

    return val,storage, Weight #return 'optimal' value, selected aircraft roster, weight accumulated

'''Sample aircraft data from sources. Multiple of the same aircraft can be used, as well as those with 
different routes & passenger/payload config'''
a_A_380 = aircraft("A380 (Trent)", 575000,575,91000,25.9, ("Dublin","Lacerna"),20100,3727,2.2,4,0.06402,
0.00044,[4.0816*10**3,3.6279*10**3],[6.6950*10**1,6.4636*10**1],[2.8697*10**1,2.1847*10**1],0.9)
a_747 = aircraft('747-400 (CF6-80C2B1F)',396893,345,113000,16.7,('Dublin','Lacerna'),20100,3727,1.983,
4,0.03910476,0.00007932,[3.2794*10**3,2.9784*10**3],[4.4259*10**1,4.2836*10**1],[2.4491*10**1,1.8704*10**1],0.9)
a_737 = aircraft('737-9 (CFM56-7B26)',88314,220,23900,20.2,('Dublin','Lacerna'),20100,3727,0.999,2,0.0224775,0.0005994,
[8.6965*10**2,7.8421*10**2],[1.2243*10**1,1.1842*10**1],[6.8512,5.2449],0.9)
a_777 = aircraft('777-200LR (GE90-110B1)',347814,317,101000,17,('Dublin','Lacerna'),20100,3727,3.47,2,0.1174595,
0.0002429,[2.9143*10**3,2.6345*10**3],[6.1023*10**1,5.9594*10**1],[4.6612*10**1,3.5256*10**1],0.9)
a_A_320 = aircraft("A320-212 (CFM56-5B4/P)", 78000,160,16600,12.2, ("Dublin","Lacerna"),20100,3727,0.935,4,0.021692,
0.0008415,[8.0563*10**2,7.2699*10**2],[1.1237*10**1,1.0899*10**1],[7.9985,6.1583],0.9)
a_A_330 = aircraft("A330-322 (CF6-80E1A2)", 218000,277,70000,15.5, ("Dublin","Lacerna"),20100,3727,2.245,4,0.04941245,
0.0000898,[1.8609*10**3,1.6885*10**3],[2.7479*10**1,2.6637*10**1],[1.2633*10**1,9.6387],0.9)

aircraft_list = [a_747, a_A_380,a_737,a_777,a_A_320,a_A_330] #primitive grouping function for sample data

cap= 200000 #sample payload quota issued by a higher entity

total_val, chosen_fleet, cap_used = maximisor(aircraft_list,cap) #calculate optimal roster from list of aircraft objects
'''Output roster with weight used and total value'''
print('The chosen fleet: ', chosen_fleet)
print('Initial capacity: ', cap, 'kg', 'Capacity used: ', cap_used, 'kg')
print(total_val)     