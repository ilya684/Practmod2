from app.config import DB_FILE
from app.state import AppState
from app.storage import SqliteStorage


def main():
    state = AppState()

    assert state.selected_note_id is None
    assert state.current_filter == "all"
    assert state.is_new_note is True

    state.select_note(10)

    assert state.selected_note_id == 10
    assert state.is_new_note is False

    state.start_new_note()

    assert state.selected_note_id is None
    assert state.is_new_note is True

    state.set_filter("pinned")

    assert state.current_filter == "pinned"

    storage = SqliteStorage(DB_FILE)

    print("All notes:", storage.count_notes("all"))
    print("Pinned notes:", storage.count_notes("pinned"))
    print("Other notes:", storage.count_notes("other"))

    storage.close()

    print("State check passed")


if __name__ == "__main__":
    main()
