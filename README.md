# Sublime BuildX

source_view = window.get_output_panel("exec")

dest_view = create a new view

on_close
  set dest_view = None

- create view: window.new_file()

there can only be **one** build running.

- Listen build command
- when build
  - create/find destination view
  - focus destination view
  - listen on_modified of output panel
  - pipe output panel content to destination view

