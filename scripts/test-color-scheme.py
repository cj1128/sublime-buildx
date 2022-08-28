import sys
sys.path.insert(0, '..')

from ansi import color_mapping

# Output some content with color to test the color scheme
def run():
  for code, name in color_mapping.items():
    print(f"\x1b[0m\x1b[{code}m{name}\x1b[0m")
    print(f"\x1b[0;1;{code}m{name}.bold\x1b[0m")

if __name__ == "__main__":
  run()
