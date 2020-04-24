import sublime
import sublime_plugin

class BuildX:
  target_view_name = 'Build Output'

  def __init__(self):
    self.source_view = None
    self.window = None

    self.target_view = None
    self.build_started = False
    self.source_last_pos = 0

  def get_target_view(self):
    if self.target_view is not None:
      return self.target_view

    # Find views with name
    found = None
    for view in self.window.views():
      if view.name() == self.target_view_name:
        found = view
        break

    if found is not None:
      self.target_view = found
      return found

    # create a view
    view = self.window.new_file()
    view.set_name(self.target_view_name)
    view.set_scratch(True)

    self.target_view = view
    return view

  def on_build_start(self):
    self.build_started = True
    window = self.window
    original_view = window.active_view()

    # focus target view in other group
    if window.num_groups() > 1:
      self.target_view = self.get_target_view()
      group_index, index = window.get_view_index(self.target_view)

      # move target view to other group
      if group_index == window.active_group():
        target_group_index = (window.active_group() + 1) % window.num_groups()
        window.set_view_index(self.target_view, target_group_index, 0)

      # focus target view
      print(original_view.file_name())
      self.window.focus_view(self.target_view)
      self.window.focus_view(original_view)

    self.target_view.run_command('content_clear')
    self.source_last_pos = 0

  def pipe_text(self):
    new_pos = self.source_view.size()
    region = sublime.Region(self.source_last_pos, new_pos)
    self.target_view.run_command('content_replace', {'start': self.source_last_pos, 'end': new_pos, 'text': self.source_view.substr(region)})
    self.source_last_pos = new_pos

  def on_source_modified(self):
    if self.build_started == False:
      self.on_build_start()

    self.pipe_text()

    # scroll to bottom
    self.target_view.show(self.target_view.size())

class BuildListener(sublime_plugin.EventListener):
  def __init__(self):
    self.buildx = BuildX()

  def on_modified(self, view):
    if self.buildx.source_view is None:
      return

    if view.id() != self.buildx.source_view.id():
      return

    self.buildx.on_source_modified()

  def on_close(self, view):
    if self.buildx.target_view is None:
      return

    if self.buildx.target_view.id() == view.id():
      self.buildx.target_view = None

  def on_query_context(self, view, key, *args):
    if key != 'for_buildx':
      return None

    buildx = self.buildx

    buildx.source_view = view.window().get_output_panel('exec')
    buildx.window = view.window()
    buildx.build_started = False

    return None



