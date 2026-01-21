import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib
from .models.project import Project
from .models.database import get_db

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        self.set_title("Project Organizer")
        self.set_default_size(900, 600)

        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        # Header bar
        header = Adw.HeaderBar()

        # Add project button
        add_button = Gtk.Button(icon_name="list-add-symbolic")
        add_button.connect("clicked", self.on_add_project_clicked)
        header.pack_start(add_button)

        main_box.append(header)

        # Content area with scrolled window
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_vexpand(True)

        # List box for projects
        self.project_list = Gtk.ListBox()
        self.project_list.set_selection_mode(Gtk.SelectionMode.NONE)
        self.project_list.add_css_class("boxed-list")

        self.scrolled_window.set_child(self.project_list)

        # Add content to main box
        content_clamp = Adw.Clamp()
        content_clamp.set_maximum_size(1000)
        content_clamp.set_child(self.scrolled_window)
        main_box.append(content_clamp)

        self.set_content(main_box)

        # Load projects
        self.refresh_projects()

    def refresh_projects(self):
        """Refresh the project list from database."""
        # Clear existing items
        while True:
            row = self.project_list.get_row_at_index(0)
            if row is None:
                break
            self.project_list.remove(row)

        # Load projects from database
        projects = Project.get_all()

        if not projects:
            # Show empty state
            status_page = Adw.StatusPage()
            status_page.set_title("No Projects")
            status_page.set_description("Add a project to get started")
            status_page.set_icon_name("folder-symbolic")
            self.project_list.append(status_page)
        else:
            for project in projects:
                row = self.create_project_row(project)
                self.project_list.append(row)

    def create_project_row(self, project):
        """Create a list row for a project."""
        row = Adw.ActionRow()
        row.set_title(project.name)
        row.set_subtitle(project.path)

        # Language badge
        if project.language:
            language_label = Gtk.Label(label=project.language)
            language_label.add_css_class("caption")
            language_label.add_css_class("dim-label")
            row.add_suffix(language_label)

        # Delete button
        delete_button = Gtk.Button(icon_name="user-trash-symbolic")
        delete_button.add_css_class("flat")
        delete_button.connect("clicked", self.on_delete_project_clicked, project.id)
        row.add_suffix(delete_button)

        return row

    def on_add_project_clicked(self, button):
        """Show dialog to add a new project."""
        dialog = Gtk.FileDialog()
        dialog.set_title("Select Project Directory")
        dialog.select_folder(None, None, self.on_folder_selected)

    def on_folder_selected(self, dialog, result):
        """Handle folder selection for new project."""
        try:
            folder = dialog.select_folder_finish(result)
            if folder:
                path = folder.get_path()
                name = folder.get_basename()

                # Show dialog to enter project details
                self.show_project_details_dialog(name, path)

        except GLib.Error as e:
            if e.code != 2:  # Ignore dismiss/cancel
                print(f"Error selecting folder: {e.message}")

    def show_project_details_dialog(self, default_name, path):
        """Show dialog to enter project details."""
        dialog = Adw.MessageDialog(transient_for=self)
        dialog.set_heading("Add Project")
        dialog.set_body("Enter project details")

        dialog.add_response("cancel", "Cancel")
        dialog.add_response("add", "Add")
        dialog.set_response_appearance("add", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("add")

        # Create form
        form_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        form_box.set_margin_top(12)
        form_box.set_margin_bottom(12)
        form_box.set_margin_start(12)
        form_box.set_margin_end(12)

        # Name entry
        name_entry = Adw.EntryRow()
        name_entry.set_title("Name")
        name_entry.set_text(default_name)
        form_box.append(name_entry)

        # Language entry
        language_entry = Adw.EntryRow()
        language_entry.set_title("Language")
        form_box.append(language_entry)

        # Description entry
        description_entry = Adw.EntryRow()
        description_entry.set_title("Description")
        form_box.append(description_entry)

        dialog.set_extra_child(form_box)

        dialog.connect("response", self.on_project_dialog_response,
                      name_entry, language_entry, description_entry, path)
        dialog.present()

    def on_project_dialog_response(self, dialog, response, name_entry,
                                   language_entry, description_entry, path):
        """Handle project details dialog response."""
        if response == "add":
            name = name_entry.get_text()
            language = language_entry.get_text() or None
            description = description_entry.get_text() or None

            if name:
                try:
                    Project.add(name, path, language, description)
                    self.refresh_projects()
                except Exception as e:
                    print(f"Error adding project: {e}")

    def on_delete_project_clicked(self, button, project_id):
        """Handle delete project button click."""
        dialog = Adw.MessageDialog(transient_for=self)
        dialog.set_heading("Delete Project?")
        dialog.set_body("This will remove the project from the organizer. The files will not be deleted.")

        dialog.add_response("cancel", "Cancel")
        dialog.add_response("delete", "Delete")
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)

        dialog.connect("response", self.on_delete_confirm_response, project_id)
        dialog.present()

    def on_delete_confirm_response(self, dialog, response, project_id):
        """Handle delete confirmation dialog response."""
        if response == "delete":
            try:
                Project.delete(project_id)
                self.refresh_projects()
            except Exception as e:
                print(f"Error deleting project: {e}")
