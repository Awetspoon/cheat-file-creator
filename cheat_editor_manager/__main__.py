from __future__ import annotations

import os

from .bootstrap import configure_tcl_environment


configure_tcl_environment()

from .app import App, create_app_root


SMOKE_ROOT_GEOMETRY = "1280x820+32000+32000"


def main() -> None:
    smoke_exit = os.environ.get("CHEAT_EDITOR_MANAGER_SMOKE_EXIT") == "1"
    root = None
    if smoke_exit:
        root = create_app_root()
        root.geometry(SMOKE_ROOT_GEOMETRY)
    app = App(root=root, enable_update_check=not smoke_exit)
    if smoke_exit:
        app.root.update_idletasks()
        app.root.update()
        app.root.destroy()
        return
    app.run()


if __name__ == "__main__":
    main()
