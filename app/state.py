class AppState:
    def __init__(self):
        self.selected_note_id = None
        self.current_filter = "all"
        self.is_new_note = True

    def select_note(self, note_id):
        self.selected_note_id = note_id
        self.is_new_note = False

    def start_new_note(self):
        self.selected_note_id = None
        self.is_new_note = True

    def set_filter(self, filter_name):
        self.current_filter = filter_name
