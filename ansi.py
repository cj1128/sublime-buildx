class Reader:
  def __init__(self, str):
    self.str = str
    self.length = len(str)
    self.index = 0

  def next(self):
    if self.is_empty():
      return ""

    result = self.str[self.index]
    self.index += 1
    return result

  def read(self, n):
    end = self.index + n
    if end > self.length:
      end = self.length
    result = self.str[self.index:end]
    self.index = end
    return result

  def read_until(self, char):
    if self.is_empty():
      return ""

    end = self.index
    found = False
    while end < self.length - 1:
      if self.str[end] == char:
        found = True
        break

      end += 1

    if found:
      result = self.str[self.index:end]
      self.index = end + 1
      return result
    else:
      return ""

  def read_int(self):
    str = ""
    while self.peek(1) in "0123456789":
      str += self.next()

    return int(str)

  def peek(self, n):
    return self.str[self.index:self.index+n]

  def is_empty(self):
    return self.index >= self.length

# [0m
# [1m
# [38;5;{0-15}m
# [{30-37,90-97}m
# compound: [0;1;{30-37,90-97}m
class ANSIProcessor:
  color_mapping = {
    30: "black",
    31: "red",
    32: "green",
    33: "yellow",
    34: "blue",
    35: "magenta",
    36: "cyan",
    37: "white",
    90: "bright_black",
    91: "bright_red",
    92: "bright_green",
    93: "bright_yellow",
    94: "bright_blue",
    95: "bright_magenta",
    96: "bright_cyan",
    97: "bright_white",
  }

  def __init__(self):
    self.bold = False
    self.color = "default"
    self.char_index = 0
    self.start_index = 0
    self.end_index = 0

  # num:
  #   - 0 ~ 15
  #   - 30 ~ 37
  #   - 90 ~ 97
  def get_color(self, num):
    index = num

    if num >= 0 and num <= 7:
      index = 30 + num % 8

    if num >= 8 and num <= 15:
      index = 90 + num % 8

    return ANSIProcessor.color_mapping[index]

  def clear(self):
    self.bold = False
    self.color = "default"
    self.char_index = 0
    self.start_index = 0
    self.end_index = 0

  def reset(self):
    self.start_index = self.char_index
    self.bold = False
    self.color = "default"

  def current_region(self):
    return (self.start_index, self.end_index, self.color, self.bold)

  def error(self, params):
    print("[ANSIProcessor] unsupported: %s" % params)
    # for debug
    # yield "[ANSIProcessor] unsupported: %s" % params

  # 假定 str 中包含完整的控制字符
  # 遇到 \033[0m 输出 region
  def process(self, str):
    r = Reader(str)

    while not r.is_empty():
      char = r.next()

      if char != "\x1b":
        yield ("char", (self.char_index, char))
        self.char_index += 1
        continue

      if r.next() != "[":
        yield ("char", (self.char_index, char))
        self.char_index += 1
        continue

      params_str = r.read_until("m")
      if params_str == "":
        continue

      params = [int(s) for s in params_str.split(";")]

      if params == [0]:
        self.end_index = self.char_index
        if self.start_index != self.end_index and (self.color != "default" or self.bold != False):
          yield ("region", self.current_region())
        self.reset()
      elif params[:2] == [38, 5]:
        color_int = params[2]
        if color_int >= 0 and color_int <= 15:
          self.color = self.get_color(color_int)
        else:
          self.error(params)
      else:
        for p in params:
          if p == 0:
            self.start_index = self.char_index
          elif p == 1:
            self.bold = True
            self.color = "white"
          elif (p >= 30 and p <= 37) or (p >= 90 and p <= 97):
            self.color = self.get_color(p)
          else:
            self.error(params)
