import sublime
import sublime_plugin
import re

def strip(str_index_tuple,pattern='todo'):  #TODO add case insensitivity command
	l = str_index_tuple[0].lower().find('todo')
	if l == -1:
		return None     #TODO figure out way to make this more efficient
	else:   #TODO figure out how to handle empty context, may add fuction name etc like a traceback.
		context = str_index_tuple[0][:l]
		comment = str_index_tuple[0][l+4:]
		return ('Line {}:\t{} \n {} \n'.format(str(str_index_tuple[1]),context,comment))


class TodoCommand(sublime_plugin.TextCommand): 
	def run(self, edit):   
		s = self.view.substr(sublime.Region(0,self.view.size()))  #assign s variable the selected region
		TODOs = [strip(x) for x in zip(s.split('\n'),list(range(len(s.split('\n')))))]
		TODOs = [x for x in TODOs if x is not None]
		currentFolder = "/".join(self.view.file_name().split("/")[:-1])
		fileName = self.view.file_name().split("/")[-1]
		new_contents = "In file {} \n---------- \n{} \n==========".format(fileName,"".join(TODOs))
		try:
			f = open("{}/TODO.txt".format(currentFolder),"r")
			contents = f.read()
			regex = 'In file {} \n---------- \n[\s\S]*? \n=========='.format(fileName)
			if re.search(regex,contents) is None:
				write_to_file = contents + "\n" + new_contents
			else:
				write_to_file = re.sub(regex,new_contents,contents) #TODO eliminate this call
			f.close()
		except:
			write_to_file = new_contents

		with open("{}/TODO.txt".format(currentFolder),"w") as f:
			f.write(write_to_file)


