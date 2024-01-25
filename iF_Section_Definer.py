# -*- coding: utf-8 -*-
"""
@author: Ihsan Engin Bal
Professor in Structural Safety and Earthquakes 
Hanze University of Applied Sciences Groningen, Netherlands
i.e.bal@pl.hanze.nl

This function adds RC fiber sections to an OpenSeesPy model.
"""
def RC_Beam_T_Section_2D(section_tag, hs, hb, bs, bw, cover, distance, Re, concrete_tags):    
    
    # Input format for the reinforcement variable Re
    #               bs
    #    -------------------------
    # hs | o  o   *  *  *   o  o | --> [o] Slab Reinforcement  &  [*] Top Beam Reinforcement
    #     ------|         |------
    #           |         | 
    #           |         |
    #       hb  | *     * | --> Body Reinforcement
    #           |         |
    #           |         |
    #           | * *** * | --> Bottom Reinforcement
    #           -----------
    #               bw
    
    # Assume we got 4 Fi 8 slab reinforcement, 3 Fi 16 Top Reinforcement, 2 Fi 12 Body Reinforcement and 5 Fi 20 Bottom Reinforcement
    # all from material tag 3, then the input is :
    # Re = [3, fi16, 3, 4, fi8, 3, 2, fi12, 3, 5, fi20, 3]
    # If there is no reinforcement on that line, then place zero for the number of reinforcement 
    
    import openseespy.opensees as os
    
    
    adet1=round(cover/distance)
    adet2=round(hs/distance)
    adet3=round(((hs+hb)/2-2*cover)/distance)
    adet4=round((hb-cover)/distance)
    
    os.section('Fiber', section_tag)
    # Create the concrete core fibers
    os.patch('quad',concrete_tags[0],1,adet3,-hb+cover, bw/2-cover, -hb+cover, -bw/2+cover, hs-cover, -bw/2+cover, hs-cover, bw/2-cover)	# Beam Core	
    os.patch('quad',concrete_tags[1],1,adet1,-hb, bw/2,-hb, -bw/2, -hb+cover, -bw/2, -hb+cover, bw/2) 				 # Bottom unconfined layer
    os.patch('quad',concrete_tags[1],1,adet4, -hb+cover, -bw/2+cover, -hb+cover, -bw/2, 0.0, -bw/2, 0.0, -bw/2+cover) 		 # Left unconfined layer
    os.patch('quad',concrete_tags[1],1,adet4, -hb+cover, bw/2, -hb+cover, bw/2-cover, 0.0, bw/2-cover, 0.0, bw/2) 		 # Right unconfined layer
    os.patch('quad',concrete_tags[1],1,adet1, hs-cover, bw/2-cover, hs-cover, -bw/2+cover, hs, -bw/2+cover, hs, bw/2-cover) # Unconfined part above the beam core
    os.patch('quad',concrete_tags[1],1,adet2, 0.0, -bw/2+cover, 0.0, -bs/2, hs, -bs/2, hs, -bw/2+cover)		# left unconfined slab block	  	
    os.patch('quad',concrete_tags[1],1,adet2, 0.0, bs/2, 0.0, bw/2-cover, hs, bw/2-cover, hs, bs/2)		# right unconfined slab block
    
        # Create reinforcement fibers
    if Re[0]>0:
        As=3.1415*Re[1]*Re[1]/4              # reinforcement area
        os.fiber(hs-cover, 0, Re[0]*As, Re[2])	     # Top beam reinforcement
    if Re[3]>0:
        As=3.1415*Re[4]*Re[4]/4              # reinforcement area
        os.fiber(hs-cover, 0, Re[3]*As, Re[5])	 # Slab reinforcement	
    if Re[6]>0:
        As=3.1415*Re[7]*Re[7]/4    # reinforcement area
        os.fiber(-hb+(hs+hb)/2, 0, Re[6]*As, Re[8])	  # Body reinforcement
    if Re[9]>0:
        As=3.1415*Re[10]*Re[10]/4    # reinforcement area
        os.fiber(-hb+cover, 0, Re[9]*As, Re[11])	  # Bottom reinforcement
        
    return


def RC_Rectangular_Column_Section_2D(section_tag, colDepth, colWidth, cover, distance, Re, concrete_tags):    
    
    # Input format for the reinforcement variable Re
    #           -----------
    #           | *  *  * | --> Top Reinforcement
    #           |         |
    #           | *     * | --> TopTop-body Reinforcement
    #           |         |
    #           | *     * | --> Top-body Reinforcement
    #  colDepth |         |
    #           | *     * | --> Central-body Reinforcement
    #           |         |
    #           | *     * | --> Bottom-body Reinforcement
    #           |         |
    #           | *     * | --> BottomBottom-body Reinforcement
    #           |         |
    #           | *  *  * | --> Bottom Reinforcement
    #           -----------
    #            colWidth
    
    # Assume we got 16 Fi 20 reinforcement from material tag 3, then the input is :
    # Re = [3, fi20, 3, 2, fi20, 3, 2, fi20, 3, 2, fi20, 3, 2, fi20, 3 , 2, fi20, 3, 3, fi20, 3]
    # If there is no reinforcement on that line, then place zero for the number of reinforcement 
    
    # IMPORTANT : The same functon can also be used for defining rectangular beam sections 
    
    import openseespy.opensees as os
    
    H=colDepth/2
    B=colWidth/2
    h=H-cover
    b=B-cover
    
    adet1=round(cover/distance)
    adet2=round(2*h/distance)
    
    os.section('Fiber', section_tag)
    # Create the concrete core fibers
    os.patch('quad',concrete_tags[0],1,adet2,-h,b,-h,-b,h,-b,h,b)	# Core
    os.patch('quad',concrete_tags[1],1,adet1,h,b,h,-b,H,-b,H,b)	    # Top Leaf 
    os.patch('quad',concrete_tags[1],1,adet1,-H,b,-H,-b,-h,-b,-h,b)	# Bottom Leaf
    os.patch('quad',concrete_tags[1],1,adet2,-H,-b,-H,-B,H,-B,H,-b)	# Left Leaf
    os.patch('quad',concrete_tags[1],1,adet2,-H,B,-H,b,H,b,H,B)	    # Right Leaf
    # Create reinforcement fibers
    if Re[0]>0:
        As=3.1415*Re[1]*Re[1]/4              
        os.fiber(h, 0, Re[0]*As, Re[2])	          # Top reinforcement
    if Re[3]>0:
        As=3.1415*Re[4]*Re[4]/4              
        os.fiber(2*h/3, 0, Re[3]*As, Re[5])	      # TopTop-body reinforcement	
    if Re[6]>0:
        As=3.1415*Re[7]*Re[7]/4              
        os.fiber(h/3, 0, Re[6]*As, Re[8])	      # Top-body reinforcement	
    if Re[9]>0:
        As=3.1415*Re[10]*Re[10]/4    
        os.fiber(0, 0, Re[9]*As, Re[11])	      # Central-body reinforcement
    if Re[12]>0:
        As=3.1415*Re[13]*Re[13]/4    
        os.fiber(-h/3, 0, Re[12]*As, Re[14])	  # Bottom-body reinforcement
    if Re[15]>0:
        As=3.1415*Re[16]*Re[16]/4    
        os.fiber(-2*h/3, 0, Re[15]*As, Re[17])	  # BottomBottom-body reinforcement
    if Re[18]>0:
        As=3.1415*Re[19]*Re[19]/4    
        os.fiber(-h, 0, Re[18]*As, Re[20]) 	      # Bottom reinforcement
        
def RC_Rectangular_Long_Column_Section_2D(section_tag, colDepth, colWidth, cover, distance, edge_Re, body_Re, concrete_tags):    
    
    # Input format for the reinforcement variables edge_Re and body_Re
    #           -----------
    #           | *  *  * | --> Edge reinforcement
    #           |         |    
    #           | *     * |    \
    #           |         |    |         
    #           | *     * |    | 
    #           |         |    |
    #           | *     * |    \   Body Reinforcement 
    #  colDepth |         |    /
    #           | *     * |    |    
    #           |         |    |
    #       --------/\  -----
    #           |     \/  |    |  
    #           |         |    |
    #           | *     * |    / 
    #           |         |    
    #           | *  *  * | --> Edge Reinforcement
    #           -----------
    #            colWidth
    
    # Assume we got 3 Fi 20 at each edge as Edge Reinforcement and a total of 16 Fi 20 at the body as Body Reinforcemet 
    # We go a total of 22 Fi 20 reinforcement in this column, from material tag 3, then the input is :
    # edge_Re = [3, fi20, 3]
    # body_Re = [16, fi20, 3]
    
    import openseespy.opensees as os
    
    H=colDepth/2
    B=colWidth/2
    h=H-cover
    b=B-cover
    
    adet1=round(cover/distance)
    adet2=round(2*h/distance)
    
    os.section('Fiber', section_tag)
    # Create the concrete core fibers
    os.patch('quad',concrete_tags[0],1,adet2,-h,b,-h,-b,h,-b,h,b)	# Core
    os.patch('quad',concrete_tags[1],1,adet1,h,b,h,-b,H,-b,H,b)	    # Top Leaf 
    os.patch('quad',concrete_tags[1],1,adet1,-H,b,-H,-b,-h,-b,-h,b)	# Bottom Leaf
    os.patch('quad',concrete_tags[1],1,adet2,-H,-b,-H,-B,H,-B,H,-b)	# Left Leaf
    os.patch('quad',concrete_tags[1],1,adet2,-H,B,-H,b,H,b,H,B)	    # Right Leaf
    # Create reinforcement fibers
    
    # Add top edge reinforcement
    As=3.1415*edge_Re[1]*edge_Re[1]/4              # reinforcement area
    os.fiber(h, 0, edge_Re[0]*As, edge_Re[2])	   # Top edge reinforcement
    
    # Add bottom edge reinforcement
    os.fiber(-h, 0, edge_Re[0]*As, edge_Re[2])	   # Bottom edge reinforcement
        
    # Add body reinforcements
    As=3.1415*body_Re[1]*body_Re[1]/4              # reinforcement area
    
    # Distribute the reinforcement to the two sides of the section equally    
    re_num = int(body_Re[0]/2)
    re_spacing = 2 * h / (re_num + 1)
        
    for rbr in range(re_num):
        os.fiber(h - re_spacing * (rbr + 1), 0, 2 * As, body_Re[2])	 # Add a body reinforcement	
        

def RC_Rectangular_Wall_Section_2D(section_tag, wallDepth, wallWidth, wallHeadDepth, cover, distance, head_edge_Re, head_body_Re, body_Re, concrete_tags):    
    
    # !! wallDepth is the section depth of the entire wall, including the head columns
    # !! This section uses 3 types of concrete materials: fully confined at the head columns, lightly confined at the wall body, 
    #    and unconfined at the cover concrete listed as concrete_tags[0], concrete_tags[1] and concrete_tags[2], respectively.
    
    
    # Input format for the reinforcement variables edge_Re and body_Re
    #
    #
    #               ------------
    #               |----------|
    #               || * *** *|| --> Head Column Edge Reinforcement - Top
    #               || *     *||   |
    #               ||        ||   \ Head Column Body Reinforcement
    #               || *     *||   /
    #               ||        ||   |
    #               || *  *  *|| --> Head Column Edge Reinforcement - Bottom
    #               |----------|   
    #               | *      * |    \
    #               |          |    |         
    #               | *      * |    | 
    #               |          |    |
    #               | *      * |    |    
    #               |          |    |
    #               | *      * |    \   Wall Body Reinforcement 
    #               |          |    /
    #               | *      * |    |
    #               |          |    |         
    #               | *      * |    | 
    #               |          |    |
    #               | *      * |    |   
    #               |          |    |
    #               | *      * |    /    
    #               |          |    
    #               |----------|
    #               || *  *  *|| --> Head Column Edge Reinforcement - Bottom
    #               ||        ||   |
    # wallHeadDepth || *     *||   \ Head Column Body Reinforcement
    #               ||        ||   /
    #               || *     *||   |
    #               || * *** *|| --> Head Column Edge Reinforcement - Top
    #               |----------|
    #               ------------
    #                 wallWidth
    
    # Assume we got :
    # 5 Fi 20 as the Head Column Edge Reinforcement at the TOP ROW of the head column
    # 3 Fi 20 as the Head Column Edge Reinforcement at the BOTTOM ROW of the head column
    # 4 Fi 20 as the body reinforcement of the head column (remaining reinforecement)
    # 12 Fi 12 as the body reinforcement of the wall body
    # All reinforcement is made of material tag 3, then the input is :
    # head_edge_Re = [5, Fi20, 3, 3, Fi20, 3]
    # head_body_Re = [4, Fi20, 3] 
    # body_Re = [12, Fi12, 3]
    
    import openseespy.opensees as os
    
    H=wallDepth/2
    B=wallWidth/2
    h=H-cover
    b=B-cover
    
    adet1 = round(cover/distance) # Number of slices of the cover concrete in the working direction of the section
    adet2 = round((wallDepth - wallHeadDepth) / distance)   # Number of mesh slices of the wall body only
    adet3 = round((wallHeadDepth - cover) / distance)  # Number of mesh slices for the head columns
    
    os.section('Fiber', section_tag)
    # Create the concrete core fibers
    
    # Top head column
    os.patch('quad',concrete_tags[0],1,adet3, H-wallHeadDepth , b , H-wallHeadDepth ,-b, h, -b, h, b)	# Head Column Core
    os.patch('quad',concrete_tags[2],1,adet1, h, b, h, -b, H, -b, H, b)	    # Top Leaf 
    os.patch('quad',concrete_tags[2],1,adet3, H-wallHeadDepth, -b, H-wallHeadDepth,-B, H, -B, H, -b)	# Left Leaf Head Column
    os.patch('quad',concrete_tags[2],1,adet3, H-wallHeadDepth, B, H-wallHeadDepth, b, H, b, H, B)	    # Right Leaf Head Column
    
    # Bottom head column
    os.patch('quad',concrete_tags[0],1,adet3, -h , b , -h ,-b, -H + wallHeadDepth, -b, -H + wallHeadDepth, b)	# Head Column Core
    os.patch('quad',concrete_tags[2],1,adet1, -H, b, -H, -b, -h, -b, -h, b)	    # Top Leaf 
    os.patch('quad',concrete_tags[2],1,adet3, -H, -b, -H,-B, -H + wallHeadDepth, -B, -H + wallHeadDepth, -b)	# Left Leaf Head Column
    os.patch('quad',concrete_tags[2],1,adet3, -H, B, -H, b, -H + wallHeadDepth, b, -H + wallHeadDepth, B)	    # Right Leaf Head Column
    
    # Main Body of the RC Wall
    os.patch('quad',concrete_tags[1],1,adet2,-H + wallHeadDepth, b, -H + wallHeadDepth, -b, H - wallHeadDepth, -b, H - wallHeadDepth, b)	# Wall Body Core
    os.patch('quad',concrete_tags[2],1,adet2,-H + wallHeadDepth,-b, -H + wallHeadDepth,-B, H - wallHeadDepth, -B, H - wallHeadDepth,-b)	# Left Leaf
    os.patch('quad',concrete_tags[2],1,adet2,-H + wallHeadDepth, B, -H + wallHeadDepth, b, H - wallHeadDepth, b, H - wallHeadDepth, B)	    # Right Leaf
    
    
    # Create reinforcement fibers
    
    # Add head column TOP edge reinforcement
    As=3.1415 * head_edge_Re[1]*head_edge_Re[1]/4              # reinforcement area
    os.fiber(H - cover, 0, head_edge_Re[0]*As, head_edge_Re[2])	   # Head column TOP edge reinforcement    
    As=3.1415*head_edge_Re[4]*head_edge_Re[4]/4              # reinforcement area
    os.fiber(H - wallHeadDepth, 0, head_edge_Re[3]*As, head_edge_Re[5])	   # Head column BOTTOM edge reinforcement    
    
    
    # Add head column BOTTOM edge reinforcement
    As=3.1415 * head_edge_Re[1]*head_edge_Re[1]/4              # reinforcement area
    os.fiber(-H + cover, 0, head_edge_Re[0]*As, head_edge_Re[2])	   # Head column TOP edge reinforcement    
    As=3.1415*head_edge_Re[4]*head_edge_Re[4]/4              # reinforcement area
    os.fiber(-H + wallHeadDepth, 0, head_edge_Re[3]*As, head_edge_Re[5])	   # Head column BOTTOM edge reinforcement
    
    
    # Add body reinforcements of the TOP and BOTTOM head columns
    As=3.1415*head_body_Re[1]*head_body_Re[1]/4              # reinforcement area    
    # Distribute the reinforcement to the two sides of the section equally    
    re_num = int(head_body_Re[0]/2)
    re_spacing = (wallHeadDepth - cover) / (re_num + 1)
    for rbr in range(re_num):
        os.fiber(H - cover - re_spacing * (rbr + 1), 0, 2*As, head_body_Re[2])	 # Add a body reinforcement	to the TOP head column
        os.fiber(-H + cover + re_spacing * (rbr + 1), 0, 2*As, head_body_Re[2])	 # Add a body reinforcement	to the BOTTOM head column
    
    # Add the BODY reinforcements of the wall body
    As=3.1415*body_Re[1]*body_Re[1]/4              # reinforcement area
    # Distribute the reinforcement to the two sides of the section equally    
    re_num = int(body_Re[0]/2)
    re_spacing = (wallDepth - 2 * wallHeadDepth) / (re_num + 1)
        
    for rbr in range(re_num):
        os.fiber(H - wallHeadDepth - re_spacing * (rbr + 1), 0, 2*As, body_Re[2])	 # Add a body reinforcement	
                
        
    return
