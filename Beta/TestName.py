import os

n = "vivian"
counter = 0 

path = f"/home/viv/GitHub/Facial Recognition/Main/Dataset/{n}/"

filename2 = f"{n}.jpg"  #Name and 0 as original number


#print(filename)

#filename= os.path.join(path , filename)

file_name= os.path.join(path , filename2)



if os.path.isfile(file_name):
    expand = 1
    while True:
        expand += 1
        new_file_name = file_name.split(".jpg")[0] + str(expand) + ".jpg"
        if os.path.isfile(new_file_name):
            print(new_file_name)
            continue
        else:
            file_name = new_file_name
            print(file_name)
            break
        print(file_name)





            '''
            if os.path.isfile(filename2): #if  x0.jpg in file direcotry, meaning that the file exists
                print ("File exist") # working
            

                while (os.path.isfile(filename2.format(counter))): 
                    
                    
                    print("There is a file here")

                    counter +=1
                    print("files here are",counter) 

                    filename2 = f"{n}{counter}.jpg"
                    filename2= os.path.join(path , filename2)

                    print(filename2) # need this to have a different file name

                    cv2.imwrite(os.path.join(path , filename2),image) 
                    break
                '''


                '''
                counter  = 1
                while True:
                    counter  += 1
                    new_file_name = filename2.split(".jpg")[0] + str(counter ) + ".jpg" # 
                    if os.path.isfile(new_file_name):
                        print("thiss is a new file",new_file_name)
                        continue
                        cv2.imwrite(os.path.join(path , filename2),image) 
                        break
                        
                    else:
                        filename2 = new_file_name

                        print("this is not a new file name" + filename2)
                        
                        cv2.imwrite(os.path.join(path , filename2),image) 
                        break

                    #print(filename2)
                '''