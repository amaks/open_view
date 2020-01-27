import sublime, sublime_plugin, os

class OpenViewCommand(sublime_plugin.TextCommand):

  def run(self, edit):

    file_name = self.view.file_name()
    if 'controllers' in file_name:
      source_path = os.path.dirname(file_name)
      self.find_action_view(file_name, source_path)
    else:
      region    = self.view.sel()[0]
      line      = self.view.line(region)
      line_text = self.view.substr(line)

      if '"' in line_text:
        file_name = line_text.split('"')[1]
      else:
        file_name = line_text.split('\'')[1]
      self.find_view_from_view(file_name)

  def find_view_from_view(self, file_name):
    if len(file_name) > 0:
      source          = self.view.file_name()
      source_path     = os.path.dirname(source)
      rails_view_path = os.path.dirname(source_path)

      if '/' in file_name:
        split_file_name = file_name.split('/')

        if len(split_file_name) == 2:
          new_file_name = split_file_name[0] + '/_' + split_file_name[1]
        else:
          new_file_name = split_file_name[0] + '/' + split_file_name[1] + '/_' + split_file_name[2]

        if split_file_name[0] in rails_view_path:
          file_path = rails_view_path.replace(split_file_name[0], '') + '/' + new_file_name
        else:
          if rails_view_path.split('/')[-2] == 'views':
            file_path = rails_view_path.replace(rails_view_path.split('/')[-1], '') + '/' + new_file_name
          else:
            file_path = rails_view_path + '/' + new_file_name
      else:
        new_file_name = file_name
        file_path = source_path + '/_' + new_file_name

      self.show_menu(file_path)

  def find_action_view(self, file_name, source_path):
    view_folder = file_name.split('/')[-1].split('_controller.rb')[0]

    region   = self.view.sel()[0]
    all_defs = self.view.find_all(' def ')

    for d in all_defs:
      if d < region:
        line      = self.view.line(d)
        line_text = self.view.substr(line)
        view_name = line_text.split('def ')[1].strip()

    rails_view_path = source_path.replace('controllers', 'views') + '/' + view_folder + '/'
    view_file_full_path = rails_view_path + view_name
    self.show_menu(view_file_full_path)

  def show_menu(self, file_path):
    for c in ['.haml', '.html.erb', '.html.slim', '.pdf.haml', '.pdf.erb', '.pdf.haml']:
      if os.path.isfile(file_path + c):
        sublime.active_window().open_file(file_path + c)
