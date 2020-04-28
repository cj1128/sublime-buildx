import sublime
import sublime_plugin
from os.path import join

target_view_name = 'Build Output'

class BuildX:
  def __init__(self):
    self.source_view = None
    self.window = None

    self.target_view = None
    self.build_inited = False
    self.source_last_pos = 0
    self.is_waiting = False

  def get_target_view(self):
    if self.target_view is not None:
      return self.target_view

    # Find views with name
    found = None
    for view in self.window.views():
      if view.name() == target_view_name:
        found = view
        break

    if found is not None:
      self.target_view = found
      return found

    # create a view
    view = self.window.new_file()
    view.set_name(target_view_name)
    view.set_scratch(True)

    view.set_syntax_file("Packages/sublime-buildx/Build Output.sublime-syntax")

    self.target_view = view
    return view

  def on_build_start(self):
    self.build_inited = True
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
      self.window.focus_view(self.target_view)
      self.window.focus_view(original_view)

    self.target_view.run_command('content_clear')
    self.source_last_pos = 0

  def pipe_text(self):
    self.is_waiting = False
    new_pos = self.source_view.size()

    region = sublime.Region(self.source_last_pos, new_pos)
    self.target_view.run_command('content_replace', {'start': self.source_last_pos, 'end': new_pos, 'text': self.source_view.substr(region)})
    self.source_last_pos = new_pos

    # scroll to bottom
    self.target_view.show(self.target_view.size())

  def on_source_modified(self):
    if self.is_waiting:
      return

    # if build is very fast
    # we will see no change in build output
    # delay 100ms so that we can see the content is flashing
    if self.build_inited == False:
      self.on_build_start()
      self.is_waiting = True
      sublime.set_timeout(self.pipe_text, 100)
    else:
      self.pipe_text()

  def on_source_selection_modified(self):
    if len(self.source_view.sel()) == 0:
      return

    target = self.source_view.sel()[0]
    if target.a == target.b:
      return

    sel = self.target_view.sel()
    sel.clear()
    sel.add(target)

    # scroll to selection region
    self.target_view.show(target.a)

    # jump to target view and back to refresh selection
    origin = self.window.active_view()
    self.window.focus_view(self.target_view)
    self.window.focus_view(origin)

class BuildXListener(sublime_plugin.EventListener):
  def __init__(self):
    # map output panel view id -> buildx object
    self.buildx_map = {}

  # view is exec output panel view
  def get_buildx(self, view):
    if view is None:
      return None

    return self.buildx_map.get(view.id())

  def set_buildx(self, buildx, view):
    self.buildx_map[view.id()] = buildx

  def on_modified(self, view):
    buildx = self.get_buildx(view)
    if buildx is None:
      return

    if view.id() != buildx.source_view.id():
      return

    buildx.on_source_modified()

  def on_selection_modified(self, view):
    buildx = self.get_buildx(view)
    if buildx is None:
      return

    if view.id() != buildx.source_view.id():
      return

    buildx.on_source_selection_modified()

  def on_close(self, view):
    if view.name() != target_view_name:
      return

    for _, buildx in self.buildx_map.items():
      if buildx.target_view is None:
        continue

      if buildx.target_view.id() == view.id():
        buildx.target_view = None

  def on_query_context(self, view, key, *args):
    if key != 'for_buildx':
      return None

    source_view = view.window().get_output_panel('exec')
    buildx = self.get_buildx(source_view)
    if buildx is None:
      buildx = BuildX()
      buildx.source_view = source_view
      buildx.window = view.window()
      self.set_buildx(buildx, source_view)

    buildx.build_inited = False

    return None

class ContentReplace(sublime_plugin.TextCommand):
  def run(self, edit, start, end, text):
    self.view.replace(edit, sublime.Region(start, end), text)

class ContentClear(sublime_plugin.TextCommand):
  def run(self, edit):
    region = sublime.Region(0, self.view.size())
    self.view.erase(edit, region)
