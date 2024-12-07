import gi
import dbus
import requests
import random
from PIL import Image
from io import BytesIO
import cairo
from gi.repository import PangoCairo
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf, Pango
import math

class SpotifyController:
    def __init__(self):
        self.session_bus = dbus.SessionBus()
        self.spotify_bus = self.session_bus.get_object(
            'org.mpris.MediaPlayer2.spotify',
            '/org/mpris/MediaPlayer2'
        )
        self.spotify_properties = dbus.Interface(
            self.spotify_bus,
            'org.freedesktop.DBus.Properties'
        )
        self.spotify_interface = dbus.Interface(
            self.spotify_bus,
            'org.mpris.MediaPlayer2.Player'
        )

    def next_track(self):
        self.spotify_interface.Next()

    def previous_track(self):
        self.spotify_interface.Previous()

    def play_pause(self):
        self.spotify_interface.PlayPause()

    def get_current_song_info(self):
        metadata = self.spotify_properties.Get(
            'org.mpris.MediaPlayer2.Player',
            'Metadata'
        )
        return {
            'title': str(metadata.get('xesam:title', 'Unknown')),
            'artist': str(metadata.get('xesam:artist', ['Unknown'])[0]),
            'art_url': str(metadata.get('mpris:artUrl', '')),
            'album': str(metadata.get('xesam:album', 'Unknown'))
        }

    def get_playback_status(self):
        return str(self.spotify_properties.Get(
            'org.mpris.MediaPlayer2.Player',
            'PlaybackStatus'
        ))
class MusicLine(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.set_size_request(-1, 50)
        self.connect('draw', self.on_draw)
        self.is_active = False
        self.bars = 40
        self.bar_heights = [0] * self.bars
        self.pattern = [
            [0.3, 0.4, 0.6, 0.8, 1.0, 0.8, 0.6, 0.4],  # Peak pattern
            [0.2, 0.3, 0.2, 0.4, 0.3, 0.2, 0.3, 0.2],  # Mid pattern
            [0.1, 0.2, 0.1, 0.2, 0.1, 0.2, 0.1, 0.2]   # Low pattern
        ]
        self.pattern_index = 0
        GLib.timeout_add(100, self.update_animation)

    def on_draw(self, widget, cr):
        width = widget.get_allocated_width()
        height = widget.get_allocated_height()
        
        bar_width = width / (self.bars * 1.5)
        spacing = bar_width / 2
        
        cr.set_source_rgba(1, 1, 1, 0.9)
        
        for i in range(self.bars):
            if self.is_active:
                bar_height = (self.bar_heights[i] * height) -5
            else:
                bar_height = (height * 0.1) -5
            
            x = i * (bar_width + spacing)
            y = (height - bar_height) / 2
            
            # Draw rounded bars
            cr.new_path()
            cr.rectangle(x, y, bar_width, bar_height)
            cr.fill()
        
        return False

    def update_animation(self):
        if self.is_active:
            pattern_length = len(self.pattern[0])
            for i in range(self.bars):
                section = i % 3  # Divide bars into three sections
                pattern_pos = (i + self.pattern_index) % pattern_length
                self.bar_heights[i] = self.pattern[section][pattern_pos]
            
            self.pattern_index = (self.pattern_index + 1) % pattern_length
            self.queue_draw()
        return True

class SpotifyOverlay(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Spotify Mini")
        self.controller = SpotifyController()

        # Window setup
        self.set_default_size(380, 80)  # Increased width to accommodate larger image
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.set_keep_above(True)
        self.set_decorated(False)

        # Main container
        self.outer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.add(self.outer_box)
        
         
        # Album art
        self.album_image = Gtk.Image()
        self.outer_box.pack_start(self.album_image, False, False, 0)

        # Main content box
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.outer_box.pack_start(self.main_box, True, True, 10)


        # Info and controls container
        self.right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.main_box.pack_start(self.right_box, True, True, 5)

        # Song info
        self.title_label = Gtk.Label()
        self.title_label.set_halign(Gtk.Align.START)
        self.title_label.set_ellipsize(Pango.EllipsizeMode.END)
        
        self.artist_label = Gtk.Label()
        self.artist_label.set_halign(Gtk.Align.START)
        self.artist_label.set_ellipsize(Pango.EllipsizeMode.END)

        # Controls
        self.controls_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.controls_box.set_halign(Gtk.Align.CENTER)

        # Create buttons
        self.prev_button = self.create_button("media-skip-backward")
        self.play_button = self.create_button("media-playback-start")
        self.next_button = self.create_button("media-skip-forward")

        # Connect signals
        self.prev_button.connect("clicked", lambda x: self.controller.previous_track())
        self.play_button.connect("clicked", self.toggle_play_pause)
        self.next_button.connect("clicked", lambda x: self.controller.next_track())

        # Pack controls
        self.controls_box.pack_start(self.prev_button, False, False, 0)
        self.controls_box.pack_start(self.play_button, False, False, 0)
        self.controls_box.pack_start(self.next_button, False, False, 0)

        # Pack everything
        self.right_box.pack_start(self.title_label, True, True, 0)
        self.right_box.pack_start(self.artist_label, True, True, 0)
        self.right_box.pack_start(self.controls_box, True, True, 0)

        # Add music line
        self.music_line = MusicLine()
        self.right_box.pack_start(self.music_line, False, False, 5)

        # Window events
        self.connect('button-press-event', self.on_press)
        self.connect('button-release-event', self.on_release)
        self.connect('motion-notify-event', self.on_motion)
        self.connect('draw', self.on_draw)

        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK
        )

        self.apply_css()
        self.dragging = False
        
        # Update timers
        GLib.timeout_add(1000, self.update_info)
        GLib.timeout_add(50, self.animate_border)
        
        # Border animation
        self.border_radius = 10
        self.animation_direction = 1

    def create_button(self, icon_name):
        button = Gtk.Button()
        icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.LARGE_TOOLBAR)
        button.set_image(icon)
        return button

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        css = """
        window {
            background-color: rgba(43, 43, 43, 0.85);
            border-radius: 12px;
        }
        label {
            color: white;
            font-size: 12px;
            margin: 2px;
        }
        button {
            background: transparent;
            border: none;
            min-height: 32px;
            min-width: 32px;
            padding: 4px;
            color: white;
        }
        button:hover {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
        }
        button image {
            color: white;
        }
        #watermark {
            color: rgba(255, 255, 255, 0.5);
            font-size: 10px;
            padding: 4px;
        }
        """
        css_provider.load_from_data(css.encode())
        context = self.get_style_context()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Set the name for the album image widget
        self.album_image.set_name("album-image")
    def on_draw(self, widget, cairo_context):
        width = widget.get_allocated_width()
        height = widget.get_allocated_height()
        
        radius = 12
        cairo_context.new_path()
        cairo_context.arc(radius, radius, radius, 3.14, 3.14 * 1.5)
        cairo_context.arc(width - radius, radius, radius, 3.14 * 1.5, 0)
        cairo_context.arc(width - radius, height - radius, radius, 0, 3.14 * 0.5)
        cairo_context.arc(radius, height - radius, radius, 3.14 * 0.5, 3.14)
        cairo_context.close_path()
        
        cairo_context.set_source_rgba(0.169, 0.169, 0.169, 1)
        cairo_context.fill()
        return False

    def animate_border(self):
        max_radius = 15
        min_radius = 8
        step = 0.5
        
        self.border_radius += step * self.animation_direction
        if self.border_radius >= max_radius:
            self.animation_direction = -1
        elif self.border_radius <= min_radius:
            self.animation_direction = 1
            
        css = f"""
        window {{
            border-radius: {self.border_radius}px;
        }}
        """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css.encode())
        context = self.get_style_context()
        context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        return True

    def update_album_art(self, art_url):
        try:
            response = requests.get(art_url)
            loader = GdkPixbuf.PixbufLoader()
            loader.write(response.content)
            loader.close()
            pixbuf = loader.get_pixbuf()

            # Get the window height
            window_height = self.get_allocated_height()

            # Calculate the new width while maintaining aspect ratio
            aspect_ratio = pixbuf.get_width() / pixbuf.get_height()
            new_width = int(window_height * aspect_ratio)

            # Scale the image to fit the window height
            scaled_pixbuf = pixbuf.scale_simple(new_width, window_height, GdkPixbuf.InterpType.BILINEAR)

            # Add watermark to the scaled image
            watermarked_pixbuf = self.overlay_watermark(scaled_pixbuf)

            self.album_image.set_from_pixbuf(watermarked_pixbuf)
        except Exception as e:
            print(f"Error loading album art: {e}")
                
    def toggle_play_pause(self, button):
        self.controller.play_pause()
        status = self.controller.get_playback_status()
        icon_name = "media-playback-start" if status != "Playing" else "media-playback-pause"
        self.play_button.set_image(
            Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.LARGE_TOOLBAR)
        )

    def update_info(self):
        try:
            info = self.controller.get_current_song_info()
            status = self.controller.get_playback_status()
            
            self.music_line.is_active = (status == "Playing")
            
            self.title_label.set_markup(
                f"<span font_weight='bold' font_size='large'>{info['title']}</span>"
            )
            self.artist_label.set_text(info['artist'])
            
            if info['art_url']:
                self.update_album_art(info['art_url'])
            
            icon_name = "media-playback-pause" if status == "Playing" else "media-playback-start"
            self.play_button.set_image(
                Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.LARGE_TOOLBAR)
            )
        except Exception as e:
            print(f"Error updating info: {e}")
            self.music_line.is_active = False
        return True

    def on_press(self, widget, event):
        if event.button == 1:
            self.dragging = True
            self.drag_x = event.x
            self.drag_y = event.y
        return True

    def on_release(self, widget, event):
        self.dragging = False
        return True

    def on_motion(self, widget, event):
        if self.dragging:
            win_x, win_y = self.get_position()
            new_x = win_x + event.x - self.drag_x
            new_y = win_y + event.y - self.drag_y
            self.move(int(new_x), int(new_y))
        return True
        
    def overlay_watermark(self, pixbuf):
        watermark_text = "@by adithya n raj"
        
        # Create a surface to draw on
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, pixbuf.get_width(), pixbuf.get_height())
        context = cairo.Context(surface)

        # Draw the original image
        Gdk.cairo_set_source_pixbuf(context, pixbuf, 0, 0)
        context.paint()

        # Set up the font
        layout = PangoCairo.create_layout(context)
        font_desc = Pango.FontDescription("Sans Bold Italic 7")
        layout.set_font_description(font_desc)
        layout.set_text(watermark_text)

        # Position of the watermark
        x, y = 5, 6

        # Draw the white outline
        context.set_source_rgb(0, 0, 0)  # White color
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            context.move_to(x + dx, y + dy)
            PangoCairo.show_layout(context, layout)

        # Draw the main text in black
        context.set_source_rgb(1, 1, 1)  # Black color
        context.move_to(x, y)
        PangoCairo.show_layout(context, layout)

        # Create a new pixbuf from the surface
        new_pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, surface.get_width(), surface.get_height())

        return new_pixbuf     
        
if __name__ == "__main__":
    win = SpotifyOverlay()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
