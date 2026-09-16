from app.config import DEFAULT_PREVIEW_LENGTH
from app.state import AppState
from app.storage import SqliteStorage


def main():
    state = AppState()

    assert state.selected_note_id is None
    assert state.current_filter == "all"
    assert state.is_new_note is True
    assert state.pinned_first is True
    assert (
        state.preview_length
        == DEFAULT_PREVIEW_LENGTH
    )

    state.set_preferences(
        False,
        45,
    )

    assert state.pinned_first is False
    assert state.preview_length == 45

    state.set_preferences(
        True,
        DEFAULT_PREVIEW_LENGTH,
    )

    storage = SqliteStorage(
        "workspace_ilya_sender.db"
    )

    all_count = storage.count_notes("all")
    pinned_count = storage.count_notes("pinned")
    other_count = storage.count_notes("other")

    print(
        f"All notes: {all_count}"
    )
    print(
        f"Pinned notes: {pinned_count}"
    )
    print(
        f"Other notes: {other_count}"
    )
    print(
        f"Default preview: "
        f"{state.preview_length}"
    )

    storage.close()

    print("State check passed")


if __name__ == "__main__":
    main()
