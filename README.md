# Sublime BuildX

![](./demo.png)

Sublime build system is amazing. You can run/build your file/project right in the sulbime. But the annoying thing is that normally we want a side-by-side view of our build result rather than the default bottom view.

This plugin enhances sublime build system to show build output right in your side (of course you need to have two columns: View->Layout:Columns:2) and make it colorful!

## Features

- Show build output in a normal view instead of default bottom panel
- Automatically focus build output view when you build if you have >=2 columns
- Ship a syntax file for build output view so it's colorful.
- Support `Build Results->Next Result` and `Build Results->Previous Result`

## Install

## Usage

1. Add `"show_panel_on_build": false` to your sublime preference to turn off default build panel.

2. Add keybings for whatever keys you use to trigger your build.

e.g. in Mac OS, default keys to trigger build are `super+b` and `super+shift+b`. You need to add two key bindings as follows:

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
