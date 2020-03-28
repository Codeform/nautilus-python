import hashlib
from urllib.parse import unquote
from gi.repository import Nautilus, Gtk, GObject
from os import path


class MD5SumPropertyPage(GObject.GObject, Nautilus.PropertyPageProvider):
    def __init__(self):
        pass

    def get_property_pages(self, files):
        self.property_label = Gtk.Label('MD5 Sum')
        self.property_label.show()

        self.contents = Gtk.ScrolledWindow(min_content_height=200)
        list_box = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        self.contents.add(list_box)

        for i in range(len(files)):
            file = files[i]
            if file.get_uri_scheme() != 'file' or file.is_directory():
                continue

            filename = unquote(file.get_uri()[len('file://'):])
            md5sum = hashlib.md5(filename.encode("utf-8")).hexdigest()

            label_fn = Gtk.Label(path.basename(filename))

            label_md5 = Gtk.Label(md5sum, selectable=True)
            entry_box = Gtk.HBox(spacing=20)
            entry_box.pack_start(label_fn, False, False, 0)
            entry_box.pack_start(label_md5, False, False, 0)
            list_box.insert(entry_box, -1)

        self.contents.show_all()

        return Nautilus.PropertyPage(name="NautilusPython::md5_sum",
                                     label=self.property_label,
                                     page=self.contents),
