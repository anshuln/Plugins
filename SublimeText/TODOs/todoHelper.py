import sublime
import sublime_plugin

def strip(str_index_tuple,pattern='todo'):	#TODO add case insensitivity command
	l = str_index_tuple[0].lower().find('todo')
	if l == -1:
		return None		#TODO figure out way to make this more efficient
	else:	#TODO figure out how to handle empty context, may add fuction name etc like a traceback.
		context = str_index_tuple[0][:l]
		comment = str_index_tuple[0][l+4:]
		return ('In line {}:\t{} \n {}'.format(str(str_index_tuple[1]),context,comment))


class TodoCommand(sublime_plugin.TextCommand): 
	def run(self, edit):   
		s = self.view.substr(sublime.Region(0,self.view.size()))  #assign s variable the selected region
		TODOs = [strip(x) for x in zip(s.split('\n'),list(range(len(s.split('\n')))))]
		TODOs = [x for x in TODOs if x is not None]
		# print(TODOs)
		print(TODOs)

