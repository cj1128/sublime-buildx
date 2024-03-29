# Sublime BuildX

[![License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](http://mit-license.org/2016)

Show build output side by side with color!

![](./demo.gif)

Sublime build system is amazing. You can run/build your file/project right in the sulbime. But the annoying thing is that normally we want a side-by-side view of our build result rather than the default bottom view.

This plugin enhances sublime build system to show build output right in your side (of course you need to have two columns: View->Layout:Columns:2) and make it colorful!

## Features

- Show build output in a normal view instead of the default bottom panel
- Automatically focus build output view if you have >=2 columns
- Support ANSI colors
- Support `Build Results->Next Result` and `Build Results->Previous Result`

## Install

Search `buildx` in [Package Control](https://packagecontrol.io/).

## Usage

1. Add `"show_panel_on_build": false` to your sublime preference to turn off default build panel.

2. Add keybings for whatever keys you want to use to trigger the build.

e.g. If you want to use `super+b` to trigger build and `super+shift+b` to select the build target, add these key bindings:

```js
{
  "keys": ["super+b"],
  "command": "build",
  "context": [{"key": "for_buildx", "operator":"equal", "operand":true}]
},
{
  "keys": ["super+shift+b"],
  "command": "build",
  "args": {"select": true},
  "context": [{"key": "for_buildx", "operator":"equal", "operand":true}]
},
```

## Releases

### 1.3.0

- Add `clear_output_when_build_starts` setting, closes [#4](https://github.com/cj1128/sublime-buildx/issues/4).


## MIT License

Released under the [MIT license](http://mit-license.org/2020).
