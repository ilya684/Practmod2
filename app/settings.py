from PySide6.QtCore import QByteArray, QObject, QSettings, Signal

from app.config import ORG_NAME


class AppSettings(QObject):
    settings_changed = Signal()

    FONT_SIZE_KEY = "ui/font_size"
    PREVIEW_LENGTH_KEY = "ui/preview_length"
    AUTOSAVE_KEY = "editor/autosave"
    AUTOSAVE_INTERVAL_KEY = "editor/autosave_interval_s"
    CONFIRM_DELETE_KEY = "editor/confirm_delete"
    LOG_LEVEL_KEY = "logging/level"
    WINDOW_GEOMETRY_KEY = "window/geometry"
    WINDOW_STATE_KEY = "window/state"

    DEFAULT_FONT_SIZE = 12
    DEFAULT_PREVIEW_LENGTH = 40
    DEFAULT_AUTOSAVE = True
    DEFAULT_AUTOSAVE_INTERVAL = 30
    DEFAULT_CONFIRM_DELETE = True
    DEFAULT_LOG_LEVEL = "INFO"
    RECENT_EXPORTS_KEY = "exports/recent"
    RECENT_EXPORTS_KEY = "exports/recent"

    MIN_FONT_SIZE = 8
    MAX_FONT_SIZE = 32
    MIN_PREVIEW_LENGTH = 10
    MAX_PREVIEW_LENGTH = 200
    MIN_AUTOSAVE_INTERVAL = 5
    MAX_AUTOSAVE_INTERVAL = 600

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings(ORG_NAME, "NotesManager")

    def _int_value(self, key, default, minimum, maximum):
        try:
            value = int(self.settings.value(key, default))
        except (TypeError, ValueError):
            value = default

        return max(minimum, min(value, maximum))

    def _bool_value(self, key, default):
        value = self.settings.value(key, default)

        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            normalized = value.strip().lower()

            if normalized in {"true", "1", "yes"}:
                return True

            if normalized in {"false", "0", "no"}:
                return False

        return default

    def _str_value(self, key, default, allowed):
        value = self.settings.value(key, default)

        if isinstance(value, str) and value in allowed:
            return value

        return default

    @property
    def font_size(self):
        return self._int_value(
            self.FONT_SIZE_KEY,
            self.DEFAULT_FONT_SIZE,
            self.MIN_FONT_SIZE,
            self.MAX_FONT_SIZE,
        )

    @property
    def preview_length(self):
        return self._int_value(
            self.PREVIEW_LENGTH_KEY,
            self.DEFAULT_PREVIEW_LENGTH,
            self.MIN_PREVIEW_LENGTH,
            self.MAX_PREVIEW_LENGTH,
        )

    @property
    def autosave(self):
        return self._bool_value(
            self.AUTOSAVE_KEY,
            self.DEFAULT_AUTOSAVE,
        )

    @property
    def autosave_interval_s(self):
        return self._int_value(
            self.AUTOSAVE_INTERVAL_KEY,
            self.DEFAULT_AUTOSAVE_INTERVAL,
            self.MIN_AUTOSAVE_INTERVAL,
            self.MAX_AUTOSAVE_INTERVAL,
        )

    @property
    def confirm_delete(self):
        return self._bool_value(
            self.CONFIRM_DELETE_KEY,
            self.DEFAULT_CONFIRM_DELETE,
        )

    @property
    def log_level(self):
        return self._str_value(
            self.LOG_LEVEL_KEY,
            self.DEFAULT_LOG_LEVEL,
            {"INFO", "DEBUG"},
        )

    @property
    def window_geometry(self):
        value = self.settings.value(
            self.WINDOW_GEOMETRY_KEY,
            QByteArray(),
        )

        return value if isinstance(value, QByteArray) else QByteArray()

    @property
    def window_state(self):
        value = self.settings.value(
            self.WINDOW_STATE_KEY,
            QByteArray(),
        )

        return value if isinstance(value, QByteArray) else QByteArray()

    def set_font_size(self, value):
        value = max(
            self.MIN_FONT_SIZE,
            min(int(value), self.MAX_FONT_SIZE),
        )
        self.settings.setValue(self.FONT_SIZE_KEY, value)
        self.settings_changed.emit()

    def set_preview_length(self, value):
        value = max(
            self.MIN_PREVIEW_LENGTH,
            min(int(value), self.MAX_PREVIEW_LENGTH),
        )
        self.settings.setValue(
            self.PREVIEW_LENGTH_KEY,
            value,
        )
        self.settings_changed.emit()

    def set_autosave(self, value):
        self.settings.setValue(
            self.AUTOSAVE_KEY,
            bool(value),
        )
        self.settings_changed.emit()

    def set_autosave_interval_s(self, value):
        value = max(
            self.MIN_AUTOSAVE_INTERVAL,
            min(int(value), self.MAX_AUTOSAVE_INTERVAL),
        )
        self.settings.setValue(
            self.AUTOSAVE_INTERVAL_KEY,
            value,
        )
        self.settings_changed.emit()

    def set_confirm_delete(self, value):
        self.settings.setValue(
            self.CONFIRM_DELETE_KEY,
            bool(value),
        )
        self.settings_changed.emit()

    def set_log_level(self, value):
        if value not in {"INFO", "DEBUG"}:
            value = self.DEFAULT_LOG_LEVEL

        self.settings.setValue(
            self.LOG_LEVEL_KEY,
            value,
        )
        self.settings_changed.emit()

    def set_window_geometry(self, value):
        if isinstance(value, QByteArray):
            self.settings.setValue(
                self.WINDOW_GEOMETRY_KEY,
                value,
            )

    def set_window_state(self, value):
        if isinstance(value, QByteArray):
            self.settings.setValue(
                self.WINDOW_STATE_KEY,
                value,
            )


    @property
    def recent_exports(self):
        value = self.settings.value(
            self.RECENT_EXPORTS_KEY,
            [],
        )

        if not isinstance(value, list):
            return []

        return [str(item) for item in value]

    def set_recent_exports(self, paths):
        self.settings.setValue(
            self.RECENT_EXPORTS_KEY,
            list(paths),
        )
        self.settings.sync()

    @property
    def recent_exports(self):
        value = self.settings.value(
            self.RECENT_EXPORTS_KEY,
            [],
        )

        if not isinstance(value, list):
            return []

        return [str(item) for item in value]

    def set_recent_exports(self, paths):
        self.settings.setValue(
            self.RECENT_EXPORTS_KEY,
            list(paths),
        )
        self.settings.sync()

    def sync(self):
        self.settings.sync()
