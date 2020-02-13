# The binary values of each tag orientaiton is determoined and stored to comapare for the proper substition of the 'Lena' image onto the tag.
BinaryTag_Pattern1 = [[0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],[0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],[1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0]]

BinaryTag_Pattern2 = [[0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],[1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0],[0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1]]

BinaryTag_Pattern3 = [[0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],[1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0],[0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],[0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1]]

BinaryTag_Pattern4 = [[0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1],[0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],[1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0]]

BinaryTag_Pattern5 = [[1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],[0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0],[0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1],[0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0]]

MulTag_Table=[BinaryTag_Pattern1, BinaryTag_Pattern2, BinaryTag_Pattern3, BinaryTag_Pattern4,BinaryTag_Pattern5]

 
# Comapring the binary values obtained thorugh program and the manually determined binary values to determoine the tag orientation
def Compare_Binary_ID(Binary_ID):
    
    IDTag_Recog = False
    Count_Rot = None
    Repl_TagVal = None
    
    for iteration in BinaryTag_Pattern1:        
        for idx, val in enumerate (BinaryTag_Pattern1):    
            if Binary_ID == val: 
                IDTag_Recog = True
                Count_Rot = idx
                Repl_TagVal = BinaryTag_Pattern1[idx]
            #print ("No.of.rotation", idx)
            #print ("Coressp Pattern",Repl_TagVal)
                break
        if IDTag_Recog: break

    for iteration in BinaryTag_Pattern4:        
        for idx, val in enumerate (BinaryTag_Pattern4):    
            if Binary_ID == val: 
                IDTag_Recog = True
                Count_Rot = idx
                Repl_TagVal = BinaryTag_Pattern4[idx]
            #print ("No.of.rotation", idx)
            #print ("Coressp Pattern",Repl_TagVal)
                break
        if IDTag_Recog: break


    for iteration in BinaryTag_Pattern5:        
        for idx, val in enumerate (BinaryTag_Pattern5):    
            if Binary_ID == val: 
                IDTag_Recog = True
                Count_Rot = idx
                Repl_TagVal = BinaryTag_Pattern5[idx]
            #print ("No.of.rotation", idx)
            #print ("Coressp Pattern",Repl_TagVal)
                break
        if IDTag_Recog: break


    for iteration in BinaryTag_Pattern2:        
        for idx, val in enumerate (BinaryTag_Pattern2):    
            if Binary_ID == val: 
                IDTag_Recog = True
                Count_Rot = idx
                Repl_TagVal = BinaryTag_Pattern2[idx]
            #print ("No.of.rotation", idx)
            #print ("Coressp Pattern",Repl_TagVal)
                break
        if IDTag_Recog: break

    for iteration in BinaryTag_Pattern3:        
        for idx, val in enumerate (BinaryTag_Pattern3):    
            if Binary_ID == val: 
                IDTag_Recog = True
                Count_Rot = idx
                Repl_TagVal = BinaryTag_Pattern3[idx]
            #print ("No.of.rotation", idx)
            #print ("Coressp Pattern",Repl_TagVal)
                break
        if IDTag_Recog: break

    #When the binary pattern is detected then it is returned along woth its orientation positoin which helps in super imposing the image
    return (IDTag_Recog, Count_Rot, Repl_TagVal)

    

