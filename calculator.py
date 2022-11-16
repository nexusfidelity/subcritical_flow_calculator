import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Flow Calculator",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Subcritical Flow Calculator")

col1, col2, col3 = st.columns([1, 1, 3])

#initial variable
with col1:
    n = st.number_input('n',value=0.02)
    slope = st.number_input('ib',value=float(1/1000),step=5.0)
    B = st.number_input('B',value=200.0)
    x = st.number_input('x',value=5000)
    delta_x = st.number_input('delta_x',value=500)
# n = 0.02
# slope = float(1/1000)
# B = 200.0

#initial at downstream

with col2:
    q = st.number_input('Q',value=2000.0)
    h2 = st.number_input('h2',value=5)
    z2 = st.number_input('z2',value=0.0)
# q = 2000.0
# h2 = 5
# z2 = 0.0

#default var
g = 9.81
e = 10**-4
h1_assumption = 5
#distance
# x = 5000
# delta_x = 500.0
x_increment = delta_x

delta_x_list=[]
river_bed = []
river_height = []
uniform_flow = []
Ø3_list = []

if x%delta_x != 0:
    print('input is not acceptable')
else:
    river_bed.append(z2)
    river_height.append(h2)
    delta_x_list.append(delta_x)
    i=x/delta_x
    
    Ø1 = (q**2)/((2*g)*(B**2))
    Ø2 = -(q**2)*((n**2)*(x_increment))/(2*(B**2))
    
    
    for x in range(int(i)-1):
        z = slope*delta_x
        river_bed.append(z)
        delta_x = delta_x + x_increment
        delta_x_list.append(delta_x)
    
    Ø3 = river_bed[1]-river_bed[0]-h2-((q**2)/(((2*g)*(B**2))*(h2**2)))-((q**2)*((n**2)*(x_increment))/((2*(B**2))*(h2**(10/3))))
    f_h = h1_assumption + (Ø1/(h1_assumption**2)) + (Ø2/(h1_assumption**(10/3))) + Ø3
    
    while True:
        altf_h=1.0-2.0*(Ø1/(h1_assumption**3))-(10/3)*(Ø2/h1_assumption**(13/3))
        # print(altf_h)
        delta_h=-(f_h/altf_h)
        # print(delta_h)
        h1_assumption=h1_assumption+delta_h
        # print(h_new)
        f_h = h1_assumption + (Ø1/(h1_assumption**2)) + (Ø2/(h1_assumption**(10/3))) + Ø3
        #print(f_h)
        if f_h<e:
            # print(h1_assumption)
            river_height.append(h1_assumption)
            break

    
    start_loop = 2
    while True:
        Ø3 = river_bed[start_loop]-river_bed[start_loop-1]-h1_assumption-((q**2)/(((2*g)*(B**2))*(h1_assumption**2)))-((q**2)*((n**2)*(x_increment))/((2*(B**2))*(h1_assumption**(10/3))))
        f_h = h1_assumption + (Ø1/(h1_assumption**2)) + (Ø2/(h1_assumption**(10/3))) + Ø3
        while True:
            altf_h=1.0-2.0*(Ø1/(h1_assumption**3))-(10/3)*(Ø2/h1_assumption**(13/3))
            # print(altf_h)
            delta_h=-(f_h/altf_h)
            # print(delta_h)
            h1_assumption=h1_assumption+delta_h
            # print(h_new)
            f_h = h1_assumption + (Ø1/(h1_assumption**2)) + (Ø2/(h1_assumption**(10/3))) + Ø3
            #print(f_h)
            if f_h<e:
                # print(h1_assumption)
                river_height.append(h1_assumption)
                break
        if len(river_height)==len(river_bed):
            break
        
    #
    from operator import add
    total_height = list(map(add, river_bed, river_height) )
    
    # import math
    # uniform_flow_depth = ((q*n)/B*(math.sqrt(slope)))**(3/5)
    # uniform_flow = [x+uniform_flow_depth for x in river_bed]
    
    # print(river_bed)
    # print(uniform_flow)
    
    # visualize the data
    fig, ax = plt.subplots()
    plt.plot(delta_x_list,river_bed, label = "riverbed")
    # plt.plot(delta_x_list,uniform_flow, label = "uniform_flow_depth")
    plt.plot(delta_x_list,total_height, linestyle = 'dotted')
    # plt.show()
    
with col3:
    
    st.pyplot(fig)

def load_data():
    return pd.DataFrame(
        {
            "riverbed height": river_bed,
            "true h at each interval": river_height,
            "total height":total_height
        }
    )

# Boolean to resize the dataframe, stored as a session state variable
# st.checkbox("Use container width", value=False, key="use_container_width")

df = load_data()
st.dataframe(df)
