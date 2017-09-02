class sentence:
    def __init__(self, window, label):
        self.window = window
        self.label = label

    def __str__(self):
        sent = ""
        for word in self.window:
            sent += word
        return "{window- " + sent + ", label- " + self.label + "}"

    def __repr__(self):
        sent = ""
        for word in self.window:
            sent += word
        return "{window- " + sent + ", label- " + self.label + "}"
