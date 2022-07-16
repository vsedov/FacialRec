import os
# new Stuff for import of paths
import os.path
import pathlib
import shutil



from Adding_Upgrading import list_files



def remove():
	

	List= str(input("Please enter yes or not if you want to see a listing of who you want to remove "))

	if List.lower() == "yes":

		pathds = '/home/viv/GitHub/Facial Recognition/Main/Dataset/'
		print("Path to Direcotry", pathds)



		list_files(pathds)

		name = str(input("Please enter the name that you would like to remove"))
		shutil.rmtree('/home/viv/GitHub/Facial Recognition/Main/Dataset/' + f"{name}",ignore_errors=True)

		print(f"you have removed Folder  :{name} from the data set ")


if '__main__' == __name__:
    remove()

