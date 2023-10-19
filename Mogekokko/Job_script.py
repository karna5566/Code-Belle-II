import subprocess,argparse,csv
parser = argparse.ArgumentParser()
parser.add_argument('-f','--File',nargs='?',help='File name',default='Qo.py')
parser.add_argument('-s','--Sample',nargs='?',help='Bucket26..36 or Prompt_data',default='Bucket26')
parser.add_argument('-n','--N_Cell', nargs='?',help='Number of cell', type=int)
parser.add_argument('-extra','--Extra', nargs='?',help='Extra command (str)', type=str)

args = parser.parse_args()





#energy = [[50,100],[100,200]]
energy = [[50,100],[100,200],[200,400],[400,1000]]

for i in [1000,4000,8000]:
	for j in energy:
		Test = subprocess.Popen(["nohup","python3",args.File,"-s",args.Sample,"-id"] + [str(id) for id in range(i,i+args.N_Cell)] + ["-e",str(j[0]),str(j[1])] + args.Extra.split())
		#Check = subprocess.run(["echo","python3",args.File,"-s",args.Sample,"-id"] + [str(id) for id in range(i,i+args.N_Cell)] + ["-e",str(j[0]),str(j[1])] + args.Extra.split() + ["&"],capture_output=True,text=True)
		#Test = subprocess.run(["python3",f"{args.File}","-h"])
		#Test = subprocess.run(["echo",f"{args.File} -s {args.Sample} -id {{{i}..{i+args.N_Cell-1}}} -e {j[0]} {j[1]} {args.Extra}"])

		print("the commandline is {}".format(Test.args))
#print(Test.stdout)
#print(Test.stderr)
#print("The exit code was: %d" % list_files.returncode)
